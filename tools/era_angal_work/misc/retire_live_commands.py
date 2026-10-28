from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_cp932(relative: str) -> str:
    return (ROOT / relative).read_bytes().decode("cp932").replace("\r\n", "\n")


def write_cp932(relative: str, text: str) -> None:
    data = text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932")
    (ROOT / relative).write_bytes(data)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count == 0:
        if new in text:
            return text
        raise RuntimeError(f"{label}: source block not found")
    if count != 1:
        raise RuntimeError(f"{label}: expected one source block, found {count}")
    return text.replace(old, new, 1)


def retire_train_command() -> None:
    relative = "CSV/Train.csv"
    text = read_cp932(relative)
    lines = text.splitlines()
    target = ";322,ストリートライブ,;廃止（互換性維持のため番号は予約）"
    found = False
    for index, line in enumerate(lines):
        if line.lstrip(";").startswith("322,ストリートライブ,"):
            lines[index] = target
            found = True
    if not found:
        raise RuntimeError("Train COM322: mapping not found")
    text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    write_cp932(relative, text)

    relative = "CSV/_Rename.csv"
    text = read_cp932(relative)
    lines = text.splitlines()
    target = ";TRAIN:322 , 調教:ストリートライブ（廃止）"
    found = False
    for index, line in enumerate(lines):
        if line.lstrip(";").startswith("TRAIN:322 , 調教:ストリートライブ"):
            lines[index] = target
            found = True
    if not found:
        raise RuntimeError("Rename COM322: mapping not found")
    text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")
    write_cp932(relative, text)

    relative = "ERB/COMF/COMF322.ERB"
    text = read_cp932(relative)
    start = text.index("@COM_ABLE322")
    end = text.index("@COM322", start)
    disabled = """@COM_ABLE322
;廃止済み。旧セーブ・旧参照との互換性維持のため関数本体は残す。
RETURN 0


"""
    text = text[:start] + disabled + text[end:]
    write_cp932(relative, text)


def retire_shop_concert() -> None:
    relative = "ERB/SHOP_ショップ.ERB"
    text = read_cp932(relative)
    menu_block = """	ELSEIF COUNT == 21 && TARGET > 0 && ITEM:45 > 0 && TFLAG:79 == 0 && ABL:7 >= 4 && (TALENT:85 || ABL:0 >= 5)
		LOCALS '= @"[130] - 野外ライブを開く"
		PRINTFORM %LOCALS,28,LEFT%
"""
    text = replace_once(text, menu_block, "", "shop live menu")
    text = text.replace(" || RESULT == 130", "", 1)
    handler = """ELSEIF RESULT == 130
	IF TARGET > 0
		IF ITEM:45 > 0 && TFLAG:79 == 0 && ABL:7 >= 4 && (TALENT:85 || ABL:0 >= 5)
			CALL CONCERT
			RETURN 1
		ENDIF
	ELSE
		RETURN 0
	ENDIF
"""
    retired_handler = """ELSEIF RESULT == 130
	;廃止済み番号を直接入力された場合の互換ガード
	PRINTFORMW 野外ライブは廃止されました。
	RETURN 0
"""
    text = replace_once(
        text, handler, retired_handler, "shop live result handler"
    )
    if "CALL CONCERT" in text or "[130] - 野外ライブを開く" in text:
        raise RuntimeError("shop live entry point still present")
    write_cp932(relative, text)


def update_microphone_description() -> None:
    relative = "CSV/Item.csv"
    text = read_cp932(relative)
    text = replace_once(
        text,
        "45,マイク,40000,;野外ライブを開くことができる",
        "45,マイク,40000,;調合「フラワーロック」の歌唱経験獲得量が増える",
        "microphone description",
    )
    write_cp932(relative, text)


def add_culture_festival_singing_bonus() -> None:
    relative = "ERB/SCHOOL_EVENT_体育祭・文化祭.ERB"
    text = read_cp932(relative)
    text = text.replace(
        "PRINTFORML 表現技能と表現素質が高いほど観客の反応がよくなる。",
        "PRINTFORML 表現技能・表現素質に加え、歌唱技能と歌唱経験もステージの評価に影響する。",
        1,
    )
    score_block = """;アイドルの素質補正
IF TALENT:MASTER:223
	LOCAL:0 += 25
	PRINTFORML ★あなたのアイドルオーラがステージを輝かせた！
ENDIF
IF TALENT:TARGET:223
	LOCAL:1 += 15
	PRINTFORML ★%CALLNAME:TARGET%のアイドルオーラが観客を魅了した！
ENDIF
LOCAL:2 = LOCAL:0 + LOCAL:1
"""
    score_with_singing = """;アイドルの素質補正
IF TALENT:MASTER:223
	LOCAL:0 += 25
	PRINTFORML ★あなたのアイドルオーラがステージを輝かせた！
ENDIF
IF TALENT:TARGET:223
	LOCAL:1 += 15
	PRINTFORML ★%CALLNAME:TARGET%のアイドルオーラが観客を魅了した！
ENDIF

;歌唱技能・歌唱経験によるステージボーナス
CALL GET_CULTURE_SINGING_BONUS, MASTER
LOCAL:7 = RESULT
IF LOCAL:7 > 0
	LOCAL:0 += LOCAL:7
	PRINTFORML ★あなたの歌唱力が文化祭ステージを盛り上げた！　歌唱ボーナス+{LOCAL:7}
ENDIF
CALL GET_CULTURE_SINGING_BONUS, TARGET
LOCAL:8 = RESULT
IF LOCAL:8 > 0
	LOCAL:1 += LOCAL:8
	PRINTFORML ★%CALLNAME:TARGET%の歌唱力が観客を惹きつけた！　歌唱ボーナス+{LOCAL:8}
ENDIF
LOCAL:2 = LOCAL:0 + LOCAL:1
"""
    text = replace_once(
        text, score_block, score_with_singing, "culture festival singing score"
    )

    marker = """;---------------------------------------------------------
;文化祭
;---------------------------------------------------------
@CULTURE_FESTIVAL
"""
    helper_body = """;---------------------------------------------------------
;文化祭の歌唱ボーナス
;ARG = 対象キャラ。歌唱技能は最大20点、歌唱経験は最大20点。
;カラオケや歌の練習で得た経験が、年1回の文化祭で実利に繋がる。
;---------------------------------------------------------
@GET_CULTURE_SINGING_BONUS, ARG
LOCAL = MIN(ABL:ARG:92 / 2, 20)

IF EXP:ARG:93 >= EXPLV:5
	LOCAL += 20
ELSEIF EXP:ARG:93 >= EXPLV:4
	LOCAL += 15
ELSEIF EXP:ARG:93 >= EXPLV:3
	LOCAL += 10
ELSEIF EXP:ARG:93 >= EXPLV:2
	LOCAL += 6
ELSEIF EXP:ARG:93 >= EXPLV:1
	LOCAL += 3
ENDIF

RETURN LOCAL

"""
    while text.count(helper_body) > 1:
        text = text.replace(helper_body + helper_body, helper_body, 1)
    if "@GET_CULTURE_SINGING_BONUS" not in text:
        text = replace_once(
            text, marker, helper_body + marker, "culture festival helper"
        )
    write_cp932(relative, text)


def mark_templates_retired() -> None:
    for relative in (
        "ERB/CHAR/CHAR_TEMPLATE_COM.ERB",
        "ERB/KOUJO/KOUJO_TEMPLATE.ERB",
    ):
        text = read_cp932(relative)
        text = text.replace(
            "COM322 ストリートライブ ---",
            "COM322 ストリートライブ（廃止済み・互換性維持） ---",
            1,
        )
        write_cp932(relative, text)


def validate() -> None:
    train = read_cp932("CSV/Train.csv")
    if "\n322,ストリートライブ" in "\n" + train:
        raise RuntimeError("COM322 remains enabled in Train.csv")

    shop = read_cp932("ERB/SHOP_ショップ.ERB")
    if "[130] - 野外ライブを開く" in shop or "CALL CONCERT" in shop:
        raise RuntimeError("shop concert remains reachable")

    school = read_cp932("ERB/SCHOOL_EVENT_体育祭・文化祭.ERB")
    if school.count("@GET_CULTURE_SINGING_BONUS") != 1:
        raise RuntimeError("culture singing helper is missing or duplicated")
    if school.count("CALL GET_CULTURE_SINGING_BONUS") != 2:
        raise RuntimeError("culture singing bonus is not applied to both participants")


def main() -> None:
    retire_train_command()
    retire_shop_concert()
    update_microphone_description()
    add_culture_festival_singing_bonus()
    mark_templates_retired()
    validate()
    print("Retired live commands and moved singing value to the culture festival.")


if __name__ == "__main__":
    main()
