#!/usr/bin/env python3
"""
アセットバンドルマニフェストを解析して画像URLリストを出力する

使い方:
  python parse_asset_manifest.py               # マニフェスト取得＆解析
  python parse_asset_manifest.py --images-only # 立ち絵URLのみ出力
"""

import argparse
import json
import re
import sys
from pathlib import Path

import requests
import UnityPy

BASE_CDN = "http://assets.kimisaki.hekk.org"
MANIFEST_URL = f"{BASE_CDN}/asset_bundles/android/android"
OUT_FILE = Path("asset_bundle_list.txt")

HEADERS = {
    "User-Agent": "UnityPlayer/2022.3.6f2 (UnityWebRequest/1.0, libcurl/8.10.1-DEV)",
}


def fetch_manifest() -> bytes:
    print(f"マニフェスト取得中: {MANIFEST_URL}")
    r = requests.get(MANIFEST_URL, headers=HEADERS, timeout=30)
    r.raise_for_status()
    print(f"  {len(r.content):,} bytes")
    return r.content


def parse_manifest(data: bytes) -> list[str]:
    """UnityPyでマニフェストを解析してアセットバンドルパス一覧を返す"""
    paths = []
    try:
        env = UnityPy.load(data)
        for obj in env.objects:
            try:
                d = obj.read()
                # AssetBundleManifest型
                if hasattr(d, "m_AssetBundleInfos"):
                    for name, info in d.m_AssetBundleInfos.items():
                        paths.append(name)
                    break
                # 文字列として探す
                raw = str(d)
                found = re.findall(r'asset_bundles/android/[^\s\'"]+', raw)
                paths.extend(found)
            except Exception:
                continue
    except Exception as e:
        print(f"UnityPy解析エラー: {e}")

    # UnityPyで取れなかった場合はバイナリから直接抽出
    if not paths:
        print("  バイナリから直接パスを抽出...")
        text = data.decode("utf-8", errors="replace")
        paths = re.findall(r'(?:image|audio|spine)/[^\x00\s\'"<>]+\.unity3d[^\x00\s\'"<>]*', text)

    return sorted(set(paths))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--images-only", action="store_true", help="立ち絵URLのみ出力")
    parser.add_argument("--save-raw", action="store_true", help="生データをファイルに保存")
    args = parser.parse_args()

    data = fetch_manifest()

    if args.save_raw:
        Path("manifest_raw.unity3d").write_bytes(data)
        print("  → manifest_raw.unity3d に保存")

    print("解析中...")
    paths = parse_manifest(data)
    print(f"  {len(paths)}件のアセットバンドルパスを検出")

    if args.images_only:
        paths = [p for p in paths if "character/talk" in p]
        print(f"  うち立ち絵: {len(paths)}件")

    # ファイル出力
    lines = [f"{BASE_CDN}/asset_bundles/android/{p}" for p in paths]
    OUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"→ {OUT_FILE} に保存しました")

    # サンプル表示
    print("\nサンプル（最初の10件）:")
    for line in lines[:10]:
        print(f"  {line}")


if __name__ == "__main__":
    main()
