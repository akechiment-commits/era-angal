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


def fix_life_limit() -> None:
    relative = "ERB/INFO_情報表示.ERB"
    text = read_cp932(relative)
    start = text.index("@LIFE_LIMIT\n")
    end = text.index(";-------------------------------------------------\n;記念日", start)
    replacement = """@LIFE_LIMIT
;体力・気力の固定9999上限は廃止。
;耐力だけはエンジンの整数範囲を意識した安全上限を維持する。
SIF MAXBASE:4 > 999999999999999999
	MAXBASE:4 = 999999999999999999
SIF MAXBASE:MASTER:4 > 999999999999999999
	MAXBASE:MASTER:4 = 999999999999999999
SIF BASE:4 > 999999999999999999
	BASE:4 = 999999999999999999
SIF BASE:MASTER:4 > 999999999999999999
	BASE:MASTER:4 = 999999999999999999

CALL LIFE_LIMIT_MAXBASE

;-----------------------------------------------
;体力等調整処理
;主人公の体力・気力は、レベルアップやアイテムによる一時超過を保持する。
;-----------------------------------------------
@LIFE_LIMIT_MAXBASE
;パートナーは従来どおり通常上限に合わせる。
;J用アイテムにより一時的に体力上限がなくなっていれば体力は合わせない。
IF TEQUIP:41 == 0
	SIF BASE:0 > MAXBASE:0
		BASE:0 = MAXBASE:0
ENDIF
SIF BASE:1 > MAXBASE:1
	BASE:1 = MAXBASE:1

;耐力は主人公・パートナーとも通常上限に合わせる。
SIF BASE:4 > MAXBASE:4
	BASE:4 = MAXBASE:4
SIF BASE:MASTER:4 > MAXBASE:MASTER:4
	BASE:MASTER:4 = MAXBASE:MASTER:4

"""
    text = text[:start] + replacement + text[end:]
    write_cp932(relative, text)


def fix_club_costs() -> None:
    relative = "ERB/CLUB_ACTIVITY_部活動システム.ERB"
    text = read_cp932(relative)
    replacements = (
        (
            """	;耐力消費
	LOCAL:2 = MAXBASE:MASTER:0 / 5
	BASE:MASTER:4 -= LOCAL:2
	SIF BASE:MASTER:4 < 0
		BASE:MASTER:4 = 0
	PRINTFORML 　体力 -{LOCAL:2}（残り {BASE:MASTER:0}/{MAXBASE:MASTER:0}）
""",
            """	;体力消費
	LOCAL:2 = MAXBASE:MASTER:0 / 5
	BASE:MASTER:0 -= LOCAL:2
	SIF BASE:MASTER:0 < 0
		BASE:MASTER:0 = 0
	PRINTFORML 　体力 -{LOCAL:2}（残り {BASE:MASTER:0}/{MAXBASE:MASTER:0}）
""",
            "sports activity health cost",
        ),
        (
            """	;体力・気力消費は少ない
	BASE:MASTER:4 -= 20
	SIF BASE:MASTER:4 < 0
		BASE:MASTER:4 = 0
	BASE:MASTER:1 -= 30
""",
            """	;体力・気力消費は少ない
	BASE:MASTER:0 -= 20
	SIF BASE:MASTER:0 < 0
		BASE:MASTER:0 = 0
	BASE:MASTER:1 -= 30
""",
            "study activity health cost",
        ),
        (
            """		BASE:MASTER:4 -= MAXBASE:MASTER:0 / 5
		SIF BASE:MASTER:4 < 0
			BASE:MASTER:4 = 0
""",
            """		BASE:MASTER:0 -= MAXBASE:MASTER:0 / 5
		SIF BASE:MASTER:0 < 0
			BASE:MASTER:0 = 0
""",
            "sports event health cost",
        ),
    )
    for old, new, label in replacements:
        text = replace_once(text, old, new, label)
    write_cp932(relative, text)


def update_healing_comment() -> None:
    relative = "ERB/COMF/COMF325.ERB"
    text = read_cp932(relative)
    text = replace_once(
        text,
        ";お茶請けなので限界突破はしない\nCALL LIFE_LIMIT_MAXBASE",
        ";パートナーは通常上限に合わせ、主人公の体力・気力は一時超過を保持する\nCALL LIFE_LIMIT_MAXBASE",
        "healing overflow comment",
    )
    write_cp932(relative, text)


def preserve_overflow_on_full_heals() -> None:
    for relative in (
        "ERB/LUNCH_EAT_昼食・食事.ERB",
        "ERB/LUNCH_SELF_EAT_自分用昼食.ERB",
    ):
        text = read_cp932(relative)
        guard = """SIF BASE:MASTER:0 < MAXBASE:MASTER:0
	BASE:MASTER:0 = MAXBASE:MASTER:0"""
        if guard not in text:
            text = replace_once(
                text,
                "\nBASE:MASTER:0 = MAXBASE:MASTER:0\n",
                f"\n{guard}\n",
                f"{relative}: lunch full heal",
            )
        write_cp932(relative, text)

    relative = "ERB/RANDOM_S_ランダムイベント.ERB"
    text = read_cp932(relative)
    text = replace_once(
        text,
        """;体力、気力が上昇していた場合、全快させる
SIF BASE:MASTER:0 != MAXBASE:MASTER:0
	BASE:MASTER:0 = MAXBASE:MASTER:0
SIF BASE:MASTER:1 != MAXBASE:MASTER:1
	BASE:MASTER:1 = MAXBASE:MASTER:1
""",
        """;体力、気力が上昇していた場合、全快させる。一時超過中は減らさない。
SIF BASE:MASTER:0 < MAXBASE:MASTER:0
	BASE:MASTER:0 = MAXBASE:MASTER:0
SIF BASE:MASTER:1 < MAXBASE:MASTER:1
	BASE:MASTER:1 = MAXBASE:MASTER:1
""",
        "random event full heal",
    )
    write_cp932(relative, text)


def validate() -> None:
    info = read_cp932("ERB/INFO_情報表示.ERB")
    forbidden = (
        "MAXBASE:0 > 9999",
        "MAXBASE:MASTER:0 > 9999",
        "MAXBASE:1 > 9999",
        "MAXBASE:MASTER:1 > 9999",
        "BASE:0 > 9999",
        "BASE:MASTER:0 > 9999",
        "BASE:1 > 9999",
        "BASE:MASTER:1 > 9999",
        "BASE:MASTER:0 > MAXBASE:MASTER:0",
        "BASE:MASTER:1 > MAXBASE:MASTER:1",
    )
    for fragment in forbidden:
        if fragment in info:
            raise RuntimeError(f"resource limit remains: {fragment}")

    club = read_cp932("ERB/CLUB_ACTIVITY_部活動システム.ERB")
    if "BASE:MASTER:4 -= MAXBASE:MASTER:0" in club:
        raise RuntimeError("club activity still deducts endurance using max health")
    if "BASE:MASTER:4 -= 20" in club:
        raise RuntimeError("study activity still deducts endurance as health")
    if club.count("BASE:MASTER:0 -= LOCAL:2") < 3:
        raise RuntimeError("club health costs were not applied as expected")

    for relative in (
        "ERB/LUNCH_EAT_昼食・食事.ERB",
        "ERB/LUNCH_SELF_EAT_自分用昼食.ERB",
        "ERB/RANDOM_S_ランダムイベント.ERB",
    ):
        text = read_cp932(relative)
        if "BASE:MASTER:0 = MAXBASE:MASTER:0" in text:
            guard = (
                "SIF BASE:MASTER:0 < MAXBASE:MASTER:0\n"
                "\tBASE:MASTER:0 = MAXBASE:MASTER:0"
            )
            if guard not in text:
                raise RuntimeError(f"{relative}: health full heal can erase overflow")


def main() -> None:
    fix_life_limit()
    fix_club_costs()
    update_healing_comment()
    preserve_overflow_on_full_heals()
    validate()
    print("Fixed resource overflow limits and club activity health costs.")


if __name__ == "__main__":
    main()
