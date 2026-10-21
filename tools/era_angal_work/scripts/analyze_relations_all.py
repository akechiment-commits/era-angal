"""
全キャラ一括関係性分析スクリプト

使い方:
    python analyze_relations_all.py <シナリオフォルダ> <セリフ出力フォルダ>

シナリオを1回だけ読み込み、全キャラ分の関係性分析を一気に出力する。
"""

import os
import sys
import glob
import re
from analyze_relations import load_scenarios, analyze_character, format_report

def main():
    if len(sys.argv) != 3:
        print("使い方: python analyze_relations_all.py <シナリオフォルダ> <セリフ出力フォルダ>")
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
        if basename.startswith("_") or basename.endswith("_分析.txt") or basename.endswith("_関係性分析.txt"):
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
        outpath = os.path.join(output_dir, f"{name}_関係性分析.txt")

        # 既に存在する場合はスキップ（再実行時用）
        if os.path.exists(outpath):
            print(f"[{i}/{len(targets)}] {name} - スキップ（既存）")
            skipped += 1
            continue

        print(f"[{i}/{len(targets)}] {name} ...", end=" ")
        try:
            coappear, partner_lines, partner_emotion_dist, partner_samples = analyze_character(scenarios, name)

            if not partner_lines:
                print("セリフなし、スキップ")
                skipped += 1
                continue

            report = format_report(name, coappear, partner_lines, partner_emotion_dist, partner_samples)

            with open(outpath, "w", encoding="utf-8") as f:
                f.write(report)

            total_responses = sum(len(v) for v in partner_lines.values())
            print(f"OK（応答{total_responses}件、相手{len(partner_lines)}人）")
            success += 1
        except Exception as e:
            print(f"エラー: {e}")

    print(f"\n=== 完了 ===")
    print(f"成功: {success}件")
    print(f"スキップ: {skipped}件")
    print(f"出力先: {output_dir}")

if __name__ == "__main__":
    main()
