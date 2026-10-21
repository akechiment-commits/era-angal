# -*- coding: utf-8 -*-
import sys

# 1. Update ERB/SHOP_ITEM_ショップアイテム定義.ERB
target_erb = 'ERB/SHOP_ITEM_ショップアイテム定義.ERB'
with open(target_erb, 'r', encoding='cp932', errors='strict') as f:
    erb_content = f.read()

# Part A: ITEMSALES 86, 87
old_part_a = """;赤い首輪（奴隷エンド条件はここで処理）
ITEMSALES:86 = 0
IF TARGET > 0 && ASSI < 0 && FLAG:5 != 9 && ITEM:85 == 0 && ITEM:86 == 0
	SIF TALENT:76 && TALENT:85 && TALENT:89 == 0 && TALENT:180 == 0 && CFLAG:2 >= 2500 && MARK:2 >= 3 && MARK:3 == 0 && (ABL:0+ABL:1+ABL:6 >= 15) && (ABL:2+ABL:8+ABL:11 >= 13) && (EXP:0+EXP:1 >= 200) && EXP:11 >= 150 && EXP:22 >= 150 && EXP:40 < 500
		ITEMSALES:86 = 1
ENDIF

;隷属の証
ITEMSALES:87 = 0
IF TARGET > 0 && ASSI < 0 && FLAG:1 < 9
	IF TALENT:MASTER:122 && EXP:40 >= 1500
		ITEMSALES:87 = 0
	ELSEIF TALENT:76 && TALENT:85 && TALENT:89 == 0 && TALENT:180 == 0 && MARK:2 >= 3 && MARK:3 == 0 && (ABL:0+ABL:1 >= 8) && (ABL:2+ABL:6 >= 7) && (ABL:8 >= 2 && ABL:10 >= 2 && ABL:11 >= 2) && (EXP:0+EXP:1 >= 100) && EXP:11 >= 50 && EXP:22 >= 50
		ITEMSALES:87 = 1
	ENDIF
ENDIF"""

new_part_a = """;赤い首輪（オミット：購入不可）
ITEMSALES:86 = 0
;IF TARGET > 0 && ASSI < 0 && FLAG:5 != 9 && ITEM:85 == 0 && ITEM:86 == 0
;	SIF TALENT:76 && TALENT:85 && TALENT:89 == 0 && TALENT:180 == 0 && CFLAG:2 >= 2500 && MARK:2 >= 3 && MARK:3 == 0 && (ABL:0+ABL:1+ABL:6 >= 15) && (ABL:2+ABL:8+ABL:11 >= 13) && (EXP:0+EXP:1 >= 200) && EXP:11 >= 150 && EXP:22 >= 150 && EXP:40 < 500
;		ITEMSALES:86 = 1
;ENDIF

;隷属の証（オミット：購入不可）
ITEMSALES:87 = 0
;IF TARGET > 0 && ASSI < 0 && FLAG:1 < 9
;	IF TALENT:MASTER:122 && EXP:40 >= 1500
;		ITEMSALES:87 = 0
;	ELSEIF TALENT:76 && TALENT:85 && TALENT:89 == 0 && TALENT:180 == 0 && MARK:2 >= 3 && MARK:3 == 0 && (ABL:0+ABL:1 >= 8) && (ABL:2+ABL:6 >= 7) && (ABL:8 >= 2 && ABL:10 >= 2 && ABL:11 >= 2) && (EXP:0+EXP:1 >= 100) && EXP:11 >= 50 && EXP:22 >= 50
;		ITEMSALES:87 = 1
;	ENDIF
;ENDIF"""

# Part B: Descriptions
old_part_b = """SIF BOUGHT == 86
	PRINTL 最高の妻にして奴隷である証を与えます
SIF BOUGHT == 87
	PRINTL 烙印を押して自分の妾にします"""

new_part_b = """;SIF BOUGHT == 86
;	PRINTL 最高の妻にして奴隷である証を与えます
;SIF BOUGHT == 87
;	PRINTL 烙印を押して自分の妾にします"""

# Part C: Who to use
old_part_c = """IF BOUGHT == 86 || BOUGHT == 87
	PRINTL 誰に与えますか？
ELSE
	PRINTL 誰に使いますか？
ENDIF"""

new_part_c = """;IF BOUGHT == 86 || BOUGHT == 87
;	PRINTL 誰に与えますか？
;ELSE
	PRINTL 誰に使いますか？
;ENDIF"""

# Part D: Target filter
old_part_d = """	SIF BOUGHT == 86 && COUNT != TARGET
		CONTINUE
	SIF BOUGHT == 87 && COUNT != TARGET
		CONTINUE"""

new_part_d = """;	SIF BOUGHT == 86 && COUNT != TARGET
;		CONTINUE
;	SIF BOUGHT == 87 && COUNT != TARGET
;		CONTINUE"""

# Part E: Item use (86 and 87)
old_part_e = """;奴隷エンド
IF BOUGHT == 86
	PRINTFORMW %NAME:MASTER%は%NAME:TARGET%の体を引き寄せると、その首に赤い首輪をかけてやった
	TFLAG:13 = 14
	CALL SELF_KOJO
	PRINTFORML %NAME:TARGET%は呆けたような表情を浮かべたものの、我に帰ると%NAME:MASTER%にしなだれかかり
	PRINTFORMW とろんとした瞳で見上げて服従の誓いを述べた
	PRINTFORM %NAME:TARGET%の名前が刻印されたネームプレートが
	IF TIME == 0
		PRINT 夕陽を受けて
	ELSE
		PRINT 月の光を受けて
	ENDIF
	PRINTW きらりと光っている……
	PRINTL  
	;一線越えない消滅
	IF TALENT:27
		PRINTFORMW %NAME:TARGET%は[%TALENTNAME:27%]を失った
		TALENT:27 = 0
	ENDIF
	;貞操観念消滅
	IF TALENT:30
		PRINTFORMW %NAME:TARGET%は[%TALENTNAME:30%]を失った
		TALENT:30 = 0
	ENDIF
	PRINTFORMW %NAME:MASTER%はしなだれかかっている%NAME:TARGET%の頭を長い間撫でながら
	PRINTFORMW 空を見上げ、今後の調教に思いを馳せていった……
	PRINTL  
	;服従取得
	IF TALENT:180 == 0
		PRINTFORMW %NAME:TARGET%は[%TALENTNAME:180%]を得た
		TALENT:180 = 1
	ENDIF
	;隷属取得
	IF TALENT:182 == 0
		PRINTFORMW %NAME:TARGET%は[%TALENTNAME:182%]を得た
		TALENT:182 = 1
	ENDIF
	;売却不可フラグ(首輪売却を不可にしたい場合は“;”を外してください)
;	CFLAG:7 = 1
	WAIT
	IF FLAG:1 == 9
		;FLAG:1が9のときは特殊ハーレムエンドへ。
		;“IF FLAG:1 == 9”を奴隷エンドと分けることは可能
		;烙印9＋赤い首輪のハーレムエンドはIF ITEM:86で仕分けすればいけるか？
		CALL SLAVE_ENDING
	ELSE
		CALL SINGLE_ENDING
	ENDIF

;	IF FLAG:5 != 9
;		PRINTFORMW ―――奴隷エンド条件達成―――
;		PRINTFORMW …………
;		PRINTFORMW ………
;		PRINTFORMW ……
;		CALL GAME_CONTINUE
;	ENDIF
ENDIF

;烙印
IF BOUGHT == 87
	ITEM:87 = 0
	PRINTFORMW ※注意！　%NAME:TARGET%に烙印を押すと二度と別れられなくなります。
	PRINTW それでもいいですか？
	DRAWLINE
	PRINTFORML [0] - %NAME:TARGET%に烙印を押す
	PRINTL [100] - やめる
	DRAWLINE
	$INPUT_LOOP_RAKUIN
	INPUT
	IF RESULT == 100
		MONEY += 100000
		RETURN 0
	ELSEIF RESULT == 0
		PRINTFORMW %NAME:MASTER%は%NAME:TARGET%に烙印を押した
		;TFLAG:13 = 14を奴隷エンド口上、TFLAG:13 = 15を烙印が押された時の口上とする
		TFLAG:13 = 15
		CALL SELF_KOJO
		FLAG:1 += 1
		PRINTFORMW %NAME:TARGET%は%NAME:MASTER%の所有物となったことに
		PRINTFORMW この上ない悦びを感じているようだ……
		;一線越えない消滅
		IF TALENT:27
			PRINTFORMW %NAME:TARGET%は[%TALENTNAME:27%]を失った
			TALENT:27 = 0
		ENDIF
		PRINTFORMW %NAME:MASTER%は%NAME:TARGET%の躰に刻まれた烙印を指先で撫で、
		PRINTFORMW %NAME:TARGET%の従属心を煽りたてた
		PRINTL  
		;服従取得
		IF TALENT:180 == 0
			PRINTFORMW %NAME:TARGET%は[%TALENTNAME:180%]を得た
			TALENT:180 = 1
		ENDIF
		;烙印取得
		IF TALENT:181 == 0
			PRINTFORMW %NAME:TARGET%は[%TALENTNAME:181%]を得た
			TALENT:181 = 1
		ENDIF
		;売却不可フラグ
		CFLAG:7 = 1
		PRINTFORMW ―――%NAME:TARGET%は身も心も%NAME:MASTER%の支配下になりました―――
		PRINTFORMW …………
		PRINTFORMW ………
		PRINTFORMW ……
;		IF FLAG:1 < 9
;			PRINTFORMW ＜購入できる%ITEMNAME:87%は残り{9-FLAG:1}個です＞
;		ELSE
;			PRINTFORMW ＜%ITEMNAME:87%は売り切れました＞
;		ENDIF
		PRINTFORMW ＜%NAME:TARGET%と別れられなくなりました＞
		WAIT
	ELSE
		PRINTFORML 正しい値を入力してください
		GOTO INPUT_LOOP_RAKUIN
	ENDIF
ENDIF"""

new_part_e = """;奴隷エンド（オミット：取得不可）
;IF BOUGHT == 86
;	PRINTFORMW %NAME:MASTER%は%NAME:TARGET%の体を引き寄せると、その首に赤い首輪をかけてやった
;	TFLAG:13 = 14
;	CALL SELF_KOJO
;	PRINTFORML %NAME:TARGET%は呆けたような表情を浮かべたものの、我に帰ると%NAME:MASTER%にしなだれかかり
;	PRINTFORMW とろんとした瞳で見上げて服従の誓いを述べた
;	PRINTFORM %NAME:TARGET%の名前が刻印されたネームプレートが
;	IF TIME == 0
;		PRINT 夕陽を受けて
;	ELSE
;		PRINT 月の光を受けて
;	ENDIF
;	PRINTW きらりと光っている……
;	PRINTL  
;	;一線越えない消滅
;	IF TALENT:27
;		PRINTFORMW %NAME:TARGET%は[%TALENTNAME:27%]を失った
;		TALENT:27 = 0
;	ENDIF
;	;貞操観念消滅
;	IF TALENT:30
;		PRINTFORMW %NAME:TARGET%は[%TALENTNAME:30%]を失った
;		TALENT:30 = 0
;	ENDIF
;	PRINTFORMW %NAME:MASTER%はしなだれかかっている%NAME:TARGET%の頭を長い間撫でながら
;	PRINTFORMW 空を見上げ、今後の調教に思いを馳せていった……
;	PRINTL  
;	;服従取得
;	IF TALENT:180 == 0
;		PRINTFORMW %NAME:TARGET%は[%TALENTNAME:180%]を得た
;		TALENT:180 = 1
;	ENDIF
;	;隷属取得
;	IF TALENT:182 == 0
;		PRINTFORMW %NAME:TARGET%は[%TALENTNAME:182%]を得た
;		TALENT:182 = 1
;	ENDIF
;	;売却不可フラグ(首輪売却を不可にしたい場合は“;”を外してください)
;;	CFLAG:7 = 1
;	WAIT
;	IF FLAG:1 == 9
;		;FLAG:1が9のときは特殊ハーレムエンドへ。
;		;“IF FLAG:1 == 9”を奴隷エンドと分けることは可能
;		;烙印9＋赤い首輪のハーレムエンドはIF ITEM:86で仕分けすればいけるか？
;		CALL SLAVE_ENDING
;	ELSE
;		CALL SINGLE_ENDING
;	ENDIF
;ENDIF

;烙印（オミット：取得不可）
;IF BOUGHT == 87
;	ITEM:87 = 0
;	PRINTFORMW ※注意！　%NAME:TARGET%に烙印を押すと二度と別れられなくなります。
;	PRINTW それでもいいですか？
;	DRAWLINE
;	PRINTFORML [0] - %NAME:TARGET%に烙印を押す
;	PRINTL [100] - やめる
;	DRAWLINE
;	$INPUT_LOOP_RAKUIN
;	INPUT
;	IF RESULT == 100
;		MONEY += 100000
;		RETURN 0
;	ELSEIF RESULT == 0
;		PRINTFORMW %NAME:MASTER%は%NAME:TARGET%に烙印を押した
;		;TFLAG:13 = 14を奴隷エンド口上、TFLAG:13 = 15を烙印が押された時の口上とする
;		TFLAG:13 = 15
;		CALL SELF_KOJO
;		FLAG:1 += 1
;		PRINTFORMW %NAME:TARGET%は%NAME:MASTER%の所有物となったことに
;		PRINTFORMW この上ない悦びを感じているようだ……
;		;一線越えない消滅
;		IF TALENT:27
;			PRINTFORMW %NAME:TARGET%は[%TALENTNAME:27%]を失った
;			TALENT:27 = 0
;		ENDIF
;		PRINTFORMW %NAME:MASTER%は%NAME:TARGET%の躰に刻まれた烙印を指先で撫で、
;		PRINTFORMW %NAME:TARGET%の従属心を煽りたてた
;		PRINTL  
;		;服従取得
;		IF TALENT:180 == 0
;			PRINTFORMW %NAME:TARGET%は[%TALENTNAME:180%]を得た
;			TALENT:180 = 1
;		ENDIF
;		;烙印取得
;		IF TALENT:181 == 0
;			PRINTFORMW %NAME:TARGET%は[%TALENTNAME:181%]を得た
;			TALENT:181 = 1
;		ENDIF
;		;売却不可フラグ
;		CFLAG:7 = 1
;		PRINTFORMW ―――%NAME:TARGET%は身も心も%NAME:MASTER%の支配下になりました―――
;		PRINTFORMW …………
;		PRINTFORMW ………
;		PRINTFORMW ……
;		PRINTFORMW ＜%NAME:TARGET%と別れられなくなりました＞
;		WAIT
;	ELSE
;		PRINTFORML 正しい値を入力してください
;		GOTO INPUT_LOOP_RAKUIN
;	ENDIF
;ENDIF"""

# Normalize line endings to test match
def replace_chunk(content, old, new):
    old_crlf = old.replace('\r\n', '\n').replace('\n', '\r\n')
    new_crlf = new.replace('\r\n', '\n').replace('\n', '\r\n')
    if old_crlf in content:
        return content.replace(old_crlf, new_crlf, 1)
    old_lf = old.replace('\r\n', '\n')
    new_lf = new.replace('\r\n', '\n')
    if old_lf in content:
        return content.replace(old_lf, new_lf, 1)
    raise ValueError("Target chunk not found in content!")

try:
    c = replace_chunk(erb_content, old_part_a, new_part_a)
    c = replace_chunk(c, old_part_b, new_part_b)
    c = replace_chunk(c, old_part_c, new_part_c)
    c = replace_chunk(c, old_part_d, new_part_d)
    c = replace_chunk(c, old_part_e, new_part_e)
    # Ensure CRLF
    c = c.replace('\r\n', '\n').replace('\n', '\r\n')
    with open(target_erb, 'wb') as f:
        f.write(c.encode('cp932'))
    print("Successfully updated ERB/SHOP_ITEM_ショップアイテム定義.ERB")
except Exception as e:
    print(f"Failed to update ERB: {e}")
    sys.exit(1)

# 2. Update CSV/Item.csv
with open('CSV/Item.csv', 'r', encoding='cp932') as f:
    item_lines = f.readlines()

new_item_lines = []
for line in item_lines:
    if line.startswith('86,赤い首輪') or line.startswith('87,隷属の証'):
        new_item_lines.append(';' + line)
    else:
        new_item_lines.append(line)

with open('CSV/Item.csv', 'wb') as f:
    f.write(''.join(new_item_lines).replace('\r\n', '\n').replace('\n', '\r\n').encode('cp932'))
print("Successfully updated CSV/Item.csv")

# 3. Update CSV/Talent.csv
with open('CSV/Talent.csv', 'r', encoding='cp932') as f:
    talent_lines = f.readlines()

new_talent_lines = []
for line in talent_lines:
    if line.startswith('181,烙印') or line.startswith('182,隷属'):
        new_talent_lines.append(';' + line)
    else:
        new_talent_lines.append(line)

with open('CSV/Talent.csv', 'wb') as f:
    f.write(''.join(new_talent_lines).replace('\r\n', '\n').replace('\n', '\r\n').encode('cp932'))
print("Successfully updated CSV/Talent.csv")
