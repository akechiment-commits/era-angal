#!/usr/bin/env python3
"""
あんガル キャラクター台詞検索スクリプト（API不要・完全無料）
実際のゲームセリフからキャラらしい台詞を検索して返す

使い方:
  python generate_dialogue.py ひまり
  python generate_dialogue.py ひまり --keyword "好き"
  python generate_dialogue.py --list
"""

import argparse
import json
import random
import re
from pathlib import Path

SCENARIO_DIR = Path("scenarios")
PROFILES_FILE = Path("character_profiles.json")

# シチュエーション別キーワード
SITUATION_KEYWORDS = {
    "挨拶・会う":       ["おはよ", "こんにち", "こんばん", "はじめまして", "久しぶ", "やあ", "あ、"],
    "好意・好き":       ["好き", "大好き", "嬉し", "素敵", "かわい", "かっこい", "ありがと"],
    "励ます・応援":     ["頑張", "諦めない", "大丈夫", "できる", "応援", "一緒に", "負けない"],
    "照れ・恥ずかし":   ["えっ", "そんな", "恥ずかし", "照れ", "ど、どうして", "もう", "やだ"],
    "怒る・不満":       ["もう", "なんで", "どうして", "信じられない", "最悪", "ひどい", "怒"],
    "悲しむ":           ["悲し", "つらい", "寂し", "泣", "辛い", "嫌だ", "どうしよう"],
    "楽しい・喜ぶ":     ["楽し", "嬉し", "やった", "最高", "すごい", "わあ", "うれし"],
    "テスト・勉強":     ["テスト", "勉強", "試験", "点数", "授業", "宿題", "先生"],
    "放課後・帰宅":     ["放課後", "帰ろ", "一緒に帰", "部活", "寄り道", "どこ行く"],
    "食べ物":           ["食べ", "おいし", "料理", "お腹", "ご飯", "おやつ", "甘い"],
}


def load_character_lines(name: str) -> list[str]:
    """指定キャラの全セリフを収集"""
    all_lines = []
    pattern = re.compile(rf"^【{re.escape(name)}】(.+)$", re.MULTILINE)
    for txt in sorted(SCENARIO_DIR.glob("*.txt")):
        try:
            content = txt.read_text(encoding="utf-8")
            all_lines.extend(pattern.findall(content))
        except Exception:
            continue
    return all_lines


def search_lines(lines: list[str], keywords: list[str], n: int = 10) -> list[str]:
    """キーワードに一致するセリフを検索してランダムに返す"""
    matched = []
    for line in lines:
        if any(kw in line for kw in keywords):
            matched.append(line)

    if not matched:
        # ヒットしない場合はランダムに返す
        return random.sample(lines, min(n, len(lines)))

    if len(matched) <= n:
        return matched
    return random.sample(matched, n)


def load_profile(name: str) -> dict | None:
    if not PROFILES_FILE.exists():
        return None
    with open(PROFILES_FILE, encoding="utf-8") as f:
        profiles = json.load(f)
    for p in profiles:
        if p["name"] == name:
            return p
    return None


def list_characters():
    if not PROFILES_FILE.exists():
        print("character_profiles.json が見つかりません。analyze_characters.py を先に実行してください")
        return
    with open(PROFILES_FILE, encoding="utf-8") as f:
        profiles = json.load(f)
    print(f"キャラ数: {len(profiles)}人\n")
    for p in profiles:
        print(f"  {p['name']:15s} {p['total_lines']:4d}行  一人称:{p['main_first_person']}")


def show_all_situations(name: str, lines: list[str], n: int):
    out_dir = Path(f"dialogue_{name}")
    out_dir.mkdir(exist_ok=True)
    for situation, keywords in SITUATION_KEYWORDS.items():
        results = search_lines(lines, keywords, n)
        out_file = out_dir / f"{situation}.txt"
        out_file.write_text("\n".join(results), encoding="utf-8")
        print(f"\n【{name}】{situation} ({len(results)}件)")
        for l in results:
            print(f"  ・{l}")
    print(f"\n→ {out_dir}/ に保存しました")


def main():
    parser = argparse.ArgumentParser(description="あんガル キャラ台詞検索（API不要）")
    parser.add_argument("name", nargs="?", help="キャラ名")
    parser.add_argument("--keyword", "-k", help="検索キーワード（複数はカンマ区切り）")
    parser.add_argument("--situation", "-s",
                        help=f"シチュエーション: {', '.join(SITUATION_KEYWORDS.keys())}")
    parser.add_argument("--count", "-n", type=int, default=10, help="取得件数")
    parser.add_argument("--list", "-l", action="store_true", help="キャラ一覧表示")
    parser.add_argument("--all", "-a", action="store_true", help="全シチュエーション出力")
    args = parser.parse_args()

    if args.list:
        list_characters()
        return

    if not args.name:
        parser.print_help()
        return

    name = args.name
    lines = load_character_lines(name)
    if not lines:
        print(f"エラー: 「{name}」のセリフが見つかりません")
        return

    profile = load_profile(name)
    if profile:
        print(f"\n【{name}】 {profile['total_lines']}行 / 一人称:{profile['main_first_person']}")

    if args.all:
        show_all_situations(name, lines, args.count)
        return

    # キーワード指定
    if args.keyword:
        keywords = [k.strip() for k in args.keyword.split(",")]
    elif args.situation and args.situation in SITUATION_KEYWORDS:
        keywords = SITUATION_KEYWORDS[args.situation]
        print(f"シチュエーション「{args.situation}」で検索")
    else:
        # 何も指定なしはランダム
        keywords = []

    if keywords:
        results = search_lines(lines, keywords, args.count)
        print(f"キーワード {keywords} にマッチ: {len(results)}件\n")
    else:
        results = random.sample(lines, min(args.count, len(lines)))
        print(f"ランダム {len(results)}件\n")

    for l in results:
        print(f"・{l}")


if __name__ == "__main__":
    main()
