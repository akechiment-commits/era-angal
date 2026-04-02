#!/usr/bin/env python3
"""
hatotank.net/ensemble_girls/egcardlist.php からカードデータを取得して card_data.csv に保存する

ページ構造（debug_cardlist.html から確認済み）:
  No.X キャラ名 (セクションヘッダー)
  基本：キャラ名 / 学年 (クラス)
  レア：N/R/SR/SSR/UR
  タグ：部活名
  属性：
  必殺技：カード名（スキル名）
  マイページセリフ：...

使い方:
  cd tools
  python scrape_cards.py              # 全ページ取得（1〜68ページ）
  python scrape_cards.py --local      # debug_cardlist.html を使ってページ1だけパース（テスト用）
  python scrape_cards.py --pages 3    # 先頭3ページだけ取得（テスト用）
  python scrape_cards.py --inspect 2  # ページ2のHTMLを debug_page2.html に保存して終了

出力: tools/card_data.csv
  id, char_name, rarity, rarity_name, card_name, bonus_type
"""

import argparse
import csv
import html as html_module
import re
import time
import urllib.request
from pathlib import Path

BASE_URL = "https://hatotank.net/ensemble_girls/egcardlist.php"
OUT_CSV = Path("card_data.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
    "Referer": "https://hatotank.net/ensemble_girls/",
}

RARITY_MAP = {"UR": 5, "SSR": 4, "SR": 3, "R": 2, "N": 1}

# タグ（部活）→ ボーナスタイプ推定
TAG_BONUS_MAP = {
    "音楽": 0, "演劇": 0, "文化": 0, "芸術": 0, "合唱": 0, "軽音": 0,
    "バレー": 1, "バスケ": 1, "サッカー": 1, "テニス": 1, "陸上": 1,
    "ラクロス": 1, "体操": 1, "水泳": 1, "剣道": 1, "柔道": 1,
    "科学": 2, "数学": 2, "文学": 2, "料理": 2, "茶道": 2, "書道": 2,
}


def fetch_html(url: str, save_as: str = None) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        raw = resp.read()
        for enc in ("utf-8", "shift_jis", "cp932", "euc-jp"):
            try:
                html = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            html = raw.decode("utf-8", errors="replace")
        if save_as:
            Path(save_as).write_text(html, encoding="utf-8")
        return html
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {url}")
        return ""
    except Exception as e:
        print(f"  ERROR: {e}")
        return ""


def page_url(page_no: int) -> str:
    if page_no == 1:
        return BASE_URL
    return f"{BASE_URL}?p={page_no}"


def detect_max_page(html: str) -> int:
    """ページネーションから最大ページ数を取得"""
    # "1|2|3|...|68" のようなリンク列を探す
    m = re.search(r'\|\s*(\d+)\s*$', html.replace('\n', ' '))
    if m:
        return int(m.group(1))
    # <a href="...p=N"> の最大値を探す
    nums = re.findall(r'[?&]p=(\d+)', html)
    if nums:
        return max(int(n) for n in nums)
    return 1


def strip_tags(s: str) -> str:
    return html_module.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def guess_bonus_type(tag: str, skill: str) -> int:
    for keyword, btype in TAG_BONUS_MAP.items():
        if keyword in tag or keyword in skill:
            return btype
    return hash(skill) % 4


def parse_page(html: str) -> list[dict]:
    """
    ページHTMLからカードエントリを解析する

    各エントリの形式:
      <セクションヘッダー> No.X キャラ名
      レア：N/R/SR/SSR/UR
      必殺技：スキル名（= カード名として使用）
      タグ：部活名（ボーナスタイプ推定に使用）
    """
    cards = []

    # セクション分割: "No.数字 キャラ名" のヘッダーで区切る
    # <th>, <h2>, <h3>, <td class="..."> などいろんなタグが使われる可能性あり
    # まずテキスト全体を行に分解してパターンマッチ
    text = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    text = re.sub(r'</p>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</div>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</tr>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</td>', '\t', text, flags=re.IGNORECASE)
    text = re.sub(r'</th>', '\t', text, flags=re.IGNORECASE)
    lines = [strip_tags(line) for line in text.split('\n')]
    lines = [l for l in lines if l]

    # エントリ開始パターン: "No.1 高原ちあき" のような行
    NO_PAT = re.compile(r'^No\.(\d+)\s+(.+)$')
    # フィールドパターン
    RARITY_PAT = re.compile(r'^レア[ィリ]?[ティ]?[：:]\s*(UR|SSR|SR|R|N)\b', re.IGNORECASE)
    SKILL_PAT = re.compile(r'^必殺技[：:]\s*(.+)$')
    TAG_PAT = re.compile(r'^タグ[：:]\s*(.+)$')

    current_no = None
    current_char = ""
    current_rarity = None
    current_skill = ""
    current_tag = ""

    def flush():
        nonlocal current_no, current_char, current_rarity, current_skill, current_tag
        if current_no is not None and current_rarity and current_skill:
            cards.append({
                "no": current_no,
                "char_name": current_char,
                "rarity": RARITY_MAP.get(current_rarity, 1),
                "rarity_name": current_rarity,
                "card_name": current_skill,
                "bonus_type": guess_bonus_type(current_tag, current_skill),
            })
        current_no = None
        current_char = ""
        current_rarity = None
        current_skill = ""
        current_tag = ""

    for line in lines:
        # タブ区切りのセルも処理
        for cell in line.split('\t'):
            cell = cell.strip()
            if not cell:
                continue

            m = NO_PAT.match(cell)
            if m:
                flush()
                current_no = int(m.group(1))
                current_char = m.group(2).strip()
                continue

            m = RARITY_PAT.match(cell)
            if m and current_no is not None:
                rarity = m.group(1).upper()
                if rarity in RARITY_MAP:
                    current_rarity = rarity
                continue

            m = SKILL_PAT.match(cell)
            if m and current_no is not None:
                current_skill = m.group(1).strip()
                continue

            m = TAG_PAT.match(cell)
            if m and current_no is not None:
                current_tag = m.group(1).strip()
                continue

    flush()
    return cards


def run_local_test():
    """debug_cardlist.html をパースしてテスト"""
    local = Path("debug_cardlist.html")
    if not local.exists():
        print("debug_cardlist.html が見つかりません")
        return []
    html = local.read_text(encoding="utf-8", errors="replace")
    max_page = detect_max_page(html)
    print(f"最大ページ: {max_page}")
    cards = parse_page(html)
    print(f"ページ1: {len(cards)}件")
    for c in cards[:5]:
        print(f"  No.{c['no']:4d} [{c['rarity_name']}] {c['char_name']:12s}  {c['card_name']}")
    return cards


def scrape_all(max_pages: int = 0) -> list[dict]:
    all_cards = []

    # ページ1取得（最大ページ数も確認）
    print(f"取得中: {page_url(1)}")
    html1 = fetch_html(page_url(1), save_as="debug_page1.html")
    if not html1:
        print("ページ1の取得に失敗しました")
        return []

    detected = detect_max_page(html1)
    print(f"最大ページ検出: {detected}")
    total = max_pages if (max_pages and max_pages < detected) else detected

    cards = parse_page(html1)
    print(f"  ページ1: {len(cards)}件")
    all_cards.extend(cards)

    for page in range(2, total + 1):
        url = page_url(page)
        print(f"  ページ{page}/{total}: {url}")
        html = fetch_html(url)
        if not html:
            print(f"    取得失敗、スキップ")
            continue
        c = parse_page(html)
        print(f"    {len(c)}件")
        all_cards.extend(c)
        time.sleep(0.5)

    return all_cards


def assign_ids(cards: list[dict]) -> list[dict]:
    # No. 順でソートして連番 id を付与
    cards.sort(key=lambda c: c["no"])
    for i, c in enumerate(cards, 1):
        c["id"] = i
    return cards


def save_csv(cards: list[dict]):
    if not cards:
        print("カードが0件です、保存しません")
        return
    fieldnames = ["id", "char_name", "rarity", "rarity_name", "card_name", "bonus_type"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(cards)

    from collections import Counter
    rarity_count = Counter(c["rarity_name"] for c in cards)
    char_count = Counter(c["char_name"] for c in cards)
    print(f"\n保存: {OUT_CSV}  ({len(cards)}件)")
    print("レア度分布:", dict(sorted(rarity_count.items())))
    print(f"キャラ数: {len(char_count)}人")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", action="store_true",
                        help="debug_cardlist.html をパースしてテスト（通信なし）")
    parser.add_argument("--pages", type=int, default=0,
                        help="取得するページ数上限（0=全件）")
    parser.add_argument("--inspect", type=int, metavar="PAGE",
                        help="指定ページのHTMLを debug_pageN.html に保存して終了")
    args = parser.parse_args()

    print("=== あんガル カードデータ取得 (egcardlist) ===\n")

    if args.inspect:
        url = page_url(args.inspect)
        print(f"取得: {url}")
        html = fetch_html(url, save_as=f"debug_page{args.inspect}.html")
        if html:
            cards = parse_page(html)
            print(f"検出件数: {len(cards)}")
            for c in cards[:10]:
                print(f"  No.{c['no']:4d} [{c['rarity_name']}] {c['char_name']:12s}  {c['card_name']}")
        return

    if args.local:
        cards = run_local_test()
        if cards:
            cards = assign_ids(cards)
            save_csv(cards)
        return

    cards = scrape_all(max_pages=args.pages)
    if cards:
        cards = assign_ids(cards)
        save_csv(cards)
    else:
        print("\n取得できませんでした。")
        print("まず debug_cardlist.html が正しく取得できているか確認してください:")
        print("  python scrape_cards.py --inspect 1")
        print("  # → debug_page1.html を確認して構造を調べる")


if __name__ == "__main__":
    main()
