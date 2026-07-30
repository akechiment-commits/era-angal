#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""すごろくイベントからFLAG:38の進捗判定を除き、周回数でエリア移行する。"""

from pathlib import Path

path = Path('ERB/EVENT_BOARD_イベントボード周回.ERB')
text = path.read_bytes().decode('cp932').replace('\r\n', '\n')

old_advance = '''IF LOCAL:5 > 0
	A = 71 + FLAG:68
	LOCAL:6 = 20 + RAND:11
	FLAG:A += LOCAL:6
	FLAG:113 += LOCAL:5
	FLAG:37 += LOCAL:5
	PRINTFORMW ◆ 周回ボーナス！　PT +{LOCAL:6}　ブロンズガチャチケット入手！（計{FLAG:113}枚）
ENDIF

IF FLAG:A < 20
	;エリア進捗 +10
	FLAG:38 += 10

	;ランダムドロップ（PT + 稀にアイテム）
	CALL EVENT_BOARD_RANDOM_DROP

	;エリア踏破チェック
	SIF FLAG:38 >= 100
		CALL EVENT_BOARD_AREA_COMPLETE
ENDIF

PRINTFORML 体力 -{LOCAL:0}　サイコロ: {LOCAL:2}　マス{LOCAL:3}→マス{FLAG:33}（進捗: {FLAG:38}/100）
'''
new_advance = '''IF LOCAL:5 > 0
	A = 71 + FLAG:68
	LOCAL:6 = 20 + RAND:11
	FLAG:A += LOCAL:6
	FLAG:113 += LOCAL:5
	FLAG:37 += LOCAL:5
	PRINTFORMW ◆ 周回ボーナス！　PT +{LOCAL:6}　ブロンズガチャチケット入手！（計{FLAG:113}枚）

	; すごろくのエリア移行は3周ごと。FLAG:38の進捗は使わない。
	A = FLAG:68 + 98
	SIF FLAG:A < 20 && FLAG:37 % 3 == 0
		CALL EVENT_BOARD_AREA_COMPLETE
ENDIF

; ランダムドロップは既存どおり、周回エリア到達前のサイコロごとに判定する。
A = FLAG:68 + 98
SIF FLAG:A < 20
	CALL EVENT_BOARD_RANDOM_DROP

PRINTFORML 体力 -{LOCAL:0}　サイコロ: {LOCAL:2}　マス{LOCAL:3}→マス{FLAG:33}
'''
if old_advance not in text:
    raise SystemExit('すごろく進捗ブロックの置換対象が見つかりません。')
text = text.replace(old_advance, new_advance, 1)

old_status = '''IF TFLAG:91 == 3
	PRINTFORML エリア{FLAG:A}　周回数:{FLAG:37}周
ELSEIF FLAG:A >= 20'''
new_status = '''IF TFLAG:91 == 3
	IF FLAG:A < 20
		LOCAL:0 = FLAG:37 % 3
		PRINTFORML エリア{FLAG:A}　周回数:{FLAG:37}周（次のエリアまで{3 - LOCAL:0}周）
	ELSE
		PRINTFORML エリア{FLAG:A}　周回数:{FLAG:37}周
	ENDIF
ELSEIF FLAG:A >= 20'''
if old_status not in text:
    raise SystemExit('すごろく状態表示の置換対象が見つかりません。')
text = text.replace(old_status, new_status, 1)

path.write_bytes(text.encode('cp932'))
print('すごろくを周回数のみで進行する方式へ更新しました。')
