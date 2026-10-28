# -*- coding: utf-8 -*-
"""
ERB/REVMODE_リバースモード.ERB を全面改修するスクリプト。
1. 地の文の多パターン化（RAND・過熱度・相手性格による分岐）
2. 過熱度（TFLAG:108）および継続ターン（TFLAG:109）の導入
3. 主導権返還コマンド（[9] 主導権を返してもらう）の追加
4. 過熱度に応じた快感ソース倍率・体力消費緩和
"""

import sys

def main():
    target_path = 'ERB/REVMODE_リバースモード.ERB'
    with open(target_path, 'rb') as f:
        raw = f.read()
    text = raw.decode('cp932')
    text = text.replace('\r\n', '\n')

    # 1. GET_TRAINNAME_ACTIVECOM に CASE 9 追加
    pos = text.find(';おねだり\nCASE 8\n\tRETURNF "おねだり"\nENDSELECT')
    if pos != -1:
        old_snip = ';おねだり\nCASE 8\n\tRETURNF "おねだり"\nENDSELECT'
        new_snip = ';おねだり\nCASE 8\n\tRETURNF "おねだり"\n;主導権返還\nCASE 9\n\tRETURNF "主導権を返してもらう"\nENDSELECT'
        text = text.replace(old_snip, new_snip, 1)
        print("1. GET_TRAINNAME_ACTIVECOM updated.")
    else:
        print("Warning: 1. GET_TRAINNAME_ACTIVECOM target not found directly, checking...")

    # 2. REVMODE_SHOW_USERCOM に過熱度表示と 0 TO 9 へのループ拡張
    pos2 = text.find('FOR LCOUNT, 0, 9\n\t;REVMODEに固有のCOMABLE\n\tSIF !REVMODE_ACTIVE_COMABLE(SELECTCOM, LCOUNT)')
    if pos2 != -1:
        old_snip2 = 'FOR LCOUNT, 0, 9\n\t;REVMODEに固有のCOMABLE\n\tSIF !REVMODE_ACTIVE_COMABLE(SELECTCOM, LCOUNT)'
        new_snip2 = '''IF TFLAG:44
\tPRINTFORM 【熱中度:
\tIF TFLAG:108 >= 3
\t\tSETCOLOR 255, 50, 150
\t\tPRINTFORM ★★★ 陶酔・絶頂狂乱
\tELSEIF TFLAG:108 == 2
\t\tSETCOLOR 255, 100, 200
\t\tPRINTFORM ★★ 昂揚・本気攻め
\tELSEIF TFLAG:108 == 1
\t\tSETCOLOR 255, 150, 200
\t\tPRINTFORM ★ 熱気・積極的
\tELSE
\t\tPRINTFORM ☆ 探り合い
\tENDIF
\tRESETCOLOR
\tPRINTFORML 】(連続:{TFLAG:109}ターン)
ENDIF
FOR LCOUNT, 0, 10
\t;REVMODEに固有のCOMABLE
\tSIF !REVMODE_ACTIVE_COMABLE(SELECTCOM, LCOUNT)'''
        text = text.replace(old_snip2, new_snip2, 1)
        print("2. REVMODE_SHOW_USERCOM updated.")

    # 3. REVMODE_ACTIVE_COMABLE に CASE 9 (常に1) 追加
    pos3 = text.find('@REVMODE_ACTIVE_COMABLE(ARG:0, ARG:1)\n#FUNCTION\nSELECTCASE ARG:1\n;キス\nCASE 0')
    if pos3 != -1:
        old_snip3 = '@REVMODE_ACTIVE_COMABLE(ARG:0, ARG:1)\n#FUNCTION\nSELECTCASE ARG:1\n;キス\nCASE 0'
        new_snip3 = '@REVMODE_ACTIVE_COMABLE(ARG:0, ARG:1)\n#FUNCTION\nSELECTCASE ARG:1\n;主導権返還\nCASE 9\n\tRETURNF 1\n;キス\nCASE 0'
        text = text.replace(old_snip3, new_snip3, 1)
        print("3. REVMODE_ACTIVE_COMABLE updated.")

    # 4. REVMODE_ACTIVEPHASE に CASE 9 処理追加
    pos4 = text.find('@REVMODE_ACTIVEPHASE\n#DIM LINE, 1\n#DIM DYNAMIC REACTION, 1\nLINE = LINECOUNT\nDRAWLINE\nINPUT\nSELECTCASE RESULT\n;COM\nCASE 0 TO 9')
    if pos4 != -1:
        old_snip4 = '@REVMODE_ACTIVEPHASE\n#DIM LINE, 1\n#DIM DYNAMIC REACTION, 1\nLINE = LINECOUNT\nDRAWLINE\nINPUT\nSELECTCASE RESULT\n;COM\nCASE 0 TO 9'
        new_snip4 = '''@REVMODE_ACTIVEPHASE
#DIM LINE, 1
#DIM DYNAMIC REACTION, 1
LINE = LINECOUNT
DRAWLINE
INPUT
;主導権返還コマンド
IF RESULT == 9
\tPRINTFORML %CALLNAME:PLAYER%は%CALLNAME:TARGET%に優しく微笑みかけ、そろそろ主導権を戻してほしいと頼んだ…
\tPRINTFORM %CALLNAME:TARGET%は
\tIF TFLAG:108 >= 2
\t\tPRINTFORML 名残惜しそうに熱い息を吐きながらも、愛おしそうに頷いてくれた…
\tELSE
\t\tPRINTFORML 満足そうに小さく笑って、主導権を譲ってくれた…
\tENDIF
\tTFLAG:34 = 0
\tCFLAG:15 = 0
\tTFLAG:108 = 0
\tTFLAG:109 = 0
\tWAIT
\tRETURN 0
ENDIF
SELECTCASE RESULT
;COM
CASE 0 TO 8'''
        text = text.replace(old_snip4, new_snip4, 1)
        print("4. REVMODE_ACTIVEPHASE updated.")

    # 5. REVMODE_ACTIVECOM に過熱度計算追加
    pos5 = text.find('@REVMODE_ACTIVECOM(ARG:0, ARG:1)\n#DIM LCOUNT, 1')
    if pos5 != -1:
        # find the end of repeat block
        rend_pos = text.find('REND\nTFLAG:100 = 0\nTFLAG:540 = 0\n', pos5)
        if rend_pos != -1:
            target_str = 'REND\nTFLAG:100 = 0\nTFLAG:540 = 0\n'
            add_str = '''REND
TFLAG:100 = 0
TFLAG:540 = 0

;連続ターンカウント
TFLAG:109 += 1

;プレイヤーのリアクションに応じた過熱度の計算
SELECTCASE ARG:1
;積極的にやる / 快感を受け入れる
CASE 5, 7
\tTFLAG:108 = MIN(TFLAG:108 + 1, 3)
;おねだり
CASE 8
\tTFLAG:108 = MIN(TFLAG:108 + 2, 3)
;快感に耐える
CASE 6
\t;相手がサドなら焦らされて過熱度急上昇
\tIF TALENT:TARGET:83 || ABL:TARGET:15 >= 3
\t\tTFLAG:108 = MIN(TFLAG:108 + 1, 3)
\tENDIF
;消極的にやる
CASE 4
\tTFLAG:108 = MAX(TFLAG:108 - 1, 0)
ENDSELECT
'''
            text = text[:rend_pos] + add_str + text[rend_pos + len(target_str):]
            print("5. REVMODE_ACTIVECOM updated.")

    # 6. REVMODE_SOURCE_CHECK に過熱度ソース補正＆体力軽減追加
    pos6 = text.find('BASE:0 -= LOSEBASE:0\nBASE:1 -= LOSEBASE:1')
    if pos6 != -1:
        # find preceding LOSEBASE section
        prev_idx = text.rfind(';体力・気力の減少', 0, pos6)
        if prev_idx != -1:
            old_lb = text[prev_idx:pos6 + len('BASE:0 -= LOSEBASE:0\nBASE:1 -= LOSEBASE:1')]
            new_lb = ''';過熱度に応じた快感ソースボーナス（熱中するほど濃厚に）
IF TFLAG:108 >= 3
\tFOR LCOUNT, 0, 5
\t\tTIMES SOURCE:LCOUNT, 1.60
\tNEXT
\tTIMES SOURCE:18, 1.50
ELSEIF TFLAG:108 == 2
\tFOR LCOUNT, 0, 5
\t\tTIMES SOURCE:LCOUNT, 1.35
\tNEXT
\tTIMES SOURCE:18, 1.30
ELSEIF TFLAG:108 == 1
\tFOR LCOUNT, 0, 5
\t\tTIMES SOURCE:LCOUNT, 1.15
\tNEXT
ENDIF

;体力・気力の減少
;パートナー主導の一手は、体力・気力・耐力の実消費量と表示をともに半額にする。
;さらに過熱状態中は夢中になって疲労を感じにくくなるよう持続支援
IF TFLAG:108 >= 2
\tLOSEBASE:0 = (LOSEBASE:0 + 2) / 3
\tLOSEBASE:1 = (LOSEBASE:1 + 2) / 3
ELSEIF TFLAG:543
\tLOSEBASE:0 = (LOSEBASE:0 + 1) / 2
\tLOSEBASE:1 = (LOSEBASE:1 + 1) / 2
\tDOWNBASE:MASTER:4 = (DOWNBASE:MASTER:4 + 1) / 2
ENDIF
BASE:0 -= LOSEBASE:0
BASE:1 -= LOSEBASE:1'''
            text = text[:prev_idx] + new_lb + text[prev_idx + len(old_lb):]
            print("6. REVMODE_SOURCE_CHECK updated.")

    # Save to file
    text_crlf = text.replace('\n', '\r\n')
    with open(target_path, 'wb') as f:
        f.write(text_crlf.encode('cp932'))
    print("Full updates saved successfully.")

if __name__ == '__main__':
    main()
