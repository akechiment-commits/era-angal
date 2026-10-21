"""
全キャラ一括分析スクリプト

使い方:
    python analyze_all.py <セリフ出力フォルダ>

例:
    python analyze_all.py D:\output

_地の文.txt と _分析.txt は自動スキップ
"""

import os
import sys
import glob
from analyze_dialogue import analyze

def main():
    if len(sys.argv) != 2:
        print("使い方: python analyze_all.py <セリフ出力フォルダ>")
        sys.exit(1)

    folder = sys.argv[1]
    files = sorted(glob.glob(os.path.join(folder, "*.txt")))

    targets = [
        f for f in files
        if not os.path.basename(f).startswith("_")
        and not f.endswith("_分析.txt")
    ]

    print(f"対象: {len(targets)}キャラ\n")

    for i, f in enumerate(targets, 1):
        name = os.path.splitext(os.path.basename(f))[0]
        print(f"[{i}/{len(targets)}] {name}")
        try:
            analyze(f)
        except Exception as e:
            print(f"  [エラー] {e}")
        print()

    print(f"=== 全{len(targets)}キャラの分析完了 ===")

if __name__ == "__main__":
    main()
