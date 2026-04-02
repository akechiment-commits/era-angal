#!/usr/bin/env python3
"""
hatotank.net/kmskwiki/chara/N からあんガル カードデータを取得して card_data.csv に保存する

使い方:
  cd tools
  python scrape_cards.py              # 全キャラ取得（ID 1〜）
  python scrape_cards.py --inspect 3  # キャラ3のHTMLを debug_chara_3.html に保存して終了
  python scrape_cards.py --max 10     # キャラID 1〜10 だけ取得（テスト用）
  python scrape_cards.py --start 5    # キャラID 5 から開始

出力: tools/card_data.csv
  id, char_name, rarity, rarity_name, card_name, card_type, bonus_type
"""

import argparse
import csv
import html as html_module
import re
import time
import urllib.request
from pathlib import Path

BASE_WIKI = "https://hatotank.net/kmskwiki"
CHARA_URL = f"{BASE_WIKI}/chara"
OUT_CSV = Path("card_data.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
    "Referer": BASE_WIKI + "/",
}

# レア度マッピング
RARITY_MAP = {
    "UR": 5, "SSR": 4, "SR": 3, "R": 2, "N": 1,
    "ur": 5, "ssr": 4, "sr": 3, "r": 2, "n": 1,
    "5": 5, "4": 4, "3": 3, "2": 2, "1": 1,
}

RARITY_NAMES = {"UR", "SSR", "SR", "R", "N"}

# カードタイプ → ボーナスタイプ変換
# 収拾系=0(表現), バトル系=1(運動), 宝探し系=2(学力), すごろく系=3(好感度)
TYPE_BONUS_MAP = {
    "歌": 0, "音楽": 0, "文化": 0, "芸術": 0, "演劇": 0, "パフォーマンス": 0,
    "運動": 1, "スポーツ": 1, "バトル": 1, "武道": 1, "アクション": 1,
    "学": 2, "勉強": 2, "知識": 2, "理系": 2, "文系": 2, "サイエンス": 2,
    "交流": 3, "友情": 3, "恋愛": 3, "日常": 3, "アイドル": 3,
}


def fetch(url: str, debug_name: str = None) -> str:
    """URLを取得してHTMLを返す"""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        raw = resp.read()
        # エンコード検出: UTF-8を試みてからShift-JIS
        for enc in ("utf-8", "shift_jis", "cp932", "euc-jp"):
            try:
                html = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            html = raw.decode("utf-8", errors="replace")
        if debug_name:
            Path(f"debug_{debug_name}.html").write_text(html, encoding="utf-8")
            print(f"  HTML保存: debug_{debug_name}.html")
        return html
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None  # キャラ存在しない
        print(f"  HTTP ERROR {e.code}: {url}")
        return ""
    except Exception as e:
        print(f"  ERROR: {url} -> {e}")
        return ""


def guess_bonus_type(card_name: str, char_name: str = "") -> int:
    """カード名からボーナスタイプを推定"""
    text = card_name + char_name
    for keyword, btype in TYPE_BONUS_MAP.items():
        if keyword in text:
            return btype
    return hash(card_name) % 4


def parse_rarity(rarity_str: str) -> int:
    """レア度文字列を数値に変換"""
    s = rarity_str.strip().upper()
    return RARITY_MAP.get(s, RARITY_MAP.get(s.lower(), 1))


def extract_char_name(html: str) -> str:
    """ページのキャラ名を抽出"""
    # <title> タグから取得
    m = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
    if m:
        title = html_module.unescape(m.group(1)).strip()
        # "キャラ名 - wikiサイト名" の形式が多い
        for sep in [" - ", " | ", "　", "/"]:
            if sep in title:
                title = title.split(sep)[0].strip()
        if title and title not in ("", "Wiki", "wiki"):
            return title

    # h1 タグから取得
    m = re.search(r'<h1[^>]*>\s*(.+?)\s*</h1>', html, re.DOTALL | re.IGNORECASE)
    if m:
        return html_module.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()

    return ""


def parse_cards_from_html(html: str, char_name: str) -> list[dict]:
    """HTMLからカードデータを解析（複数パターンに対応）"""
    cards = []

    # パターン1: テーブル内の行でレア度とカード名を探す
    # テーブルタグを全て抽出してそれぞれ解析
    tables = re.findall(r'<table[^>]*>(.*?)</table>', html, re.DOTALL | re.IGNORECASE)
    for table in tables:
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', table, re.DOTALL | re.IGNORECASE)
        for row in rows:
            cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.DOTALL | re.IGNORECASE)
            texts = [html_module.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in cells]
            texts = [t for t in texts if t]
            if not texts:
                continue

            # レア度セルを探す
            rarity_str = None
            card_name = None
            for t in texts:
                t_upper = t.upper().replace('\u3000', '').strip()
                if t_upper in RARITY_NAMES:
                    rarity_str = t_upper
                elif rarity_str and not card_name:
                    # レア度の次のセルがカード名候補
                    # ただし短すぎる（1文字）や数字だけはスキップ
                    if len(t) >= 2 and not re.match(r'^\d+$', t):
                        card_name = t

            if rarity_str and card_name and card_name != char_name:
                cards.append({
                    "char_name": char_name,
                    "rarity": parse_rarity(rarity_str),
                    "rarity_name": rarity_str,
                    "card_name": card_name,
                    "bonus_type": guess_bonus_type(card_name, char_name),
                })

    # パターン2: テーブル外でレア度とカード名がリスト・div形式の場合
    if not cards:
        # 行ごとにレア度パターンを探す
        lines = html.split('\n')
        for line in lines:
            clean = html_module.unescape(re.sub(r'<[^>]+>', ' ', line)).strip()
            clean = re.sub(r'\s+', ' ', clean)
            if not clean:
                continue
            # "SSR カード名" や "[SR] カード名" パターン
            m = re.match(
                r'^[\[\(【]?\s*(UR|SSR|SR|R|N)\s*[\]\)】]?\s*[：:　\s]\s*(.{2,})',
                clean, re.IGNORECASE
            )
            if m:
                rarity_str = m.group(1).upper()
                card_name = m.group(2).strip()
                if card_name and card_name != char_name:
                    cards.append({
                        "char_name": char_name,
                        "rarity": parse_rarity(rarity_str),
                        "rarity_name": rarity_str,
                        "card_name": card_name,
                        "bonus_type": guess_bonus_type(card_name, char_name),
                    })

    # 重複除去（同じカード名＋レア度の組み合わせ）
    seen = set()
    unique = []
    for c in cards:
        key = (c["card_name"], c["rarity_name"])
        if key not in seen:
            seen.add(key)
            unique.append(c)

    return unique


def scrape_all_chars(max_id: int = 200, start_id: int = 1) -> list[dict]:
    """全キャラページからカードを収集"""
    all_cards = []
    consecutive_404 = 0

    for cid in range(start_id, max_id + 1):
        url = f"{CHARA_URL}/{cid}"
        html = fetch(url)

        if html is None:  # 404
            consecutive_404 += 1
            if consecutive_404 >= 5:
                print(f"  5連続404、ID={cid-4}〜{cid}。終了します。")
                break
            print(f"  [{cid}] 404 (スキップ)")
            continue

        consecutive_404 = 0

        if not html:
            print(f"  [{cid}] 取得失敗")
            continue

        char_name = extract_char_name(html)
        if not char_name:
            char_name = f"キャラ{cid}"

        cards = parse_cards_from_html(html, char_name)
        print(f"  [{cid}] {char_name}: {len(cards)}枚")
        all_cards.extend(cards)

        time.sleep(0.3)

    return all_cards


def assign_ids(cards: list[dict]) -> list[dict]:
    for i, card in enumerate(cards, 1):
        card["id"] = i
    return cards


def save_csv(cards: list[dict]):
    fieldnames = ["id", "char_name", "rarity", "rarity_name", "card_name", "bonus_type"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cards)
    print(f"\n保存完了: {OUT_CSV} ({len(cards)}件)")

    from collections import Counter
    rarity_count = Counter(c["rarity_name"] for c in cards)
    char_count = Counter(c["char_name"] for c in cards)
    print("\nレア度分布:", dict(sorted(rarity_count.items())))
    print(f"キャラ数: {len(char_count)}人")
    print("カード数の多いキャラ上位5:", char_count.most_common(5))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inspect", type=int, metavar="ID",
                        help="指定IDのHTMLを保存して構造確認用に終了")
    parser.add_argument("--max", type=int, default=200,
                        help="最大キャラID（デフォルト200）")
    parser.add_argument("--start", type=int, default=1,
                        help="開始キャラID（デフォルト1）")
    args = parser.parse_args()

    print("=== あんガル カードデータ取得 (kmskwiki) ===\n")

    if args.inspect is not None:
        url = f"{CHARA_URL}/{args.inspect}"
        print(f"取得中: {url}")
        html = fetch(url, f"chara_{args.inspect}")
        if not html:
            print("取得失敗")
            return
        char_name = extract_char_name(html)
        print(f"キャラ名: {char_name}")
        cards = parse_cards_from_html(html, char_name)
        print(f"検出カード数: {len(cards)}")
        for c in cards[:10]:
            print(f"  [{c['rarity_name']}] {c['card_name']}")
        if len(cards) > 10:
            print(f"  ... 他 {len(cards)-10} 枚")
        return

    print(f"キャラID {args.start}〜{args.max} を取得します\n")
    cards = scrape_all_chars(max_id=args.max, start_id=args.start)

    if not cards:
        print("\nカードを取得できませんでした。")
        print("  --inspect 3 オプションでHTMLを確認してください:")
        print(f"  python scrape_cards.py --inspect 3")
        return

    cards = assign_ids(cards)
    save_csv(cards)


if __name__ == "__main__":
    main()
