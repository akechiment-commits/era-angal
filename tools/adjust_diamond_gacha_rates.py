#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ダイヤガチャと同率の抽選を R11 / HR28 / SR40 / UR15 / MR6 に設定する。"""

from pathlib import Path

path = Path('ERB/GACHA_ガチャシステム.ERB')
text = path.read_bytes().decode('cp932')

old_label = 'R10% HR25% SR35% UR24% MR6%'
new_label = 'R11% HR28% SR40% UR15% MR6%'

if old_label in text:
    # 3箇所: 通常ガチャ、イベント中ピックアップ、校内巡り遭遇ガチャ
    if text.count(old_label) != 4:
        raise RuntimeError(f'旧ダイヤ排出率の表記数が想定外です: {text.count(old_label)}')
    if text.count('LOCAL:9 < 3500') != 3 or text.count('LOCAL:9 < 7000') != 3:
        raise RuntimeError('ダイヤ抽選の閾値を期待どおり特定できません')

    text = text.replace(old_label, new_label)
    text = text.replace('LOCAL:9 < 1000', 'LOCAL:9 < 1100')
    text = text.replace('LOCAL:9 < 3500', 'LOCAL:9 < 3900')
    text = text.replace('LOCAL:9 < 7000', 'LOCAL:9 < 7900')
    # URの上限9400はそのまま。9400〜9999をMR 6%に維持する。
    text = text.replace('（MR 6\\%　R10\\% HR25\\% SR35\\% UR24\\%）', '（MR 6\\%　R11\\% HR28\\% SR40\\% UR15\\%）')

path.write_bytes(text.encode('cp932'))
print('ダイヤ系ガチャを R11% / HR28% / SR40% / UR15% / MR6% に設定しました。')
