#!/usr/bin/env python3
"""
https://hatotank.net/kmskwiki/chara/N キャラ個別ページからカードデータを取得

ページ構造（chara/1 から確認済み）:
  テーブル行: [画像] | ID | ☆N(SR) | [タイトル]キャラ名

使い方:
  cd tools
  python scrape_cards.py              # chara/1 〜 chara/200 を取得
  python scrape_cards.py --max 10     # chara/1 〜 chara/10 だけ（テスト）
  python scrape_cards.py --inspect 1  # chara/1 のHTMLを debug_chara1.html に保存

出力: tools/card_data.csv
  id, char_name, card_id, rarity, rarity_name, card_title, card_name, bonus_type
"""

import argparse
import csv
import html as html_module
import re
import time
import urllib.request
from pathlib import Path

BASE = "https://hatotank.net/kmskwiki/chara"
OUT_CSV = Path("card_data.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
    "Referer": "https://hatotank.net/kmskwiki/",
}

# ☆N(TYPE) の TYPE → 数値・名称マッピング
# HR=Hyper Rare, MR=Mega Rare, LR=Legend Rare 等の独自表記も対応
RARITY_ABBR = {
    "N": (1, "N"), "R": (2, "R"), "HR": (2, "R"),
    "SR": (3, "SR"), "SSR": (4, "SSR"),
    "UR": (5, "UR"), "MR": (5, "UR"), "LR": (5, "UR"),
}
# ☆数 → レア度フォールバック（括弧内TYPE不明のとき）
STAR_RARITY = {1: (1,"N"), 2: (1,"N"), 3: (2,"R"), 4: (3,"SR"),
               5: (4,"SSR"), 6: (5,"UR"), 7: (5,"UR")}


def parse_rarity(text: str):
    """
    '☆4(SR)' や '☆5(UR)' などからレア度数値と略称を返す
    """
    text = text.strip()
    # 括弧内の略称を優先
    m = re.search(r'\(([A-Za-z]+)\)', text)
    if m:
        abbr = m.group(1).upper()
        if abbr in RARITY_ABBR:
            return RARITY_ABBR[abbr]
    # ☆数からフォールバック
    m = re.search(r'[★☆](\d)', text)
    if m:
        stars = int(m.group(1))
        return STAR_RARITY.get(stars, (1, "N"))
    return (1, "N")


def fetch(url: str, save_as: str = None) -> str | None:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
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
        if e.code == 404:
            return None
        print(f"  HTTP {e.code}: {url}")
        return ""
    except Exception as e:
        print(f"  ERROR: {e}")
        return ""


def strip_tags(s: str) -> str:
    return html_module.unescape(re.sub(r'<[^>]+>', '', s)).strip()


def get_char_name_from_page(html: str) -> str:
    """ページタイトルからキャラ名を取得（読み・サイト名を除去）"""
    # <title>三波なつみ（みなみなつみ）[あんガル DB補完Wiki] など
    m = re.search(r'<title[^>]*>\s*([^<]+)', html, re.IGNORECASE)
    if m:
        name = m.group(1).strip()
        # 括弧・【】以降を除去: 「三波なつみ（みなみ...）」→「三波なつみ」
        name = re.sub(r'[（(【\[].*', '', name).strip()
        # サイト名区切り以降を除去
        for sep in [' - ', ' | ', '　']:
            if sep in name:
                name = name.split(sep)[0].strip()
        if name:
            return name
    # h1
    m = re.search(r'<h1[^>]*>\s*([^<]+)\s*</h1>', html, re.IGNORECASE)
    if m:
        name = strip_tags(m.group(1))
        name = re.sub(r'[（(【\[].*', '', name).strip()
        return name
    return ""


def parse_cards(html: str, char_name: str) -> list[dict]:
    """
    ページHTMLからカードテーブルを解析

    想定テーブル形式（各行）:
      <td>画像</td> <td>カードID</td> <td>☆N(SR)</td> <td>[タイトル]キャラ名</td>
    """
    cards = []

    # テーブル行を全て取得
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html, re.DOTALL | re.IGNORECASE)
    for row in rows:
        cells_raw = re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row, re.DOTALL | re.IGNORECASE)
        cells = [strip_tags(c) for c in cells_raw]
        cells = [c for c in cells if c]  # 空セル除去

        if len(cells) < 3:
            continue

        # 列を特定
        card_id = None
        rarity_val = None
        rarity_name = None
        card_name_full = None

        for cell in cells:
            # カードID: 数字のみ
            if card_id is None and re.match(r'^\d{3,5}$', cell):
                card_id = int(cell)
                continue

            # レア度: ☆N(SR) パターン
            if rarity_val is None and re.search(r'[☆★]\d', cell):
                rarity_val, rarity_name = parse_rarity(cell)
                continue

            # カード名: [タイトル]キャラ名 パターン
            if card_name_full is None and re.match(r'^\[.+\].+', cell):
                card_name_full = cell
                continue
            # または「タイトル キャラ名」など角括弧なしでもキャラ名を含む
            if card_name_full is None and char_name and char_name in cell and len(cell) > len(char_name):
                card_name_full = cell
                continue

        if card_id and rarity_val and card_name_full:
            # [タイトル]キャラ名 → タイトル部分を抽出
            m = re.match(r'^\[(.+?)\](.+)$', card_name_full)
            if m:
                card_title = m.group(1)
                card_char = m.group(2).strip()
            else:
                card_title = card_name_full
                card_char = char_name

            cards.append({
                "char_name": card_char or char_name,
                "card_id": card_id,
                "rarity": rarity_val,
                "rarity_name": rarity_name,
                "card_title": card_title,
                "card_name": card_name_full,
            })

    return cards


def scrape_all(max_id: int = 200) -> list[dict]:
    all_cards = []
    consecutive_404 = 0

    for cid in range(1, max_id + 1):
        url = f"{BASE}/{cid}"
        html = fetch(url)

        if html is None:
            consecutive_404 += 1
            if consecutive_404 >= 5:
                print(f"  5連続404（ID {cid-4}〜{cid}）終了")
                break
            print(f"  [{cid:3d}] 404")
            continue

        consecutive_404 = 0

        if not html:
            print(f"  [{cid:3d}] 取得失敗")
            continue

        char_name = get_char_name_from_page(html)
        cards = parse_cards(html, char_name)
        print(f"  [{cid:3d}] {char_name:12s}: {len(cards)}枚")
        all_cards.extend(cards)
        time.sleep(0.4)

    return all_cards


def assign_ids(cards: list[dict]) -> list[dict]:
    cards.sort(key=lambda c: c["card_id"])
    for i, c in enumerate(cards, 1):
        c["id"] = i
    return cards


def save_csv(cards: list[dict]):
    fieldnames = ["id", "char_name", "card_id", "rarity", "rarity_name",
                  "card_title", "card_name"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(cards)

    from collections import Counter
    rc = Counter(c["rarity_name"] for c in cards)
    cc = Counter(c["char_name"] for c in cards)
    print(f"\n保存: {OUT_CSV}  {len(cards)}件")
    print("レア度分布:", dict(sorted(rc.items())))
    print(f"キャラ数: {len(cc)}人")
    print("カード数多い上位5:", cc.most_common(5))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max", type=int, default=200,
                        help="最大キャラID（デフォルト200）")
    parser.add_argument("--inspect", type=int, metavar="N",
                        help="chara/N のHTMLを debug_charaN.html に保存してパース結果表示")
    args = parser.parse_args()

    print("=== あんガル カードデータ取得 (kmskwiki/chara/N) ===\n")

    if args.inspect is not None:
        url = f"{BASE}/{args.inspect}"
        print(f"取得: {url}")
        html = fetch(url, save_as=f"debug_chara{args.inspect}.html")
        if not html:
            print("取得失敗")
            return
        char_name = get_char_name_from_page(html)
        print(f"キャラ名: {char_name}")
        cards = parse_cards(html, char_name)
        print(f"カード数: {len(cards)}枚")
        for c in cards:
            print(f"  ID:{c['card_id']:5d} [{c['rarity_name']:3s}] {c['card_name']}")
        return

    cards = scrape_all(max_id=args.max)
    if not cards:
        print("カードを取得できませんでした")
        print("  python scrape_cards.py --inspect 1  でHTML構造を確認してください")
        return
    cards = assign_ids(cards)
    save_csv(cards)


if __name__ == "__main__":
    main()
