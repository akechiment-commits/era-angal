# -*- coding: utf-8 -*-
"""
ERB/REVMODE_リバースモード.ERB を全面改修するスクリプト。
1. 地の文の多パターン化（RAND・過熱度・相手性格による分岐）
2. 過熱度（TFLAG:108）および継続ターン（TFLAG:109）の導入
3. 主導権返還コマンド（[9] 主導権を返してもらう）の追加
4. 過熱度に応じた快感ソース倍率・体力消費緩和
"""

import re
import sys

def main():
    target_path = 'ERB/REVMODE_リバースモード.ERB'
    with open(target_path, 'rb') as f:
        text = f.read().decode('cp932')

    # Normalize newlines
    text = text.replace('\r\n', '\n')

    # 1. Update GET_TRAINNAME_ACTIVECOM to add CASE 9
    pattern_name = r'(@GET_TRAINNAME_ACTIVECOM\(ARG\).*?CASE 8\n\tRETURNF "おねだり"\n)(ENDSELECT)'
    match = re.search(pattern_name, text, re.DOTALL)
    assert match, "GET_TRAINNAME_ACTIVECOM pattern not found"
    replacement_name = match.group(1) + ';主導権返還\nCASE 9\n\tRETURNF "主導権を返してもらう"\n' + match.group(2)
    text = text[:match.start()] + replacement_name + text[match.end():]

    # 2. Update REVMODE_SHOW_USERCOM loop to include 0 to 9, and display heatup
    old_show_u = '''@REVMODE_SHOW_USERCOM
#DIM LCOUNT, 1
VARSET C
FOR LCOUNT, 0, 9
	;REVMODEに固有のCOMABLE
	SIF !REVMODE_ACTIVE_COMABLE(SELECTCOM, LCOUNT)
		CONTINUE
	;コマンド名を表示
	PRINTFORML %GET_TRAINNAME_ACTIVECOM(LCOUNT)%[{LCOUNT, 3}]
NEXT'''

    new_show_u = '''@REVMODE_SHOW_USERCOM
#DIM LCOUNT, 1
VARSET C
;過熱度の表示
IF TFLAG:44
	PRINTFORM 【熱中度:
	IF TFLAG:108 >= 3
		SETCOLOR 255, 50, 150
		PRINTFORM ★★★ 陶酔・絶頂狂乱
	ELSEIF TFLAG:108 == 2
		SETCOLOR 255, 100, 200
		PRINTFORM ★★ 昂揚・本気攻め
	ELSEIF TFLAG:108 == 1
		SETCOLOR 255, 150, 200
		PRINTFORM ★ 熱気・積極的
	ELSE
		PRINTFORM ☆ 探り合い
	ENDIF
	RESETCOLOR
	PRINTFORML 】(連続:{TFLAG:109}ターン)
ENDIF
FOR LCOUNT, 0, 10
	;REVMODEに固有のCOMABLE
	SIF !REVMODE_ACTIVE_COMABLE(SELECTCOM, LCOUNT)
		CONTINUE
	;コマンド名を表示
	PRINTFORML %GET_TRAINNAME_ACTIVECOM(LCOUNT)%[{LCOUNT, 3}]
NEXT'''

    assert old_show_u in text, "old_show_u not found"
    text = text.replace(old_show_u, new_show_u, 1)

    # 3. Update REVMODE_ACTIVE_COMABLE to include CASE 9 (always allowed)
    old_active_comable = '''@REVMODE_ACTIVE_COMABLE(ARG:0, ARG:1)
#FUNCTION
SELECTCASE ARG:1
;キス
CASE 0'''

    new_active_comable = '''@REVMODE_ACTIVE_COMABLE(ARG:0, ARG:1)
#FUNCTION
SELECTCASE ARG:1
;主導権返還
CASE 9
	RETURNF 1
;キス
CASE 0'''

    assert old_active_comable in text, "old_active_comable not found"
    text = text.replace(old_active_comable, new_active_comable, 1)

    # 4. Update REVMODE_ACTIVEPHASE to handle CASE 9 (surrender leadership back)
    pattern_aphase = r'(@REVMODE_ACTIVEPHASE\n#DIM LINE, 1\n#DIM DYNAMIC REACTION, 1\nLINE = LINECOUNT\nDRAWLINE\nINPUT\n)(SELECTCASE RESULT\n;COM\nCASE 0 TO 9)'
    match_ap = re.search(pattern_aphase, text)
    assert match_ap, "pattern_aphase not found"
    
    new_aphase_code = match_ap.group(1) + ''';主導権返還コマンド
IF RESULT == 9
	PRINTFORML %CALLNAME:PLAYER%は%CALLNAME:TARGET%に優しく微笑みかけ、そろそろ主導権を戻してほしいと頼んだ…
	PRINTFORM %CALLNAME:TARGET%は
	IF TFLAG:108 >= 2
		PRINTFORML 名残惜しそうに熱い息を吐きながらも、愛おしそうに頷いてくれた…
	ELSE
		PRINTFORML 満足そうに小さく笑って、主導権を譲ってくれた…
	ENDIF
	TFLAG:34 = 0
	CFLAG:15 = 0
	TFLAG:108 = 0
	TFLAG:109 = 0
	WAIT
	RETURN 0
ENDIF
SELECTCASE RESULT
;COM
CASE 0 TO 8'''
    text = text[:match_ap.start()] + new_aphase_code + text[match_ap.end():]

    # 5. Update REVMODE_ACTIVECOM with heatup logic using regex
    pattern_acom = r'(@REVMODE_ACTIVECOM\(ARG:0, ARG:1\)\n#DIM LCOUNT, 1\n\n.*?REPEAT 30\n\tTFLAG:COUNT = 0\nREND\n(?:TFLAG:100 = 0\n)?(?:TFLAG:540 = 0\n)?)'
    match_ac = re.search(pattern_acom, text)
    assert match_ac, "pattern_acom not found"
    
    new_acom_code = match_ac.group(1) + '''\n;連続ターンカウント
TFLAG:109 += 1

;プレイヤーのリアクションに応じた過熱度の計算
SELECTCASE ARG:1
;積極的にやる / 快感を受け入れる
CASE 5, 7
	TFLAG:108 = MIN(TFLAG:108 + 1, 3)
;おねだり
CASE 8
	TFLAG:108 = MIN(TFLAG:108 + 2, 3)
;快感に耐える
CASE 6
	;相手がサドなら焦らされて過熱度急上昇
	IF TALENT:TARGET:83 || ABL:TARGET:15 >= 3
		TFLAG:108 = MIN(TFLAG:108 + 1, 3)
	ENDIF
;消極的にやる
CASE 4
	TFLAG:108 = MAX(TFLAG:108 - 1, 0)
ENDSELECT\n'''
    text = text[:match_ac.start()] + new_acom_code + text[match_ac.end():]

    # 6. Update REVMODE_SOURCE_CHECK to apply heatup bonus and stamina mitigation
    pattern_source = r'(;体力・気力の減少\n.*?BASE:0 -= LOSEBASE:0\nBASE:1 -= LOSEBASE:1)'
    match_sc = re.search(pattern_source, text)
    assert match_sc, "pattern_source not found"
    
    new_source_code = ''';過熱度に応じた快感ソースボーナス（熱中するほど濃厚に）
IF TFLAG:108 >= 3
	FOR LCOUNT, 0, 5
		TIMES SOURCE:LCOUNT, 1.60
	NEXT
	TIMES SOURCE:18, 1.50
ELSEIF TFLAG:108 == 2
	FOR LCOUNT, 0, 5
		TIMES SOURCE:LCOUNT, 1.35
	NEXT
	TIMES SOURCE:18, 1.30
ELSEIF TFLAG:108 == 1
	FOR LCOUNT, 0, 5
		TIMES SOURCE:LCOUNT, 1.15
	NEXT
ENDIF

;体力・気力の減少
;パートナー主導の一手は、体力・気力・耐力の実消費量と表示をともに半額にする。
;さらに過熱状態中は夢中になって疲労を感じにくくなるよう持続支援
IF TFLAG:108 >= 2
	LOSEBASE:0 = (LOSEBASE:0 + 2) / 3
	LOSEBASE:1 = (LOSEBASE:1 + 2) / 3
ELSEIF TFLAG:543
	LOSEBASE:0 = (LOSEBASE:0 + 1) / 2
	LOSEBASE:1 = (LOSEBASE:1 + 1) / 2
	DOWNBASE:MASTER:4 = (DOWNBASE:MASTER:4 + 1) / 2
ENDIF
BASE:0 -= LOSEBASE:0
BASE:1 -= LOSEBASE:1'''
    text = text[:match_sc.start()] + new_source_code + text[match_sc.end():]

    # Write back as CP932 with CRLF
    text_crlf = text.replace('\n', '\r\n')
    with open(target_path, 'wb') as f:
        f.write(text_crlf.encode('cp932'))

    print("Step 1 (Base REVMODE logic) successfully applied.")

if __name__ == '__main__':
    main()
