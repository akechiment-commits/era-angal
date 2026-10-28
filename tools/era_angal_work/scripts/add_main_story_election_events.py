#!/usr/bin/env python3
"""Register the main-story election arc and the home-club contest.

The existing event board reserves six slots per month even though some months
currently use only four or five.  This uses the sixth slot in April through
July, so the original 52 event indexes remain stable and the new events use
indexes 52-55.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "ERB" / "EVENT_BOARD_DATA_イベントデータ.ERB"

EVENTS = [
    {
        "month": 4,
        "slot": 5,
        "local_index": 23,
        "event_index": 52,
        "title": "生徒会長再任選挙・第一部 発端",
        "kind": 4,
        "kind_label": "親愛度",
        "cards": [103, 104, 105, 113, 115, 117, 120, 286, 1362],
        "reward_cards": {10500: 113, 12800: 103},
        "extra_reward_points": [11000, 12400, 14100, 15800, 17300, 18200, 19300],
    },
    {
        "month": 5,
        "slot": 5,
        "local_index": 29,
        "event_index": 53,
        "title": "生徒会長再任選挙・第二部 協力と騒乱",
        "kind": 1,
        "kind_label": "バトル",
        "cards": [101, 106, 107, 108, 110, 111, 118, 119, 1363, 1364, 141],
        "reward_cards": {10500: 110, 12800: 111},
        "extra_reward_points": [11000, 12000, 13500, 14700, 15800, 17000, 17900, 18600, 19300],
    },
    {
        "month": 6,
        "slot": 5,
        "local_index": 35,
        "event_index": 54,
        "title": "生徒会長再任選挙・第三部 暗黒文化祭",
        "kind": 0,
        "kind_label": "収拾",
        "cards": [102, 109, 112, 116, 1366, 140, 190, 207, 243],
        "reward_cards": {10500: 116, 12800: 112},
        "extra_reward_points": [11000, 12400, 14100, 15800, 17300, 18600, 19300],
    },
    {
        "month": 7,
        "slot": 5,
        "local_index": 41,
        "event_index": 55,
        "title": "帰宅部争奪戦",
        "kind": 1,
        "kind_label": "バトル",
        "cards": [483, 821, 1357, 1359, 1360, 1367, 1368],
        "reward_cards": {10500: 483, 12800: 821, 15000: 1357, 20000: 1359},
        "extra_reward_points": [11000, 14100, 15800],
    },
]


def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932").replace("\r\n", "\n")


def write_cp932(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


def remove_marked_blocks(text: str, prefix: str) -> str:
    pattern = re.compile(
        rf"(?m)^; {re.escape(prefix)}_BEGIN\n.*?^; {re.escape(prefix)}_END\n?",
        re.DOTALL,
    )
    return pattern.sub("", text)


def event_title_block(event: dict) -> str:
    marker = "MAIN_STORY_HOME_CLUB" if event["title"] == "帰宅部争奪戦" else "MAIN_STORY_ELECTION"
    display_slot = 104 if event["month"] == 7 else 105
    return "\n".join(
        [
            f"; {marker}_{event['month']}_MONTH_BEGIN",
            f"\tTSTR:{display_slot} = \"{event['title']}\"",
            f"\tTFLAG:{display_slot} = {event['kind']}\t;{event['kind_label']}",
            f"; {marker}_{event['month']}_MONTH_END",
        ]
    )


def pickup_block(event: dict) -> str:
    lines = [
        f"; MAIN_STORY_ELECTION_PICKUP_{event['local_index']}_BEGIN",
        f"CASE {event['local_index']}\t;{event['month']}月[{event['slot']}] {event['title']}",
    ]
    lines.extend(f"\tGLOBAL:{2200 + i} = {card}" for i, card in enumerate(event["cards"]))
    lines.append(f"\tGLOBAL:2199 = {len(event['cards'])}")
    lines.append(f"; MAIN_STORY_ELECTION_PICKUP_{event['local_index']}_END")
    return "\n".join(lines)


ITEM_REWARDS = {
    1300: (1, 3, "おにぎり×3"),
    3500: (3, 2, "ドーナッツ×2"),
    7400: (2, 1, "カレー×1"),
    10500: (8, 20, "ダイヤ×20"),
    12800: (6, 3, "シルバー×3"),
    15000: (7, 1, "ゴールド×1"),
    20000: (8, 40, "ダイヤ×40"),
}


def reward_block(template: str, event: dict) -> str:
    lines = template.splitlines()
    header = f"CASE 22\t;4月[4] 青春＊さわやか淑女修行"
    replacement = f"CASE {event['local_index']}\t;{event['month']}月[{event['slot']}] {event['title']}"
    if header not in lines:
        raise SystemExit("reward template header not found")
    lines[lines.index(header)] = replacement

    card_positions = []
    for index, line in enumerate(lines):
        match = re.match(r"\s*GLOBAL:31(\d+) = 9\s*$", line)
        if match:
            suffix = match.group(1)
            if index + 1 >= len(lines):
                raise SystemExit("reward card value line is missing")
            card_positions.append((index, suffix))
    if len(card_positions) != 7:
        raise SystemExit(f"reward template card count mismatch: {len(card_positions)}")
    original_card_type_indices = {type_index for type_index, _ in card_positions}

    for type_index, suffix in card_positions:
        comment_index = type_index - 1
        point_match = re.search(r"GLOBAL:30\d+ = (\d+)", lines[comment_index])
        if not point_match:
            raise SystemExit("reward point line is missing")
        point = int(point_match.group(1))
        card_id = event.get("reward_cards", {}).get(point)
        if card_id is not None:
            lines[comment_index] = re.sub(
                r";.*$", f";[関連カード] No.{card_id}", lines[comment_index]
            )
            lines[type_index + 1] = re.sub(
                r"= \d+\s*$", f"= {card_id}", lines[type_index + 1]
            )
            continue

        item_type, quantity, label = ITEM_REWARDS[point]
        lines[comment_index] = re.sub(r";.*$", f";{label}", lines[comment_index])
        lines[type_index] = re.sub(r"= \d+\s*$", f"= {item_type}", lines[type_index])
        lines[type_index + 1] = re.sub(
            r"= \d+\s*$", f"= {quantity}", lines[type_index + 1]
        )

    # Keep every event card obtainable as a point reward.  The regular table
    # has only the conventional seven card slots, so replace selected item
    # rows from 10,000pt onward with the remaining related cards.  The points
    # are deliberately spread across the high-point section rather than
    # placing all extra cards next to one another.
    reward_card_ids = set(event.get("reward_cards", {}).values())
    extra_cards = [card for card in event["cards"] if card not in reward_card_ids]
    item_positions_by_point = {}
    for type_index, line in enumerate(lines):
        if type_index in original_card_type_indices:
            continue
        if not re.match(r"\s*GLOBAL:31\d+ = \d+\s*$", line):
            continue
        comment_index = type_index - 1
        point_match = re.search(r"GLOBAL:30\d+ = (\d+)", lines[comment_index])
        if point_match and int(point_match.group(1)) >= 10700:
            item_positions_by_point[int(point_match.group(1))] = type_index
    extra_points = event.get("extra_reward_points", [])
    if len(extra_points) != len(extra_cards):
        raise SystemExit(
            f"extra reward point count mismatch: {len(extra_points)} != {len(extra_cards)}"
        )
    missing_points = [point for point in extra_points if point not in item_positions_by_point]
    if missing_points:
        raise SystemExit(
            f"high-point item reward slots are missing: {missing_points}"
        )
    for point, card_id in zip(extra_points, extra_cards):
        type_index = item_positions_by_point[point]
        comment_index = type_index - 1
        lines[comment_index] = re.sub(
            r";.*$", f";[関連カード] No.{card_id}", lines[comment_index]
        )
        lines[type_index] = re.sub(r"= \d+\s*$", "= 9", lines[type_index])
        lines[type_index + 1] = re.sub(
            r"= \d+\s*$", f"= {card_id}", lines[type_index + 1]
        )
    return "\n".join(lines)


def insert_once(text: str, anchor: str, block: str, label: str) -> str:
    if text.count(anchor) != 1:
        raise SystemExit(f"{label}: anchor count is {text.count(anchor)}")
    return text.replace(anchor, block + "\n" + anchor, 1)


def update_month_titles(text: str) -> str:
    month_start = text.index("@LOAD_MONTH_EVENTS")
    pickup_start = text.index("@LOAD_EVENT_PICKUP_CARDS", month_start)
    month_region = text[month_start:pickup_start]
    for event in EVENTS:
        marker = "MAIN_STORY_HOME_CLUB" if event["title"] == "帰宅部争奪戦" else "MAIN_STORY_ELECTION"
        marker_prefix = f"{marker}_{event['month']}_MONTH"
        month_region = remove_marked_blocks(month_region, marker_prefix)
        if event["month"] == 4:
            anchor = '\tTFLAG:104 = 4\t;親愛度\n\tRETURN 5'
        elif event["month"] == 5:
            anchor = '\tTFLAG:104 = 3\t;すごろく\n\tRETURN 5'
        elif event["month"] == 6:
            anchor = '\tTFLAG:104 = 2\t;宝探し\n\tRETURN 5'
        elif event["month"] == 7:
            anchor = '\tTFLAG:103 = 1\t;バトル\n\tRETURN 4'
        else:
            raise SystemExit("unexpected main-story month")
        base_return = {4: 5, 5: 5, 6: 5, 7: 4}[event["month"]]
        replacement = anchor.replace(
            f"\n\tRETURN {base_return}",
            "\n" + event_title_block(event) + f"\n\tRETURN {base_return + 1}",
        )
        case_start = month_region.index(f"CASE {event['month']}\n")
        case_end = month_region.find("\nCASE ", case_start + 1)
        if case_end < 0:
            case_end = len(month_region)
        case_region = month_region[case_start:case_end]
        # When rerunning, remove_marked_blocks leaves the added CASE's
        # previous RETURN 6 behind; restore the original month return before
        # inserting the marked block again.
        case_region = re.sub(
            r"\n\tRETURN [56]", f"\n\tRETURN {base_return}", case_region, count=1
        )
        if case_region.count(anchor) != 1:
            raise SystemExit(
                f"month {event['month']}: insertion anchor count is {case_region.count(anchor)}"
            )
        case_region = case_region.replace(anchor, replacement, 1)
        month_region = month_region[:case_start] + case_region + month_region[case_end:]
    return text[:month_start] + month_region + text[pickup_start:]


def update_pickups(text: str) -> str:
    pickup_start = text.index("@LOAD_EVENT_PICKUP_CARDS")
    reward_start = text.index("@LOAD_EVENT_REWARDS", pickup_start)
    pickup_region = text[pickup_start:reward_start]
    for event in EVENTS:
        pickup_region = remove_marked_blocks(
            pickup_region, f"MAIN_STORY_ELECTION_PICKUP_{event['local_index']}"
        )
    anchors = {23: "CASE 24\t;5月[0] CHEER!!立夏の校内合宿", 29: "CASE 30\t;6月[0] 雨模様＊あの日の空と愛の傘", 35: "CASE 36\t;7月[0] 夏盛り＊浴衣姿でお祭り騒ぎ！", 41: "CASE 42\t;8月[0] 夢うつつ＊満月の下でお泊まり会"}
    for event in EVENTS:
        pickup_region = insert_once(
            pickup_region,
            anchors[event["local_index"]],
            pickup_block(event),
            f"pickup {event['title']}",
        )
    return text[:pickup_start] + pickup_region + text[reward_start:]


def update_rewards(text: str) -> str:
    reward_start = text.index("@LOAD_EVENT_REWARDS")
    next_function = text.index("@EVENT_BOARD_GET_EVENT_INDEX", reward_start)
    reward_region = text[reward_start:next_function]
    reward_header = "CASE 22\t;4月[4] 青春＊さわやか淑女修行"
    template_start = reward_region.index(reward_header)
    template_end = reward_region.index("\nCASE ", template_start + 1)
    template = reward_region[template_start:template_end]
    # Older reruns could leave an orphaned marker immediately after the
    # template.  Never carry registration markers into the next template.
    template = re.sub(
        r"(?m)^; MAIN_STORY_ELECTION_REWARD_\d+_(?:BEGIN|END)\n?", "", template
    ).rstrip()
    for event in EVENTS:
        reward_region = remove_marked_blocks(
            reward_region, f"MAIN_STORY_ELECTION_REWARD_{event['local_index']}"
        )
    anchors = {23: "CASE 24\t;5月[0] CHEER!!立夏の校内合宿", 29: "CASE 30\t;6月[0] 雨模様＊あの日の空と愛の傘", 35: "CASE 36\t;7月[0] 夏盛り＊浴衣姿でお祭り騒ぎ！", 41: "CASE 42\t;8月[0] 夢うつつ＊満月の下でお泊まり会"}
    for event in EVENTS:
        block = "\n".join(
            [
                f"; MAIN_STORY_ELECTION_REWARD_{event['local_index']}_BEGIN",
                reward_block(template, event),
                f"; MAIN_STORY_ELECTION_REWARD_{event['local_index']}_END",
            ]
        )
        reward_region = insert_once(
            reward_region,
            anchors[event["local_index"]],
            block,
            f"reward {event['title']}",
        )
    return text[:reward_start] + reward_region + text[next_function:]


def update_event_index(text: str) -> str:
    start = text.index("@EVENT_BOARD_GET_EVENT_INDEX")
    end = text.index("@EVENT_BOARD_IS_EVENT_CARD", start)
    region = text[start:end]
    region = region.replace("イベント通し番号(0-51)", "イベント通し番号(0-55)", 1)
    region = region.replace("イベント通し番号(0-54)", "イベント通し番号(0-55)", 1)
    replacement = """CASE 4
\tIF FLAG:68 == 5
\t\tRETURN 52
\tENDIF
\tRETURN 12 + FLAG:68
CASE 5
\tIF FLAG:68 == 5
\t\tRETURN 53
\tENDIF
\tRETURN 17 + FLAG:68
CASE 6
\tIF FLAG:68 == 5
\t\tRETURN 54
\tENDIF
\tRETURN 22 + FLAG:68
CASE 7
\tIF FLAG:68 == 5
\t\tRETURN 55
\tENDIF
\t;旧7月の欠番は8月の物語IDへ流さない。
\tSIF FLAG:68 == 4
\t\tRETURN -1
\tRETURN 27 + FLAG:68
"""
    region, count = re.subn(
        r"(?m)^CASE 4\n.*?(?=^CASE 8\n)",
        replacement,
        region,
        flags=re.MULTILINE | re.DOTALL,
        count=1,
    )
    if count != 1:
        raise SystemExit("event index block replacement failed")
    return text[:start] + region + text[end:]


def card_case_values(region: str) -> set[int]:
    values: set[int] = set()
    for match in re.finditer(r"(?m)^CASE ([0-9, ]+)", region):
        values.update(int(value) for value in match.group(1).split(","))
    return values


def update_event_card_contracts(text: str) -> str:
    all_cards = [card for event in EVENTS for card in event["cards"]]
    unique_cards = list(dict.fromkeys(all_cards))
    is_start = text.index("@EVENT_BOARD_IS_EVENT_CARD")
    source_start = text.index("@EVENT_BOARD_GET_CARD_SOURCE", is_start)
    is_region = text[is_start:source_start]
    is_region = remove_marked_blocks(is_region, "MAIN_STORY_ELECTION_EVENT_CARD")
    missing = [card for card in unique_cards if card not in card_case_values(is_region)]
    if missing:
        block = "\n".join(
            [
                "; MAIN_STORY_ELECTION_EVENT_CARD_BEGIN",
                "CASE " + ", ".join(str(card) for card in missing),
                "\tRETURN 1",
                "; MAIN_STORY_ELECTION_EVENT_CARD_END",
            ]
        )
        anchor = "\nCASE "
        position = is_region.index(anchor)
        is_region = is_region[:position] + "\n" + block + is_region[position:]

    source_end = text.index("ENDSELECT\nRETURN 0", source_start) + len("ENDSELECT\nRETURN 0")
    source_region = text[source_start:source_end]
    source_region = remove_marked_blocks(source_region, "MAIN_STORY_ELECTION_CARD_SOURCE")
    source_cases = []
    for event in EVENTS:
        source_cases.extend(
            [
                f"CASE {', '.join(str(card) for card in event['cards'])}",
                f"\tRESULTS = \"イベント「{event['title']}」\"",
                "\tRETURN 1",
            ]
        )
    source_block = "\n".join(
        [
            "; MAIN_STORY_ELECTION_CARD_SOURCE_BEGIN",
            *source_cases,
            "; MAIN_STORY_ELECTION_CARD_SOURCE_END",
        ]
    )
    anchor = "\nCASE "
    position = source_region.index(anchor)
    source_region = source_region[:position] + "\n" + source_block + source_region[position:]

    return text[:is_start] + is_region + text[source_start:source_start] + source_region + text[source_end:]


def main() -> None:
    text = read_cp932(DATA)
    text = text.replace(
        "; 月別イベントリスト（event_card_list.txtより生成）",
        "; 月別イベントリスト（event_card_list.txt + main_story_election_event_cards.mdより生成）",
        1,
    )
    text = update_month_titles(text)
    text = update_pickups(text)
    text = update_rewards(text)
    text = update_event_index(text)
    text = update_event_card_contracts(text)
    write_cp932(DATA, text)
    print("registered 4 main-story events and 36 event cards")


if __name__ == "__main__":
    main()
