"""
キャラセリフ分析スクリプト - プロンプト改善用

使い方:
    python analyze_dialogue.py <キャラセリフファイル>

例:
    python analyze_dialogue.py D:\output\かなえ.txt

出力:
    同じフォルダに「かなえ_分析.txt」を生成
"""

import re
import sys
import os
from collections import Counter, defaultdict

def analyze(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # ヘッダ行スキップ、セリフ抽出
    dialogues = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # [番号] セリフ の形式
        m = re.match(r"^\[(\d+)\]\s*(.+)$", line)
        if m:
            file_id = int(m.group(1))
            text = m.group(2)
            dialogues.append((file_id, text))

    if not dialogues:
        print("セリフが見つかりません")
        return

    results = []
    results.append(f"=== セリフ分析結果 ===")
    results.append(f"総セリフ数: {len(dialogues)}")
    results.append(f"登場シナリオ数: {len(set(d[0] for d in dialogues))}")

    # --- 1. 一人称分析 ---
    first_person = Counter()
    for _, text in dialogues:
        # 文頭や助詞の前の一人称を検出
        for p in ["私", "わたし", "あたし", "わたくし", "あっし", "僕", "ぼく", "俺", "おれ", "うち", "自分"]:
            if p in text:
                first_person[p] += 1
    results.append(f"\n--- 一人称 ---")
    for word, count in first_person.most_common():
        results.append(f"  {word}: {count}回")

    # --- 2. 語尾分析 ---
    endings = Counter()
    for _, text in dialogues:
        # セリフ末尾の語尾パターン
        clean = re.sub(r"[♪☆…！？～」）】]+$", "", text)
        if len(clean) >= 2:
            endings[clean[-3:]] += 1
    results.append(f"\n--- 語尾パターン（上位30） ---")
    for ending, count in endings.most_common(30):
        results.append(f"  「...{ending}」: {count}回")

    # --- 3. 固有名詞・人名の出現頻度 ---
    # ひらがな・カタカナの名前っぽいもの + 漢字名
    name_patterns = Counter()
    for _, text in dialogues:
        # 「〇〇さん」「〇〇先輩」「〇〇部長」等のパターン
        for m in re.finditer(r"([\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]{2,6})(さん|ちゃん|先輩|部長|くん|君|様|殿|氏)", text):
            name_patterns[m.group(0)] += 1
        # 転校生
        if "転校生" in text:
            name_patterns["転校生"] += 1
    results.append(f"\n--- 人名・呼称（上位30） ---")
    for name, count in name_patterns.most_common(30):
        results.append(f"  {name}: {count}回")

    # --- 4. 感情表現の分類 ---
    emotion_markers = {
        "照れ・動揺": [r"[あわう]っ", r"す、", r"は、は", r"べ、別に", r"そ、そんな", r"ば、"],
        "ツン": [r"お気遣いなく", r"勝手に", r"知りません", r"関係ない", r"別に"],
        "デレ・優しさ": [r"守ります", r"大丈夫", r"心配", r"い～こ", r"甘やか", r"よくできました"],
        "真剣・決意": [r"負けません", r"全力", r"覚悟", r"私が[、。！]", r"絶対"],
        "困惑": [r"困りました", r"はぁ", r"やれやれ", r"まったく"],
        "笑い・余裕": [r"ふふ", r"ふぅむ", r"おや", r"ほう"],
        "怒り・苛立ち": [r"腹立たし", r"許さ", r"いい加減", r"ひどい"],
        "悲しみ・不安": [r"怖[いく]", r"嫌な", r"不安", r"寂し", r"泣[いき]"],
    }
    results.append(f"\n--- 感情表現の出現数 ---")
    emotion_examples = defaultdict(list)
    for category, patterns in emotion_markers.items():
        count = 0
        for _, text in dialogues:
            for p in patterns:
                if re.search(p, text):
                    count += 1
                    if len(emotion_examples[category]) < 3:
                        emotion_examples[category].append(text)
                    break
        results.append(f"  {category}: {count}件")
        for ex in emotion_examples[category]:
            short = ex[:60] + "..." if len(ex) > 60 else ex
            results.append(f"    例: {short}")

    # --- 5. セリフ長の分布 ---
    lengths = [len(text) for _, text in dialogues]
    results.append(f"\n--- セリフ長 ---")
    results.append(f"  平均: {sum(lengths)/len(lengths):.1f}文字")
    results.append(f"  最短: {min(lengths)}文字")
    results.append(f"  最長: {max(lengths)}文字")
    brackets = [(0,10),(10,30),(30,60),(60,100),(100,999)]
    for lo, hi in brackets:
        c = sum(1 for l in lengths if lo <= l < hi)
        results.append(f"  {lo}～{hi}文字: {c}件 ({c/len(lengths)*100:.1f}%)")

    # --- 6. 括弧書き（心の声）の割合 ---
    inner_voice = [(fid, t) for fid, t in dialogues if t.startswith("（") or t.startswith("(")]
    results.append(f"\n--- 心の声（括弧書き） ---")
    results.append(f"  {len(inner_voice)}件 ({len(inner_voice)/len(dialogues)*100:.1f}%)")
    for _, ex in inner_voice[:5]:
        short = ex[:60] + "..." if len(ex) > 60 else ex
        results.append(f"    例: {short}")

    # --- 7. 共演キャラ分析（同一シナリオに登場するキャラ） ---
    # これは単体ファイルではできないのでスキップ
    results.append(f"\n--- 場面タグ付きセリフ（感情別サンプル各5件） ---")
    for category, patterns in emotion_markers.items():
        samples = []
        for _, text in dialogues:
            for p in patterns:
                if re.search(p, text):
                    samples.append(text)
                    break
            if len(samples) >= 5:
                break
        if samples:
            results.append(f"\n  [{category}]")
            for s in samples:
                short = s[:80] + "..." if len(s) > 80 else s
                results.append(f"    {short}")

    # --- 8. 「私」vs「わたし」の文脈比較 ---
    results.append(f"\n--- 「私」vs「わたし」使用例（各10件） ---")
    watashi_kanji = []
    watashi_hira = []
    for _, text in dialogues:
        if "わたし" in text and len(watashi_hira) < 10:
            short = text[:80] + "..." if len(text) > 80 else text
            watashi_hira.append(short)
        elif "私" in text and "わたし" not in text and len(watashi_kanji) < 10:
            short = text[:80] + "..." if len(text) > 80 else text
            watashi_kanji.append(short)
    results.append(f"  漢字「私」({len(watashi_kanji)}件サンプル):")
    for s in watashi_kanji:
        results.append(f"    {s}")
    results.append(f"  ひらがな「わたし」({len(watashi_hira)}件サンプル):")
    for s in watashi_hira:
        results.append(f"    {s}")

    # 出力
    basename = os.path.splitext(os.path.basename(filepath))[0]
    outpath = os.path.join(os.path.dirname(filepath), f"{basename}_分析.txt")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print("\n".join(results))
    print(f"\n→ 分析結果を保存: {outpath}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使い方: python analyze_dialogue.py <キャラセリフファイル>")
        print("例:     python analyze_dialogue.py D:\\output\\かなえ.txt")
        sys.exit(1)
    analyze(sys.argv[1])
