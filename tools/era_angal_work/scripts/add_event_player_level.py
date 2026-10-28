import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT_BOARD = ROOT / "ERB" / "EVENT_BOARD_イベントボード周回.ERB"
SHOP = ROOT / "ERB" / "SHOP_ショップ.ERB"
FLAG_CSV = ROOT / "CSV" / "Flag.csv"


def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\n", "\r\n")


def write_cp932(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


def crlf(text: str) -> str:
    return text.replace("\n", "\r\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    if new not in text:
        raise SystemExit(f"{label} anchor not found")
    return text


def update_event_board() -> None:
    text = read_cp932(EVENT_BOARD)

    old_header = ";   FLAG:15020～15025 = 今月イベント別報酬受取数\r\n"
    new_header = crlf(
        """;   FLAG:15020～15025 = 今月イベント別報酬受取数
;   FLAG:15070 = プレイヤーレベル（0は未初期化、通常は1以上）
;   FLAG:15071 = 現在レベル内のプレイヤー経験値
"""
    )
    header_addition = new_header.removeprefix(old_header)
    if header_addition not in text:
        text = replace_once(text, old_header, new_header, "player-level flag header")
    while header_addition + header_addition in text:
        text = text.replace(header_addition + header_addition, header_addition, 1)

    old_main_init = crlf(
        """ENDIF

;年月変更チェック。6イベントすべての月内状態を一括リセットする。
CALL EVENT_BOARD_MONTHLY_RESET
"""
    )
    new_main_init = crlf(
        """ENDIF

;既存セーブを含め、初回にプレイヤーレベルをLv1で初期化する。
CALL EVENT_BOARD_PLAYER_LEVEL_INIT

;年月変更チェック。6イベントすべての月内状態を一括リセットする。
CALL EVENT_BOARD_MONTHLY_RESET
"""
    )
    if "CALL EVENT_BOARD_PLAYER_LEVEL_INIT\r\n" not in text:
        text = replace_once(
            text,
            old_main_init,
            new_main_init,
            "player-level initialization",
        )

    status_anchor = crlf(
        """;---------------------------------------------------------
; ステータス表示
;---------------------------------------------------------
@EVENT_BOARD_STATUS
"""
    )
    level_functions = crlf(
        """;---------------------------------------------------------
; プレイヤーレベル初期化
; FLAG:15070=Lv、FLAG:15071=現在Lv内EXP
;---------------------------------------------------------
@EVENT_BOARD_PLAYER_LEVEL_INIT
IF FLAG:15070 <= 0
	FLAG:15070 = 1
	FLAG:15071 = 0
ENDIF
RETURN 1

;---------------------------------------------------------
; 次レベルに必要な経験値
; Lv1→2は800。以後、現在Lvが1上がるごとに50増える。
;---------------------------------------------------------
@EVENT_BOARD_PLAYER_NEXT_EXP(ARG)
LOCAL:0 = 750 + ARG * 50
SIF LOCAL:0 < 800
	LOCAL:0 = 800
RETURN LOCAL:0

;---------------------------------------------------------
; 体力・気力消費によるプレイヤー経験値獲得
; ARG:0=実際の消費量。消費量10につき1EXP（最低1EXP）。
;---------------------------------------------------------
@EVENT_BOARD_PLAYER_ADD_EXP(ARG)
CALL EVENT_BOARD_PLAYER_LEVEL_INIT
LOCAL:0 = ARG / 10
SIF LOCAL:0 < 1
	LOCAL:0 = 1
FLAG:15071 += LOCAL:0
PRINTFORML プレイヤーEXP +{LOCAL:0}

$EVENT_PLAYER_LEVEL_CHECK
CALL EVENT_BOARD_PLAYER_NEXT_EXP, FLAG:15070
LOCAL:1 = RESULT
IF FLAG:15071 < LOCAL:1
	PRINTFORML プレイヤーLv{FLAG:15070}　EXP {FLAG:15071}/{LOCAL:1}
	RETURN 0
ENDIF

FLAG:15071 -= LOCAL:1
FLAG:15070 += 1
MAXBASE:MASTER:0 += 10
MAXBASE:MASTER:1 += 10
;「全回復」ではなく新しい最大値ぶんを加算し、超過回復をそのまま保持する。
BASE:MASTER:0 += MAXBASE:MASTER:0
BASE:MASTER:1 += MAXBASE:MASTER:1
DRAWLINE
SETCOLOR 0xFFD700
PRINTL ★★★★★★★★★★★★★★★★★★★★★★★★★
PRINTFORML ★ プレイヤーレベルアップ！　Lv{FLAG:15070} ★
PRINTFORML 体力・気力最大値 +10　現在の最大値ぶん回復！
PRINTFORML 体力:{BASE:MASTER:0}/{MAXBASE:MASTER:0}　気力:{BASE:MASTER:1}/{MAXBASE:MASTER:1}
PRINTL ★★★★★★★★★★★★★★★★★★★★★★★★★
RESETCOLOR
DRAWLINE
GOTO EVENT_PLAYER_LEVEL_CHECK

;---------------------------------------------------------
; ステータス表示
;---------------------------------------------------------
@EVENT_BOARD_STATUS
"""
    )
    level_block = level_functions.removesuffix(status_anchor)
    if "@EVENT_BOARD_PLAYER_LEVEL_INIT" not in text:
        text = replace_once(text, status_anchor, level_functions, "player-level functions")
    while level_block + level_block in text:
        text = text.replace(level_block + level_block, level_block, 1)
    if text.count("@EVENT_BOARD_PLAYER_LEVEL_INIT") != 1:
        raise SystemExit("duplicate player-level function definitions")
    legacy_level_notice = crlf(
        """DRAWLINE
PRINTFORML ★ プレイヤーLv{FLAG:15070}にアップ！
PRINTFORML 体力・気力最大値 +10　現在の最大値ぶん回復！
PRINTFORML 体力:{BASE:MASTER:0}/{MAXBASE:MASTER:0}　気力:{BASE:MASTER:1}/{MAXBASE:MASTER:1}
DRAWLINE
"""
    )
    highlighted_level_notice = crlf(
        """DRAWLINE
SETCOLOR 0xFFD700
PRINTL ★★★★★★★★★★★★★★★★★★★★★★★★★
PRINTFORML ★ プレイヤーレベルアップ！　Lv{FLAG:15070} ★
PRINTFORML 体力・気力最大値 +10　現在の最大値ぶん回復！
PRINTFORML 体力:{BASE:MASTER:0}/{MAXBASE:MASTER:0}　気力:{BASE:MASTER:1}/{MAXBASE:MASTER:1}
PRINTL ★★★★★★★★★★★★★★★★★★★★★★★★★
RESETCOLOR
DRAWLINE
"""
    )
    text = replace_once(
        text,
        legacy_level_notice,
        highlighted_level_notice,
        "highlighted player-level notice",
    )
    text = replace_once(
        text,
        crlf(
            """; Lv1→2は150。以後、現在Lvが1上がるごとに50増える。
;---------------------------------------------------------
@EVENT_BOARD_PLAYER_NEXT_EXP(ARG)
LOCAL:0 = 100 + ARG * 50
SIF LOCAL:0 < 150
	LOCAL:0 = 150
"""
        ),
        crlf(
            """; Lv1→2は800。以後、現在Lvが1上がるごとに50増える。
;---------------------------------------------------------
@EVENT_BOARD_PLAYER_NEXT_EXP(ARG)
LOCAL:0 = 750 + ARG * 50
SIF LOCAL:0 < 800
	LOCAL:0 = 800
"""
        ),
        "player-level experience curve",
    )

    old_status = crlf(
        """CALL EVENT_BOARD_CALC_HAKKIICHI
PRINTFORML 体力:{BASE:MASTER:0}/{MAXBASE:MASTER:0}　気力:{BASE:MASTER:1}/{MAXBASE:MASTER:1}　発揮値:{RESULT}
"""
    )
    new_status = crlf(
        """CALL EVENT_BOARD_CALC_HAKKIICHI
LOCAL:14 = RESULT
CALL EVENT_BOARD_PLAYER_LEVEL_INIT
CALL EVENT_BOARD_PLAYER_NEXT_EXP, FLAG:15070
LOCAL:15 = RESULT
PRINTFORML プレイヤーLv:{FLAG:15070}　EXP:{FLAG:15071}/{LOCAL:15}
PRINTFORML 体力:{BASE:MASTER:0}/{MAXBASE:MASTER:0}　気力:{BASE:MASTER:1}/{MAXBASE:MASTER:1}　発揮値:{LOCAL:14}
"""
    )
    text = replace_once(text, old_status, new_status, "player-level status display")

    advance_spend = crlf(
        """BASE:MASTER:0 -= LOCAL:0

IF FLAG:A < 20
"""
    )
    advance_spend_with_exp = crlf(
        """BASE:MASTER:0 -= LOCAL:0
CALL EVENT_BOARD_PLAYER_ADD_EXP, LOCAL:0

IF FLAG:A < 20
"""
    )
    text = replace_once(
        text, advance_spend, advance_spend_with_exp, "area stamina experience"
    )

    attack_spend = crlf(
        """BASE:MASTER:1 -= LOCAL:0
FLAG:15051 += LOCAL:1
"""
    )
    attack_spend_with_exp = crlf(
        """BASE:MASTER:1 -= LOCAL:0
CALL EVENT_BOARD_PLAYER_ADD_EXP, LOCAL:0
FLAG:15051 += LOCAL:1
"""
    )
    text = replace_once(
        text, attack_spend, attack_spend_with_exp, "mission energy experience"
    )

    sugoroku_spend = crlf(
        """BASE:MASTER:0 -= LOCAL:0
LOCAL:2 = RAND:6 + 1
"""
    )
    sugoroku_spend_with_exp = crlf(
        """BASE:MASTER:0 -= LOCAL:0
CALL EVENT_BOARD_PLAYER_ADD_EXP, LOCAL:0
LOCAL:2 = RAND:6 + 1
"""
    )
    text = replace_once(
        text, sugoroku_spend, sugoroku_spend_with_exp, "sugoroku stamina experience"
    )

    # イベント内の加算回復はすべて超過保持を許可する。これにより、すでに
    # 最大値超過中に別の回復が起きても超過分を最大値まで切り捨てない。
    cap_pairs = [
        crlf(
            """	SIF BASE:MASTER:0 > MAXBASE:MASTER:0
		BASE:MASTER:0 = MAXBASE:MASTER:0
"""
        ),
        crlf(
            """SIF BASE:MASTER:0 > MAXBASE:MASTER:0
	BASE:MASTER:0 = MAXBASE:MASTER:0
"""
        ),
        crlf(
            """	SIF BASE:MASTER:1 > MAXBASE:MASTER:1
		BASE:MASTER:1 = MAXBASE:MASTER:1
"""
        ),
        crlf(
            """SIF BASE:MASTER:1 > MAXBASE:MASTER:1
	BASE:MASTER:1 = MAXBASE:MASTER:1
"""
        ),
    ]
    removed_caps = 0
    for pair in cap_pairs:
        removed_caps += text.count(pair)
        text = text.replace(pair, "")
    for base_index in (0, 1):
        cap_pattern = re.compile(
            rf"(?m)^([ \t]*)SIF BASE:MASTER:{base_index} > MAXBASE:MASTER:{base_index}\r\n"
            rf"\1\tBASE:MASTER:{base_index} = MAXBASE:MASTER:{base_index}\r\n"
        )
        text, removed = cap_pattern.subn("", text)
        removed_caps += removed
    if removed_caps == 0 and "EVENT_BOARD_PLAYER_ADD_EXP" not in text:
        raise SystemExit("event recovery caps not found")

    old_bento = crlf(
        """ITEM:94 -= 1
BASE:MASTER:0 = MAXBASE:MASTER:0
BASE:MASTER:1 = MAXBASE:MASTER:1
PRINTFORMW お弁当を食べた！　体力・気力が全回復した！　（残り{ITEM:94}個）
"""
    )
    legacy_bento = crlf(
        """ITEM:94 -= 1
;最大値未満だけ最大値まで戻す。すでに超過している値は減らさない。
SIF BASE:MASTER:0 < MAXBASE:MASTER:0
	BASE:MASTER:0 = MAXBASE:MASTER:0
SIF BASE:MASTER:1 < MAXBASE:MASTER:1
	BASE:MASTER:1 = MAXBASE:MASTER:1
PRINTFORMW お弁当を食べた！　体力・気力が全回復した！　（残り{ITEM:94}個）
"""
    )
    new_bento = crlf(
        """ITEM:94 -= 1
;現在の最大値と同じ量を加算し、超過回復分もそのまま保持する。
BASE:MASTER:0 += MAXBASE:MASTER:0
BASE:MASTER:1 += MAXBASE:MASTER:1
PRINTFORMW お弁当を食べた！　体力 +{MAXBASE:MASTER:0}　気力 +{MAXBASE:MASTER:1}　（残り{ITEM:94}個）
"""
    )
    if legacy_bento in text:
        text = text.replace(legacy_bento, new_bento, 1)
    else:
        text = replace_once(text, old_bento, new_bento, "bento maximum-value recovery")

    text = text.replace(
        "お弁当を食べる（体力・気力全回復）",
        "お弁当を食べる（体力・気力を最大値分回復）",
    )
    text = text.replace(
        "; アイテム使用：お弁当（体力・気力全回復）",
        "; アイテム使用：お弁当（体力・気力を最大値分回復）",
    )

    write_cp932(EVENT_BOARD, text)


def update_flag_csv() -> None:
    text = read_cp932(FLAG_CSV)
    old = "15099,追加FLAG領域移行バージョン\r\n"
    player_flags = crlf(
        """15070,イベントプレイヤーレベル
15071,イベントプレイヤー経験値
"""
    )
    new = player_flags + old
    if player_flags not in text:
        text = replace_once(text, old, new, "player-level flag names")
    while player_flags + player_flags in text:
        text = text.replace(player_flags + player_flags, player_flags, 1)
    if text.count("15070,イベントプレイヤーレベル\r\n") != 1:
        raise SystemExit("duplicate player-level flag names")
    write_cp932(FLAG_CSV, text)


def update_shop() -> None:
    text = read_cp932(SHOP)
    legacy_maximums = crlf(
        """;実績SPで購入した最大体力/気力強化を適用（セーブ固有、FLAG:5020/5021。旧GLOBAL:220/221）
MAXBASE:MASTER:0 = 5000 + FLAG:5020 * 100
MAXBASE:MASTER:1 = 3000 + FLAG:5021 * 100
"""
    )
    player_level_maximums = crlf(
        """;実績SPとイベントプレイヤーLvによる最大体力/気力強化を適用。
;Lv1は補正なし。Lv2以降、1Lvごとに体力・気力を各10加算する。
MAXBASE:MASTER:0 = 5000 + FLAG:5020 * 100 + MAX(FLAG:15070 - 1, 0) * 10
MAXBASE:MASTER:1 = 3000 + FLAG:5021 * 100 + MAX(FLAG:15070 - 1, 0) * 10
"""
    )
    overflow_safe_maximums = crlf(
        """;実績SPとイベントプレイヤーLvによる最大体力/気力強化を適用。
;Lv1は補正なし。Lv2以降、1Lvごとに体力・気力を各10加算する。
;MAXBASE再代入時の自動丸めから、レベルアップ・アイテム回復の一時超過分を守る。
LOCAL:92 = BASE:MASTER:0
LOCAL:93 = BASE:MASTER:1
MAXBASE:MASTER:0 = 5000 + FLAG:5020 * 100 + MAX(FLAG:15070 - 1, 0) * 10
MAXBASE:MASTER:1 = 3000 + FLAG:5021 * 100 + MAX(FLAG:15070 - 1, 0) * 10
SIF LOCAL:92 > BASE:MASTER:0
	BASE:MASTER:0 = LOCAL:92
SIF LOCAL:93 > BASE:MASTER:1
	BASE:MASTER:1 = LOCAL:93
"""
    )
    if legacy_maximums in text:
        text = text.replace(legacy_maximums, player_level_maximums, 1)
    if player_level_maximums in text:
        text = text.replace(player_level_maximums, overflow_safe_maximums, 1)
    elif overflow_safe_maximums not in text:
        raise SystemExit("shop overflow-safe player-level maximums anchor not found")

    partner_energy_line = crlf(
        """	CALL PRINT_BAR, A, MAXBASE:1, 32, UNICODE(0x2585), UNICODE(0x2585), BARCOLORSET("緑"), RESULT:1
	PRINTFORM ({BASE:1,4}/{MAXBASE:1,4})
ELSE
"""
    )
    partner_energy_line_with_break = crlf(
        """	CALL PRINT_BAR, A, MAXBASE:1, 32, UNICODE(0x2585), UNICODE(0x2585), BARCOLORSET("緑"), RESULT:1
	PRINTFORML ({BASE:1,4}/{MAXBASE:1,4})
ELSE
"""
    )
    text = replace_once(
        text,
        partner_energy_line,
        partner_energy_line_with_break,
        "partner energy line break",
    )

    legacy_status_end = crlf(
        """ELSE
	PRINTL 
ENDIF

PRINTL 
"""
    )
    compact_player_status = crlf(
        """ELSE
	PRINTL 
ENDIF

;イベント用プレイヤー体力・気力は、パートナーの有無に関係なく常時表示する。
SETCOLOR 0x88CCFF
PRINTFORML プレイヤー　体力:{BASE:MASTER:0}/{MAXBASE:MASTER:0}　気力:{BASE:MASTER:1}/{MAXBASE:MASTER:1}
RESETCOLOR
PRINTL 
"""
    )
    player_bar_status = crlf(
        """ELSE
	PRINTL 
ENDIF

;イベント用プレイヤー体力・気力は、パートナーと同じバー形式で常時表示する。
SETCOLOR 0x88CCFF
PRINTL あなた
RESETCOLOR
PRINT           体力
A = BASE:MASTER:0
SIF BASE:MASTER:0 < 0
	A = 0
CALL PRINT_BAR_0, A, MAXBASE:MASTER:0, 32
PRINTFORML ({BASE:MASTER:0,4}/{MAXBASE:MASTER:0,4})
PRINT           気力
A = BASE:MASTER:1
SIF BASE:MASTER:1 < 0
	A = 0
CALL PRINT_BAR, A, MAXBASE:MASTER:1, 32, UNICODE(0x2585), UNICODE(0x2585), BARCOLORSET("緑"), RESULT:1
PRINTFORML ({BASE:MASTER:1,4}/{MAXBASE:MASTER:1,4})
PRINTL 
"""
    )
    if legacy_status_end in text:
        text = text.replace(legacy_status_end, compact_player_status, 1)
    if compact_player_status in text:
        text = text.replace(compact_player_status, player_bar_status, 1)
    elif player_bar_status not in text:
        raise SystemExit("shop player bar status anchor not found")
    write_cp932(SHOP, text)


def main() -> None:
    update_event_board()
    update_shop()
    update_flag_csv()
    print(f"updated {EVENT_BOARD}")
    print(f"updated {SHOP}")
    print(f"updated {FLAG_CSV}")


if __name__ == "__main__":
    main()
