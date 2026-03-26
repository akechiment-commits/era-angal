#!/usr/bin/env python3
"""
あんガル キャラクター疑似人格分析スクリプト
scenarios/*.txt から各キャラの全セリフを集めて話し方の特徴を抽出する
"""

import re
import json
from pathlib import Path
from collections import Counter, defaultdict

SCENARIO_DIR = Path("scenarios")
OUT_FILE = Path("character_profiles.json")
OUT_TEXT = Path("character_profiles.txt")

# 一人称リスト（出現頻度を数える）
FIRST_PERSON = ["私", "わたし", "あたし", "あたくし", "僕", "ぼく", "俺", "おれ", "オレ",
                "我", "わし", "うち", "自分", "ワタシ", "アタシ", "ボク", "ウチ"]

# 語尾パターン（セリフ末尾から抽出）
ENDING_PATTERNS = [
    "だよ", "だよね", "だよ！", "だよ♪", "だよ～",
    "です", "ます", "ですね", "ますね", "ですよ", "ますよ", "ですわ", "ますわ",
    "だわ", "わよ", "のよ", "かしら", "のね", "わね",
    "だぞ", "だぜ", "だな", "だろ", "だろう",
    "ね", "よ", "わ", "ぞ", "な", "か",
    "！", "♪", "～", "…", "。",
]

# よく使われる感情・口癖ワード
KEYWORD_PATTERNS = [
    "えへへ", "ふふ", "ははは", "うふふ", "えへ",
    "うーん", "えーと", "あのね", "ねえ", "ほら",
    "すごい", "すごく", "とっても", "めちゃ", "超",
    "かわいい", "かっこいい", "素敵", "最高", "嬉しい",
    "頑張", "諦めない", "絶対", "必ず", "きっと",
    "大好き", "好き", "嫌い", "怖い", "寂しい",
]


def parse_scenarios() -> dict[str, list[str]]:
    """全シナリオファイルを読み込み、キャラ別にセリフを集める"""
    char_lines: dict[str, list[str]] = defaultdict(list)
    count = 0

    for txt in sorted(SCENARIO_DIR.glob("*.txt")):
        try:
            content = txt.read_text(encoding="utf-8")
        except Exception:
            continue

        for line in content.splitlines():
            m = re.match(r"^【(.+?)】(.+)$", line)
            if m:
                speaker = m.group(1).strip()
                text = m.group(2).strip()
                if speaker and text and speaker != "ナレーション" and speaker != "???":
                    char_lines[speaker].append(text)
                    count += 1

    print(f"総セリフ数: {count:,}行, キャラ数: {len(char_lines)}人")
    return dict(char_lines)


def analyze_character(name: str, lines: list[str]) -> dict:
    """1キャラの話し方を分析"""
    all_text = " ".join(lines)
    total = len(lines)

    # 一人称の出現数
    first_person = {}
    for fp in FIRST_PERSON:
        count = all_text.count(fp)
        if count > 0:
            first_person[fp] = count
    # 最もよく使う一人称
    main_fp = max(first_person, key=first_person.get) if first_person else "不明"

    # 語尾分析（セリフ末尾の最後の2〜4文字）
    endings = Counter()
    for line in lines:
        clean = re.sub(r"[！？!?♪～〜…。、「」『』\s]", "", line)
        if len(clean) >= 2:
            endings[clean[-2:]] += 1
        if len(clean) >= 3:
            endings[clean[-3:]] += 1

    top_endings = [e for e, _ in endings.most_common(10) if len(e) >= 2]

    # キーワード出現
    keywords = {}
    for kw in KEYWORD_PATTERNS:
        count = all_text.count(kw)
        if count > 0:
            keywords[kw] = count

    # よく使う単語（ひらがな・カタカナ・漢字の2文字以上の語）
    words = re.findall(r"[ぁ-ん]{2,}|[ァ-ン]{2,}|[一-龥]{2,}", all_text)
    # ストップワード除外
    stop = {"こと", "それ", "これ", "あれ", "もの", "ため", "から", "けど", "だけ",
            "でも", "って", "ここ", "そこ", "あそこ", "みんな", "みんなの", "わたし",
            "たち", "など", "ない", "ある", "いる", "なる", "する", "できる", "なって",
            "して", "しても", "しては", "してる", "してた", "いっている", "いった"}
    word_count = Counter(w for w in words if w not in stop and len(w) >= 2)
    top_words = [w for w, _ in word_count.most_common(20)]

    # 感情傾向（ポジティブ/ネガティブワード数）
    positive = sum(all_text.count(w) for w in ["嬉しい", "楽しい", "好き", "大好き", "素敵", "最高", "すごい", "頑張", "笑"])
    negative = sum(all_text.count(w) for w in ["悲しい", "辛い", "嫌い", "怖い", "寂しい", "嫌", "つらい"])

    # 平均セリフ長
    avg_len = sum(len(l) for l in lines) / total if total > 0 else 0

    return {
        "name": name,
        "total_lines": total,
        "avg_line_length": round(avg_len, 1),
        "main_first_person": main_fp,
        "first_person_usage": dict(sorted(first_person.items(), key=lambda x: -x[1])[:5]),
        "top_endings": top_endings[:8],
        "top_words": top_words[:15],
        "keywords": dict(sorted(keywords.items(), key=lambda x: -x[1])[:10]),
        "positive_score": positive,
        "negative_score": negative,
        "tone": "明るい" if positive > negative * 1.5 else ("暗め" if negative > positive else "中立"),
    }


def format_profile(p: dict) -> str:
    lines = [
        f"{'='*50}",
        f"【{p['name']}】 ({p['total_lines']}行, 平均{p['avg_line_length']}文字)",
        f"  一人称: {p['main_first_person']}  {p['first_person_usage']}",
        f"  語尾: {', '.join(p['top_endings'][:6])}",
        f"  頻出語: {', '.join(p['top_words'][:10])}",
        f"  口癖: {', '.join(f'{k}({v})' for k, v in list(p['keywords'].items())[:5])}",
        f"  トーン: {p['tone']} (ポジ{p['positive_score']} / ネガ{p['negative_score']})",
    ]
    return "\n".join(lines)


def main():
    if not SCENARIO_DIR.exists():
        print(f"エラー: {SCENARIO_DIR} フォルダが見つかりません")
        print("download_scenarios.py を先に実行してください")
        return

    print("シナリオ読み込み中...")
    char_lines = parse_scenarios()

    print("キャラクター分析中...")
    profiles = []
    for name, lines in sorted(char_lines.items(), key=lambda x: -len(x[1])):
        if len(lines) < 5:  # セリフが少なすぎるキャラはスキップ
            continue
        p = analyze_character(name, lines)
        profiles.append(p)

    # JSON保存
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=2)
    print(f"\nJSON → {OUT_FILE} ({len(profiles)}キャラ)")

    # テキスト保存 & 表示
    text_lines = [f"あんガル キャラクター疑似人格レポート\n登場キャラ数: {len(profiles)}人\n"]
    for p in profiles:
        text_lines.append(format_profile(p))

    report = "\n".join(text_lines)
    OUT_TEXT.write_text(report, encoding="utf-8")
    print(f"テキスト → {OUT_TEXT}")

    # 上位20キャラをコンソール表示
    print("\n\n=== セリフ数上位20キャラ ===")
    for p in profiles[:20]:
        print(format_profile(p))


if __name__ == "__main__":
    main()
