from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT_BOARD = ROOT / "ERB" / "EVENT_BOARD_イベントボード周回.ERB"
EVENT_DATA = ROOT / "ERB" / "EVENT_BOARD_DATA_イベントデータ.ERB"
SUMMARIES = ROOT / "tools" / "event_scenario_summaries.md"
RECOLLECTIONS = ROOT / "tools" / "event_scenario_recollections.md"

OVERVIEW_HOOK_BEGIN = "; EVENT_STORY_OVERVIEW_HOOK_BEGIN"
OVERVIEW_HOOK_END = "; EVENT_STORY_OVERVIEW_HOOK_END"
COMPLETION_HOOK_BEGIN = "; EVENT_STORY_COMPLETION_HOOK_BEGIN"
COMPLETION_HOOK_END = "; EVENT_STORY_COMPLETION_HOOK_END"
FUNCTIONS_BEGIN = "; EVENT_STORY_FUNCTIONS_BEGIN"
FUNCTIONS_END = "; EVENT_STORY_FUNCTIONS_END"


def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932").replace("\r\n", "\n")


def write_cp932(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if text.count(old) != 1:
        raise SystemExit(f"{label}: expected one anchor, found {text.count(old)}")
    return text.replace(old, new, 1)


def upsert_marked_block(
    text: str,
    begin: str,
    end: str,
    block: str,
    *,
    anchor: str,
    insert_after: bool,
    label: str,
) -> str:
    pattern = re.compile(
        rf"(?m)^{re.escape(begin)}\n.*?^{re.escape(end)}\n?",
        re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(block.rstrip("\n") + "\n", text, count=1)
    if insert_after:
        return replace_once(text, anchor, anchor + block, label)
    return replace_once(text, anchor, block + anchor, label)


def load_story_texts() -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
    summary_text = SUMMARIES.read_text(encoding="utf-8")
    recollection_text = RECOLLECTIONS.read_text(encoding="utf-8")

    summaries = re.findall(
        r"^### (.+?)\n\n\*\*概要：\*\* (.+?)$",
        summary_text,
        re.MULTILINE,
    )
    recollections = re.findall(
        r"^### (.+?)\n\n\*\*回想（(.+?)）：\*\*「(.+?)」$",
        recollection_text,
        re.MULTILINE,
    )

    if len(summaries) != 52 or len(recollections) != 52:
        raise SystemExit(
            f"story data count mismatch: summaries={len(summaries)}, "
            f"recollections={len(recollections)}"
        )
    summary_titles = [title for title, _ in summaries]
    recollection_titles = [title for title, _, _ in recollections]
    if summary_titles != recollection_titles:
        raise SystemExit("summary and recollection event order differs")
    speakers = [speaker for _, speaker, _ in recollections]
    if len(set(speakers)) != 52:
        raise SystemExit("recollection speakers are not unique")

    event_data = read_cp932(EVENT_DATA)
    data_titles = re.findall(r'^\s*TSTR:\d+ = "(.+?)"$', event_data, re.MULTILINE)[:52]
    if summary_titles != data_titles:
        for index, (summary_title, data_title) in enumerate(
            zip(summary_titles, data_titles)
        ):
            if summary_title != data_title:
                raise SystemExit(
                    f"event title mismatch at {index}: "
                    f"{summary_title!r} != {data_title!r}"
                )
        raise SystemExit(
            f"event title count mismatch: stories={len(summary_titles)}, "
            f"event data={len(data_titles)}"
        )

    for title, overview in summaries:
        if "\n" in title or "\n" in overview:
            raise SystemExit(f"multiline overview is not supported: {title}")
    for title, speaker, dialogue in recollections:
        if any("\n" in value for value in (title, speaker, dialogue)):
            raise SystemExit(f"multiline dialogue is not supported: {title}")

    # Fail here with a useful error instead of corrupting the generated CP932 ERB.
    str(summaries + recollections).encode("cp932")
    return summaries, recollections


def make_story_functions(
    summaries: list[tuple[str, str]],
    recollections: list[tuple[str, str, str]],
) -> str:
    lines = [
        FUNCTIONS_BEGIN,
        ";---------------------------------------------------------",
        "; イベント物語表示の開催年リセット",
        "; FLAG:26=強くてニューゲーム周回数、DAY:3=開催年",
        ";---------------------------------------------------------",
        "@EVENT_BOARD_STORY_CYCLE_RESET",
        "#DIM DYNAMIC STORY_CYCLE_KEY, 1",
        "",
        "STORY_CYCLE_KEY = FLAG:26 * 10000 + DAY:3",
        ";導入前セーブでは、既存の完走済みイベントを現在年の表示済みとして引き継ぐ。",
        "IF FLAG:5015 == 0",
        "\tFLAG:5014 = FLAG:5004",
        "\tFLAG:5015 = STORY_CYCLE_KEY",
        "\tRETURN 0",
        "ENDIF",
        "SIF FLAG:5015 == STORY_CYCLE_KEY",
        "\tRETURN 0",
        "",
        ";翌年の再開催と強くてニューゲームでは、概要・完走台詞を再表示できる。",
        "FLAG:5013 = 0",
        "FLAG:5014 = 0",
        "FLAG:5015 = STORY_CYCLE_KEY",
        "RETURN 1",
        "",
        ";---------------------------------------------------------",
        "; イベント初参加時の概要（FLAG:5013のイベント別・開催年内ビット）",
        ";---------------------------------------------------------",
        "@EVENT_BOARD_SHOW_OVERVIEW(ARG)",
        "DRAWLINE",
        "SETCOLOR 0x88CCFF",
        "PRINTL 【イベント概要】",
        "RESETCOLOR",
        "SELECTCASE ARG:0",
    ]
    for index, (title, overview) in enumerate(summaries):
        lines.extend(
            [
                f"CASE {index}\t;{title}",
                f"\tPRINTL {overview}",
            ]
        )
    lines.extend(
        [
            "ENDSELECT",
            "DRAWLINE",
            "WAIT",
            "RETURN 0",
            "",
            ";---------------------------------------------------------",
            "; イベント完走時の台詞（FLAG:5014のイベント別・開催年内ビット）",
            ";---------------------------------------------------------",
            "@EVENT_BOARD_SHOW_COMPLETION_DIALOGUE(ARG)",
            "DRAWLINE",
            "SETCOLOR 0xFFD700",
            "PRINTL 【イベント完走】",
            "RESETCOLOR",
            "SELECTCASE ARG:0",
        ]
    )
    for index, (title, speaker, dialogue) in enumerate(recollections):
        lines.extend(
            [
                f"CASE {index}\t;{title}",
                f"\tPRINTL {speaker}「{dialogue}」",
            ]
        )
    lines.extend(
        [
            "ENDSELECT",
            "DRAWLINE",
            "WAIT",
            "RETURN 0",
            FUNCTIONS_END,
            "",
        ]
    )
    return "\n".join(lines)


def update_event_board(
    summaries: list[tuple[str, str]],
    recollections: list[tuple[str, str, str]],
) -> None:
    text = read_cp932(EVENT_BOARD)

    flag_header = ";   FLAG:5013 = イベント初参加概要の表示済みビット（0～51、月替わりで維持）\n"
    story_flag_headers = "\n".join(
        [
            flag_header.rstrip("\n"),
            ";   FLAG:5014 = 現在の開催年に表示したイベント完走台詞のビット（0～51）",
            ";   FLAG:5015 = イベント物語表示の周回・開催年キー",
            "",
        ]
    )
    header_anchor = ";   FLAG:15071 = 現在レベル内のプレイヤー経験値\n"
    if ";   FLAG:5014 = " not in text:
        text = text.replace(flag_header, "", 1)
        text = replace_once(
            text,
            header_anchor,
            story_flag_headers + header_anchor,
            "overview flag header",
        )

    story_reset_call = "\n".join(
        [
            ";開催年の変更または強くてニューゲームの周回開始時に、一度限り表示を再解禁する。",
            "CALL EVENT_BOARD_STORY_CYCLE_RESET",
            "",
        ]
    )
    reset_call_anchor = ";年月変更チェック。6イベントすべての月内状態を一括リセットする。\n"
    if story_reset_call not in text:
        text = replace_once(
            text,
            reset_call_anchor,
            story_reset_call + reset_call_anchor,
            "event story cycle reset call",
        )

    overview_hook = "\n".join(
        [
            OVERVIEW_HOOK_BEGIN,
            ";選択したイベントの概要は、セーブデータ内でイベントごとに初回だけ表示する。",
            "CALL EVENT_BOARD_GET_EVENT_INDEX",
            "LOCAL:7 = RESULT",
            "IF LOCAL:7 >= 0 && !GETBIT(FLAG:5013, LOCAL:7)",
            "\tSETBIT FLAG:5013, LOCAL:7",
            "\tCALL EVENT_BOARD_SHOW_OVERVIEW, LOCAL:7",
            "ENDIF",
            OVERVIEW_HOOK_END,
            "",
        ]
    )
    selection_anchor = "FLAG:68 = LOCAL:8\t;イベントインデックス保存(0-5)\n"
    text = upsert_marked_block(
        text,
        OVERVIEW_HOOK_BEGIN,
        OVERVIEW_HOOK_END,
        overview_hook,
        anchor=selection_anchor,
        insert_after=True,
        label="event overview hook",
    )
    # Older generator runs placed a leading blank inside the replaceable block.
    # Collapse those blanks so repeated generation is byte-for-byte stable.
    text = re.sub(
        rf"{re.escape(selection_anchor)}\n+{re.escape(OVERVIEW_HOOK_BEGIN)}",
        selection_anchor + OVERVIEW_HOOK_BEGIN,
        text,
        count=1,
    )

    completion_hook = "\n".join(
        [
            COMPLETION_HOOK_BEGIN,
            ";20000PT報酬で永久完走フラグを立て、現在の開催年で初回なら台詞表示を予約する。",
            "LOCAL:10 = 0",
            "IF LOCAL:7 == 20000",
            "\tCALL EVENT_BOARD_GET_EVENT_INDEX",
            "\tLOCAL:9 = RESULT",
            "\tIF LOCAL:9 >= 0",
            "\t\tSETBIT FLAG:5004, LOCAL:9",
            "\t\tIF !GETBIT(FLAG:5014, LOCAL:9)",
            "\t\t\tSETBIT FLAG:5014, LOCAL:9",
            "\t\t\tLOCAL:10 = 1",
            "\t\tENDIF",
            "\tENDIF",
            "ENDIF",
            COMPLETION_HOOK_END,
            "",
        ]
    )
    old_completion = "\n".join(
        [
            ";20000PT報酬取得でイベント完走フラグをセット（LOCAL:7が基本PT閾値、セーブ固有。旧GLOBAL:204）",
            "IF LOCAL:7 == 20000",
            "\tCALL EVENT_BOARD_GET_EVENT_INDEX",
            "\tSETBIT FLAG:5004, RESULT",
            "ENDIF",
            "",
        ]
    )
    if COMPLETION_HOOK_BEGIN not in text:
        text = replace_once(
            text,
            old_completion,
            completion_hook,
            "event completion hook",
        )
    else:
        text = upsert_marked_block(
            text,
            COMPLETION_HOOK_BEGIN,
            COMPLETION_HOOK_END,
            completion_hook,
            anchor="",
            insert_after=True,
            label="event completion hook",
        )

    dialogue_call = "\n".join(
        [
            "CALL EVENT_BOARD_GIVE_REWARD, LOCAL:7, LOCAL:8",
            "IF LOCAL:10",
            "\tCALL EVENT_BOARD_SHOW_COMPLETION_DIALOGUE, LOCAL:9",
            "ENDIF",
        ]
    )
    dialogue_anchor = "CALL EVENT_BOARD_GIVE_REWARD, LOCAL:7, LOCAL:8"
    if dialogue_call not in text:
        text = replace_once(
            text,
            dialogue_anchor,
            dialogue_call,
            "completion dialogue call",
        )

    functions = make_story_functions(summaries, recollections)
    status_anchor = "\n".join(
        [
            ";---------------------------------------------------------",
            "; ステータス表示",
            ";---------------------------------------------------------",
            "@EVENT_BOARD_STATUS",
        ]
    )
    text = upsert_marked_block(
        text,
        FUNCTIONS_BEGIN,
        FUNCTIONS_END,
        functions,
        anchor=status_anchor,
        insert_after=False,
        label="event story functions",
    )

    write_cp932(EVENT_BOARD, text)


def main() -> None:
    summaries, recollections = load_story_texts()
    update_event_board(summaries, recollections)
    print(
        "イベント物語表示を更新: "
        f"概要{len(summaries)}件 / 完走台詞{len(recollections)}件"
    )


if __name__ == "__main__":
    main()
