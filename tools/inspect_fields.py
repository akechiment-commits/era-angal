#!/usr/bin/env python3
"""
story_script AssetBundleの全フィールドを調べる
タイトル・章名が含まれていないか確認
"""

import json
import requests
import UnityPy

BASE_CDN = "http://assets.kimisaki.hekk.org/datas/Android"
WEB_BASE = "http://assets.kimisaki.hekk.org/web/20170729"

def inspect_story_script(story_id: int):
    url = f"{BASE_CDN}/data-assets/scriptableobject/stories/story_script/{story_id}.asset.unity3d"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        print(f"  {story_id}: {r.status_code}")
        return

    env = UnityPy.load(r.content)
    for obj in env.objects:
        if obj.type.name == "MonoBehaviour":
            mb = obj.read()
            attrs = [a for a in dir(mb) if not a.startswith("_")]
            print(f"\n=== story_script/{story_id} のフィールド ===")
            print(f"  attrs: {attrs}")
            for attr in attrs:
                val = getattr(mb, attr, None)
                if val is None:
                    continue
                if isinstance(val, (str, int, float, bool)):
                    print(f"  {attr}: {repr(val)[:200]}")
                elif isinstance(val, (list, dict)):
                    print(f"  {attr}: ({type(val).__name__}, len={len(val)})")
            return

# いくつかのIDを検査
print("=== story_script フィールド調査 ===")
for sid in [1, 2, 41, 100, 1000]:
    inspect_story_script(sid)

# web リソースパスを探索
print("\n\n=== web/20170729/ パスを探索 ===")
web_candidates = [
    f"{WEB_BASE}/",
    f"{WEB_BASE}/story",
    f"{WEB_BASE}/story_chapter.json",
    f"{WEB_BASE}/story_master.json",
    f"{WEB_BASE}/chapter_list.json",
    f"{WEB_BASE}/master/story.json",
    f"{WEB_BASE}/master/story_chapter.json",
    f"{WEB_BASE}/master/chapter.json",
]
for url in web_candidates:
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            print(f"  ✅ {r.status_code} ({len(r.content):,} bytes) {url}")
            try:
                print(f"     {r.text[:300]}")
            except Exception:
                pass
        else:
            print(f"  ✗  {r.status_code}  {url}")
    except Exception as e:
        print(f"  ERR: {e}")
