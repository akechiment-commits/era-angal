#!/usr/bin/env python3
"""
あんガル CDN マスターデータ探索スクリプト
ストーリータイトルが入っていそうなパスを全部試す
"""

import requests

BASE = "http://assets.kimisaki.hekk.org"

CANDIDATES = [
    # stories フォルダ直下
    "/datas/Android/data-assets/scriptableobject/stories/story_chapter.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/stories/story_chapter_list.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/stories/story_info.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/stories/story_list.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/stories/story_master.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/stories/story_title.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/stories/chapter_list.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/stories/chapter_master.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/stories/story_data.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/stories/story_catalog.asset.unity3d",
    # master フォルダ
    "/datas/Android/data-assets/scriptableobject/master/story_master.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/master/story_chapter.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/master/story_chapter_master.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/master/story.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/master/chapter.asset.unity3d",
    "/datas/Android/data-assets/masterdata/story_master.asset.unity3d",
    "/datas/Android/data-assets/masterdata/story_chapter.asset.unity3d",
    "/datas/Android/data-assets/masterdata/story.asset.unity3d",
    "/datas/Android/data-assets/masterdata/chapter.asset.unity3d",
    # catalog / manifest
    "/datas/Android/data-assets/catalog.json",
    "/datas/Android/catalog.json",
    "/datas/Android/data-assets/manifest.json",
    "/datas/Android/data-assets/asset_catalog.json",
    "/datas/Android/Android",
    "/datas/Android/Android.manifest",
    "/datas/Android/data-assets/scriptableobject/stories/story_script/manifest.asset.unity3d",
    # story_chapter_script
    "/datas/Android/data-assets/scriptableobject/stories/story_chapter_script.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/stories/story_chapter_info.asset.unity3d",
    # events
    "/datas/Android/data-assets/scriptableobject/events/event_list.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/events/event_master.asset.unity3d",
    # その他
    "/datas/Android/data-assets/scriptableobject/story_chapter.asset.unity3d",
    "/datas/Android/data-assets/scriptableobject/story_master.asset.unity3d",
]

print("CDN パスをプローブ中...\n")
found = []
for path in CANDIDATES:
    url = BASE + path
    try:
        r = requests.get(url, timeout=8)
        status = r.status_code
        size = len(r.content)
        if status == 200:
            print(f"  ✅ {status} ({size:,} bytes) {path}")
            found.append((path, size, r.content))
        else:
            print(f"  ✗  {status}  {path}")
    except Exception as e:
        print(f"  ERR {path}: {e}")

print(f"\n結果: {len(found)}件ヒット")
for path, size, data in found:
    print(f"\n=== {path} ({size:,} bytes) ===")
    # テキストとして読める場合は先頭200文字表示
    try:
        text = data.decode("utf-8")
        print(text[:300])
    except Exception:
        # バイナリ（Unity3d）の場合はUnityPyで解析
        try:
            import UnityPy
            env = UnityPy.load(data)
            for obj in env.objects:
                print(f"  obj type: {obj.type.name}")
                if obj.type.name == "MonoBehaviour":
                    mb = obj.read()
                    attrs = [a for a in dir(mb) if not a.startswith("_")]
                    print(f"  attrs: {attrs[:20]}")
                    break
        except Exception as e2:
            print(f"  バイナリ解析失敗: {e2}")
            print(f"  先頭16バイト: {data[:16].hex()}")
