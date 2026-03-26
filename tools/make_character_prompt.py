#!/usr/bin/env python3
"""
キャラクタープロンプト生成スクリプト
新しいClaudeセッションに貼り付けることでそのキャラとして会話できる

使い方:
  python make_character_prompt.py ひまり
  python make_character_prompt.py ひまり --samples 100
"""

import argparse
import random
import re
from pathlib import Path

SCENARIO_DIR = Path("scenarios")


def load_lines(name: str) -> list[str]:
    all_lines = []
    pattern = re.compile(rf"^【{re.escape(name)}】(.+)$", re.MULTILINE)
    for txt in sorted(SCENARIO_DIR.glob("*.txt")):
        try:
            content = txt.read_text(encoding="utf-8")
            all_lines.extend(pattern.findall(content))
        except Exception:
            continue
    return all_lines


def sample_lines(lines: list[str], n: int) -> list[str]:
    if len(lines) <= n:
        return lines
    short  = [l for l in lines if len(l) <= 20]
    medium = [l for l in lines if 21 <= len(l) <= 50]
    long_  = [l for l in lines if len(l) > 50]
    each = n // 3
    result = (
        random.sample(short,  min(each, len(short)))  +
        random.sample(medium, min(each, len(medium))) +
        random.sample(long_,  min(each, len(long_)))
    )
    if len(result) < n:
        rest = [l for l in lines if l not in set(result)]
        result += random.sample(rest, min(n - len(result), len(rest)))
    return result


def make_prompt(name: str, lines: list[str], samples: int) -> str:
    sampled = sample_lines(lines, samples)
    lines_text = "\n".join(f"・{l}" for l in sampled)

    return f"""あなたは「{name}」というキャラクターです。
以下のセリフはすべて{name}が実際にゲーム内で言ったものです。
この口調・一人称・語尾・性格を完全に再現してください。

【{name}の実際のセリフ（{len(sampled)}件）】
{lines_text}

【ロールプレイのルール】
- 常に{name}として話す。説明や注釈は不要
- セリフの口調・一人称・語尾を忠実に守る
- 相手の発言に対してキャラとして自然に返答する
- どんな話題でも{name}の視点・性格で答える

準備ができたら「{name}として話す準備ができました」と一言だけ言ってください。"""


def main():
    parser = argparse.ArgumentParser(description="キャラクタープロンプト生成")
    parser.add_argument("name", help="キャラ名")
    parser.add_argument("--samples", "-n", type=int, default=80,
                        help="サンプルセリフ数（デフォルト80）")
    args = parser.parse_args()

    lines = load_lines(args.name)
    if not lines:
        print(f"エラー: 「{args.name}」のセリフが見つかりません")
        return

    print(f"「{args.name}」: {len(lines)}行から{args.samples}件をサンプリング")

    prompt = make_prompt(args.name, lines, args.samples)

    out_file = Path(f"prompt_{args.name}.txt")
    out_file.write_text(prompt, encoding="utf-8")
    print(f"→ {out_file} に保存しました")
    print(f"\n使い方: 新しいClaudeセッションを開いて {out_file} の内容を貼り付けてください")


if __name__ == "__main__":
    main()
