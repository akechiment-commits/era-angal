#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""すごろくを0番スタート兼周回マスへ変更し、19番ゴール依存を除く。"""

from pathlib import Path

path = Path('ERB/EVENT_BOARD_イベントボード周回.ERB')
text = path.read_bytes().decode('cp932').replace('\r\n', '\n')

old_move = '''LOCAL:2 = RAND:6 + 1
LOCAL:3 = FLAG:33	;移動前の位置
FLAG:33 = (FLAG:33 + LOCAL:2) % 20
'''
new_move = '''LOCAL:2 = RAND:6 + 1
LOCAL:3 = FLAG:33	;移動前の位置
LOCAL:4 = FLAG:33 + LOCAL:2
FLAG:33 = LOCAL:4 % 20
LOCAL:5 = LOCAL:4 / 20

; 20を越えた時点で周回成立。19番マスへ止まる必要はない。
IF LOCAL:5 > 0
	A = 71 + FLAG:68
	LOCAL:6 = 20 + RAND:11
	FLAG:A += LOCAL:6
	FLAG:113 += LOCAL:5
	FLAG:37 += LOCAL:5
	PRINTFORMW ◆ 周回ボーナス！　PT +{LOCAL:6}　ブロンズガチャチケット入手！（計{FLAG:113}枚）
ENDIF
'''
if old_move not in text:
    raise SystemExit('移動計算の置換対象が見つかりません。')
text = text.replace(old_move, new_move, 1)

old_normal = 'IF FLAG:33 == 1 || FLAG:33 == 2 || FLAG:33 == 4 || FLAG:33 == 7'
new_normal = 'IF FLAG:33 == 1 || FLAG:33 == 2 || FLAG:33 == 4 || FLAG:33 == 7 || FLAG:33 == 19'
if old_normal not in text:
    raise SystemExit('通常マス条件の置換対象が見つかりません。')
text = text.replace(old_normal, new_normal, 1)

goal_start = text.index(';ゴールマス: 19')
goal_end = text.index('ENDIF\nRETURN 1', goal_start)
text = text[:goal_start] + 'ENDIF\nRETURN 1' + text[goal_end + len('ENDIF\nRETURN 1'):]

path.write_bytes(text.encode('cp932'))
print('すごろくをスタート兼周回マス方式へ更新しました。')
