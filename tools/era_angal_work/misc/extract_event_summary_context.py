#!/usr/bin/env python3
"""イベント要約作成用に、シナリオ範囲から導入と結末を簡潔に抽出する。"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MAPPING_PATH = ROOT / "tools" / "event_scenario_mapping.md"
SCENARIO_DIR = ROOT / "tools" / "scenarios"

ROW_RE = re.compile(
    r"^\| (?P<title>[^|]+?) \| (?P<start>\d+)～(?P<end>\d+) \| (?P<confidence>高|中) \|$"
)
SPEECH_RE = re.compile(r"^【(?P<speaker>[^】]*)】(?P<text>.*)$")


def load_mapping() -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    month = 0
    for line in MAPPING_PATH.read_text(encoding="utf-8").splitlines():
        month_match = re.match(r"^## (\d+)月$", line)
        if month_match:
            month = int(month_match.group(1))
            continue
        row_match = ROW_RE.match(line)
        if row_match:
            events.append(
                {
                    "month": month,
                    "title": row_match.group("title").strip(),
                    "start": int(row_match.group("start")),
                    "end": int(row_match.group("end")),
                    "confidence": row_match.group("confidence"),
                }
            )
    return events


def load_speeches(scenario_id: int) -> list[tuple[str, str]]:
    path = SCENARIO_DIR / f"{scenario_id}.txt"
    speeches: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = SPEECH_RE.match(line)
        if not match:
            continue
        text = match.group("text").strip().strip("「」")
        if text:
            speeches.append((match.group("speaker") or "地の文", text))
    return speeches


def shorten(text: str, limit: int = 72) -> str:
    text = re.sub(r"\s+", " ", text)
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def print_event(event: dict[str, object], sample_count: int | None = None) -> None:
    start = int(event["start"])
    end = int(event["end"])
    speaker_counts: Counter[str] = Counter()
    rows: list[tuple[int, str, str]] = []

    for scenario_id in range(start, end + 1):
        speeches = load_speeches(scenario_id)
        speaker_counts.update(speaker for speaker, _ in speeches)
        if not speeches:
            rows.append((scenario_id, "（台詞なし）", "（台詞なし）"))
            continue
        first = f"{speeches[0][0]}: {shorten(speeches[0][1])}"
        last = f"{speeches[-1][0]}: {shorten(speeches[-1][1])}"
        rows.append((scenario_id, first, last))

    print(
        f"## {event['title']} "
        f"({start}～{end}, 確度{event['confidence']})"
    )
    print("主要話者:", "、".join(name for name, _ in speaker_counts.most_common(12)))
    display_rows = rows
    if sample_count == 1 and rows:
        display_rows = [rows[0]]
    elif sample_count and len(rows) > sample_count:
        indexes = {
            round(index * (len(rows) - 1) / (sample_count - 1))
            for index in range(sample_count)
        }
        display_rows = [row for index, row in enumerate(rows) if index in indexes]

    for scenario_id, first, last in display_rows:
        print(f"- {scenario_id}: 導入={first} / 終端={last}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", type=int, help="1～12の開催月")
    parser.add_argument("--title", help="イベント名の一部")
    parser.add_argument(
        "--samples",
        type=int,
        help="イベントごとに等間隔で表示するシナリオ数",
    )
    args = parser.parse_args()

    events = load_mapping()
    if args.month:
        events = [event for event in events if event["month"] == args.month]
    if args.title:
        events = [event for event in events if args.title in str(event["title"])]

    if not events:
        raise SystemExit("該当イベントがありません")

    for event in events:
        print_event(event, args.samples)


if __name__ == "__main__":
    main()
