#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gitの現行基準版からイベントボードデータを復旧するための緊急用スクリプト。"""

from pathlib import Path
import subprocess

target = Path('ERB/EVENT_BOARD_DATA_イベントデータ.ERB')
git_path = 'ERB/EVENT_BOARD_DATA_イベントデータ.ERB'
result = subprocess.run(
    ['git', '-c', 'safe.directory=C:/Users/guile/era-angal', 'show', f'HEAD:{git_path}'],
    capture_output=True,
    check=True,
)
target.write_bytes(result.stdout)
print(f'復旧完了: {target} ({len(result.stdout)} bytes)')
