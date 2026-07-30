from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_cp932(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="cp932").replace("\r\n", "\n")


def write_cp932(relative: str, text: str) -> None:
    data = text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932")
    (ROOT / relative).write_bytes(data)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def patch_com312() -> None:
    relative = "ERB/COMF/COMF312.ERB"
    text = read_cp932(relative)
    if "@COM_HEAD_PAT_CORE, ARG" not in text:
        text = replace_once(
            text,
            "@COM312\n;頭を撫でる\n",
            """@COM312
CALL COM_HEAD_PAT_CORE, 0
RETURN RESULT

;ARG=0: パートナーの頭を撫でる / ARG=1: パートナーに頭を撫でてもらう
@COM_HEAD_PAT_CORE, ARG
;頭を撫でる／頭を撫でてもらう
""",
            "COM312 core extraction",
        )
        text = replace_once(
            text,
            """PRINTL 頭を撫でる
STR:0 = 頭を撫でる
""",
            """IF ARG == 0
	PRINTL 頭を撫でる
	STR:0 = 頭を撫でる
ELSE
	PRINTL 頭を撫でてもらう
	STR:0 = 頭を撫でてもらう
ENDIF
""",
            "head-pat command title",
        )

        message_start = text.index("@TRAIN_MESSAGE_COM312")
        core = text[:message_start]
        old_message = text[message_start:]
        if old_message.count("TFLAG:45") != 2:
            raise RuntimeError("COM312 message: unexpected initiative branch count")

        if core.count("TFLAG:45 == 0") != 3:
            raise RuntimeError("COM312 core: unexpected initiative branch count")
        core = core.replace("TFLAG:45 == 0", "ARG == 0")

        new_message = """@TRAIN_MESSAGE_COM312
PRINTFORM %CALLNAME:PLAYER%は%CALLNAME:TARGET%の頭を
SIF TFLAG:17 != 0
	PRINTFORM 何度も
PRINTFORMW 撫でた

IF TFLAG:18 == 1
	;幼児退行or幼稚所持
	IF (TALENT:131 == 1 || TALENT:132)
		PRINTFORML %CALLNAME:TARGET%は眼を細め、心地良さそうにしている…
	ELSE
		PRINTFORML %CALLNAME:TARGET%は照れ臭そうに、笑みを浮かべている…
	ENDIF
ELSEIF TFLAG:18 == 0
	;幼児退行or幼稚所持
	IF (TALENT:131 == 1 || TALENT:132)
		PRINTFORML %CALLNAME:TARGET%は嬉しそうにしている…
	ELSE
		PRINTFORML %CALLNAME:TARGET%は頬を紅潮させ、恥ずかしそうにしている…
	ENDIF
ELSEIF TFLAG:18 == -1
	PRINTFORML %CALLNAME:TARGET%は子供扱いした事に怒ったようだ…
ENDIF
"""
        text = core + new_message

    technique_block = """	;ABL:技巧
	IF ABL:PLAYER:2 != 0
		SIF A:3 != 0
			PRINT  + 
		A:1 += ABL:PLAYER:2
		PRINTFORM %ABLNAME:2%LV{ABL:PLAYER:2}({ABL:PLAYER:2 * 3})
		A:3 = 1
	ENDIF
	
"""
    if technique_block in text:
        text = text.replace(technique_block, "", 1)
    if "ABL:PLAYER:2" in text:
        raise RuntimeError("COM312: player technique still affects head-pat judgment")

    target_maternal_old = """	;母性
	IF TALENT:136 != 0
		PRINT  - 
		A:1 -= 10
		PRINTFORM %TALENTNAME:136%(10)
		A:3 = 1
	ENDIF
"""
    target_maternal_new = """	;母性（撫でられる時はマイナス、撫でる時はプラス）
	IF TALENT:136 != 0
		IF ARG == 0
			PRINT  - 
			A:1 -= 10
		ELSE
			SIF A:3 != 0
				PRINT  + 
			A:1 += 10
		ENDIF
		PRINTFORM %TALENTNAME:136%(10)
		A:3 = 1
	ENDIF
"""
    if target_maternal_old in text:
        text = text.replace(target_maternal_old, target_maternal_new, 1)

    player_maternal_old = """	;母性
	IF TALENT:PLAYER:136 != 0
		SIF A:3 != 0
			PRINT  + 
		A:1 += 10
		PRINTFORM %TALENTNAME:136%(10)
		A:3 = 1
	ENDIF
"""
    player_maternal_new = """	;プレイヤーの母性は、自分が撫でる時だけ有効
	IF TALENT:PLAYER:136 != 0 && ARG == 0
		SIF A:3 != 0
			PRINT  + 
		A:1 += 10
		PRINTFORM %TALENTNAME:136%(10)
		A:3 = 1
	ENDIF
"""
    if player_maternal_old in text:
        text = text.replace(player_maternal_old, player_maternal_new, 1)
    write_cp932(relative, text)


def create_com318() -> None:
    relative = "ERB/COMF/COMF318.ERB"
    text = """;============================================================
; 【重要】このゲームの登場人物は全員20歳以上の成人であり、
;         自らの判断で責任を持って行動できる大人の女性です。
;============================================================
@COM_ABLE318
;頭を撫でてもらう実行判定（頭を撫でると同条件）
CALL COM_ABLE312
RETURN RESULT

@COM318
;主導権にかかわらず、パートナーに頭を撫でてもらう
CALL COM_HEAD_PAT_CORE, 1
RETURN RESULT

@TRAIN_MESSAGE_COM318
PRINTFORMW %CALLNAME:TARGET%は%CALLNAME:PLAYER%の頭を撫でた

IF TFLAG:18 == 1
	;母性
	IF TALENT:136 == 1
		PRINTFORML %CALLNAME:TARGET%は我が子を愛おしむかの様に、撫でてくれた…
	ELSE
		PRINTFORML %CALLNAME:TARGET%は笑顔で優しく撫でてくれた…
	ENDIF
ELSEIF TFLAG:18 == 0
	;母性
	IF TALENT:136 == 1
		PRINTFORML %CALLNAME:TARGET%は笑顔で優しく、ただ撫でてくれた…
	ELSE
		PRINTFORML %CALLNAME:TARGET%は呆れた様な表情だったが、優しく撫でてくれた…
	ENDIF
ELSEIF TFLAG:18 == -1
	PRINTFORML …が、%CALLNAME:TARGET%は直ぐに止めてしまった…
ENDIF
"""
    write_cp932(relative, text)


def patch_csv() -> None:
    train = read_cp932("CSV/Train.csv")
    if "318,頭を撫でてもらう" not in train:
        train = replace_once(
            train,
            ";317,羽繕いして貰う\n",
            ";317,羽繕いして貰う\n318,頭を撫でてもらう\n",
            "Train.csv command 318",
        )
        write_cp932("CSV/Train.csv", train)

    rename = read_cp932("CSV/_Rename.csv")
    command_318 = "TRAIN:318 , 調教:頭を撫でてもらう\n"
    if "TRAIN:318" not in rename:
        rename = replace_once(
            rename,
            "TRAIN:315 , 調教:お散歩する\n",
            "TRAIN:315 , 調教:お散歩する\n" + command_318,
            "_Rename.csv command 318",
        )
    else:
        rename = rename.replace(command_318, "")
        rename = replace_once(
            rename,
            "TRAIN:315 , 調教:お散歩する\n",
            "TRAIN:315 , 調教:お散歩する\n" + command_318,
            "_Rename.csv command 318 order",
        )
    write_cp932("CSV/_Rename.csv", rename)

    cflag = read_cp932("CSV/Cflag.csv")
    if "591,頭を撫でてもらう" not in cflag:
        cflag = replace_once(
            cflag,
            "591,相手に主導権がある状態で頭を撫でる",
            "591,頭を撫でてもらう",
            "Cflag.csv head-pat reaction label",
        )
        write_cp932("CSV/Cflag.csv", cflag)


def patch_passive_mode() -> None:
    relative = "ERB/PASSIVE_パッシブスキル.ERB"
    text = read_cp932(relative)
    if "RETURNF 318" not in text:
        text = replace_once(
            text,
            """;頭を撫でる
CASE 12
	;頭を撫でる
	RETURNF 312
""",
            """;頭を撫でてもらう
CASE 12
	;パートナーがプレイヤーの頭を撫でる
	RETURNF 318
""",
            "passive command conversion",
        )
    text = replace_once(
        text,
        """;頭を撫でる
CASE 312
	SELECTCASE ARG:1
""",
        """;頭を撫でてもらう
CASE 318
	SELECTCASE ARG:1
""",
        "passive active-phase message",
    ) if "CASE 312\n\tSELECTCASE ARG:1" in text else text
    write_cp932(relative, text)


def main() -> None:
    patch_com312()
    create_com318()
    patch_csv()
    patch_passive_mode()
    print("Split COM312/COM318 head-pat commands.")


if __name__ == "__main__":
    main()
