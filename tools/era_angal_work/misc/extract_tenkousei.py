"""
転校生関連セリフ抽出スクリプト

指定キャラが「転校生」に言及しているセリフ、または
直前に発話者タグがない（＝転校生への応答と推定される）セリフを
前後の文脈つきで抽出する。

使い方:
    python extract_tenkousei.py <シナリオフォルダ> <キャラ名>

例:
    python extract_tenkousei.py "C:/Users/guile/era-angal/tools/scenarios" つばさ

出力:
    同じフォルダに「キャラ名_転校生.txt」を生成
"""

import os
import re
import sys

def main():
    if len(sys.argv) < 3:
        print("使い方: python extract_tenkousei.py <シナリオフォルダ> <キャラ名> [追加検索ワード...]")
        print('例:     python extract_tenkousei.py "C:/Users/guile/era-angal/tools/scenarios" こはる お兄ちゃん')
        sys.exit(1)

    scenario_dir = sys.argv[1]
    target_name = sys.argv[2]
    extra_keywords = sys.argv[3:]  # 追加検索ワード（お兄ちゃん、ヘルプマン等）
    search_words = ["転校生"] + extra_keywords
    pattern = re.compile(r"^【(.*?)】(.*)$")

    results = []

    for i in range(1, 10000):
        filepath = os.path.join(scenario_dir, f"{i}.txt")
        if not os.path.exists(filepath):
            continue

        for enc in ("utf-8", "cp932", "utf-8-sig"):
            try:
                with open(filepath, "r", encoding=enc) as f:
                    raw_lines = f.readlines()
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        else:
            continue

        # パース
        dialogue = []
        for line in raw_lines:
            line = line.strip().replace("story_user_name", "転校生")
            if not line or line.startswith("==="):
                continue
            m = pattern.match(line)
            if m:
                name = m.group(1).strip()
                text = m.group(2).strip()
                if text:
                    dialogue.append((name, text))

        if not dialogue:
            continue

        # 対象キャラが登場するか
        names = set(n for n, t in dialogue)
        if target_name not in names:
            continue

        # 対象キャラの行で、転校生に言及 or 直前が地の文（転校生応答の推定）
        hit_indices = set()
        for idx, (name, text) in enumerate(dialogue):
            if name == target_name:
                # 検索ワードに言及している
                if any(w in text for w in search_words):
                    hit_indices.add(idx)
                    continue
                # 直前が地の文（発話者タグなし→転校生への応答推定）
                if idx > 0:
                    prev_name = dialogue[idx - 1][0]
                    if prev_name == "":
                        hit_indices.add(idx)

        if not hit_indices:
            continue

        # ヒットした行の前後3行を文脈として収集
        context_indices = set()
        for idx in hit_indices:
            for j in range(max(0, idx - 3), min(len(dialogue), idx + 4)):
                context_indices.add(j)

        # 連続する区間にまとめて出力
        sorted_idx = sorted(context_indices)
        blocks = []
        current_block = [sorted_idx[0]]
        for k in range(1, len(sorted_idx)):
            if sorted_idx[k] == sorted_idx[k-1] + 1:
                current_block.append(sorted_idx[k])
            else:
                blocks.append(current_block)
                current_block = [sorted_idx[k]]
        blocks.append(current_block)

        for block in blocks:
            lines_out = []
            for idx in block:
                name, text = dialogue[idx]
                marker = ">>>" if idx in hit_indices else "   "
                if name:
                    lines_out.append(f"{marker} 【{name}】{text}")
                else:
                    lines_out.append(f"{marker} （地の文）{text}")
            results.append((i, lines_out))

    # 出力
    out = []
    out.append(f"=== {target_name} 転校生関連セリフ抽出 ===\n")
    out.append(f"検索ワード: {', '.join(search_words)}")
    out.append(f"抽出条件: 上記ワードを含む or 直前が地の文（転校生応答推定）")
    out.append(f">>> がついた行がヒット行、前後3行を文脈として表示\n")
    out.append(f"抽出結果: {len(results)}ブロック\n")

    for fid, lines in results:
        out.append(f"--- シナリオ {fid} ---")
        for l in lines:
            out.append(l)
        out.append("")

    outpath = os.path.join(os.path.dirname(sys.argv[0]) or ".", f"{target_name}_転校生.txt")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"抽出完了: {len(results)}ブロック → {outpath}")

if __name__ == "__main__":
    main()
