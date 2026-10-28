# -*- coding: utf-8 -*-
"""
リバースモードのUI表示位置・フロー・コマンド定義の不整合を解消するスクリプト。
1. CSV/Train.csv に 509,主導権を返してもらう を登録
2. ERB/COMF/COMF500.ERB に COM_ABLE509 と COM509 を実装
3. ERB/COMF/COMABLE.ERB にて COM509 を TFLAG:34 中に許可
4. ERB/INFO_情報表示.ERB 内のステータス途中の PASSIVEPHASE 呼び出しを削除
5. ERB/USERCOM_コマンド一覧表示.ERB の @SHOW_USERCOM 冒頭で、
   ステータス表示後に目立つバナーと地の文を描画し、選択肢を提示するように統合
"""

import sys

def main():
    # 1. Update CSV/Train.csv
    train_path = 'CSV/Train.csv'
    with open(train_path, 'rb') as f:
        t_raw = f.read().decode('cp932')
    t_text = t_raw.replace('\r\n', '\n')
    
    pos_508 = t_text.find('508,おねだり')
    if pos_508 != -1 and '509,主導権を返してもらう' not in t_text:
        t_text = t_text[:pos_508] + '508,おねだり\n509,主導権を返してもらう' + t_text[pos_508 + len('508,おねだり'):]
        with open(train_path, 'wb') as f:
            f.write(t_text.replace('\n', '\r\n').encode('cp932'))
        print("1. CSV/Train.csv updated with COM509.")
    else:
        print("1. CSV/Train.csv COM509 already exists or 508 not found.")

    # 2. Update ERB/COMF/COMF500.ERB
    comf500_path = 'ERB/COMF/COMF500.ERB'
    with open(comf500_path, 'rb') as f:
        c500_text = f.read().decode('cp932').replace('\r\n', '\n')

    if '@COM_ABLE509' not in c500_text:
        com509_code = '''

;-------------------------------------------------
;主導権を返してもらう(REVMODE)
;-------------------------------------------------
@COM_ABLE509
;実行判定
;COM_ABLE共通判定
CALL COM_ABLE_COMMON, SELECTCOM
SIF RESULT == 0
	RETURN 0
RETURN 1

@COM509
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
'''
        c500_text += com509_code
        with open(comf500_path, 'wb') as f:
            f.write(c500_text.replace('\n', '\r\n').encode('cp932'))
        print("2. ERB/COMF/COMF500.ERB updated with COM509.")
    else:
        print("2. COM509 already in COMF500.ERB.")

    # 3. Update ERB/COMF/COMABLE.ERB to allow COM509 during TFLAG:34
    comable_path = 'ERB/COMF/COMABLE.ERB'
    with open(comable_path, 'rb') as f:
        cable_text = f.read().decode('cp932').replace('\r\n', '\n')

    target_rev = 'IF TFLAG:34\n\tIF ARG >= 500 && ARG <= 510'
    new_rev = 'IF TFLAG:34\n\tIF ARG == 509\n\t\tRETURN 1\n\tELSEIF ARG >= 500 && ARG <= 510'
    if target_rev in cable_text:
        cable_text = cable_text.replace(target_rev, new_rev, 1)
        with open(comable_path, 'wb') as f:
            f.write(cable_text.replace('\n', '\r\n').encode('cp932'))
        print("3. ERB/COMF/COMABLE.ERB updated for COM509.")
    else:
        print("3. Target in COMABLE.ERB already updated or not found.")

    # 4. Remove mid-status PASSIVEPHASE call from ERB/INFO_情報表示.ERB
    info_path = 'ERB/INFO_情報表示.ERB'
    with open(info_path, 'rb') as f:
        info_text = f.read().decode('cp932').replace('\r\n', '\n')

    old_info_block = ''';完全にパートナーに主導権を握らせている場合
IF TFLAG:34
	;ウフフ中
	IF TFLAG:44
		;REVMODE
		CALL REVMODE_PASSIVEPHASE(TARGET)
	;非ウフフ中
	ELSE
		;パートナーのターン処理
		CALL PASSIVEMODE_PASSIVEPHASE(TARGET)
	ENDIF
ENDIF'''

    if old_info_block in info_text:
        info_text = info_text.replace(old_info_block, ';完全主導権時の行動呼び出しはステータス出力完了後のSHOW_USERCOM冒頭へ移動', 1)
        with open(info_path, 'wb') as f:
            f.write(info_text.replace('\n', '\r\n').encode('cp932'))
        print("4. ERB/INFO_情報表示.ERB mid-status call relocated.")
    else:
        print("4. Mid-status call in INFO_情報表示.ERB already moved or not found.")

    # 5. Place REVMODE PASSIVEPHASE and banner at SHOW_USERCOM in ERB/USERCOM_コマンド一覧表示.ERB
    usercom_path = 'ERB/USERCOM_コマンド一覧表示.ERB'
    with open(usercom_path, 'rb') as f:
        ucom_text = f.read().decode('cp932').replace('\r\n', '\n')

    target_ucom = '@SHOW_USERCOM\nVARSET Q, -1\nVARSET C, 0\n;CALLTRAINは表示しない\nSIF TFLAG:CALLTRAIN\n\tRETURN 0'
    new_ucom = '''@SHOW_USERCOM
VARSET Q, -1
VARSET C, 0
;CALLTRAINは表示しない
SIF TFLAG:CALLTRAIN
	RETURN 0

;完全にパートナーに主導権を握らせている場合：ステータス表示が完了した直後に相手の行動を描画
IF TFLAG:34
	DRAWLINE
	IF TFLAG:44
		PRINTFORM 【主導権完全委譲中】相手の熱中度:
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
		PRINTFORML  (連続:{TFLAG:109}ターン)
		;相手の行動を決定し、情熱的な地の文を出力
		CALL REVMODE_PASSIVEPHASE(TARGET)
	ELSE
		PRINTFORML 【主導権完全委譲中】（%CALLNAME:TARGET%が自由に主導権を握っています）
		CALL PASSIVEMODE_PASSIVEPHASE(TARGET)
	ENDIF
	DRAWLINE
ENDIF'''

    if target_ucom in ucom_text:
        ucom_text = ucom_text.replace(target_ucom, new_ucom, 1)
        with open(usercom_path, 'wb') as f:
            f.write(ucom_text.replace('\n', '\r\n').encode('cp932'))
        print("5. ERB/USERCOM_コマンド一覧表示.ERB SHOW_USERCOM updated.")
    else:
        print("5. Target in USERCOM_コマンド一覧表示.ERB not found.")

    print("All UI and flow fixes applied successfully.")

if __name__ == '__main__':
    main()
