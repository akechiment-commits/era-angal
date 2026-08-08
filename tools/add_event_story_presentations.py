from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT_BOARD = ROOT / "ERB" / "EVENT_BOARD_イベントボード周回.ERB"
EVENT_DATA = ROOT / "ERB" / "EVENT_BOARD_DATA_イベントデータ.ERB"
SUMMARIES = ROOT / "tools" / "event_scenario_summaries.md"
RECOLLECTIONS = ROOT / "tools" / "event_scenario_recollections.md"
MILESTONES = ROOT / "tools" / "event_scenario_milestones.md"
V3_PROMPTS = ROOT / "tools" / "v3prompt"
CHARACTER_TEXTS = ROOT / "tools" / "output"

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


def load_story_texts() -> tuple[
    list[tuple[str, str]],
    list[tuple[str, str, str]],
    list[tuple[str, tuple[str, str], tuple[str, str], tuple[str, str]]],
]:
    summary_text = SUMMARIES.read_text(encoding="utf-8")
    recollection_text = RECOLLECTIONS.read_text(encoding="utf-8")
    milestone_text = MILESTONES.read_text(encoding="utf-8")

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
    milestone_rows = re.findall(
        r"^### (.+?)\n"
        r"\*\*5000PT（(.+?)）：\*\*「(.+?)」\n"
        r"\*\*10000PT（(.+?)）：\*\*「(.+?)」\n"
        r"\*\*15000PT（(.+?)）：\*\*「(.+?)」$",
        milestone_text,
        re.MULTILINE,
    )
    milestones = [
        (title, (speaker_5, text_5), (speaker_10, text_10), (speaker_15, text_15))
        for title, speaker_5, text_5, speaker_10, text_10, speaker_15, text_15
        in milestone_rows
    ]

    if len(summaries) != 52 or len(recollections) != 52 or len(milestones) != 52:
        raise SystemExit(
            f"story data count mismatch: summaries={len(summaries)}, "
            f"milestones={len(milestones)}, recollections={len(recollections)}"
        )
    summary_titles = [title for title, _ in summaries]
    recollection_titles = [title for title, _, _ in recollections]
    milestone_titles = [title for title, *_ in milestones]
    if summary_titles != milestone_titles or summary_titles != recollection_titles:
        raise SystemExit("summary, milestone and recollection event order differs")
    for milestone, recollection in zip(milestones, recollections):
        title = milestone[0]
        speakers = [stage[0] for stage in milestone[1:]] + [recollection[1]]
        if len(set(speakers)) != 4:
            raise SystemExit(
                f"story speakers must be four distinct characters: {title}: "
                + ", ".join(speakers)
            )
    speakers = [speaker for _, speaker, _ in recollections]
    if len(set(speakers)) != 52:
        raise SystemExit("recollection speakers are not unique")

    story_speakers = set(speakers)
    story_speakers.update(
        speaker
        for _, *stages in milestones
        for speaker, _ in stages
    )
    for speaker in sorted(story_speakers):
        prompt_path = V3_PROMPTS / f"prompt_{speaker}_v3.txt"
        character_text_path = CHARACTER_TEXTS / f"{speaker}_転校生.txt"
        for source_path in (prompt_path, character_text_path):
            if not source_path.exists() or not source_path.read_text(encoding="utf-8").strip():
                raise SystemExit(f"character voice source is missing or empty: {source_path}")

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
    for title, *stages in milestones:
        for speaker, dialogue in stages:
            if any("\n" in value for value in (title, speaker, dialogue)):
                raise SystemExit(f"multiline milestone is not supported: {title}")

    # Fail here with a useful error instead of corrupting the generated CP932 ERB.
    str(summaries + milestones + recollections).encode("cp932")
    return summaries, recollections, milestones


def make_story_functions(
    summaries: list[tuple[str, str]],
    recollections: list[tuple[str, str, str]],
    milestones: list[
        tuple[str, tuple[str, str], tuple[str, str], tuple[str, str]]
    ],
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
        ";中間台詞初版で表示前に立てた可能性がある表示済みビットを、一度だけ修復する。",
        "IF FLAG:5019 < 1",
        "\tFLAG:5016 = 0",
        "\tFLAG:5017 = 0",
        "\tFLAG:5018 = 0",
        "\tFLAG:5019 = 1",
        "ENDIF",
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
        ";翌年の再開催と強くてニューゲームでは、概要・中間・完走台詞を再表示できる。",
        "FLAG:5013 = 0",
        "FLAG:5014 = 0",
        "FLAG:5016 = 0",
        "FLAG:5017 = 0",
        "FLAG:5018 = 0",
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
            "FORCEWAIT",
            "RETURN 0",
            "",
            ";---------------------------------------------------------",
            "; イベント中間シナリオ（ARG:1=1:序盤 / 2:中盤 / 3:後半）",
            ";---------------------------------------------------------",
            "@EVENT_BOARD_SHOW_PROGRESS_DIALOGUE(ARG, ARG:1)",
            "DRAWLINE",
            "SETCOLOR 0xFFCC66",
            "IF ARG:1 == 1",
            "\tPRINTL 【イベントシナリオ・序盤】",
            "ELSEIF ARG:1 == 2",
            "\tPRINTL 【イベントシナリオ・中盤】",
            "ELSEIF ARG:1 == 3",
            "\tPRINTL 【イベントシナリオ・後半】",
            "ENDIF",
            "RESETCOLOR",
            "IF ARG:1 == 1",
            "\tCALL EVENT_BOARD_SHOW_PROGRESS_5000, ARG:0",
            "ELSEIF ARG:1 == 2",
            "\tCALL EVENT_BOARD_SHOW_PROGRESS_10000, ARG:0",
            "ELSEIF ARG:1 == 3",
            "\tCALL EVENT_BOARD_SHOW_PROGRESS_15000, ARG:0",
            "ENDIF",
            "DRAWLINE",
            "FORCEWAIT",
            "RETURN 0",
            "",
            ";---------------------------------------------------------",
            "; 受取済み報酬を含め、現在PTに到達済みの未表示シナリオを追いつき表示する",
            ";---------------------------------------------------------",
            "@EVENT_BOARD_SHOW_REACHED_PROGRESS",
            "#DIM DYNAMIC STORY_EVENT_INDEX, 1",
            "#DIM DYNAMIC STORY_PT_INDEX, 1",
            "#DIM DYNAMIC STORY_CURRENT_PT, 1",
            "CALL EVENT_BOARD_GET_EVENT_INDEX",
            "STORY_EVENT_INDEX = RESULT",
            "SIF STORY_EVENT_INDEX < 0",
            "\tRETURN 0",
            "STORY_PT_INDEX = 71 + FLAG:68",
            "A = STORY_PT_INDEX",
            "STORY_CURRENT_PT = FLAG:A",
            "IF STORY_CURRENT_PT >= 5000 && !GETBIT(FLAG:5016, STORY_EVENT_INDEX)",
            "\tCALL EVENT_BOARD_SHOW_PROGRESS_DIALOGUE, STORY_EVENT_INDEX, 1",
            "\tSETBIT FLAG:5016, STORY_EVENT_INDEX",
            "ENDIF",
            "IF STORY_CURRENT_PT >= 10000 && !GETBIT(FLAG:5017, STORY_EVENT_INDEX)",
            "\tCALL EVENT_BOARD_SHOW_PROGRESS_DIALOGUE, STORY_EVENT_INDEX, 2",
            "\tSETBIT FLAG:5017, STORY_EVENT_INDEX",
            "ENDIF",
            "IF STORY_CURRENT_PT >= 15000 && !GETBIT(FLAG:5018, STORY_EVENT_INDEX)",
            "\tCALL EVENT_BOARD_SHOW_PROGRESS_DIALOGUE, STORY_EVENT_INDEX, 3",
            "\tSETBIT FLAG:5018, STORY_EVENT_INDEX",
            "ENDIF",
            "RETURN 0",
            "",
        ]
    )
    for stage_index, (threshold, stage_label) in enumerate(
        ((5000, "序盤"), (10000, "中盤"), (15000, "後半")),
        start=1,
    ):
        lines.extend(
            [
                f"; {threshold}PT・{stage_label}",
                f"@EVENT_BOARD_SHOW_PROGRESS_{threshold}(ARG)",
                "SELECTCASE ARG:0",
            ]
        )
        for index, milestone in enumerate(milestones):
            title = milestone[0]
            speaker, dialogue = milestone[stage_index]
            lines.extend(
                [
                    f"CASE {index}\t;{title}",
                    f"\tPRINTL {speaker}「{dialogue}」",
                ]
            )
        lines.extend(["ENDSELECT", "RETURN 0", ""])
    lines.extend(
        [
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
            "FORCEWAIT",
            "RETURN 0",
            FUNCTIONS_END,
            "",
        ]
    )
    return "\n".join(lines)


def update_event_board(
    summaries: list[tuple[str, str]],
    recollections: list[tuple[str, str, str]],
    milestones: list[
        tuple[str, tuple[str, str], tuple[str, str], tuple[str, str]]
    ],
) -> None:
    text = read_cp932(EVENT_BOARD)

    flag_header = ";   FLAG:5013 = イベント初参加概要の表示済みビット（0～51、月替わりで維持）\n"
    story_flag_headers = "\n".join(
        [
            flag_header.rstrip("\n"),
            ";   FLAG:5014 = 現在の開催年に表示したイベント完走台詞のビット（0～51）",
            ";   FLAG:5015 = イベント物語表示の周回・開催年キー",
            ";   FLAG:5016 = 現在の開催年に表示した5000PT序盤台詞のビット（0～51）",
            ";   FLAG:5017 = 現在の開催年に表示した10000PT中盤台詞のビット（0～51）",
            ";   FLAG:5018 = 現在の開催年に表示した15000PT後半台詞のビット（0～51）",
            ";   FLAG:5019 = 中間台詞表示処理のセーブ移行バージョン",
            "",
        ]
    )
    header_anchor = ";   FLAG:15071 = 現在レベル内のプレイヤー経験値\n"
    story_header_pattern = re.compile(r"(?m)(?:^;   FLAG:501[3-9] = .*\n)+")
    if story_header_pattern.search(text):
        text = story_header_pattern.sub(story_flag_headers, text, count=1)
    else:
        text = text.replace(flag_header, "", 1)
        text = replace_once(text, header_anchor, story_flag_headers + header_anchor, "story flag header")

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
            ";導入前に到達・受取済みだった中間台詞も、イベント選択時に未表示分だけ追いつく。",
            "CALL EVENT_BOARD_SHOW_REACHED_PROGRESS",
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

    # 報酬表の閾値は4700→5100のように物語到達点と一致しない。
    # 報酬受取処理ではなく、実際にイベントPTを加算して表示した直後に判定する。
    malformed_area_hook = (
        ";エリア踏破アイテム抽選\n"
        "CALL EVENT_BOARD_SHOW_REACHED_PROGRESS（おにぎり15% / ドーナッツ15% / ガチャチケット70%）"
    )
    if malformed_area_hook in text:
        text = text.replace(
            malformed_area_hook,
            ";エリア踏破アイテム抽選（おにぎり15% / ドーナッツ15% / ガチャチケット70%）",
            1,
        )
    progress_gain_anchors = (
        ("PRINTFORML 現在のイベントPT:{FLAG:B}", "mission clear PT gain"),
        (
            "PRINTFORML イベントPT +{LOCAL:0}\n\n"
            ";エリア踏破アイテム抽選（おにぎり15% / ドーナッツ15% / ガチャチケット70%）",
            "area complete PT gain",
        ),
        (
            "PRINTFORMW ◆ 周回ボーナス！　PT +{LOCAL:6}　ブロンズガチャチケット入手！（計{FLAG:15001}枚）",
            "sugoroku lap PT gain",
        ),
        ("PRINTFORML 　→ イベントPT +{LOCAL:0}", "random drop PT gain"),
    )
    for anchor, label in progress_gain_anchors:
        hooked = anchor + "\nCALL EVENT_BOARD_SHOW_REACHED_PROGRESS"
        if hooked not in text:
            text = replace_once(text, anchor, hooked, label)

    completion_hook = "\n".join(
        [
            COMPLETION_HOOK_BEGIN,
            ";5000/10000/15000PTの中間台詞と、20000PT完走台詞を開催年内に各1回だけ予約する。",
            "LOCAL:10 = 0",
            "IF GROUPMATCH(LOCAL:7, 5000, 10000, 15000, 20000)",
            "\tCALL EVENT_BOARD_GET_EVENT_INDEX",
            "\tLOCAL:9 = RESULT",
            "\tIF LOCAL:9 >= 0",
            "\t\tSELECTCASE LOCAL:7",
            "\t\tCASE 5000",
            "\t\t\tIF !GETBIT(FLAG:5016, LOCAL:9)",
            "\t\t\t\tLOCAL:10 = 1",
            "\t\t\tENDIF",
            "\t\tCASE 10000",
            "\t\t\tIF !GETBIT(FLAG:5017, LOCAL:9)",
            "\t\t\t\tLOCAL:10 = 2",
            "\t\t\tENDIF",
            "\t\tCASE 15000",
            "\t\t\tIF !GETBIT(FLAG:5018, LOCAL:9)",
            "\t\t\t\tLOCAL:10 = 3",
            "\t\t\tENDIF",
            "\t\tCASE 20000",
            "\t\t\tSETBIT FLAG:5004, LOCAL:9",
            "\t\t\tIF !GETBIT(FLAG:5014, LOCAL:9)",
            "\t\t\t\tLOCAL:10 = 4",
            "\t\t\tENDIF",
            "\t\tENDSELECT",
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
            "IF LOCAL:10 >= 1 && LOCAL:10 <= 3",
            "\tCALL EVENT_BOARD_SHOW_PROGRESS_DIALOGUE, LOCAL:9, LOCAL:10",
            "\tSELECTCASE LOCAL:10",
            "\tCASE 1",
            "\t\tSETBIT FLAG:5016, LOCAL:9",
            "\tCASE 2",
            "\t\tSETBIT FLAG:5017, LOCAL:9",
            "\tCASE 3",
            "\t\tSETBIT FLAG:5018, LOCAL:9",
            "\tENDSELECT",
            "ELSEIF LOCAL:10 == 4",
            "\tCALL EVENT_BOARD_SHOW_COMPLETION_DIALOGUE, LOCAL:9",
            "\tSETBIT FLAG:5014, LOCAL:9",
            "ENDIF",
        ]
    )
    dialogue_anchor = "CALL EVENT_BOARD_GIVE_REWARD, LOCAL:7, LOCAL:8"
    legacy_dialogue_call = "\n".join(
        [
            dialogue_anchor,
            "IF LOCAL:10",
            "\tCALL EVENT_BOARD_SHOW_COMPLETION_DIALOGUE, LOCAL:9",
            "ENDIF",
        ]
    )
    legacy_dialogue_tail = "\n".join(
        [
            "IF LOCAL:10",
            "\tCALL EVENT_BOARD_SHOW_COMPLETION_DIALOGUE, LOCAL:9",
            "ENDIF",
        ]
    )
    legacy_progress_dialogue_tail = "\n".join(
        [
            "IF LOCAL:10 >= 1 && LOCAL:10 <= 3",
            "\tCALL EVENT_BOARD_SHOW_PROGRESS_DIALOGUE, LOCAL:9, LOCAL:10",
            "ELSEIF LOCAL:10 == 4",
            "\tCALL EVENT_BOARD_SHOW_COMPLETION_DIALOGUE, LOCAL:9",
            "ENDIF",
        ]
    )
    if legacy_dialogue_call in text:
        text = replace_once(
            text,
            legacy_dialogue_call,
            dialogue_call,
            "legacy completion dialogue call",
        )
    elif dialogue_call not in text:
        text = replace_once(
            text,
            dialogue_anchor,
            dialogue_call,
            "completion dialogue call",
        )
    if f"{dialogue_call}\n{legacy_dialogue_tail}" in text:
        text = replace_once(
            text,
            f"{dialogue_call}\n{legacy_dialogue_tail}",
            dialogue_call,
            "duplicate legacy completion dialogue call",
        )
    if f"{dialogue_call}\n{legacy_progress_dialogue_tail}" in text:
        text = replace_once(
            text,
            f"{dialogue_call}\n{legacy_progress_dialogue_tail}",
            dialogue_call,
            "duplicate legacy progress dialogue call",
        )

    functions = make_story_functions(summaries, recollections, milestones)
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
    summaries, recollections, milestones = load_story_texts()
    update_event_board(summaries, recollections, milestones)
    print(
        "イベント物語表示を更新: "
        f"概要{len(summaries)}件 / 中間台詞{len(milestones) * 3}件 / "
        f"完走台詞{len(recollections)}件"
    )


if __name__ == "__main__":
    main()
