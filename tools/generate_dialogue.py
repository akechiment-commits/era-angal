#!/usr/bin/env python3
"""
あんガル キャラクター台詞生成スクリプト
実際のゲームセリフをもとにClaude APIでキャラらしい台詞を生成する

使い方:
  python generate_dialogue.py 小鳥遊音花
  python generate_dialogue.py 小鳥遊音花 --situation "放課後に主人公に話しかける"
  python generate_dialogue.py --list   # キャラ一覧表示
"""

import argparse
import json
import random
import re
from pathlib import Path

import anthropic

SCENARIO_DIR = Path("scenarios")
PROFILES_FILE = Path("character_profiles.json")

client = anthropic.Anthropic()  # ANTHROPIC_API_KEY 環境変数から自動取得


def load_character_lines(name: str, max_samples: int = 800) -> list[str]:
    """シナリオファイルから指定キャラのセリフを収集する
    全行数が max_samples 以下ならすべて使う。
    超える場合は短文・中文・長文をバランスよくサンプリング。
    """
    all_lines = []
    pattern = re.compile(rf"^【{re.escape(name)}】(.+)$", re.MULTILINE)

    for txt in sorted(SCENARIO_DIR.glob("*.txt")):
        try:
            content = txt.read_text(encoding="utf-8")
            matches = pattern.findall(content)
            all_lines.extend(matches)
        except Exception:
            continue

    if len(all_lines) <= max_samples:
        return all_lines

    # 短文(〜20字)・中文(21〜50字)・長文(51字〜)に分けて均等サンプリング
    short  = [l for l in all_lines if len(l) <= 20]
    medium = [l for l in all_lines if 21 <= len(l) <= 50]
    long_  = [l for l in all_lines if len(l) > 50]

    each = max_samples // 3
    result = (
        random.sample(short,  min(each, len(short)))  +
        random.sample(medium, min(each, len(medium))) +
        random.sample(long_,  min(each, len(long_)))
    )
    # 端数を補充
    if len(result) < max_samples:
        rest = [l for l in all_lines if l not in set(result)]
        result += random.sample(rest, min(max_samples - len(result), len(rest)))
    return result


def load_profile(name: str) -> dict | None:
    """character_profiles.json からプロフィールを読み込む"""
    if not PROFILES_FILE.exists():
        return None
    with open(PROFILES_FILE, encoding="utf-8") as f:
        profiles = json.load(f)
    for p in profiles:
        if p["name"] == name:
            return p
    return None


def generate_dialogue(name: str, situation: str, n: int = 10) -> list[str]:
    """Claude APIでキャラらしい台詞を生成"""
    lines = load_character_lines(name)
    if not lines:
        print(f"エラー: 「{name}」のセリフが見つかりません")
        return []

    profile = load_profile(name)
    profile_info = ""
    if profile:
        profile_info = f"""
話し方の特徴:
- 一人称: {profile.get('main_first_person', '?')}
- よく使う語尾: {', '.join(profile.get('top_endings', [])[:5])}
- 頻出ワード: {', '.join(profile.get('top_words', [])[:8])}
- トーン: {profile.get('tone', '?')}
"""

    sample_text = "\n".join(f"・{l}" for l in lines)

    prompt = f"""あなたはキャラクター「{name}」として台詞を生成します。

以下は「{name}」の実際のゲーム内セリフです:
{sample_text}

{profile_info}

状況: {situation}

上記のセリフのパターン・口調・一人称・語尾を忠実に再現して、
この状況に合った自然な台詞を{n}個生成してください。

出力形式（この形式のみ、説明不要）:
1. （台詞）
2. （台詞）
...
"""

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text
    # 番号付きリストをパース
    result = []
    for line in text.splitlines():
        m = re.match(r"^\d+\.\s*(.+)$", line.strip())
        if m:
            result.append(m.group(1).strip())
    return result


def list_characters():
    """利用可能なキャラ一覧を表示"""
    if not PROFILES_FILE.exists():
        print("character_profiles.json が見つかりません。analyze_characters.py を先に実行してください")
        return
    with open(PROFILES_FILE, encoding="utf-8") as f:
        profiles = json.load(f)
    print(f"キャラ数: {len(profiles)}人\n")
    for p in profiles:
        print(f"  {p['name']:15s} {p['total_lines']:4d}行  一人称:{p['main_first_person']}")


DEFAULT_SITUATIONS = [
    "主人公に初めて話しかける",
    "放課後、廊下で偶然会う",
    "テストの結果を話す",
    "好きなものについて話す",
    "励ます・応援する",
    "照れているとき",
    "怒っているとき",
    "一緒に帰るとき",
]


def main():
    parser = argparse.ArgumentParser(description="あんガル キャラ台詞生成")
    parser.add_argument("name", nargs="?", help="キャラ名")
    parser.add_argument("--situation", "-s", help="状況・シチュエーション")
    parser.add_argument("--count", "-n", type=int, default=10, help="生成する台詞数")
    parser.add_argument("--list", "-l", action="store_true", help="キャラ一覧表示")
    parser.add_argument("--all-situations", action="store_true", help="デフォルト状況を全部生成")
    args = parser.parse_args()

    if args.list:
        list_characters()
        return

    if not args.name:
        parser.print_help()
        return

    name = args.name

    if args.all_situations:
        out_dir = Path(f"dialogue_{name}")
        out_dir.mkdir(exist_ok=True)
        for situation in DEFAULT_SITUATIONS:
            print(f"\n生成中: {name} / {situation}")
            lines = generate_dialogue(name, situation, args.count)
            out_file = out_dir / f"{situation}.txt"
            out_file.write_text("\n".join(lines), encoding="utf-8")
            for i, l in enumerate(lines, 1):
                print(f"  {i}. {l}")
        print(f"\n→ {out_dir}/ に保存しました")
        return

    situation = args.situation or "主人公に話しかける"
    print(f"\n【{name}】 / {situation}\n")
    lines = generate_dialogue(name, situation, args.count)
    for i, l in enumerate(lines, 1):
        print(f"{i}. {l}")


if __name__ == "__main__":
    main()
