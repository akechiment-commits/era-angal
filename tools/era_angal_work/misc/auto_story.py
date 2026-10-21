#!/usr/bin/env python3
"""
あんガル ストーリー自動スキップスクリプト
チャプター内のストーリーを自動でスキップし続ける

使い方:
  python auto_story.py          # デフォルト100話
  python auto_story.py 500      # 500話スキップ
  python auto_story.py 0        # 無限ループ（Ctrl+Cで停止）
"""

import subprocess
import time
import sys

DEVICE = "127.0.0.1:5555"

# ボタン座標（Android解像度 1600x900 基準）
MENU_BTN   = (1490, 70)   # 右上の ≡ メニューボタン
SKIP_BTN   = (1120, 70)   # メニュー内の「スキップ」
YOMU_BTN   = (1030, 585)  # 「次のストーリー」ポップアップの「読む」
TITLE_TAP  = (800, 450)   # タイトル画面をタップ


def tap(x, y):
    subprocess.run(
        ["adb", "-s", DEVICE, "shell", "input", "tap", str(x), str(y)],
        capture_output=True
    )


def skip_one_story():
    tap(*MENU_BTN)
    time.sleep(1.0)
    tap(*SKIP_BTN)
    time.sleep(1.5)
    tap(*YOMU_BTN)
    time.sleep(3.0)   # 次の話のロード待ち
    tap(*TITLE_TAP)
    time.sleep(1.5)


def main():
    count = 100
    if len(sys.argv) >= 2:
        count = int(sys.argv[1])

    infinite = count == 0
    print(f"開始します（{'無限' if infinite else count}話）")
    print("Ctrl+C で停止")

    i = 0
    try:
        while infinite or i < count:
            skip_one_story()
            i += 1
            print(f"  {i}話スキップ完了")
    except KeyboardInterrupt:
        print(f"\n停止しました（{i}話完了）")


if __name__ == "__main__":
    main()
