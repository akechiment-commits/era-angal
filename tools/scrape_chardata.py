#!/usr/bin/env python3
"""
hatotank.net からあんガルキャラデータを取得して character_data.csv に保存する

使い方:
  python scrape_chardata.py            # 全取得
  python scrape_chardata.py --debug    # HTMLをファイルに保存してデバッグ
"""

import argparse
import csv
import html as html_module
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

FIELDS = ["name", "height", "weight", "three_sizes", "birthday", "blood_type",
          "club", "committee", "class", "grade", "fav_color", "family", "hobbies",
          "intro", "old_intro"]

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
    """一覧ページからキャラ名とURLを抽出（画像リンク・テキストリンク両対応）"""
    seen_urls = set()
    result = []

    # パターン1: <a href="egchar.php?...">キャラ名</a>（テキストリンク）
    for url, name in re.findall(
        r'href=["\']?(egchar[^"\'>\s]*)["\']?[^>]*>([^<\[\]]{2,15})</a',
        html, re.IGNORECASE
    ):
        name = name.strip()
        url_full = f"{BASE}/{url}"
        if url_full not in seen_urls and is_valid_char_name(name):
            seen_urls.add(url_full)
            result.append((url_full, name))

    # パターン2: alt="[キャラ名]" の img タグから名前を抽出してURLを取得
    for m in re.finditer(
        r'<a\s+href=["\']?(egchar[^"\'>\s]*)["\']?[^>]*>\s*<img[^>]+alt=["\'\[]([^\]"\']{2,15})[\]"\']*[^>]*>',
        html, re.IGNORECASE
    ):
        url, name = m.group(1), m.group(2).strip()
        url_full = f"{BASE}/{url}"
        if url_full not in seen_urls and is_valid_char_name(name):
            seen_urls.add(url_full)
            result.append((url_full, name))

    return result


def get_all_list_pages() -> list[str]:
    """一覧ページを全ページ取得（ページネーション対応）"""
    pages = []

    # まず名前順ソートで全件取得を試みる
    sort_urls = [
        LIST_URL,
        LIST_URL + "?sort=name",
        LIST_URL + "?order=name",
        LIST_URL + "?sort=kana",
    ]

    html = ""
    for url in sort_urls:
        try:
            html = fetch(url)
            pages.append(html)
            print(f"  取得: {url}")
            break
        except Exception as e:
            print(f"  失敗: {url} ({e})")

    if not html:
        return pages

    # ページネーションリンクを探す
    page_links = re.findall(
        r'href=["\']?(egcharlist[^"\'>\s]*(?:page|p|start|offset)=[^"\'>\s&]*)["\']?',
        html, re.IGNORECASE
    )
    page_links += re.findall(
        r'href=["\']?(egcharlist\.php\?[^"\'>\s]*)["\']?',
        html, re.IGNORECASE
    )

    seen_pages = {LIST_URL}
    for link in page_links:
        url = f"{BASE}/{link}" if not link.startswith("http") else link
        if url not in seen_pages:
            seen_pages.add(url)
            try:
                page_html = fetch(url)
                pages.append(page_html)
                print(f"  追加ページ取得: {url}")
                time.sleep(0.3)
            except Exception as e:
                print(f"  追加ページ失敗: {url} ({e})")

    return pages


def clean_text(s: str) -> str:
    """HTMLエンティティをデコードして余分な空白を除去"""
    s = html_module.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def is_intro_text(s: str) -> bool:
    """紹介文らしいテキストかどうか判定（日本語の文章であること）"""
    # 数字・記号・スラッシュだけはNG（スリーサイズ等を除外）
    if re.match(r"^[\d\s/\-・&;nbsp]+$", s):
        return False
    # 日本語文字が10文字以上含まれていること
    jp_chars = re.findall(r"[ぁ-んァ-ン一-龥]", s)
    if len(jp_chars) < 10:
        return False
    return True


def parse_char_page(html: str, name: str) -> dict:
    """個別キャラページからプロフィールを抽出"""
    data = {"name": name}

    # HTMLエンティティをデコードしてテキスト化
    text = re.sub(r"<[^>]+>", " ", html)
    text = clean_text(text)

    # 各フィールドの抽出パターン
    patterns = {
        "height":     [r"身長[：:\s]*(\d{3})\s*(?:cm|ｃｍ)?", r"(\d{3})cm"],
        "weight":     [r"体重[：:\s]*(\d{2,3})\s*(?:kg|ｋｇ)?", r"(\d{2})kg"],
        "birthday":   [r"誕生日[：:\s]*(\d{1,2})[月/](\d{1,2})日?"],
        "blood_type": [r"血液型[：:\s]*([ABOB]{1,2}型?)"],
        "club":       [r"部活動?[：:\s]*([^\s。、\d]{2,12}部)"],
        "committee":  [r"([^\s。、]{2,10}委員会)"],
        "class":      [r"(\d)\s*[-ー]\s*([A-Z])"],
        "grade":      [r"(\d)\s*年生?"],
        "fav_color":  [r"好きな色[：:\s]*([^\s。、\n]{2,20})"],
        "family":     [r"家族構成[：:\s]*([^\n。]{5,60})", r"家族[：:\s]*([^\n。]{5,60})"],
        "hobbies":    [r"趣味[：:\s]*([^\n。、]{2,40})"],
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

    # スリーサイズ (B/W/H)
    ts = re.search(r"スリーサイズ[：:\s]*(\d{2,3})\s*/\s*(\d{2,3})\s*/\s*(\d{2,3})", text)
    if not ts:
        ts = re.search(r"B[：:\s]*(\d{2,3})\s*[/・]\s*W[：:\s]*(\d{2,3})\s*[/・]\s*H[：:\s]*(\d{2,3})", text)
    if not ts:
        # 数値3つのスラッシュ区切り（文脈からスリーサイズと判断できる場合）
        ts = re.search(r"(?:バスト|ウエスト|ヒップ)[^\d]*(\d{2,3})\s*/\s*(\d{2,3})\s*/\s*(\d{2,3})", text)
    if ts:
        data["three_sizes"] = f"{ts.group(1)}/{ts.group(2)}/{ts.group(3)}"

    # 紹介文と旧紹介文：日本語の文章が入っているtd/p/divを抽出
    intro_texts = []
    for tag in ("td", "p", "div", "span"):
        for m in re.finditer(
            rf'<{tag}[^>]*>(.*?)</{tag}>',
            html, re.DOTALL | re.IGNORECASE
        ):
            raw = m.group(1)
            # 内部タグを除去してテキスト化
            t = re.sub(r"<[^>]+>", "", raw)
            t = clean_text(t)
            if len(t) >= 25 and is_intro_text(t):
                intro_texts.append(t)

    # 重複除去・長い順にソート
    seen = set()
    unique_intros = []
    for t in intro_texts:
        key = t[:30]
        if key not in seen:
            seen.add(key)
            unique_intros.append(t)

    # 除外ワード（ナビ・UI系）
    unique_intros = [t for t in unique_intros
                     if not re.search(r"Copyright|メニュー|ログイン|検索|一覧に戻|プロフィール", t)]

    if len(unique_intros) >= 1:
        data["intro"] = unique_intros[0][:200]
    if len(unique_intros) >= 2:
        data["old_intro"] = unique_intros[1][:200]

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


def dump_char_html(name: str):
    """1キャラのHTMLと抽出テキストをファイルに保存してデバッグ"""
    print(f"一覧ページ取得中...")
    pages = get_all_list_pages()
    all_links = {}
    for html in pages:
        for url, n in parse_char_links(html):
            all_links[n] = url

    if name not in all_links:
        print(f"「{name}」が見つかりません。検出済み: {list(all_links.keys())[:10]}")
        return

    url = all_links[name]
    print(f"取得中: {url}")
    html = fetch(url)

    # 生HTML保存
    Path(f"debug_{name}.html").write_text(html, encoding="utf-8")
    print(f"→ debug_{name}.html に保存")

    # タグ除去テキスト保存
    text = re.sub(r"<[^>]+>", " ", html)
    text = clean_text(text)
    Path(f"debug_{name}_text.txt").write_text(text, encoding="utf-8")
    print(f"→ debug_{name}_text.txt に保存")

    # parse結果表示
    data = parse_char_page(html, name)
    print(f"\n抽出結果:")
    for k, v in data.items():
        print(f"  {k}: {v!r}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="HTMLをファイルに保存")
    parser.add_argument("--id-scan", action="store_true", help="IDブルートフォースも実行")
    parser.add_argument("--dump-char", metavar="キャラ名", help="1キャラのHTMLを保存してデバッグ")
    args = parser.parse_args()

    if args.dump_char:
        dump_char_html(args.dump_char)
        return

    print(f"一覧ページ取得中（全ページ）...")
    pages = get_all_list_pages()
    if not pages:
        print("一覧ページ取得失敗")
        return

    if args.debug:
        for i, html in enumerate(pages):
            fname = f"debug_list_p{i+1}.html"
            Path(fname).write_text(html, encoding="utf-8")
            print(f"→ {fname} に保存しました")

    results = []

    # 方法1: 全ページから個別ページリンクをたどる
    print("\n【方法1】個別ページリンク取得")
    all_links = {}
    for html in pages:
        for url, name in parse_char_links(html):
            if url not in all_links:
                all_links[url] = name
    print(f"  リンク検出: {len(all_links)}件")

    for i, (url, name) in enumerate(all_links.items(), 1):
        print(f"  [{i:2d}/{len(all_links)}] {name} ... ", end="", flush=True)
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

    print(f"  → {len(results)}件取得")

    # 方法2: 一覧ページからの直接解析（リンクで取れなかった分の補完）
    print("\n【方法2】一覧ページ直接解析（補完）")
    existing_names = {r["name"] for r in results}
    for html in pages:
        direct_results = scrape_list_direct(html)
        new_direct = [r for r in direct_results if r["name"] not in existing_names]
        for r in new_direct:
            existing_names.add(r["name"])
        results.extend(new_direct)
    print(f"  → 合計{len(dedup(results))}件")

    # 方法3: IDブルートフォース（取得数が少ない場合）
    if args.id_scan or len(dedup(results)) < 60:
        print(f"\n【方法3】IDブルートフォース（現在{len(dedup(results))}件）")
        id_results = scrape_by_id(max_id=100)
        existing_names = {r["name"] for r in results}
        new_id = [r for r in id_results if r["name"] not in existing_names]
        print(f"  → {len(new_id)}件追加")
        results.extend(new_id)

    final = dedup(results)
    print(f"\n合計: {len(final)}件")
    if final:
        save_csv(final)
    else:
        print("データが取得できませんでした")


if __name__ == "__main__":
    main()
