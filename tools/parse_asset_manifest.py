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
    """マニフェストバイナリからアセットバンドルパス一覧を返す"""
    paths = []

    try:
        env = UnityPy.load(data)
        for obj in env.objects:
            try:
                # type treeから辞書として読む
                tree = obj.read_typetree()
                raw = json.dumps(tree, ensure_ascii=False)
                # image/audio等で始まるパスを抽出
                found = re.findall(r'(?:image|audio|spine|effect|ui)/[\w./+\-]+', raw)
                paths.extend(found)
            except Exception:
                # フォールバック: str変換
                try:
                    d = obj.read()
                    raw = str(d)
                    found = re.findall(r'(?:image|audio|spine)/[\w./+\-]+', raw)
                    paths.extend(found)
                except Exception:
                    pass
    except Exception as e:
        print(f"  UnityPy: {e}")

    # UnityPyで不十分な場合はバイナリから長い文字列を抽出
    if len(paths) < 100:
        print("  UnityPy結果が少ないためバイナリ直接抽出...")
        # Unityは文字列を4バイト長+文字列の形式で格納する
        # 長さ8以上のASCII文字列を全部取る
        for m in re.finditer(rb'(image|audio|spine|effect|ui)/([\x21-\x7e/._+\-]+)', data):
            try:
                paths.append(m.group(0).decode("ascii"))
            except Exception:
                pass

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
