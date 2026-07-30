#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""通常ガチャにイベント報酬カードの重み付け抽選を組み込む。"""

from pathlib import Path

GACHA_PATH = Path('ERB/GACHA_ガチャシステム.ERB')
text = GACHA_PATH.read_bytes().decode('cp932').replace('\r\n', '\n')

old_normal_pick = '''A = GLOBAL:2100
LOCAL:4 = RAND:A
LOCAL:3 = 2101 + LOCAL:4
A = LOCAL:3
LOCAL:7 = GLOBAL:A
'''
new_normal_pick = '''CALL GACHA_PICK_NORMAL_CARD, LOCAL:5, LOCAL:8
LOCAL:7 = RESULT
'''

old_pickup_normal_pick = '''A = GLOBAL:2100
LOCAL:4 = RAND:A
LOCAL:3 = 2101 + LOCAL:4
A = LOCAL:3
LOCAL:7 = GLOBAL:A
CALL GACHA_ACQUIRE_CARD, LOCAL:7
RETURN LOCAL:7
'''
new_pickup_normal_pick = '''CALL GACHA_PICK_NORMAL_CARD, LOCAL:5, LOCAL:8
LOCAL:7 = RESULT
CALL GACHA_ACQUIRE_CARD, LOCAL:7
RETURN LOCAL:7
'''

helper = '''
;--------------------------------------------------
; 通常カード抽選（ARG:0=キャラNo, ARG:1=レア度）
; イベント報酬カードは通常カードの10分の1の重みで抽選する。
; レア度とキャラの抽選確率は変更しない。
;--------------------------------------------------
@GACHA_PICK_NORMAL_CARD(ARG, ARG:1)
CALL CARD_GET_CHARPOOL, ARG:0, ARG:1
SIF GLOBAL:2100 == 0
	RETURN 0

LOCAL:0 = 0
FOR LOCAL:1, 0, GLOBAL:2100
	A = 2101 + LOCAL:1
	CALL EVENT_BOARD_IS_EVENT_CARD, GLOBAL:A
	IF RESULT
		LOCAL:0 += 1
	ELSE
		LOCAL:0 += 10
	ENDIF
NEXT

A = LOCAL:0
LOCAL:2 = RAND:A
FOR LOCAL:1, 0, GLOBAL:2100
	A = 2101 + LOCAL:1
	CALL EVENT_BOARD_IS_EVENT_CARD, GLOBAL:A
	LOCAL:3 = RESULT ? 1 # 10
	IF LOCAL:2 < LOCAL:3
		RETURN GLOBAL:A
	ENDIF
	LOCAL:2 -= LOCAL:3
NEXT

RETURN GLOBAL:2101

'''

if '@GACHA_PICK_NORMAL_CARD(ARG, ARG:1)' not in text:
    if text.count(old_normal_pick) != 2:
        raise RuntimeError(f'通常抽選ブロックを期待どおり2件特定できません: {text.count(old_normal_pick)}件')
    if text.count(old_pickup_normal_pick) != 1:
        raise RuntimeError(f'ピックアップ通常枠の抽選箇所を一意に特定できません: {text.count(old_pickup_normal_pick)}件')
    text = text.replace(old_normal_pick, new_normal_pick, 1)
    text = text.replace(old_pickup_normal_pick, new_pickup_normal_pick, 1)
    marker = '@GACHA_ACQUIRE_CARD(ARG)'
    if marker not in text:
        raise RuntimeError('関数の挿入位置が見つかりません')
    text = text.replace(marker, helper + marker, 1)

# RAND:LOCAL:n はこの Emuera では多次元添字として扱われるため、
# 既存の生成済み関数も通常変数を経由する書式へ補正する。
text = text.replace('LOCAL:2 = RAND:LOCAL:0', 'A = LOCAL:0\nLOCAL:2 = RAND:A')

GACHA_PATH.write_bytes(text.encode('cp932'))
print('通常ガチャのイベント報酬カード重みを 1/10 に設定しました。')
