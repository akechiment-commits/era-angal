#!/usr/bin/env python3
"""
asset_bundles/ パスのマニフェストを探し、ストーリータイトル関連データを見つける
game_settings.json で判明した別CDNパス: http://assets.kimisaki.hekk.org/asset_bundles/
"""

import re
import requests
import UnityPy

ASSET_BUNDLE_BASE = "http://assets.kimisaki.hekk.org/asset_bundles"
ASSET_BUNDLE_VERSION = "20180226233215"

MANIFEST_CANDIDATES = [
    f"{ASSET_BUNDLE_BASE}/Android",
    f"{ASSET_BUNDLE_BASE}/Android/Android",
    f"{ASSET_BUNDLE_BASE}/{ASSET_BUNDLE_VERSION}/Android",
    f"{ASSET_BUNDLE_BASE}/{ASSET_BUNDLE_VERSION}/Android/Android",
]

MANIFEST_TEXT_CANDIDATES = [
    f"{ASSET_BUNDLE_BASE}/Android.manifest",
    f"{ASSET_BUNDLE_BASE}/Android/Android.manifest",
    f"{ASSET_BUNDLE_BASE}/{ASSET_BUNDLE_VERSION}/Android.manifest",
    f"{ASSET_BUNDLE_BASE}/{ASSET_BUNDLE_VERSION}/Android/Android.manifest",
]

# all_bundles.txt の中からstory_script以外のファイルを表示
print("=== all_bundles.txt の story_script 以外 ===")
try:
    with open("all_bundles.txt", encoding="utf-8") as f:
        all_bundles = f.read().splitlines()
    non_script = [b for b in all_bundles if "story_script" not in b]
    print(f"story_script 以外: {len(non_script)}件")
    for b in non_script:
        print(f"  {b}")
except FileNotFoundError:
    print("  all_bundles.txt が見つかりません。parse_manifest.py を先に実行してください")

print("\n=== asset_bundles/ パスを探索 ===")

found = []
for url in MANIFEST_CANDIDATES + MANIFEST_TEXT_CANDIDATES:
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            print(f"  ✅ {r.status_code} ({len(r.content):,} bytes) {url}")
            found.append((url, r.content))
        else:
            print(f"  ✗  {r.status_code}  {url}")
    except Exception as e:
        print(f"  ERR {url}: {e}")

# 見つかったマニフェストを解析
for url, data in found:
    print(f"\n=== 解析: {url} ===")
    # テキスト形式を試す
    try:
        text = data.decode("utf-8")
        names = re.findall(r"^\s+Name:\s+(.+)$", text, re.MULTILINE)
        if names:
            print(f"  AssetBundle数: {len(names)}")
            # story/chapter/master/json関連を抽出
            interesting = [n for n in names if any(k in n.lower() for k in [
                "story", "chapter", "master", "json", "event", "title", "info", "catalog", "menu"
            ])]
            non_script2 = [n for n in interesting if "story_script" not in n]
            print(f"  story_script以外の関連: {len(non_script2)}件")
            for n in non_script2[:30]:
                print(f"    {n}")
            with open("asset_bundle_manifest.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(names))
            print(f"  → asset_bundle_manifest.txt に保存")
            continue
    except Exception:
        pass
    # バイナリを試す
    try:
        env = UnityPy.load(data)
        names2 = []
        for obj in env.objects:
            if obj.type.name == "AssetBundleManifest":
                mb = obj.read()
                infos = getattr(mb, "AssetBundleInfos", {})
                for info in (infos.values() if hasattr(infos, "values") else []):
                    name = getattr(info, "Name", None)
                    if name:
                        names2.append(name)
        if names2:
            print(f"  AssetBundle数: {len(names2)}")
            non_script3 = [n for n in names2 if "story_script" not in n]
            for n in non_script3[:30]:
                print(f"    {n}")
    except Exception as e:
        print(f"  解析失敗: {e}")

# story_ids.txt を読んでIDの範囲と欠番を確認
print("\n=== story_ids.txt の統計 ===")
try:
    with open("story_ids.txt") as f:
        ids = [int(x) for x in f.read().splitlines() if x]
    ids.sort()
    print(f"  件数: {len(ids)}")
    print(f"  範囲: {ids[0]} 〜 {ids[-1]}")
    # 1000刻みでの分布
    for start in range(0, ids[-1]+1, 1000):
        count = sum(1 for i in ids if start <= i < start+1000)
        if count > 0:
            print(f"  {start:4d}-{start+999:4d}: {count}件")
except FileNotFoundError:
    print("  story_ids.txt が見つかりません")
