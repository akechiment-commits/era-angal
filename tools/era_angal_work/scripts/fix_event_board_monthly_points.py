from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT_BOARD = ROOT / "ERB" / "EVENT_BOARD_イベントボード周回.ERB"
SHOP = ROOT / "ERB" / "SHOP_ショップ.ERB"


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


def main() -> None:
    board = read_cp932(EVENT_BOARD)

    old_month_reset = crlf(
        """;月変更チェック → ミッションLv・イベントポイント・エリア番号リセット
IF FLAG:67 != DAY:8
	REPEAT 6
		FLAG:(71 + COUNT) = 0	;イベントポイント
		FLAG:(98 + COUNT) = 1	;エリア番号
	REND
	REPEAT 18
		FLAG:(78 + COUNT) = 1	;イベント別ミッションLv（各3スロット×6イベント）
	REND
	FLAG:37 = 0	;すごろく周回数リセット
	REPEAT 6
		FLAG:(104 + COUNT) = 0	;マイルストーン達成数リセット
	REND
	FLAG:67 = DAY:8
ENDIF
"""
    )
    new_month_reset = crlf(
        """;年月変更チェック。6イベントすべての月内状態を一括リセットする。
CALL EVENT_BOARD_MONTHLY_RESET
"""
    )
    board = replace_once(
        board,
        old_month_reset,
        new_month_reset,
        "event board inline monthly reset",
    )

    reset_function = crlf(
        """;---------------------------------------------------------
; イベントボード月次リセット
; 年月キーで判定し、別月の同じイベント枠からポイント・報酬状態が混入するのを防ぐ。
;---------------------------------------------------------
@EVENT_BOARD_MONTHLY_RESET
#DIM DYNAMIC MONTH_KEY, 1

MONTH_KEY = DAY:3 * 100 + DAY:8
SIF FLAG:67 == MONTH_KEY
	RETURN 0

REPEAT 6
	FLAG:(71 + COUNT) = 0	;イベント別月間PT
	FLAG:(98 + COUNT) = 1	;イベント別エリア番号
	FLAG:(104 + COUNT) = 0	;イベント別マイルストーン達成数
	FLAG:(120 + COUNT) = 0	;イベント別報酬受取数
	FLAG:(127 + COUNT) = 0	;旧累計PTを消去（以後は月間PTへ一本化）
REND
REPEAT 18
	FLAG:(78 + COUNT) = 1	;イベント別ミッションLv
REND

;選択中イベントだけが使う共有進行状態も月替わりで破棄する。
FLAG:32 = 0
FLAG:33 = 0
FLAG:34 = 0
FLAG:35 = 0
FLAG:36 = 0
FLAG:37 = 0
FLAG:38 = 0
FLAG:64 = 1
FLAG:65 = 1
FLAG:66 = 1
FLAG:68 = 0
FLAG:67 = MONTH_KEY
RETURN 1

"""
    )
    if "@EVENT_BOARD_MONTHLY_RESET\r\n" not in board:
        main_anchor = "@EVENT_BOARD_MAIN\r\n"
        if main_anchor not in board:
            raise SystemExit("EVENT_BOARD_MAIN anchor not found")
        board = board.replace(main_anchor, reset_function + main_anchor, 1)

    status_old = crlf(
        """PRINTFORML %TSTR:99%PT:{FLAG:B}
B = 127 + FLAG:68
PRINTFORML 累計PT:{FLAG:B}
A = FLAG:68 * 3 + 78	;通常Lv index
"""
    )
    status_new = crlf(
        """PRINTFORML %TSTR:99%PT:{FLAG:B}
A = FLAG:68 * 3 + 78	;通常Lv index
"""
    )
    board = replace_once(board, status_old, status_new, "status cumulative PT")

    next_reward_old = "A = 127 + FLAG:68\r\n\tLOCAL:8 = FLAG:A\t;現在の累計PT\r\n"
    next_reward_new = "A = 71 + FLAG:68\r\n\tLOCAL:8 = FLAG:A\t;現在のイベント別月間PT\r\n"
    board = replace_once(
        board,
        next_reward_old,
        next_reward_new,
        "next reward PT source",
    )

    mission_clear_old = crlf(
        """B = 71 + FLAG:68
FLAG:B += LOCAL:0
B = 127 + FLAG:68
FLAG:B += LOCAL:0
PRINTFORML イベントPT +{LOCAL:0}
CALL EVENT_BOARD_CLAIM_REWARDS
B = 127 + FLAG:68
PRINTFORML 累計PT:{FLAG:B}
"""
    )
    mission_clear_new = crlf(
        """B = 71 + FLAG:68
FLAG:B += LOCAL:0
PRINTFORML イベントPT +{LOCAL:0}
CALL EVENT_BOARD_CLAIM_REWARDS
B = 71 + FLAG:68
PRINTFORML 現在のイベントPT:{FLAG:B}
"""
    )
    board = replace_once(
        board,
        mission_clear_old,
        mission_clear_new,
        "mission clear PT update",
    )

    area_complete_old = crlf(
        """B = 71 + FLAG:68
FLAG:B += LOCAL:0
B = 127 + FLAG:68
FLAG:B += LOCAL:0
PRINTFORML イベントPT +{LOCAL:0}
"""
    )
    area_complete_new = crlf(
        """B = 71 + FLAG:68
FLAG:B += LOCAL:0
PRINTFORML イベントPT +{LOCAL:0}
"""
    )
    board = replace_once(
        board,
        area_complete_old,
        area_complete_new,
        "area complete PT update",
    )

    reward_list_index_old = "LOCAL:0 = 127 + FLAG:68\t;累計PTインデックス\r\n"
    reward_list_index_new = "LOCAL:0 = 71 + FLAG:68\t;イベント別月間PTインデックス\r\n"
    if reward_list_index_old in board:
        board = board.replace(reward_list_index_old, reward_list_index_new)
    elif board.count(reward_list_index_new) != 2:
        raise SystemExit("reward PT index anchors not found")
    board = board.replace(
        "PRINTFORML 累計PT: {LOCAL:3}\r\n",
        "PRINTFORML イベントPT: {LOCAL:3}\r\n",
        1,
    )
    board = board.replace(
        "LOCAL:3 = FLAG:A\t\t;現在の累計PT\r\n",
        "LOCAL:3 = FLAG:A\t\t;現在のイベント別月間PT\r\n",
        1,
    )
    board = board.replace(
        "LOCAL:2 = FLAG:A\t\t;累計クレーム数\r\n",
        "LOCAL:2 = FLAG:A\t\t;今月の報酬受取数\r\n",
    )

    board = board.replace(
        ";   FLAG:67  = 月変更検知用（前回月）\r\n",
        ";   FLAG:67  = 年月変更検知用（DAY:3*100+DAY:8）\r\n",
        1,
    )

    board = replace_once(
        board,
        "\tPRINTFORMW 気力が足りない！攻撃できない。\r\n",
        "\tPRINTFORMW 気力が足りない！挑戦できない！\r\n",
        "insufficient energy message",
    )

    next_reward_threshold_old = (
        "\tLOCAL:7 = LOCAL:4 * LOCAL:5 + LOCAL:6\t;次tierに必要な累計PT\r\n"
    )
    next_reward_threshold_new = (
        "\tCALL EVENT_BOARD_REWARD_REQUIRED_PT, LOCAL:6, LOCAL:5, LOCAL:4\r\n"
        "\tLOCAL:7 = RESULT\t;次tierに必要な累計PT\r\n"
    )
    board = replace_once(
        board,
        next_reward_threshold_old,
        next_reward_threshold_new,
        "next reward scaled threshold",
    )
    board = replace_once(
        board,
        "\tPRINTFORML 報酬進捗: {LOCAL:3}/{LOCAL:2}（ループ{LOCAL:4}周目）\r\n",
        "\tPRINTFORML 報酬進捗: {LOCAL:3}/{LOCAL:2}（ループ{LOCAL:4+1}周目）\r\n",
        "next reward human loop number",
    )

    reward_threshold_function = crlf(
        """;---------------------------------------------------------
; ループ報酬の累計必要PT
; ARG:0=ループ内の基本閾値 ARG:1=1周目の最終閾値 ARG:2=完了ループ数
; 1周目=1.0倍、2周目=1.5倍、3周目=2.0倍……と周回コストを線形増加する。
;---------------------------------------------------------
@EVENT_BOARD_REWARD_REQUIRED_PT(ARG, ARG:1, ARG:2)
#DIM DYNAMIC LOOP_OFFSET, 1
#DIM DYNAMIC LOOP_TIER_PT, 1

;完了済み周回の必要PT合計: 1.0 + 1.5 + 2.0 + ...
LOOP_OFFSET = ARG:1 * ARG:2 * (ARG:2 + 3) / 4
;現在周回の各閾値も、その周回の倍率に合わせる。
LOOP_TIER_PT = ARG * (ARG:2 + 2) / 2
RETURN LOOP_OFFSET + LOOP_TIER_PT

"""
    )
    if "@EVENT_BOARD_REWARD_REQUIRED_PT(ARG, ARG:1, ARG:2)\r\n" not in board:
        reward_list_anchor = "@EVENT_BOARD_SHOW_REWARDS\r\n"
        if reward_list_anchor not in board:
            raise SystemExit("event reward list anchor not found")
        board = board.replace(
            reward_list_anchor,
            reward_threshold_function + reward_list_anchor,
            1,
        )

    reward_list_threshold_old = (
        "\tLOCAL:8 = LOCAL:6 * LOCAL:5 + LOCAL:7\t;現ループでの必要PT\r\n"
    )
    reward_list_threshold_new = (
        "\tCALL EVENT_BOARD_REWARD_REQUIRED_PT, LOCAL:7, LOCAL:5, LOCAL:6\r\n"
        "\tLOCAL:8 = RESULT\t;現ループでの必要PT\r\n"
    )
    board = replace_once(
        board,
        reward_list_threshold_old,
        reward_list_threshold_new,
        "reward list scaled threshold",
    )
    board = replace_once(
        board,
        "\tPRINTFORML ループ{LOCAL:6}周目（全報酬×{LOCAL:6}周取得済み）\r\n",
        "\tPRINTFORML ループ{LOCAL:6+1}周目（全報酬×{LOCAL:6}周取得済み）\r\n",
        "reward list human loop number",
    )

    claim_threshold_old = (
        "LOCAL:8 = LOCAL:5 * LOCAL:6 + LOCAL:7\t;実際に必要なPT\r\n"
    )
    claim_threshold_new = (
        "CALL EVENT_BOARD_REWARD_REQUIRED_PT, LOCAL:7, LOCAL:6, LOCAL:5\r\n"
        "LOCAL:8 = RESULT\t;実際に必要なPT\r\n"
    )
    board = replace_once(
        board,
        claim_threshold_old,
        claim_threshold_new,
        "reward claim scaled threshold",
    )
    write_cp932(EVENT_BOARD, board)

    shop = read_cp932(SHOP)
    shop_reset_old = crlf(
        """;年月日、曜日、天気等取得
CALL YOUBI
CALL GET_SEMESTER_NAME
"""
    )
    shop_reset_new = crlf(
        """;年月日、曜日、天気等取得
CALL YOUBI
;イベント画面を開かなくても、月が変わった時点で全イベントの月内状態をリセットする。
CALL EVENT_BOARD_MONTHLY_RESET
CALL GET_SEMESTER_NAME
"""
    )
    shop = replace_once(shop, shop_reset_old, shop_reset_new, "shop monthly reset call")
    write_cp932(SHOP, shop)

    print(f"updated {EVENT_BOARD}")
    print(f"updated {SHOP}")


if __name__ == "__main__":
    main()
