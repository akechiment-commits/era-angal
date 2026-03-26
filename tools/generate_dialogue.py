#!/usr/bin/env python3
"""
あんガル キャラクター台詞生成スクリプト
実際のゲームセリフをもとにGoogle Gemini API（無料）でキャラらしい台詞を生成する

使い方:
  python generate_dialogue.py ひまり
  python generate_dialogue.py ひまり --situation "放課後に主人公に話しかける"
  python generate_dialogue.py --list   # キャラ一覧表示

APIキー取得（無料）:
  1. aistudio.google.com を開く
  2. 「Get API key」→「Create API key」
  3. PowerShellで: $env:GEMINI_API_KEY = "AIzaSy..."
"""

import argparse
import json
import os
import random
import re
import time
import urllib.request
import urllib.error
from pathlib import Path

SCENARIO_DIR = Path("scenarios")
PROFILES_FILE = Path("character_profiles.json")

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def call_gemini(prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY が設定されていません。\n"
                           "aistudio.google.com で無料APIキーを取得して:\n"
                           '$env:GEMINI_API_KEY = "AIzaSy..."')

    url = f"{GEMINI_API_URL}?key={api_key}"
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"maxOutputTokens": 2048}
    }).encode("utf-8")

    req = urllib.request.Request(url, data=body,
                                  headers={"Content-Type": "application/json"},
                                  method="POST")
    with urllib.request.urlopen(req, timeout=30) as res:
        result = json.loads(res.read())

    return result["candidates"][0]["content"]["parts"][0]["text"]


def load_character_lines(name: str, max_samples: int = 150) -> list[str]:
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

    short  = [l for l in all_lines if len(l) <= 20]
    medium = [l for l in all_lines if 21 <= len(l) <= 50]
    long_  = [l for l in all_lines if len(l) > 50]

    each = max_samples // 3
    result = (
        random.sample(short,  min(each, len(short)))  +
        random.sample(medium, min(each, len(medium))) +
        random.sample(long_,  min(each, len(long_)))
    )
    if len(result) < max_samples:
        rest = [l for l in all_lines if l not in set(result)]
        result += random.sample(rest, min(max_samples - len(result), len(rest)))
    return result


def load_profile(name: str) -> dict | None:
    if not PROFILES_FILE.exists():
        return None
    with open(PROFILES_FILE, encoding="utf-8") as f:
        profiles = json.load(f)
    for p in profiles:
        if p["name"] == name:
            return p
    return None


def generate_dialogue(name: str, situation: str, n: int = 10) -> list[str]:
    lines = load_character_lines(name)
    if not lines:
        print(f"エラー: 「{name}」のセリフが見つかりません")
        return []

    print(f"  ({len(lines)}行のセリフを参照中...)")

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

    for attempt in range(3):
        try:
            text = call_gemini(prompt)
            break
        except urllib.error.HTTPError as e:
            body = e.read().decode()
            if e.code == 429 and attempt < 2:
                wait = 60
                try:
                    info = json.loads(body)
                    for d in info.get("error", {}).get("details", []):
                        delay = d.get("retryDelay", "")
                        if delay:
                            wait = int(delay.rstrip("s")) + 5
                            break
                except Exception:
                    pass
                print(f"  レート制限中、{wait}秒待ちます...")
                time.sleep(wait)
            else:
                raise RuntimeError(f"APIエラー {e.code}: {body}")
    else:
        raise RuntimeError("リトライ上限に達しました")

    result = []
    for line in text.splitlines():
        m = re.match(r"^\d+\.\s*(.+)$", line.strip())
        if m:
            result.append(m.group(1).strip())
    return result


def list_characters():
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
    parser = argparse.ArgumentParser(description="あんガル キャラ台詞生成（Gemini無料API使用）")
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
