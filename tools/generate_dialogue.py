#!/usr/bin/env python3
"""
あんガル キャラクター台詞生成スクリプト（フレーズ連鎖・API不要）
読点で区切ったフレーズを繋いで自然な日本語のセリフを生成する

使い方:
  python generate_dialogue.py ひまり
  python generate_dialogue.py ひまり --keyword 好き
  python generate_dialogue.py ひまり --situation 励ます・応援
  python generate_dialogue.py ひまり --all
  python generate_dialogue.py --list
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
    "挨拶・会う":     ["おはよ", "こんにち", "こんばん", "はじめまして", "久しぶ"],
    "好意・好き":     ["好き", "大好き", "嬉し", "素敵", "かわい", "ありがと"],
    "励ます・応援":   ["頑張", "諦めない", "大丈夫", "できる", "応援", "一緒"],
    "照れ・恥ずかし": ["えっ", "そんな", "恥ずかし", "照れ", "もう", "やだ"],
    "怒る・不満":     ["もう", "なんで", "どうして", "信じられない", "ひどい"],
    "悲しむ":         ["悲し", "つらい", "寂し", "泣", "辛い", "どうしよう"],
    "楽しい・喜ぶ":   ["楽し", "嬉し", "やった", "最高", "すごい", "わあ"],
    "テスト・勉強":   ["テスト", "勉強", "試験", "点数", "授業", "宿題"],
    "放課後・帰宅":   ["放課後", "帰ろ", "一緒に帰", "部活", "寄り道"],
    "食べ物":         ["食べ", "おいし", "料理", "お腹", "ご飯", "甘い"],
}

# 文末判定
SENTENCE_ENDS = re.compile(r"[。！？…♪～〜]$")
# フレーズ分割（読点・文末記号で分割しつつ記号を保持）
SPLIT_PATTERN = re.compile(r"([^、。！？…♪～〜]+[、。！？…♪～〜]?)")


def split_to_phrases(line: str) -> list[str]:
    """1行を読点・文末記号単位のフレーズに分割"""
    line = line.strip()
    phrases = [m.group(0) for m in SPLIT_PATTERN.finditer(line) if m.group(0).strip()]
    return phrases


def build_model(lines: list[str]) -> dict:
    """
    フレーズ遷移モデルを構築
    - transitions: フレーズ → 次のフレーズの頻度
    - starters: 文頭になりやすいフレーズ
    - terminals: 文末フレーズ（。！？で終わるもの）
    - by_keyword: キーワード → そのキーワードを含むフレーズ
    """
    transitions = defaultdict(Counter)
    starters = Counter()
    terminals = set()
    by_keyword = defaultdict(list)
    all_phrases = set()

    for line in lines:
        phrases = split_to_phrases(line)
        if not phrases:
            continue

        starters[phrases[0]] += 1
        for phrase in phrases:
            all_phrases.add(phrase)
            if SENTENCE_ENDS.search(phrase):
                terminals.add(phrase)

        for i in range(len(phrases) - 1):
            transitions[phrases[i]][phrases[i + 1]] += 1

    # キーワードインデックス
    for phrase in all_phrases:
        for kw_list in SITUATION_KEYWORDS.values():
            for kw in kw_list:
                if kw in phrase:
                    by_keyword[kw].append(phrase)

    return {
        "transitions": dict(transitions),
        "starters": starters,
        "terminals": terminals,
        "by_keyword": dict(by_keyword),
        "all_phrases": list(all_phrases),
    }


def sample_weighted(counter: Counter) -> str:
    total = sum(counter.values())
    r = random.randint(0, total - 1)
    for item, cnt in counter.items():
        r -= cnt
        if r < 0:
            return item
    return random.choice(list(counter.keys()))


def generate_line(model: dict, keyword: str = None, max_phrases: int = 5) -> str:
    """フレーズ連鎖で1文生成"""
    transitions = model["transitions"]
    starters = model["starters"]
    terminals = model["terminals"]
    by_keyword = model["by_keyword"]

    # 開始フレーズを選択
    if keyword:
        # キーワードを含むフレーズからスタート
        candidates = by_keyword.get(keyword[:2], [])
        if candidates:
            start = random.choice(candidates)
        else:
            start = sample_weighted(starters)
    else:
        start = sample_weighted(starters)

    phrases = [start]

    for _ in range(max_phrases - 1):
        current = phrases[-1]
        # 既に文末なら終了
        if SENTENCE_ENDS.search(current):
            break
        # 遷移先があれば続ける
        if current in transitions:
            next_phrase = sample_weighted(transitions[current])
            phrases.append(next_phrase)
            if SENTENCE_ENDS.search(next_phrase):
                break
        else:
            # 遷移先がなければ文末フレーズをランダムに付ける
            if terminals:
                phrases.append(random.choice(list(terminals)))
            break

    return "".join(phrases)


def generate_many(model: dict, n: int = 10, keyword: str = None,
                  min_len: int = 6) -> list[str]:
    """重複なしでn個生成"""
    results = []
    seen = set()
    for _ in range(n * 15):
        if len(results) >= n:
            break
        line = generate_line(model, keyword=keyword)
        if len(line) < min_len or line in seen:
            continue
        seen.add(line)
        results.append(line)
    return results


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
    parser = argparse.ArgumentParser(description="あんガル キャラ台詞生成（フレーズ連鎖）")
    parser.add_argument("name", nargs="?", help="キャラ名")
    parser.add_argument("--keyword", "-k", help="話題キーワード（例: 好き）")
    parser.add_argument("--situation", "-s",
                        help=f"シチュエーション: {', '.join(SITUATION_KEYWORDS.keys())}")
    parser.add_argument("--count", "-n", type=int, default=10, help="生成する台詞数")
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

    model = build_model(lines)
    print(f"フレーズ数: {len(model['all_phrases']):,}  文頭候補: {len(model['starters']):,}\n")

    keyword = args.keyword
    if not keyword and args.situation:
        kws = SITUATION_KEYWORDS.get(args.situation, [])
        keyword = kws[0] if kws else None
        if keyword:
            print(f"シチュエーション「{args.situation}」→ キーワード「{keyword}」\n")

    if args.all:
        out_dir = Path(f"dialogue_{name}")
        out_dir.mkdir(exist_ok=True)
        for situation, kws in SITUATION_KEYWORDS.items():
            generated = generate_many(model, args.count, keyword=kws[0])
            out_file = out_dir / f"{situation}.txt"
            out_file.write_text("\n".join(generated), encoding="utf-8")
            print(f"  {situation}: {len(generated)}件")
        print(f"\n→ {out_dir}/ に保存しました")
        return

    generated = generate_many(model, args.count, keyword=keyword)
    for i, l in enumerate(generated, 1):
        print(f"{i}. {l}")


if __name__ == "__main__":
    main()
