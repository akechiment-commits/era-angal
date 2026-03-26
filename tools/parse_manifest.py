#!/usr/bin/env python3
"""
Android.manifest を解析して全AssetBundle一覧を取得し、
ストーリー関連のものを探す
"""

import re
import requests
import UnityPy

BASE = "http://assets.kimisaki.hekk.org/datas/Android"
MANIFEST_URL = f"{BASE}/Android.manifest"


def fetch_manifest():
    print(f"マニフェスト取得中: {MANIFEST_URL}")
    r = requests.get(MANIFEST_URL, timeout=15)
    r.raise_for_status()
    return r.content


def parse_manifest(data: bytes) -> list[str]:
    env = UnityPy.load(data)
    for obj in env.objects:
        if obj.type.name == "AssetBundleManifest":
            mb = obj.read()
            # AssetBundleInfos から Name を全部取得
            names = []
            infos = getattr(mb, "AssetBundleInfos", None) or getattr(mb, "m_AssetBundleInfos", None)
            if infos:
                for info in infos.values() if hasattr(infos, "values") else infos:
                    name = getattr(info, "Name", None) or getattr(info, "m_Name", None)
                    if name:
                        names.append(name)
            return names
    return []


def parse_manifest_text(data: bytes) -> list[str]:
    """テキスト形式のマニフェストからName行を抽出"""
    try:
        text = data.decode("utf-8")
        names = re.findall(r"^\s+Name:\s+(.+)$", text, re.MULTILINE)
        return names
    except Exception:
        return []


def download_and_inspect(path: str):
    url = f"{BASE}/{path}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return
        data = r.content
        print(f"\n=== {path} ({len(data):,} bytes) ===")
        # JSONファイルの場合
        try:
            text = data.decode("utf-8")
            print(text[:500])
            return
        except Exception:
            pass
        # Unity3dの場合
        try:
            env = UnityPy.load(data)
            for obj in env.objects:
                print(f"  obj type: {obj.type.name}")
                if obj.type.name in ("MonoBehaviour", "TextAsset"):
                    mb = obj.read()
                    attrs = [a for a in dir(mb) if not a.startswith("_")]
                    print(f"  attrs: {attrs[:30]}")
                    # テキストとして読めるか試す
                    for attr in ("m_Script", "text", "m_Text", "script", "data"):
                        val = getattr(mb, attr, None)
                        if val and isinstance(val, str) and len(val) > 10:
                            print(f"  {attr}: {val[:300]}")
                            break
                    break
        except Exception as e:
            print(f"  解析失敗: {e}")
    except Exception as e:
        print(f"  取得失敗: {e}")


def main():
    data = fetch_manifest()

    # バイナリマニフェスト (.manifest) はテキスト形式
    names = parse_manifest_text(data)
    if not names:
        names = parse_manifest(data)

    print(f"\n全AssetBundle数: {len(names)}")

    # story / chapter / master / json 関連を抽出
    story_related = [n for n in names if any(k in n for k in [
        "story", "chapter", "master", "json", "event", "title", "info", "catalog"
    ])]

    print(f"ストーリー関連: {len(story_related)}件\n")

    # json フォルダのファイルをすべて表示
    json_files = [n for n in names if "json" in n]
    print("=== JSONファイル一覧 ===")
    for n in json_files[:50]:
        print(f"  {n}")

    # story関連でscript以外（マスターデータ候補）
    print("\n=== story_script 以外のストーリー関連 ===")
    non_script = [n for n in story_related if "story_script" not in n]
    for n in non_script[:50]:
        print(f"  {n}")

    # 全story関連ファイルをダウンロード＆検査
    print("\n=== 候補ファイルを取得・検査 ===")
    for n in non_script[:20]:
        download_and_inspect(n)

    # story_script の ID一覧も保存
    script_ids = []
    for n in names:
        m = re.search(r"story_script/(\d+)\.asset\.unity3d", n)
        if m:
            script_ids.append(int(m.group(1)))
    script_ids.sort()
    if script_ids:
        print(f"\n=== story_script ID一覧 ({len(script_ids)}件) ===")
        print(f"  最小: {script_ids[0]}, 最大: {script_ids[-1]}")
        print(f"  IDs: {script_ids[:30]}...")
        with open("story_ids.txt", "w") as f:
            f.write("\n".join(map(str, script_ids)))
        print("  → story_ids.txt に保存しました")

    # 全名前をファイルに保存
    with open("all_bundles.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(names))
    print(f"\n全{len(names)}件 → all_bundles.txt に保存しました")


if __name__ == "__main__":
    main()
