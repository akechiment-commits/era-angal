"""
全キャラ一括 転校生関連セリフ抽出スクリプト

使い方:
    python extract_tenkousei_all.py <シナリオフォルダ> <セリフ出力フォルダ>

例:
    python extract_tenkousei_all.py "C:/Users/guile/era-angal/tools/scenarios" "C:/Users/guile/era-angal/tools/output"
"""

import os
import sys
import glob
import re

def load_scenarios(scenario_dir):
    pattern = re.compile(r"^【(.*?)】(.*)$")
    scenarios = {}
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
        dialogue_lines = []
        for line in raw_lines:
            line = line.strip().replace("story_user_name", "転校生")
            if not line or line.startswith("==="):
                continue
            m = pattern.match(line)
            if m:
                name = m.group(1).strip()
                text = m.group(2).strip()
                if text:
                    dialogue_lines.append((name, text))
        if dialogue_lines:
            scenarios[i] = dialogue_lines
    return scenarios


def extract_tenkousei(scenarios, target_name):
    results = []
    for fid, dialogue in scenarios.items():
        names = set(n for n, t in dialogue)
        if target_name not in names:
            continue

        hit_indices = set()
        for idx, (name, text) in enumerate(dialogue):
            if name == target_name:
                if "転校生" in text:
                    hit_indices.add(idx)
                    continue
                if idx > 0 and dialogue[idx - 1][0] == "":
                    hit_indices.add(idx)

        if not hit_indices:
            continue

        context_indices = set()
        for idx in hit_indices:
            for j in range(max(0, idx - 3), min(len(dialogue), idx + 4)):
                context_indices.add(j)

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
            results.append((fid, lines_out))

    return results


def main():
    if len(sys.argv) != 3:
        print("使い方: python extract_tenkousei_all.py <シナリオフォルダ> <セリフ出力フォルダ>")
        sys.exit(1)

    scenario_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(scenario_dir):
        print(f"エラー: {scenario_dir} が見つかりません")
        sys.exit(1)

    # セリフファイル一覧からキャラ名を取得
    files = sorted(glob.glob(os.path.join(output_dir, "*.txt")))
    targets = []
    for f in files:
        basename = os.path.basename(f)
        if basename.startswith("_") or "_分析" in basename or "_関係性分析" in basename or "_転校生" in basename:
            continue
        name = os.path.splitext(basename)[0]
        targets.append(name)

    print(f"対象: {len(targets)}キャラ")
    print(f"シナリオ読み込み中...")
    scenarios = load_scenarios(scenario_dir)
    print(f"  {len(scenarios)}ファイル読み込み完了\n")

    success = 0
    skipped = 0
    for i, name in enumerate(targets, 1):
        outpath = os.path.join(output_dir, f"{name}_転校生.txt")

        if os.path.exists(outpath):
            print(f"[{i}/{len(targets)}] {name} - スキップ（既存）")
            skipped += 1
            continue

        print(f"[{i}/{len(targets)}] {name} ...", end=" ")
        try:
            results = extract_tenkousei(scenarios, name)

            if not results:
                print("該当なし")
                skipped += 1
                continue

            out = []
            out.append(f"=== {name} 転校生関連セリフ抽出 ===\n")
            out.append(f"抽出条件: セリフに「転校生」を含む or 直前が地の文（転校生応答推定）")
            out.append(f">>> がついた行がヒット行、前後3行を文脈として表示\n")
            out.append(f"抽出結果: {len(results)}ブロック\n")

            for fid, lines in results:
                out.append(f"--- シナリオ {fid} ---")
                for l in lines:
                    out.append(l)
                out.append("")

            with open(outpath, "w", encoding="utf-8") as f:
                f.write("\n".join(out))

            print(f"OK（{len(results)}ブロック）")
            success += 1
        except Exception as e:
            print(f"エラー: {e}")

    print(f"\n=== 完了 ===")
    print(f"成功: {success}件")
    print(f"スキップ: {skipped}件")
    print(f"出力先: {output_dir}")


if __name__ == "__main__":
    main()
