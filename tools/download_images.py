#!/usr/bin/env python3
"""
キャラ立ち絵をダウンロードしてPNGとして保存する

使い方:
  python download_images.py                  # 全立ち絵(hd)をダウンロード
  python download_images.py --default-only   # default衣装のみ
  python download_images.py --list asset_bundle_list.txt
"""

import argparse
import re
import time
from pathlib import Path

import requests
import UnityPy

BUNDLE_LIST = Path("asset_bundle_list.txt")
OUT_DIR = Path("images")
HEADERS = {
    "User-Agent": "UnityPlayer/2022.3.6f2 (UnityWebRequest/1.0, libcurl/8.10.1-DEV)",
}


def extract_png(data: bytes) -> bytes | None:
    """unity3dバンドルからTexture2DをPNGとして抽出"""
    try:
        env = UnityPy.load(data)
        for obj in env.objects:
            if obj.type.name == "Texture2D":
                tex = obj.read()
                img = tex.image
                import io
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                return buf.getvalue()
    except Exception:
        pass
    return None


def url_to_outpath(url: str) -> Path:
    """URLからローカル保存パスを生成"""
    # http://...android/image/character/talk/1/apron-winter/1.png_bdc5735e3bf2659ded7725b8ada1a4f6.unity3d
    # → images/character/talk/1/apron-winter/1.png
    part = url.split("/asset_bundles/android/image/")[-1]
    # _hash.unity3d を除去
    part = re.sub(r'_[0-9a-f]{32}\.unity3d$', '', part)
    return OUT_DIR / part


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", default=str(BUNDLE_LIST), help="URLリストファイル")
    parser.add_argument("--default-only", action="store_true", help="default衣装のみ")
    parser.add_argument("--skip-existing", action="store_true", default=True, help="既存ファイルをスキップ")
    args = parser.parse_args()

    urls = Path(args.list).read_text(encoding="utf-8").splitlines()

    # character/talk のみ（.unity3d で終わるもの）
    urls = [u for u in urls if "character/talk" in u and u.endswith(".unity3d")]

    if args.default_only:
        # expressionなし（衣装フォルダ直下の番号ファイルのみ）
        urls = [u for u in urls if "_expression/" not in u]

    print(f"対象: {len(urls)}件")

    ok = skip = fail = 0
    for i, url in enumerate(urls, 1):
        out = url_to_outpath(url)
        if args.skip_existing and out.exists():
            skip += 1
            continue

        out.parent.mkdir(parents=True, exist_ok=True)

        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code != 200:
                fail += 1
                continue

            png = extract_png(r.content)
            if png:
                out.write_bytes(png)
                ok += 1
                if ok % 50 == 0 or i <= 5:
                    print(f"  [{i}/{len(urls)}] {out} ({len(png)//1024}KB)")
            else:
                fail += 1
        except Exception as e:
            fail += 1
            if fail <= 5:
                print(f"  失敗: {url} ({e})")

        time.sleep(0.05)

    print(f"\n完了: 取得{ok} / スキップ{skip} / 失敗{fail}")
    print(f"→ {OUT_DIR}/")


if __name__ == "__main__":
    main()
