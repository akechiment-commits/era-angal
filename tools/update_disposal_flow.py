# -*- coding: utf-8 -*-
import re

# 1. Update ERB/CASINO_UNDERGROUND_裏カジノ.ERB
with open('ERB/CASINO_UNDERGROUND_裏カジノ.ERB', 'r', encoding='cp932') as f:
    casino_text = f.read()

# Auto-heal negative debt at lobby start
if '; 借金負数・オーバーフローの自己修復' not in casino_text:
    casino_text = casino_text.replace(
        '@CASINO_UNDERGROUND_LOBBY\r\n#DIM VIP_CHIP\r\n',
        '@CASINO_UNDERGROUND_LOBBY\r\n#DIM VIP_CHIP\r\n\r\n; 借金負数・オーバーフローの自己修復\r\nIF CFLAG:MASTER:785 < 0\r\n\tCFLAG:MASTER:785 = 0\r\nENDIF\r\n'
    )
    print("Added negative debt self-heal to lobby.")

# Lobby option 4 calling UNDERGROUND_DISPOSAL_STAGE_EVENT
old_lobby_opt4 = r'''ELSEIF RESULT == 4 && (CFLAG:MASTER:785 > 0 || VIP_CHIP <= 0 || IS_UNDERGROUND_PARTNER_BROKEN(TARGET))
	IF IS_UNDERGROUND_PARTNER_BROKEN(TARGET)
		PRINTL 
		SETCOLOR 0x990000
		PRINTFORML 支配人「おや……？ このお嬢様は既に心身ともに限界まで壊れきっており、当カジノでの担保価値はございませんよ」
		PRINTFORML 支配人「それでも更なる破壊の余興として、廃棄処分ステージに差し出すとおっしゃるなら……喜んでお引き受けいたしましょう」
		PRINTFORML 支配人「ただし担保価値がございませんので、借金の帳消しにも救済チップの支給にも応じられません。それでもよろしいので？」
		RESETCOLOR
		PRINTL [0] ステージに差し出し、さらに破壊する
		PRINTL [1] 思いとどまる
		INPUT
		IF RESULT != 0
			GOTO UNDERGROUND_MENU
		ENDIF
	ENDIF
	CALL UNDERGROUND_BANKRUPTCY_EVENT, VIP_CHIP
	VIP_CHIP = RESULT
	GOTO UNDERGROUND_MENU'''

new_lobby_opt4 = r'''ELSEIF RESULT == 4 && (CFLAG:MASTER:785 > 0 || VIP_CHIP <= 0 || IS_UNDERGROUND_PARTNER_BROKEN(TARGET))
	IF IS_UNDERGROUND_PARTNER_BROKEN(TARGET)
		PRINTL 
		SETCOLOR 0x990000
		PRINTFORML 支配人「おや……？ このお嬢様は既に心身ともに限界まで壊れきっており、当カジノでの担保価値はございませんよ」
		PRINTFORML 支配人「それでも更なる破壊の余興として、廃棄処分ステージに差し出すとおっしゃるなら……喜んでお引き受けいたしましょう」
		PRINTFORML 支配人「ただし担保価値がございませんので、借金の帳消しにも救済チップの支給にも応じられません。それでもよろしいので？」
		RESETCOLOR
		PRINTL [0] ステージに差し出し、さらに破壊する
		PRINTL [1] 思いとどまる
		INPUT
		IF RESULT != 0
			GOTO UNDERGROUND_MENU
		ENDIF
		CALL UNDERGROUND_DISPOSAL_STAGE_EVENT, VIP_CHIP
		VIP_CHIP = RESULT
		GOTO UNDERGROUND_MENU
	ENDIF
	CALL UNDERGROUND_BANKRUPTCY_EVENT, VIP_CHIP
	VIP_CHIP = RESULT
	GOTO UNDERGROUND_MENU'''

# Normalize newlines for matching
old_opt4_crlf = old_lobby_opt4.replace('\n', '\r\n')
new_opt4_crlf = new_lobby_opt4.replace('\n', '\r\n')

if old_opt4_crlf in casino_text:
    casino_text = casino_text.replace(old_opt4_crlf, new_opt4_crlf)
    print("Updated lobby Option 4 handler.")
else:
    print("Warning: old_lobby_opt4 not found directly, checking regex...")

# Add @UNDERGROUND_DISPOSAL_STAGE_EVENT right before @UNDERGROUND_BANKRUPTCY_EVENT
disposal_event_code = r''';-------------------------------------------------
; 廃棄処分・生贄執行ステージイベント（壊れきったパートナー専用）
;-------------------------------------------------
@UNDERGROUND_DISPOSAL_STAGE_EVENT, ARG
DRAWLINE
SETCOLOR 0x990000
PRINTL ┌─────────────────────────────────┐
PRINTL │     ◆◆◆ 廃棄処分・生贄執行ステージ ◆◆◆     │
PRINTL └─────────────────────────────────┘
RESETCOLOR
PRINTL 
PRINTFORML %CALLNAME:MASTER%が合図を出すと、支配人は嗜虐的な笑みを深く刻んだ。
PRINTFORML 支配人「素晴らしいご決断です。壊れきったお嬢様がさらに徹底的に蹂躙され、壊れゆく様……観客たちも狂喜することでしょう」
PRINTFORML 支配人「黒服たち！ このお嬢様を廃棄処分ステージの壇上へお連れしなさい！」
PRINTL 
PRINTFORML 屈強な黒服の男たちが現れ、すでに抵抗する力もなくぐったりとした%CALLNAME:TARGET%を両脇から抱え上げる。
PRINTFORMW 虚ろな瞳の%CALLNAME:TARGET%は、歓声と欲望が渦巻く狂乱のステージの中央へと連行されていく……！

IF CFLAG:TARGET:786 >= 5
	TFLAG:110 = MAX(TFLAG:110, 5) + 1
ELSE
	TFLAG:110 += 1
ENDIF
CFLAG:TARGET:786 += 1
CALL UNDERGROUND_STAGE_PENALTY, TFLAG:110

PRINTL 
SETCOLOR 0xFF5555
PRINTFORML 支配人「ふふふ……観客は大いに狂喜いたしましたが、前述の通り担保価値のないお身体ですので借金の帳消しも救済チップの支給もございません」
PRINTFORMW 既に限界まで壊れきったパートナーのため、借金（${CFLAG:MASTER:785}）は帳消しにならず、救済チップも支払われませんでした。
RESETCOLOR
PRINTL 
PRINTFORMW %CALLNAME:MASTER%は限界を超えてさらに徹底的に破壊され、動かない人形のようになった%CALLNAME:TARGET%を抱き起こした……
RETURN ARG

'''
disposal_event_code_crlf = disposal_event_code.replace('\n', '\r\n')

if '@UNDERGROUND_DISPOSAL_STAGE_EVENT' not in casino_text:
    target_pos = casino_text.find(';-------------------------------------------------\r\n; 支配人の強制取り立て・破産宣告イベント\r\n@UNDERGROUND_BANKRUPTCY_EVENT')
    if target_pos != -1:
        casino_text = casino_text[:target_pos] + disposal_event_code_crlf + casino_text[target_pos:]
        print("Inserted @UNDERGROUND_DISPOSAL_STAGE_EVENT.")
    else:
        # Fallback find
        target_pos = casino_text.find('@UNDERGROUND_BANKRUPTCY_EVENT')
        casino_text = casino_text[:target_pos] + disposal_event_code_crlf + casino_text[target_pos:]
        print("Inserted @UNDERGROUND_DISPOSAL_STAGE_EVENT (fallback).")

# Update UNDERGROUND_BANKRUPTCY_EVENT to not prompt if WAS_BROKEN
old_bank_prompt = r'''PRINTL [0] パートナーを担保としてステージに差し出す
PRINTL [1] 必死に土下座して許しを乞う
INPUT
IF RESULT == 1
	PRINTFORML %CALLNAME:MASTER%は床に頭を擦り付け、どうかそれだけはと必死に哀願した……
	PRINTFORML 支配人は冷酷な笑みを浮かべ、見下すように靴の先で%CALLNAME:MASTER%の顎を持ち上げる。
	PRINTFORML 支配人「それだけは困りますね。ですが……客席にステージで歓声を上げていただければ、救済チップをお渡しする用意もございますがね」
	PRINTFORMW 屈強な黒服たちが%CALLNAME:TARGET%を取り押さえ、ステージへと引きずり込んでいく……！
ELSE
	PRINTFORML %CALLNAME:MASTER%は震える手でサインをし、%CALLNAME:TARGET%の身柄を支配人へと引き渡した……
	PRINTFORMW 屈強な黒服に両腕を掴まれ、%CALLNAME:TARGET%はステージへと連行されていく……！
ENDIF'''

new_bank_prompt = r'''IF WAS_BROKEN
	PRINTFORML すでに心身ともに限界まで壊れきった%CALLNAME:TARGET%に、もはや抗う力は残されていない……
	PRINTFORMW 黒服の男たちに無造作に抱え上げられ、%CALLNAME:TARGET%は狂乱のステージへと連行されていく……！
ELSE
	PRINTL [0] パートナーを担保としてステージに差し出す
	PRINTL [1] 必死に土下座して許しを乞う
	INPUT
	IF RESULT == 1
		PRINTFORML %CALLNAME:MASTER%は床に頭を擦り付け、どうかそれだけはと必死に哀願した……
		PRINTFORML 支配人は冷酷な笑みを浮かべ、見下すように靴の先で%CALLNAME:MASTER%の顎を持ち上げる。
		PRINTFORML 支配人「それだけは困りますね。ですが……客席にステージで歓声を上げていただければ、救済チップをお渡しする用意もございますがね」
		PRINTFORMW 屈強な黒服たちが%CALLNAME:TARGET%を取り押さえ、ステージへと引きずり込んでいく……！
	ELSE
		PRINTFORML %CALLNAME:MASTER%は震える手でサインをし、%CALLNAME:TARGET%の身柄を支配人へと引き渡した……
		PRINTFORMW 屈強な黒服に両腕を掴まれ、%CALLNAME:TARGET%はステージへと連行されていく……！
	ENDIF
ENDIF'''

old_bank_prompt_crlf = old_bank_prompt.replace('\n', '\r\n')
new_bank_prompt_crlf = new_bank_prompt.replace('\n', '\r\n')

if old_bank_prompt_crlf in casino_text:
    casino_text = casino_text.replace(old_bank_prompt_crlf, new_bank_prompt_crlf)
    print("Updated UNDERGROUND_BANKRUPTCY_EVENT prompt branching.")
else:
    print("Warning: old_bank_prompt not found in casino_text.")

with open('ERB/CASINO_UNDERGROUND_裏カジノ.ERB', 'w', encoding='cp932', newline='\r\n') as f:
    f.write(casino_text)
print("Saved ERB/CASINO_UNDERGROUND_裏カジノ.ERB")

# 2. Update ERB/SYSTEM_基本システム処理.ERB for interest overflow safety
with open('ERB/SYSTEM_基本システム処理.ERB', 'r', encoding='cp932') as f:
    sys_text = f.read()

old_interest = r'''IF CFLAG:MASTER:785 > 0 && DAY % 10 == 0
	LOCAL:5 = MAX(1, CFLAG:MASTER:785 / 2)
	CFLAG:MASTER:785 += LOCAL:5
	SETCOLOR 0xFF5555
	PRINTFORML カジノ借金に利息50％が加算されました。（借金総額：${CFLAG:MASTER:785}）
	RESETCOLOR
ENDIF'''

new_interest = r'''IF CFLAG:MASTER:785 > 0 && DAY % 10 == 0
	LOCAL:5 = MAX(1, CFLAG:MASTER:785 / 2)
	IF CFLAG:MASTER:785 > 100000000000000
		CFLAG:MASTER:785 = 100000000000000
	ELSE
		CFLAG:MASTER:785 += LOCAL:5
	ENDIF
	SETCOLOR 0xFF5555
	PRINTFORML カジノ借金に利息50％が加算されました。（借金総額：${CFLAG:MASTER:785}）
	RESETCOLOR
ELSEIF CFLAG:MASTER:785 < 0
	CFLAG:MASTER:785 = 0
ENDIF'''

old_interest_crlf = old_interest.replace('\n', '\r\n')
new_interest_crlf = new_interest.replace('\n', '\r\n')

if old_interest_crlf in sys_text:
    sys_text = sys_text.replace(old_interest_crlf, new_interest_crlf)
    with open('ERB/SYSTEM_基本システム処理.ERB', 'w', encoding='cp932', newline='\r\n') as f:
        f.write(sys_text)
    print("Updated interest overflow safety in ERB/SYSTEM_基本システム処理.ERB")
else:
    print("Warning: old_interest not found in sys_text.")
