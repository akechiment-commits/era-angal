#!/usr/bin/env python3
"""
あんガル シナリオJSONパーサー
MonoBehaviourフォルダ内のJSONファイルからセリフを抽出する
"""

import json
import sys
from pathlib import Path


def parse_scenario(json_path: Path) -> list[dict]:
    """JSONファイルからtalkコマンドを抽出する"""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    script_raw = data.get("script", "[]")
    if isinstance(script_raw, str):
        commands = json.loads(script_raw)
    else:
        commands = script_raw

    talks = []
    for cmd in commands:
        if cmd.get("command") == "talk":
            talks.append({
                "speaker": cmd.get("speaker", ""),
                "text": cmd.get("text", ""),
            })
    return talks


def format_as_text(name: str, talks: list[dict]) -> str:
    """セリフリストを読みやすいテキストに変換する"""
    lines = [f"=== {name} ===\n"]
    for t in talks:
        lines.append(f"【{t['speaker']}】{t['text']}")
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("使い方: python parse_scenario.py <MonoBehaviourフォルダのパス>")
        print("例: python parse_scenario.py C:/Users/guile/.../angal/MonoBehaviour")
        sys.exit(1)

    folder = Path(sys.argv[1])
    if not folder.is_dir():
        print(f"エラー: フォルダが見つかりません: {folder}")
        sys.exit(1)

    json_files = sorted(folder.glob("*.json"))
    output_lines = []

    for json_file in json_files:
        try:
            talks = parse_scenario(json_file)
            if not talks:
                continue
            name = json_file.stem
            output_lines.append(format_as_text(name, talks))
            output_lines.append("")
        except Exception as e:
            print(f"スキップ: {json_file.name} ({e})", file=sys.stderr)

    output_text = "\n".join(output_lines)

    out_file = folder.parent / "scenarios.txt"
    out_file.write_text(output_text, encoding="utf-8")
    print(f"出力完了: {out_file}")
    print(f"抽出したファイル数: {len([l for l in output_lines if l.startswith('===')])}")


if __name__ == "__main__":
    main()
