#!/usr/bin/env python3
"""
hatotank.net からあんガルキャラデータを取得して character_data.csv に保存する

使い方:
  python scrape_chardata.py
"""

import csv
import re
import time
import urllib.request
from pathlib import Path

BASE = "https://hatotank.net/ensemble_girls"
LIST_URL = f"{BASE}/egcharlist.php"
OUT_CSV = Path("character_data.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "ja,en;q=0.9",
    "Referer": BASE + "/",
}

FIELDS = ["name", "height", "weight", "birthday", "blood_type",
          "club", "committee", "class", "grade", "intro"]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as res:
        return res.read().decode("utf-8", errors="replace")


def parse_char_links(html: str) -> list[tuple[str, str]]:
    """キャラ一覧ページからキャラ名とURLを抽出"""
    # リンクパターン: egchar.php?id=XX や egchardetail.php?id=XX など
    links = re.findall(r'href="(egchar[^"]*\.php[^"]*)"[^>]*>([^<]{2,20})</a>', html)
    seen = set()
    result = []
    for url, name in links:
        name = name.strip()
        if name and url not in seen and not name.startswith("http"):
            seen.add(url)
            result.append((f"{BASE}/{url}", name))
    return result


def parse_char_page(html: str, name: str) -> dict:
    """個別キャラページからプロフィールを抽出"""
    data = {"name": name}

    # よくあるパターンでプロフィール抽出
    patterns = {
        "height": [r"身長[：:]\s*(\d+)\s*cm", r"(\d+)cm"],
        "weight": [r"体重[：:]\s*(\d+)\s*kg", r"(\d+)kg"],
        "birthday": [r"誕生日[：:]\s*([\d/月日]+)", r"(\d{1,2})[月/](\d{1,2})日?"],
        "blood_type": [r"血液型[：:]\s*([ABO]{1,2}[+\-型]?)", r"([ABOB型O]+型)"],
        "club": [r"部活動?[：:]\s*([^\s<\n]{2,15})", r"所属部活[：:]\s*([^\s<\n]{2,15})"],
        "committee": [r"委員会[：:]\s*([^\s<\n]{2,15})"],
        "class": [r"クラス[：:]\s*(\d[-ー]\w)", r"(\d年\w組)"],
        "grade": [r"学年[：:]\s*(\d)年?"],
    }

    # HTMLタグを除去してテキスト化
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)

    for field, pats in patterns.items():
        for pat in pats:
            m = re.search(pat, text)
            if m:
                data[field] = m.group(1).strip()
                break

    # 紹介文（テーブルの最初の長めのテキスト）
    # tdやpタグ内の長めのテキストを探す
    intro_candidates = re.findall(r'<(?:td|p)[^>]*>([^<]{20,200})</(?:td|p)>', html)
    if intro_candidates:
        # 最も長いものを紹介文として採用
        intro = max(intro_candidates, key=len).strip()
        data["intro"] = intro[:100]  # 100文字以内に収める

    return data


def scrape_from_list():
    """一覧ページからスクレイプ"""
    print(f"キャラ一覧取得中: {LIST_URL}")
    html = fetch(LIST_URL)

    links = parse_char_links(html)
    print(f"キャラリンク: {len(links)}件")

    if not links:
        # 一覧ページ自体にデータが埋め込まれている可能性
        print("リンクが見つかりません。一覧ページ直接解析を試みます...")
        return scrape_from_list_direct(html)

    results = []
    for i, (url, name) in enumerate(links, 1):
        print(f"  [{i}/{len(links)}] {name} ... ", end="", flush=True)
        try:
            char_html = fetch(url)
            data = parse_char_page(char_html, name)
            results.append(data)
            filled = sum(1 for k, v in data.items() if v and k != "name")
            print(f"OK ({filled}項目)")
        except Exception as e:
            print(f"失敗: {e}")
            results.append({"name": name})
        time.sleep(0.5)

    return results


def scrape_from_list_direct(html: str):
    """一覧ページのHTMLから直接データを抽出"""
    results = []
    # テーブル行を探す
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL)
    for row in rows:
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL)
        cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
        cells = [c for c in cells if c]
        if len(cells) >= 3:
            # 名前候補（2文字以上の日本語）
            name_cand = [c for c in cells if re.search(r"[ぁ-ん]{2,}|[ァ-ン]{2,}|[一-龥]{2,}", c)]
            if name_cand:
                data = {"name": name_cand[0]}
                # 数値を含むセルから身長・体重を推定
                nums = [(i, c) for i, c in enumerate(cells) if re.match(r"^\d{2,3}$", c)]
                for i, num in nums:
                    n = int(num)
                    if 140 <= n <= 180:
                        data["height"] = num
                    elif 35 <= n <= 70:
                        data["weight"] = num
                results.append(data)
    return results


def save_csv(results: list[dict]):
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in results:
            writer.writerow({f: row.get(f, "") for f in FIELDS})
    print(f"\n→ {OUT_CSV} に{len(results)}件保存しました")


def main():
    try:
        results = scrape_from_list()
        if results:
            save_csv(results)
        else:
            print("データが取得できませんでした")
            print("手動でCSVを作成する場合は: python manage_profiles.py --init")
    except Exception as e:
        print(f"エラー: {e}")
        print("\nサイトにアクセスできない場合は手動でCSVを作成してください:")
        print("  python manage_profiles.py --init")


if __name__ == "__main__":
    main()
