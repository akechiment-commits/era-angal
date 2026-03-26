#!/usr/bin/env python3
"""
あんガル キャラクター台詞生成スクリプト（マルコフ連鎖・API不要）
ゲームセリフを学習してキャラらしい新しい台詞を生成する

使い方:
  python generate_dialogue.py ひまり
  python generate_dialogue.py ひまり --count 20
  python generate_dialogue.py ひまり --keyword 好き
  python generate_dialogue.py --list
  python generate_dialogue.py ひまり --all
"""

import argparse
import json
import random
import re
from collections import defaultdict, Counter
from pathlib import Path

SCENARIO_DIR = Path("scenarios")
PROFILES_FILE = Path("character_profiles.json")

SITUATION_KEYWORDS = {
    "挨拶・会う":     ["おはよ", "こんにち", "こんばん", "はじめまして", "久しぶ", "やあ"],
    "好意・好き":     ["好き", "大好き", "嬉し", "素敵", "かわい", "ありがと"],
    "励ます・応援":   ["頑張", "諦めない", "大丈夫", "できる", "応援", "一緒に"],
    "照れ・恥ずかし": ["えっ", "そんな", "恥ずかし", "照れ", "もう", "やだ"],
    "怒る・不満":     ["もう", "なんで", "どうして", "信じられない", "ひどい", "怒"],
    "悲しむ":         ["悲し", "つらい", "寂し", "泣", "辛い", "どうしよう"],
    "楽しい・喜ぶ":   ["楽し", "嬉し", "やった", "最高", "すごい", "わあ"],
    "テスト・勉強":   ["テスト", "勉強", "試験", "点数", "授業", "宿題"],
    "放課後・帰宅":   ["放課後", "帰ろ", "一緒に帰", "部活", "寄り道"],
    "食べ物":         ["食べ", "おいし", "料理", "お腹", "ご飯", "甘い"],
}


# ===== マルコフ連鎖 =====

def build_markov(lines: list[str], n: int = 3) -> dict:
    """n文字マルコフ連鎖モデルを構築"""
    transitions = defaultdict(Counter)
    starters = []

    for line in lines:
        line = line.strip()
        if len(line) < n + 1:
            continue
        starters.append(line[:n])
        for i in range(len(line) - n):
            state = line[i:i + n]
            next_char = line[i + n]
            transitions[state][next_char] += 1
        # 末尾の終端マーク
        transitions[line[-n:]]["__END__"] += 3  # 重み強め

    return {"transitions": dict(transitions), "starters": starters, "n": n}


def markov_generate(model: dict, max_len: int = 60, seed: str = None) -> str:
    """マルコフ連鎖で1文生成"""
    transitions = model["transitions"]
    starters = model["starters"]
    n = model["n"]

    if not starters:
        return ""

    state = seed if (seed and len(seed) >= n and seed[:n] in transitions) else random.choice(starters)
    result = state

    for _ in range(max_len):
        if state not in transitions:
            break
        counter = transitions[state]
        total = sum(counter.values())
        r = random.randint(0, total - 1)
        cumsum = 0
        next_char = None
        for ch, cnt in counter.items():
            cumsum += cnt
            if r < cumsum:
                next_char = ch
                break

        if next_char == "__END__" or next_char in ("。", "！", "？", "…", "\n"):
            if next_char != "__END__":
                result += next_char
            break

        result += next_char
        state = result[-n:]

    return result.strip()


def generate_many(model: dict, n_lines: int = 10, keyword: str = None,
                  min_len: int = 8) -> list[str]:
    """複数行生成。短すぎる・重複を除去してn_lines個返す"""
    results = []
    seen = set()
    attempts = 0

    # キーワードに近いstarterを選ぶ
    seed = None
    if keyword and model["starters"]:
        kw_starters = [s for s in model["starters"] if keyword[:2] in s]
        if kw_starters:
            seed = random.choice(kw_starters)

    while len(results) < n_lines and attempts < n_lines * 20:
        attempts += 1
        use_seed = seed if (seed and random.random() < 0.3) else None
        line = markov_generate(model, seed=use_seed)

        if len(line) < min_len:
            continue
        if line in seen:
            continue
        seen.add(line)
        results.append(line)

    return results


# ===== ユーティリティ =====

def load_character_lines(name: str) -> list[str]:
    all_lines = []
    pattern = re.compile(rf"^【{re.escape(name)}】(.+)$", re.MULTILINE)
    for txt in sorted(SCENARIO_DIR.glob("*.txt")):
        try:
            content = txt.read_text(encoding="utf-8")
            all_lines.extend(pattern.findall(content))
        except Exception:
            continue
    return all_lines


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


def main():
    parser = argparse.ArgumentParser(description="あんガル キャラ台詞生成（マルコフ連鎖）")
    parser.add_argument("name", nargs="?", help="キャラ名")
    parser.add_argument("--keyword", "-k", help="話題キーワード")
    parser.add_argument("--situation", "-s",
                        help=f"シチュエーション: {', '.join(SITUATION_KEYWORDS.keys())}")
    parser.add_argument("--count", "-n", type=int, default=10, help="生成する台詞数")
    parser.add_argument("--order", type=int, default=3, help="マルコフ次数（デフォルト3）")
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
    total = profile["total_lines"] if profile else len(lines)
    fp = profile["main_first_person"] if profile else "?"
    print(f"\n【{name}】 {total}行を学習中... (一人称:{fp})")

    model = build_markov(lines, n=args.order)
    print(f"モデル構築完了（状態数: {len(model['transitions']):,}）\n")

    if args.all:
        out_dir = Path(f"dialogue_{name}")
        out_dir.mkdir(exist_ok=True)
        for situation, keywords in SITUATION_KEYWORDS.items():
            keyword = keywords[0]
            generated = generate_many(model, args.count, keyword=keyword)
            out_file = out_dir / f"{situation}.txt"
            out_file.write_text("\n".join(generated), encoding="utf-8")
            print(f"  {situation}: {len(generated)}件")
        print(f"\n→ {out_dir}/ に保存しました")
        return

    keyword = args.keyword
    if not keyword and args.situation:
        kws = SITUATION_KEYWORDS.get(args.situation, [])
        keyword = kws[0] if kws else None
        if keyword:
            print(f"シチュエーション「{args.situation}」→ キーワード「{keyword}」で生成\n")

    generated = generate_many(model, args.count, keyword=keyword)
    for i, l in enumerate(generated, 1):
        print(f"{i}. {l}")


if __name__ == "__main__":
    main()
