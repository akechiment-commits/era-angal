#!/usr/bin/env python3
"""
hatotank.net からあんガルキャラデータを取得して character_data.csv に保存する

使い方:
  python scrape_chardata.py            # 全取得
  python scrape_chardata.py --debug    # HTMLをファイルに保存してデバッグ
"""

import argparse
import csv
import re
import time
import urllib.request
from pathlib import Path

BASE = "https://hatotank.net/ensemble_girls"
LIST_URL = f"{BASE}/egcharlist.php"
OUT_CSV = Path("character_data.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
    "Referer": BASE + "/",
}

FIELDS = ["name", "height", "weight", "birthday", "blood_type",
          "club", "committee", "class", "grade", "intro", "old_intro"]

# 明らかにキャラ名ではない文字列
NOT_CHAR_NAMES = {
    "デフォルト", "名前", "学年クラス", "誕生日", "血液型", "身長", "体重",
    "部活", "委員会", "紹介文", "クラス", "学年", "所属", "プロフィール",
    "一覧", "検索", "フィルター", "ソート", "TOP", "トップ",
}


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as res:
        raw = res.read()
        # エンコーディング自動判定
        for enc in ("utf-8", "shift_jis", "euc-jp"):
            try:
                return raw.decode(enc)
            except Exception:
                continue
        return raw.decode("utf-8", errors="replace")


def is_valid_char_name(name: str) -> bool:
    """キャラ名として有効か判定"""
    name = name.strip()
    if len(name) < 2 or len(name) > 15:
        return False
    if name in NOT_CHAR_NAMES:
        return False
    if any(name.startswith(n) for n in NOT_CHAR_NAMES):
        return False
    # 日本語が含まれているか
    if not re.search(r"[ぁ-んァ-ン一-龥]", name):
        return False
    # 数字のみや記号のみはNG
    if re.match(r"^[\d\s\W]+$", name):
        return False
    return True


def parse_char_links(html: str) -> list[tuple[str, str]]:
    """一覧ページからキャラ名とURLを抽出"""
    # egchar.php?id=XX 形式のリンクを探す
    links = re.findall(
        r'href=["\']?(egchar[^"\'>\s]*)["\']?[^>]*>([^<]{2,20})</a',
        html, re.IGNORECASE
    )
    seen_urls = set()
    result = []
    for url, name in links:
        name = re.sub(r"<[^>]+>", "", name).strip()
        url_full = f"{BASE}/{url}"
        if url_full not in seen_urls and is_valid_char_name(name):
            seen_urls.add(url_full)
            result.append((url_full, name))
    return result


def parse_char_page(html: str, name: str) -> dict:
    """個別キャラページからプロフィールを抽出"""
    data = {"name": name}
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&nbsp;", " ", text)
    text = re.sub(r"\s+", " ", text)

    # 各フィールドの抽出パターン
    patterns = {
        "height":     [r"身長[：:\s]*(\d{3})\s*cm", r"(\d{3})cm"],
        "weight":     [r"体重[：:\s]*(\d{2,3})\s*kg", r"(\d{2})kg"],
        "birthday":   [r"誕生日[：:\s]*(\d{1,2})[月/](\d{1,2})日?",
                       r"(\d{1,2})/(\d{1,2})"],
        "blood_type": [r"血液型[：:\s]*([ABO]{1,2}[+\-型]?)\b"],
        "club":       [r"部活動?[：:\s]*([^\s。、]{2,12}部)",
                       r"所属部活[：:\s]*([^\s。、]{2,12})"],
        "committee":  [r"委員会[：:\s]*([^\s。、]{2,10}委員会)",
                       r"委員[：:\s]*([^\s。、]{2,10})"],
        "class":      [r"(\d)\s*[-ー年]\s*([A-Zａ-ｚA-Z])"],
        "grade":      [r"(\d)\s*年生?(?:生|組)?"],
    }

    for field, pats in patterns.items():
        for pat in pats:
            m = re.search(pat, text)
            if m:
                if field == "birthday" and len(m.groups()) >= 2:
                    data[field] = f"{int(m.group(1)):02d}/{int(m.group(2)):02d}"
                elif field == "class" and len(m.groups()) >= 2:
                    data[field] = f"{m.group(1)}-{m.group(2)}"
                else:
                    data[field] = m.group(1).strip()
                break

    # 紹介文と旧紹介文を抽出（長いテキストブロックから）
    # td/p/div 内の20文字以上のテキストを収集
    long_texts = re.findall(
        r'<(?:td|p|div)[^>]*>\s*([^\n<]{20,300})\s*</(?:td|p|div)>',
        html, re.DOTALL
    )
    long_texts = [t.strip() for t in long_texts if len(t.strip()) >= 20]
    # ナビゲーション・UI文字列を除外
    long_texts = [t for t in long_texts
                  if not re.search(r"Copyright|ページ|メニュー|ログイン|検索", t)]

    if len(long_texts) >= 1:
        data["intro"] = long_texts[0][:150]
    if len(long_texts) >= 2:
        data["old_intro"] = long_texts[1][:150]

    return data


def scrape_by_links(html: str) -> list[dict]:
    """個別ページリンクをたどってスクレイプ"""
    links = parse_char_links(html)
    print(f"  キャラリンク検出: {len(links)}件")

    results = []
    for i, (url, name) in enumerate(links, 1):
        print(f"  [{i:2d}/{len(links)}] {name} ... ", end="", flush=True)
        try:
            char_html = fetch(url)
            data = parse_char_page(char_html, name)
            results.append(data)
            filled = sum(1 for k, v in data.items() if v and k != "name")
            print(f"OK ({filled}項目)")
        except Exception as e:
            print(f"失敗: {e}")
            results.append({"name": name})
        time.sleep(0.3)
    return results


def scrape_by_id(max_id: int = 100) -> list[dict]:
    """ID連番で個別ページをブルートフォース取得"""
    print(f"  ID 1〜{max_id} をブルートフォース取得...")
    results = []
    consecutive_miss = 0

    for i in range(1, max_id + 1):
        url = f"{BASE}/egchar.php?id={i}"
        try:
            html = fetch(url)
            # キャラページかどうか判定（名前らしきテキストがあるか）
            text = re.sub(r"<[^>]+>", " ", html)
            if "身長" not in text and "部活" not in text:
                consecutive_miss += 1
                if consecutive_miss >= 10:
                    print(f"  ID {i}: 10連続でキャラページなし、終了")
                    break
                continue
            consecutive_miss = 0

            # 名前を抽出（h1/h2/title タグから）
            name_m = re.search(r'<(?:h1|h2|title)[^>]*>([^<]{2,15})</(?:h1|h2|title)>', html)
            name = name_m.group(1).strip() if name_m else f"キャラ{i}"
            name = re.sub(r"\s*[-|｜]\s*.*$", "", name).strip()

            if not is_valid_char_name(name):
                continue

            data = parse_char_page(html, name)
            results.append(data)
            print(f"  [ID:{i:2d}] {name} ({sum(1 for k,v in data.items() if v and k!='name')}項目)")
        except Exception:
            consecutive_miss += 1
            if consecutive_miss >= 10:
                break
        time.sleep(0.3)

    return results


def scrape_list_direct(html: str) -> list[dict]:
    """一覧ページのテーブルから直接データ抽出"""
    results = []
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL | re.IGNORECASE)
    for row in rows:
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.DOTALL | re.IGNORECASE)
        cells = [re.sub(r"<[^>]+>", "", c).strip() for c in cells]
        cells = [c for c in cells if c and c != "\xa0"]
        if len(cells) < 3:
            continue

        # 最初の日本語セルをキャラ名候補に
        name = cells[0] if is_valid_char_name(cells[0]) else None
        if not name:
            for c in cells:
                if is_valid_char_name(c):
                    name = c
                    break
        if not name:
            continue

        data = {"name": name}
        for cell in cells:
            n_match = re.match(r"^(\d{2,3})$", cell)
            if n_match:
                n = int(n_match.group(1))
                if 140 <= n <= 185 and "height" not in data:
                    data["height"] = cell
                elif 35 <= n <= 75 and "weight" not in data:
                    data["weight"] = cell
            if re.match(r"^\d{1,2}/\d{1,2}$", cell):
                data["birthday"] = cell
            if re.match(r"^[ABO]{1,2}型?$", cell):
                data["blood_type"] = cell
            if cell.endswith("部") and len(cell) <= 12:
                data["club"] = cell
            if cell.endswith("委員会") and len(cell) <= 12:
                data["committee"] = cell
            if len(cell) >= 20 and "intro" not in data:
                data["intro"] = cell[:150]

        if len(data) >= 2:
            results.append(data)

    return results


def dedup(results: list[dict]) -> list[dict]:
    """名前で重複除去"""
    seen = {}
    for r in results:
        name = r["name"]
        if name not in seen:
            seen[name] = r
        else:
            # データが多い方を採用
            if sum(1 for v in r.values() if v) > sum(1 for v in seen[name].values() if v):
                seen[name] = r
    return list(seen.values())


def save_csv(results: list[dict]):
    results = dedup(results)
    results.sort(key=lambda x: x.get("name", ""))
    with open(OUT_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in results:
            writer.writerow({f: row.get(f, "") for f in FIELDS})
    print(f"\n→ {OUT_CSV} に{len(results)}件保存しました")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="HTMLをファイルに保存")
    parser.add_argument("--id-scan", action="store_true", help="IDブルートフォースも実行")
    args = parser.parse_args()

    print(f"一覧ページ取得中: {LIST_URL}")
    try:
        html = fetch(LIST_URL)
    except Exception as e:
        print(f"一覧ページ取得失敗: {e}")
        return

    if args.debug:
        Path("debug_list.html").write_text(html, encoding="utf-8")
        print("→ debug_list.html に保存しました（ブラウザで開いて確認できます）")

    results = []

    # 方法1: 個別ページリンクをたどる
    print("\n【方法1】個別ページリンク取得")
    link_results = scrape_by_links(html)
    print(f"  → {len(link_results)}件取得")
    results.extend(link_results)

    # 方法2: 一覧ページからの直接解析
    print("\n【方法2】一覧ページ直接解析")
    direct_results = scrape_list_direct(html)
    # 方法1で取れなかった行だけ追加
    existing_names = {r["name"] for r in results}
    new_direct = [r for r in direct_results if r["name"] not in existing_names]
    print(f"  → {len(new_direct)}件追加")
    results.extend(new_direct)

    # 方法3: IDブルートフォース（オプション）
    if args.id_scan or len(results) < 60:
        print(f"\n【方法3】IDブルートフォース（現在{len(results)}件、71件未満のため実行）")
        id_results = scrape_by_id(max_id=100)
        existing_names = {r["name"] for r in results}
        new_id = [r for r in id_results if r["name"] not in existing_names]
        print(f"  → {len(new_id)}件追加")
        results.extend(new_id)

    print(f"\n合計: {len(dedup(results))}件")
    if results:
        save_csv(results)
    else:
        print("データが取得できませんでした")


if __name__ == "__main__":
    main()
