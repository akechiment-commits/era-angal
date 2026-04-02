#!/usr/bin/env python3
"""
hatotank.net からあんガル カードデータを取得して card_data.csv に保存する

使い方:
  cd tools
  python scrape_cards.py          # 全カード取得
  python scrape_cards.py --debug  # HTMLをファイルに保存してデバッグ

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

BASE = "https://hatotank.net/ensemble_girls"
CARD_LIST_URL = f"{BASE}/egcardlist.php"
OUT_CSV = Path("card_data.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
    "Referer": BASE + "/",
}

# レア度マッピング
RARITY_MAP = {
    "UR": 5, "SSR": 4, "SR": 3, "R": 2, "N": 1,
    "ur": 5, "ssr": 4, "sr": 3, "r": 2, "n": 1,
    "5": 5, "4": 4, "3": 3, "2": 2, "1": 1,
}

# カードタイプ → ボーナスタイプ変換
# 収拾系=0(表現), バトル系=1(運動), 宝探し系=2(学力), すごろく系=3(好感度)
TYPE_BONUS_MAP = {
    "歌": 0, "音楽": 0, "文化": 0, "芸術": 0, "演劇": 0,
    "運動": 1, "スポーツ": 1, "バトル": 1, "武道": 1,
    "学": 2, "勉強": 2, "知識": 2, "理系": 2, "文系": 2,
    "交流": 3, "友情": 3, "恋愛": 3, "日常": 3,
}


def fetch(url: str, debug_name: str = None) -> str:
    """URLを取得してHTMLを返す"""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode("utf-8", errors="replace")
        if debug_name:
            Path(f"debug_{debug_name}.html").write_text(html, encoding="utf-8")
        return html
    except Exception as e:
        print(f"  ERROR: {url} -> {e}")
        return ""


def guess_bonus_type(card_name: str, char_name: str = "") -> int:
    """カード名からボーナスタイプを推定"""
    text = card_name + char_name
    for keyword, btype in TYPE_BONUS_MAP.items():
        if keyword in text:
            return btype
    # デフォルト: ランダム（card_nameのハッシュで決定論的に割り振り）
    return hash(card_name) % 4


def parse_rarity(rarity_str: str) -> int:
    """レア度文字列を数値に変換"""
    rarity_str = rarity_str.strip().upper()
    return RARITY_MAP.get(rarity_str, RARITY_MAP.get(rarity_str.lower(), 1))


def scrape_card_list() -> list[dict]:
    """カード一覧ページから全カードを取得"""
    print(f"カード一覧を取得中: {CARD_LIST_URL}")
    html = fetch(CARD_LIST_URL, "cardlist")
    if not html:
        print("  取得失敗。キャラ別ページから取得を試みます...")
        return scrape_cards_by_char()

    cards = []
    # テーブル行を解析
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
    for row in rows:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.DOTALL)
        if len(cells) < 3:
            continue
        texts = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
        texts = [html_module.unescape(t) for t in texts]
        # 空行スキップ
        if not any(texts):
            continue

        # カード行の判定（レア度が含まれている行）
        rarity_str = ""
        card_name = ""
        char_name = ""

        for t in texts:
            if t.upper() in ("UR", "SSR", "SR", "R", "N"):
                rarity_str = t.upper()
            elif t and not rarity_str:
                char_name = t
            elif t and rarity_str and not card_name:
                card_name = t

        if not (rarity_str and card_name):
            continue

        cards.append({
            "char_name": char_name,
            "rarity": parse_rarity(rarity_str),
            "rarity_name": rarity_str,
            "card_name": card_name,
            "bonus_type": guess_bonus_type(card_name, char_name),
        })

    print(f"  取得: {len(cards)}件")
    return cards


def scrape_cards_by_char() -> list[dict]:
    """キャラ別ページからカードを取得"""
    # まずキャラリストを取得
    print(f"キャラリストを取得: {BASE}/egcharlist.php")
    html = fetch(f"{BASE}/egcharlist.php", "charlist_for_cards")
    if not html:
        return []

    # キャラIDを抽出
    char_ids = re.findall(r'egchardetail\.php\?id=(\d+)', html)
    char_ids = list(dict.fromkeys(char_ids))  # 重複除去
    print(f"  キャラ数: {len(char_ids)}")

    all_cards = []
    for i, cid in enumerate(char_ids):
        url = f"{BASE}/egchardetail.php?id={cid}"
        print(f"  [{i+1}/{len(char_ids)}] キャラ{cid}のカードを取得...")
        html = fetch(url)
        if not html:
            continue

        # キャラ名取得
        name_m = re.search(r'<h[12][^>]*>\s*(.+?)\s*</h[12]>', html)
        char_name = html_module.unescape(name_m.group(1)).strip() if name_m else f"キャラ{cid}"

        # カードテーブルを探す
        cards = parse_char_cards(html, char_name)
        all_cards.extend(cards)
        time.sleep(0.5)

    return all_cards


def parse_char_cards(html: str, char_name: str) -> list[dict]:
    """キャラページからカードデータを解析"""
    cards = []
    # カード情報を含むテーブル行を探す
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL)
    for row in rows:
        cells = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.DOTALL)
        texts = [html_module.unescape(re.sub(r'<[^>]+>', '', c).strip()) for c in cells]
        texts = [t for t in texts if t]
        if not texts:
            continue

        # レア度を含む行を探す
        rarity_str = None
        card_name = None
        for t in texts:
            if t.upper() in ("UR", "SSR", "SR", "R", "N"):
                rarity_str = t.upper()
            elif rarity_str and not card_name and len(t) > 1:
                card_name = t
                break

        if rarity_str and card_name and card_name != char_name:
            cards.append({
                "char_name": char_name,
                "rarity": parse_rarity(rarity_str),
                "rarity_name": rarity_str,
                "card_name": card_name,
                "bonus_type": guess_bonus_type(card_name, char_name),
            })
    return cards


def assign_ids(cards: list[dict]) -> list[dict]:
    """カードにIDを割り振り"""
    for i, card in enumerate(cards, 1):
        card["id"] = i
    return cards


def save_csv(cards: list[dict]):
    """CSVに保存"""
    fieldnames = ["id", "char_name", "rarity", "rarity_name", "card_name", "bonus_type"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cards)
    print(f"\n保存完了: {OUT_CSV} ({len(cards)}件)")

    # 統計
    from collections import Counter
    rarity_count = Counter(c["rarity_name"] for c in cards)
    char_count = Counter(c["char_name"] for c in cards)
    print("\nレア度分布:", dict(sorted(rarity_count.items())))
    print(f"キャラ数: {len(char_count)}人")
    print("カード数の多いキャラ上位5:", char_count.most_common(5))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    print("=== あんガル カードデータ取得 ===\n")
    cards = scrape_card_list()

    if not cards:
        print("\n取得できませんでした。URLを確認してください。")
        print(f"試行URL: {CARD_LIST_URL}")
        return

    cards = assign_ids(cards)
    save_csv(cards)


if __name__ == "__main__":
    main()
