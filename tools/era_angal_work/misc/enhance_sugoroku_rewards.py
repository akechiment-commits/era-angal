from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT_BOARD = ROOT / "ERB" / "EVENT_BOARD_イベントボード周回.ERB"

START_BEGIN = "; EVENT_SUGOROKU_START_BONUS_BEGIN"
START_END = "; EVENT_SUGOROKU_START_BONUS_END"
LARGE_BEGIN = "; EVENT_SUGOROKU_LARGE_BONUS_BEGIN"
LARGE_END = "; EVENT_SUGOROKU_LARGE_BONUS_END"
FREE_ROLL_BEGIN = "; EVENT_SUGOROKU_FREE_ROLL_BEGIN"
FREE_ROLL_END = "; EVENT_SUGOROKU_FREE_ROLL_END"
MISSION_SUPPORT_BEGIN = "; EVENT_SUGOROKU_MISSION_SUPPORT_BEGIN"
MISSION_SUPPORT_END = "; EVENT_SUGOROKU_MISSION_SUPPORT_END"


def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932").replace("\r\n", "\n")


def write_cp932(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


def upsert_region(
    text: str,
    begin_marker: str,
    end_marker: str,
    legacy_start: str,
    legacy_end: str,
    block: str,
) -> str:
    if begin_marker in text:
        start = text.index(begin_marker)
        end = text.index(end_marker, start) + len(end_marker)
        if end < len(text) and text[end] == "\n":
            end += 1
    else:
        function_start = text.index("@EVENT_BOARD_SUGOROKU_ADVANCE")
        start = text.index(legacy_start, function_start)
        end = text.index(legacy_end, start)
    return text[:start] + block.rstrip("\n") + "\n" + text[end:]


def main() -> None:
    text = read_cp932(EVENT_BOARD)

    free_roll_header = ";   FLAG:15056  = ボーナスで得た無料サイコロ回数\n"
    if free_roll_header not in text:
        header_anchor = ";   FLAG:15055  = エリア進捗（0～99、100で踏破報酬・リセット）\n"
        text = text.replace(header_anchor, header_anchor + free_roll_header, 1)
    mission_support_header = ";   FLAG:15057  = 次回発生ミッションの予約支援率（上限80%）\n"
    if mission_support_header not in text:
        text = text.replace(free_roll_header, free_roll_header + mission_support_header, 1)

    reset_anchor = "FLAG:15055 = 0\nFLAG:64 = 1"
    if "FLAG:15055 = 0\nFLAG:15056 = 0\nFLAG:64 = 1" not in text:
        text = text.replace(reset_anchor, "FLAG:15055 = 0\nFLAG:15056 = 0\nFLAG:64 = 1", 1)
    if "FLAG:15056 = 0\nFLAG:15057 = 0\nFLAG:64 = 1" not in text:
        text = text.replace(
            "FLAG:15056 = 0\nFLAG:64 = 1",
            "FLAG:15056 = 0\nFLAG:15057 = 0\nFLAG:64 = 1",
            1,
        )

    mission_support_function = "\n".join(
        [
            MISSION_SUPPORT_BEGIN,
            ";予約した支援率を、新しく発生したミッションの初期進捗へ一度だけ適用する。",
            "@EVENT_BOARD_APPLY_PENDING_MISSION_SUPPORT",
            "SIF FLAG:15057 <= 0 || FLAG:15053 <= 0",
            "\tRETURN 0",
            "LOCAL:0 = FLAG:15052 * FLAG:15057 / 100",
            "SIF LOCAL:0 < 1",
            "\tLOCAL:0 = 1",
            "FLAG:15051 += LOCAL:0",
            "PRINTFORML 　【予約支援発動】初期進捗 +{LOCAL:0}（{FLAG:15057}\\%／{FLAG:15051}/{FLAG:15052}）",
            "FLAG:15057 = 0",
            "RETURN 1",
            MISSION_SUPPORT_END,
        ]
    )
    text = upsert_region(
        text,
        MISSION_SUPPORT_BEGIN,
        MISSION_SUPPORT_END,
        "@EVENT_BOARD_SUGOROKU_ADVANCE\n",
        "@EVENT_BOARD_SUGOROKU_ADVANCE\n",
        mission_support_function,
    )

    mission_start_lines = (
        "\t\tPRINTFORML ▼ 通常ミッション Lv{FLAG:A} 発生！　目標値: {FLAG:15052}",
        "\t\tPRINTFORML ▼▼ 特大ミッション Lv{FLAG:A} 発生！　目標値: {FLAG:15052}",
        "\t\tPRINTFORML ▼▼▼ 緊急ミッション Lv{FLAG:A} 発生！！　目標値: {FLAG:15052}",
        "\t\tPRINTFORML 通 通常ミッションマス　▼ 通常ミッション Lv{FLAG:A} 発生！　目標値: {FLAG:15052}",
        "\t\tPRINTFORML 特 特大ミッションマス　▼▼ 特大ミッション Lv{FLAG:A} 発生！　目標値: {FLAG:15052}",
        "\t\tPRINTFORML 緊 緊急ミッションマス　▼▼▼ 緊急ミッション Lv{FLAG:A} 発生！！　目標値: {FLAG:15052}",
    )
    for mission_start_line in mission_start_lines:
        hooked = mission_start_line + "\n\t\tCALL EVENT_BOARD_APPLY_PENDING_MISSION_SUPPORT"
        if hooked not in text:
            if text.count(mission_start_line) != 1:
                raise SystemExit(f"mission support hook anchor mismatch: {mission_start_line}")
            text = text.replace(mission_start_line, hooked, 1)

    free_roll = "\n".join(
        [
            FREE_ROLL_BEGIN,
            "LOCAL:0 = 250\t;通常時の体力消費",
            "IF FLAG:15056 > 0",
            "\tFLAG:15056 -= 1",
            "\tLOCAL:0 = 0",
            "\tPRINTFORML 【ボーナス継続】サイコロの体力消費が無料！（残り{FLAG:15056}回）",
            "ENDIF",
            "",
            "IF BASE:MASTER:0 < LOCAL:0",
            "\tPRINTFORMW 体力が足りない！これ以上進めない。",
            "\tRETURN 0",
            "ENDIF",
            "",
            "BASE:MASTER:0 -= LOCAL:0",
            "SIF LOCAL:0 > 0",
            "\tCALL EVENT_BOARD_PLAYER_ADD_EXP, LOCAL:0",
            FREE_ROLL_END,
        ]
    )
    text = upsert_region(
        text,
        FREE_ROLL_BEGIN,
        FREE_ROLL_END,
        "LOCAL:0 = 250\t;体力消費固定値\n",
        "LOCAL:2 = RAND:6 + 1\n",
        free_roll,
    )

    start_and_small = "\n".join(
        [
            START_BEGIN,
            ";スタートマス：PT・プレイヤーEXP・無料サイコロからランダム抽選する。",
            "ELSEIF FLAG:15050 == 0",
            "\tLOCAL:7 = RAND:3",
            "\tPRINTL ★ スタートルーレット！",
            "\tSELECTCASE LOCAL:7",
            "\tCASE 0",
            "\t\tLOCAL:4 = 80 + RAND:81",
            "\t\tA = 71 + FLAG:68",
            "\t\tFLAG:A += LOCAL:4",
            "\t\tPRINTFORML 　【PTボーナス】イベントPT +{LOCAL:4}",
            "\t\tCALL EVENT_BOARD_SHOW_REACHED_PROGRESS",
            "\tCASE 1",
            "\t\tLOCAL:4 = 100 + RAND:5 * 25",
            "\t\tPRINTFORML 　【成長ボーナス】プレイヤーEXP +{LOCAL:4}",
            "\t\tCALL EVENT_BOARD_PLAYER_ADD_EXP, LOCAL:4 * 10",
            "\tCASE 2",
            "\t\tFLAG:15056 += 1",
            "\t\tPRINTFORML 　【無料サイコロ】次のサイコロ1回は体力消費なし！",
            "\tENDSELECT",
            "\tWAIT",
            ";ボーナスマス（小）：4種類のボーナスからランダム抽選する。",
            "ELSEIF FLAG:15050 == 3",
            "\tLOCAL:7 = RAND:4",
            "\tPRINTL ★ ボーナスルーレット！",
            "\tSELECTCASE LOCAL:7",
            "\tCASE 0",
            "\t\tLOCAL:4 = 150 + RAND:101",
            "\t\tA = 71 + FLAG:68",
            "\t\tFLAG:A += LOCAL:4",
            "\t\tPRINTFORML 　【PTボーナス】イベントPT +{LOCAL:4}",
            "\t\tCALL EVENT_BOARD_SHOW_REACHED_PROGRESS",
            "\tCASE 1",
            "\t\tLOCAL:4 = 200 + RAND:3 * 50",
            "\t\tPRINTFORML 　【成長ボーナス】プレイヤーEXP +{LOCAL:4}",
            "\t\tCALL EVENT_BOARD_PLAYER_ADD_EXP, LOCAL:4 * 10",
            "\tCASE 2",
            "\t\tFLAG:15057 += 20",
            "\t\tSIF FLAG:15057 > 80",
            "\t\t\tFLAG:15057 = 80",
            "\t\tPRINTFORML 　【ミッション支援予約】次に発生するミッションの初期進捗 +20\\%（予約{FLAG:15057}\\%）",
            "\tCASE 3",
            "\t\tFLAG:15056 += 1",
            "\t\tPRINTFORML 　【無料サイコロ】次のサイコロ1回は体力消費なし！",
            "\tENDSELECT",
            "\tWAIT",
            START_END,
        ]
    )
    text = upsert_region(
        text,
        START_BEGIN,
        START_END,
        ";スタートマス\n",
        ";アイテムマス（おにぎり or ドーナッツ）: 5,15\n",
        start_and_small,
    )

    large = "\n".join(
        [
            LARGE_BEGIN,
            ";ボーナスマス（大）：強力な4種類のボーナスからランダム抽選する。",
            "ELSEIF FLAG:15050 == 13",
            "\tLOCAL:7 = RAND:4",
            "\tPRINTL ★★ 大ボーナスルーレット！",
            "\tSELECTCASE LOCAL:7",
            "\tCASE 0",
            "\t\tLOCAL:4 = 350 + RAND:201",
            "\t\tA = 71 + FLAG:68",
            "\t\tFLAG:A += LOCAL:4",
            "\t\tPRINTFORML 　【PTジャックポット】イベントPT +{LOCAL:4}",
            "\t\tCALL EVENT_BOARD_SHOW_REACHED_PROGRESS",
            "\tCASE 1",
            "\t\tLOCAL:4 = 400 + RAND:5 * 50",
            "\t\tPRINTFORML 　【成長ジャックポット】プレイヤーEXP +{LOCAL:4}",
            "\t\tCALL EVENT_BOARD_PLAYER_ADD_EXP, LOCAL:4 * 10",
            "\tCASE 2",
            "\t\tFLAG:15057 += 50",
            "\t\tSIF FLAG:15057 > 80",
            "\t\t\tFLAG:15057 = 80",
            "\t\tPRINTFORML 　【ミッション大支援予約】次に発生するミッションの初期進捗 +50\\%（予約{FLAG:15057}\\%）",
            "\tCASE 3",
            "\t\tFLAG:15056 += 2",
            "\t\tPRINTFORML 　【無料サイコロ大当たり】次のサイコロ2回は体力消費なし！",
            "\tENDSELECT",
            "\tWAIT",
            LARGE_END,
        ]
    )
    text = upsert_region(
        text,
        LARGE_BEGIN,
        LARGE_END,
        ";ボーナスマス（大）: 13\n",
        ";ゴールドチケットマス: 16\n",
        large,
    )

    write_cp932(EVENT_BOARD, text)
    print("すごろく報酬をランダム化: スタート / 小ボーナス / 大ボーナス")


if __name__ == "__main__":
    main()
