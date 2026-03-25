#!/usr/bin/env python3
"""
あんガル シナリオ一括ダウンロード＆抽出スクリプト

使い方:
  python download_scenarios.py           # ID 1-3000を試す
  python download_scenarios.py 1 500     # ID 1-500を試す
"""

import json
import sys
import time
from pathlib import Path

import requests
import UnityPy

BASE_URL = "http://assets.kimisaki.hekk.org/datas/Android/data-assets/scriptableobject/stories/story_script/{id}.asset.unity3d"
OUT_DIR = Path("scenarios")
OUT_DIR.mkdir(exist_ok=True)


def download(story_id: int):
    url = BASE_URL.format(id=story_id)
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.content
        return None
    except Exception:
        return None


def parse_unity3d(data: bytes):
    try:
        env = UnityPy.load(data)
        for obj in env.objects:
            if obj.type.name == "MonoBehaviour":
                mb = obj.read()
                script_raw = getattr(mb, "script", None)
                if not script_raw:
                    continue
                if isinstance(script_raw, str):
                    commands = json.loads(script_raw)
                else:
                    commands = script_raw
                talks = [
                    {"speaker": c.get("speaker", ""), "text": c.get("text", "")}
                    for c in commands
                    if c.get("command") == "talk"
                ]
                if talks:
                    return talks
    except Exception:
        pass
    return None


def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    end = int(sys.argv[2]) if len(sys.argv) > 2 else 3000

    print(f"ID {start}〜{end} をダウンロードします")
    found = 0

    for story_id in range(start, end + 1):
        data = download(story_id)
        if data is None:
            continue

        talks = parse_unity3d(data)
        if talks:
            out_file = OUT_DIR / f"{story_id}.txt"
            out_file.write_text(
                f"=== {story_id} ===\n" + "\n".join(f"【{t['speaker']}】{t['text']}" for t in talks),
                encoding="utf-8"
            )
            found += 1
            print(f"  [{story_id}] {len(talks)}行")
        else:
            print(f"  [{story_id}] セリフなし")

        time.sleep(0.1)

    print(f"\n完了: {found}件取得 → {OUT_DIR}/")


if __name__ == "__main__":
    main()
