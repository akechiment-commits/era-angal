from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DAILY_ORDER_COMMANDS = (303, 304, 305, 306, 307, 309, 316, 321, 323)
DAILY_SUCCESS_COMMANDS = (
    300,
    301,
    302,
    303,
    304,
    305,
    306,
    307,
    311,
    312,
    313,
    315,
    316,
    320,
    321,
    323,
)


def read_cp932(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="cp932").replace("\r\n", "\n")


def write_cp932(relative: str, text: str) -> None:
    data = text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932")
    (ROOT / relative).write_bytes(data)


def remove_once(text: str, block: str, label: str) -> str:
    count = text.count(block)
    if count == 0:
        return text
    if count != 1:
        raise RuntimeError(f"{label}: expected at most one match, found {count}")
    return text.replace(block, "", 1)


def add_daily_order_function() -> None:
    relative = "ERB/COMORDER_コマンド表示順制御.ERB"
    text = read_cp932(relative)
    if "@COM_ORDER_DAILY" not in text:
        marker = """;-------------------------------------------------
;すべての命令に共通の要素を考慮
;(従順が高いと命令に従いやすいなど)
;-------------------------------------------------
@COM_ORDER
"""
        daily_function = """;-------------------------------------------------
;日常・交流コマンド用の共通実行判定
;性的な能力・刻印・快感状態は使わず、人間関係と性格だけを見る
;-------------------------------------------------
@COM_ORDER_DAILY
;親密
IF ABL:0
	A += ABL:0 * 3
ENDIF

;相性
R = NO:PLAYER
IF RELATION:R > 0 && RELATION:R < 70
	A -= 5
ELSEIF RELATION:R > 0 && RELATION:R < 100
	A -= 2
ELSEIF RELATION:R >= 130 && RELATION:R < 170
	A += 3
ELSEIF RELATION:R >= 170
	A += 6
ENDIF

;日常の誘いに関係する性格
SIF TALENT:11
	A -= 5
SIF TALENT:13
	A += 5
SIF TALENT:15
	A -= 5
SIF TALENT:17
	A += 3

;実行判定を表示する設定
IF ((FLAG:23 & 1p27) == 0) && FLAG:2 != 1
	IF ABL:0
		SIF S
			PRINT  + 
		PRINTS ABLNAME:0
		PRINTV 'LV,ABL:0,'(,ABL:0 * 3,')
		S = 1
	ENDIF

	R = NO:PLAYER
	IF RELATION:R > 0 && RELATION:R < 70
		PRINT  - 
		PRINT 相性
		PRINTV '(,5,')
		S = 1
	ELSEIF RELATION:R > 0 && RELATION:R < 100
		PRINT  - 
		PRINT 相性
		PRINTV '(,2,')
		S = 1
	ELSEIF RELATION:R >= 130 && RELATION:R < 170
		SIF S
			PRINT  + 
		PRINT 相性
		PRINTV '(,3,')
		S = 1
	ELSEIF RELATION:R >= 170
		SIF S
			PRINT  + 
		PRINT 相性
		PRINTV '(,6,')
		S = 1
	ENDIF

	IF TALENT:11
		PRINT  - 
		PRINTS TALENTNAME:11
		PRINTV '(,5,')
		S = 1
	ENDIF
	IF TALENT:13
		SIF S
			PRINT  + 
		PRINTS TALENTNAME:13
		PRINTV '(,5,')
		S = 1
	ENDIF
	IF TALENT:15
		PRINT  - 
		PRINTS TALENTNAME:15
		PRINTV '(,5,')
		S = 1
	ENDIF
	IF TALENT:17
		SIF S
			PRINT  + 
		PRINTS TALENTNAME:17
		PRINTV '(,3,')
		S = 1
	ENDIF
ENDIF
RETURN 1

"""
        if text.count(marker) != 1:
            raise RuntimeError("COM_ORDER marker not found exactly once")
        text = text.replace(marker, daily_function + marker, 1)

    # 初版で入れていた旧「反発感情」は廃止済み要素なので日常判定にも使わない。
    text = text.replace(
        """;反発感情
IF MARK:3
	A -= MARK:3 * 2
ENDIF

""",
        "",
        1,
    )
    text = text.replace(
        """	IF MARK:3
		PRINT  - 
		PRINTS MARKNAME:3
		PRINTV 'LV,MARK:3,'(,MARK:3 * 2,')
		S = 1
	ENDIF
""",
        "",
        1,
    )
    write_cp932(relative, text)


def add_daily_success_function() -> None:
    relative = "ERB/COMORDER_コマンド表示順制御.ERB"
    text = read_cp932(relative)
    if "@GET_DAILY_SUCCESS_RATE" not in text:
        marker = """;-------------------------------------------------
;日常・交流コマンド用の共通実行判定
"""
        helper = """;-------------------------------------------------
;日常・交流コマンド用の成功率基準値
;性的なPALAM・素質は使わず、親密・好感度・相性・性格だけを見る
;-------------------------------------------------
@GET_DAILY_SUCCESS_RATE
;親密
A = ABL:0 * 5

;性格
SIF TALENT:11
	A -= 5
SIF TALENT:12
	A -= 3
SIF TALENT:13
	A += 5
SIF TALENT:15
	A -= 5
SIF TALENT:17
	A += 3
SIF TALENT:23
	A += 3

;男嫌い
SIF TALENT:82 && TALENT:PLAYER:122
	A -= 7

;プレイヤーの対人魅力
SIF TALENT:PLAYER:91
	A += 6
SIF TALENT:PLAYER:92
	A += 6

;相性
R = NO:PLAYER
IF RELATION:R > 0 && RELATION:R < 30
	A -= 10
ELSEIF RELATION:R > 0 && RELATION:R < 70
	A -= 6
ELSEIF RELATION:R > 0 && RELATION:R < 100
	A -= 3
ELSEIF RELATION:R >= 100 && RELATION:R < 130
	A += 3
ELSEIF RELATION:R >= 130 && RELATION:R < 170
	A += 6
ELSEIF RELATION:R >= 170
	A += 10
ENDIF

;好感度と関係
A += CFLAG:2 / 50
SIF TALENT:85
	A += 20
SIF TALENT:153
	A += 20
SIF TALENT:88
	A += 40

SIF A < 0
	A = 0
RETURN 1

"""
        if text.count(marker) != 1:
            raise RuntimeError("daily order marker not found exactly once")
        text = text.replace(marker, helper + marker, 1)
        write_cp932(relative, text)


def redirect_daily_success_calls() -> None:
    for command in DAILY_SUCCESS_COMMANDS:
        relative = f"ERB/COMF/COMF{command}.ERB"
        text = read_cp932(relative)
        if "CALL GET_SUCCESS_RATE" in text:
            text = text.replace(
                "CALL GET_SUCCESS_RATE", "CALL GET_DAILY_SUCCESS_RATE"
            )
            write_cp932(relative, text)
        if "CALL GET_SUCCESS_RATE" in read_cp932(relative):
            raise RuntimeError(f"COM{command}: generic success rate still present")


def redirect_daily_order_calls() -> None:
    for command in DAILY_ORDER_COMMANDS:
        relative = f"ERB/COMF/COMF{command}.ERB"
        text = read_cp932(relative)
        if "CALL COM_ORDER_DAILY" not in text:
            count = text.count("CALL COM_ORDER\n")
            if count != 1:
                raise RuntimeError(
                    f"COM{command}: expected one generic order call, found {count}"
                )
            text = text.replace("CALL COM_ORDER\n", "CALL COM_ORDER_DAILY\n", 1)
            write_cp932(relative, text)


def remove_obsolete_rebellion_from_daily_commands() -> None:
    relative = "ERB/COMF/COMF302.ERB"
    text = read_cp932(relative)
    text = text.replace(" && MARK:3 == 0", "", 1)
    write_cp932(relative, text)

    blocks = {
        312: (
            """	;反発感情
	IF MARK:3 != 0
		PRINT  - 
		A:1 -= MARK:3 * 6
		PRINTFORM %MARKNAME:3%LV{MARK:3}({MARK:3 * 6})
		A:3 = 1
	ENDIF
""",
            """;反発があると好感度低下
IF MARK:3 >= 3
	A:1 -= 3
ELSEIF MARK:3 >= 2
	A:1 -= 2
ELSEIF MARK:3 >= 1
	A:1 -= 1
ENDIF
""",
        ),
        313: (
            """;反発があると好感度低下
IF MARK:3 >= 3
	A:1 -= 3
ELSEIF MARK:3 >= 2
	A:1 -= 2
ELSEIF MARK:3 >= 1
	A:1 -= 1
ENDIF
""",
        ),
        315: (
            """	;反発感情
	IF MARK:3 != 0
		PRINT  - 
		A:1 -= MARK:3 * 6
		PRINTFORM %MARKNAME:3%LV{MARK:3}({MARK:3 * 6})
		A:3 = 1
	ENDIF
""",
            """;反発があると好感度低下
IF MARK:3 >= 3
	A:1 -= 3
ELSEIF MARK:3 == 2
	A:1 -= 2
ELSEIF MARK:3 == 1
	A:1 -= 1
ENDIF
""",
        ),
    }
    for command, command_blocks in blocks.items():
        relative = f"ERB/COMF/COMF{command}.ERB"
        text = read_cp932(relative)
        for block in command_blocks:
            text = remove_once(
                text, block, f"COM{command} obsolete rebellion judgment"
            )
        if "MARK:3" in text:
            raise RuntimeError(
                f"COM{command}: obsolete rebellion still affects daily command"
            )
        write_cp932(relative, text)

    relative = "ERB/COMF/COMF314.ERB"
    text = read_cp932(relative)
    text = text.replace(
        """	;反発感情が1以上
	ELSEIF MARK:3 > 0
		PRINTFORML %CALLNAME:TARGET%一人が炬燵でぬくぬくしてます…
	ELSE
""",
        """	ELSE
""",
        1,
    )
    text = text.replace(
        """	IF MARK:3 > 0
		PRINTFORMW %CALLNAME:TARGET%は一人で炬燵を占拠していた…
	;狭いし密着度アップさ
	ELSEIF TALENT:85 == 1 || TALENT:153 == 1
""",
        """	;狭いし密着度アップさ
	IF TALENT:85 == 1 || TALENT:153 == 1
""",
        1,
    )
    if "MARK:3" in text:
        raise RuntimeError("COM314: obsolete rebellion narration still present")
    write_cp932(relative, text)


def fix_street_live_judgments() -> None:
    relative = "ERB/COMF/COMF322.ERB"
    text = read_cp932(relative)

    availability = """;露出癖が1以下だとダメ。ただし持っている素質によって値が変動
A = 2
;臆病
SIF TALENT:10
	A += 2
;目立ちたがり
SIF TALENT:28
	A -= 1
;抑圧
SIF TALENT:32
	A += 1
;解放
SIF TALENT:33
	A -= 1
;恥じらい
SIF TALENT:35
	A += 2
;恥薄い
SIF TALENT:36
	A -= 1
;求められる露出癖が0～5以上となるように
SIF A < 0
	A = 0
SIF A > 5
	A = 5
SIF ABL:7 < A
	RETURN 0
"""
    text = remove_once(
        text, availability, "COM322 exhibitionism availability requirement"
    )

    start = text.index(";成功できるかの判定")
    end = text.index(";目標難易度を設定", start)
    success = """;成功できるかの判定
;歌唱技能・ライブ経験・舞台向きの性格で決まる
;欲望・露出癖・欲情・性的な刻印はライブの成否には使わない
;-------------------------------------------------
A = 0
S = 0

;ABL:歌唱技能
IF ABL:92
	IF ABL:92 <= 5
		A += ABL:92 * 5
	ELSEIF ABL:92 <= 10
		A += 30 + ABL:92 / 3
	ELSEIF ABL:92 <= 20
		A += 40 + ABL:92 / 6
	ELSE
		A += 50 + ABL:92 / 9
	ENDIF
ENDIF

;歌唱経験
A += MIN(EXP:93 / 5, 20)

;舞台での振る舞いに関係する性格・素質
SIF TALENT:10
	A -= 5
SIF TALENT:23
	A += 2
SIF TALENT:28
	A += 5
SIF TALENT:91
	A += 3
SIF TALENT:92
	A += 5
SIF TALENT:118
	A += 5
SIF TALENT:126
	A += 5

"""
    text = text[:start] + success + text[end:]

    judgment_area = text[: text.index("@STREET_LIVE_SUCCESS")]
    forbidden = ("ABL:1", "ABL:7", "MARK:", "PALAM:", "TALENT:20")
    for token in forbidden:
        if token in judgment_area:
            raise RuntimeError(
                f"COM322: unrelated factor remains in live judgment: {token}"
            )
    write_cp932(relative, text)


def main() -> None:
    relative = "ERB/COMF/COMF315.ERB"
    text = read_cp932(relative)

    # 散歩の親密版移行に、性的な手技である「技巧」は関係しない。
    text = remove_once(
        text,
        """	;ABL:技巧
	IF ABL:PLAYER:2 != 0
		SIF A:3 != 0
			PRINT  + 
		A:1 += ABL:PLAYER:2
		PRINTFORM %ABLNAME:2%LV{ABL:PLAYER:2}({ABL:PLAYER:2})
		A:3 = 1
	ENDIF
""",
        "COM315 player technique judgment",
    )

    # サド素質も、腕組み・相合傘へ進む判定には無関係。
    text = remove_once(
        text,
        """	;サド
	IF TALENT:PLAYER:83 != 0
		SIF A:3 != 0
			PRINT  + 
		A:1 += 5
		PRINTFORM %TALENTNAME:83%(5)
		A:3 = 1
	ENDIF
""",
        "COM315 player sadism judgment",
    )

    # 淫乱時の濡れ量がプレイヤー技巧で増えるのも散歩として不自然。
    # パートナー自身の欲望に置き換える。
    old_liquid = "		SOURCE:10 = 300 * ABL:PLAYER:2 * TFLAG:17"
    new_liquid = "		SOURCE:10 = 300 * (ABL:1 + 1) * TFLAG:17"
    if old_liquid in text:
        text = text.replace(old_liquid, new_liquid, 1)

    if "ABL:PLAYER:2" in text:
        raise RuntimeError("COM315: player technique still affects walking")
    if "TALENT:PLAYER:83" in text:
        raise RuntimeError("COM315: player sadism still affects walking")

    write_cp932(relative, text)
    add_daily_success_function()
    redirect_daily_success_calls()
    add_daily_order_function()
    redirect_daily_order_calls()
    remove_obsolete_rebellion_from_daily_commands()
    fix_street_live_judgments()
    print("Fixed unnatural daily-command judgment factors.")


if __name__ == "__main__":
    main()
