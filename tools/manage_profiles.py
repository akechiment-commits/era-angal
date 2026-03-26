#!/usr/bin/env python3
"""
キャラクタープロフィールCSV管理スクリプト

使い方:
  python manage_profiles.py --init       # CSVテンプレート生成（キャラ名は自動抽出）
  python manage_profiles.py --show ひまり # 入力済みプロフィール確認

CSVを開いてプロフィールを手入力後、make_character_prompt.py が自動で読み込みます。
"""

import argparse
import csv
import re
from pathlib import Path

SCENARIO_DIR = Path("scenarios")
PROFILE_CSV = Path("character_data.csv")

FIELDS = [
    "name",        # キャラ名（キー）
    "height",      # 身長 (cm)
    "weight",      # 体重 (kg)
    "birthday",    # 誕生日 (MM/DD)
    "blood_type",  # 血液型
    "club",        # 部活
    "committee",   # 委員会
    "class",       # クラス (例: 2-A)
    "grade",       # 学年
    "intro",       # 紹介文（ゲーム内の説明文）
]


def get_all_char_names() -> list[str]:
    """シナリオから全キャラ名を抽出（セリフ数順）"""
    from collections import Counter
    counts = Counter()
    pattern = re.compile(r"^【(.+?)】", re.MULTILINE)
    for txt in SCENARIO_DIR.glob("*.txt"):
        try:
            content = txt.read_text(encoding="utf-8")
            for m in pattern.finditer(content):
                name = m.group(1).strip()
                if name not in ("ナレーション", "???", ""):
                    counts[name] += 1
        except Exception:
            continue
    return [name for name, _ in counts.most_common()]


def init_csv():
    """CSVテンプレートを生成"""
    if PROFILE_CSV.exists():
        print(f"{PROFILE_CSV} は既に存在します。上書きしますか？ (y/N): ", end="")
        if input().strip().lower() != "y":
            print("キャンセルしました")
            return

    print("キャラ名を抽出中...")
    names = get_all_char_names()
    print(f"{len(names)}人分のテンプレートを生成します")

    with open(PROFILE_CSV, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for name in names:
            writer.writerow({"name": name})

    print(f"→ {PROFILE_CSV} を生成しました")
    print(f"   Excelやメモ帳で開いて各キャラのプロフィールを入力してください")
    print(f"   入力例:")
    print(f"     height=158, weight=48, birthday=04/01, blood_type=A")
    print(f"     club=ラクロス部, committee=なし, class=2-A, grade=2")
    print(f"     intro=明るく元気な〜（ゲーム内の紹介文をコピー）")


def load_profile_csv() -> dict[str, dict]:
    """CSVからプロフィールを読み込む"""
    if not PROFILE_CSV.exists():
        return {}
    profiles = {}
    with open(PROFILE_CSV, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            if name:
                profiles[name] = {k: v.strip() for k, v in row.items() if v and v.strip()}
    return profiles


def show_profile(name: str):
    profiles = load_profile_csv()
    if name not in profiles:
        print(f"「{name}」のデータがありません（{PROFILE_CSV} に入力してください）")
        return
    p = profiles[name]
    print(f"\n【{name}】")
    labels = {
        "height": "身長", "weight": "体重", "birthday": "誕生日",
        "blood_type": "血液型", "club": "部活", "committee": "委員会",
        "class": "クラス", "grade": "学年", "intro": "紹介文"
    }
    for key, label in labels.items():
        val = p.get(key, "")
        if val:
            print(f"  {label}: {val}")


def main():
    parser = argparse.ArgumentParser(description="キャラクタープロフィールCSV管理")
    parser.add_argument("--init", action="store_true", help="CSVテンプレート生成")
    parser.add_argument("--show", metavar="キャラ名", help="プロフィール表示")
    args = parser.parse_args()

    if args.init:
        init_csv()
    elif args.show:
        show_profile(args.show)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
