"""
あんさんぶるガールズ!! シナリオテキストからキャラ別セリフを抽出するスクリプト

使い方:
    python extract_dialogue.py <シナリオフォルダのパス> <出力フォルダのパス>

例:
    python extract_dialogue.py D:\scenarios D:\output
"""

import os
import re
import sys
from collections import defaultdict

def extract_dialogues(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # キャラ名 -> セリフリスト
    characters = defaultdict(list)
    # 地の文（【】空）リスト
    narration = []

    pattern = re.compile(r"^【(.*?)】(.*)$")

    # 1.txt ~ 9999.txt を順番に処理
    processed = 0
    skipped = 0
    for i in range(1, 10000):
        filepath = os.path.join(input_dir, f"{i}.txt")
        if not os.path.exists(filepath):
            continue

        # UTF-8で試す、ダメならcp932
        for encoding in ("utf-8", "cp932", "utf-8-sig"):
            try:
                with open(filepath, "r", encoding=encoding) as f:
                    lines = f.readlines()
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        else:
            print(f"  [警告] {i}.txt: エンコーディング判別不能、スキップ")
            skipped += 1
            continue

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # === 10 === のようなヘッダ行をスキップ
            if line.startswith("===") and line.endswith("==="):
                continue

            m = pattern.match(line)
            if not m:
                continue

            name = m.group(1).strip()
            text = m.group(2).strip()

            if not text:
                continue

            # story_user_name を 転校生 に置換
            text = text.replace("story_user_name", "転校生")

            if name == "":
                # 地の文・SE
                narration.append(f"[{i}] {text}")
            else:
                characters[name].append(f"[{i}] {text}")

        processed += 1

    # キャラ別ファイル出力
    for name, lines in sorted(characters.items(), key=lambda x: -len(x[1])):
        safe_name = re.sub(r'[\\/:*?"<>|]', "_", name)
        outpath = os.path.join(output_dir, f"{safe_name}.txt")
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(f"# {name}（全{len(lines)}件）\n\n")
            for line in lines:
                f.write(line + "\n")

    # 地の文ファイル出力
    if narration:
        outpath = os.path.join(output_dir, "_地の文.txt")
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(f"# 地の文・SE・ナレーション（全{len(narration)}件）\n\n")
            for line in narration:
                f.write(line + "\n")

    # 統計表示
    print(f"\n=== 抽出完了 ===")
    print(f"処理ファイル数: {processed}")
    print(f"スキップ: {skipped}")
    print(f"キャラクター数: {len(characters)}")
    print(f"地の文: {len(narration)}件")
    print(f"\n--- セリフ数ランキング（上位30） ---")
    for name, lines in sorted(characters.items(), key=lambda x: -len(x[1]))[:30]:
        print(f"  {name}: {len(lines)}件")
    print(f"\n出力先: {output_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使い方: python extract_dialogue.py <シナリオフォルダ> <出力フォルダ>")
        print("例:     python extract_dialogue.py D:\\scenarios D:\\output")
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(input_dir):
        print(f"エラー: {input_dir} が見つかりません")
        sys.exit(1)

    extract_dialogues(input_dir, output_dir)
