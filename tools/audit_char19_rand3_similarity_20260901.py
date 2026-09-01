"""CHAR19のRAND3枝を、同一関係内で近似しすぎていないか確認する。"""

from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_19_猫塚みけ_COM.ERB"
THRESHOLD = 0.45
SIMPLE_TARGETS = {
    4, 7, 8, 9, 10, 18, 19, 26, 27, 28, 29, 35, 37, 38, 39, 42, 43,
    45, 46, 53, 54, 56, 57, 58, 59, 60, 61, 63, 65, 66, 67, 68, 69, 71,
    75, 80, 85, 90, 110, 130, 131, 132, 160, 181, 182, 183, 184, 185,
    186, 187, 188, 189, 196, 197, 198, 199, 200, 201, 203, 204, 205,
    255, 256, 257, 390,
}
EQUIP_TARGETS = {11, 13, 14, 15, 16, 17}


def command_blocks(lines: list[str]):
    starts = [
        i for i, line in enumerate(lines)
        if re.match(r"^(?:IF|ELSEIF) SELECTCOM == \d+\s*$", line.strip())
    ]
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        match = re.search(r"SELECTCOM == (\d+)", lines[start])
        if match:
            yield int(match.group(1)), lines[start:end]


def simple_variants(block: list[str]):
    found = []

    try:
        lover_start = next(i for i, line in enumerate(block) if line.strip().startswith("IF TALENT:TARGET:"))
        normal_start = next(
            i for i, line in enumerate(block[lover_start + 1:], lover_start + 1)
            if line.strip() == "ELSE" and i > 0 and block[i - 1].strip() == "ENDIF"
        )
    except StopIteration:
        return found

    def parse_relation(name: str, start: int, end: int) -> None:
        markers = []
        for i in range(start, end):
            stripped = block[i].strip()
            if stripped == "IF A == 0":
                markers.append((i, 0))
            elif stripped == "ELSEIF A == 1":
                markers.append((i, 1))
            elif stripped == "ELSE" and markers:
                markers.append((i, 2))
        for pos, (marker, branch) in enumerate(markers):
            limit = markers[pos + 1][0] if pos + 1 < len(markers) else end
            prints = [
                line.strip()
                for line in block[marker + 1:limit]
                if re.match(r"^\s*PRINTFORM(?:L|W)?\b", line, re.I)
            ]
            if prints:
                found.append((name, branch, " ".join(prints)))

    parse_relation("恋人", lover_start, normal_start)
    parse_relation("通常", normal_start, len(block))
    return found


def dialogue_lines(block: list[str]) -> list[str]:
    return [
        line.strip()
        for line in block
        if "「" in line and re.match(r"^\s*PRINTFORM(?:L|W)?\b", line, re.I)
    ]


def normalize(text: str) -> str:
    text = re.sub(r"PRINTFORM\w*", "", text)
    text = re.sub(r"%[^%]+%", "", text)
    text = text.replace("あたし", "").replace("先輩", "").replace("おに～さん", "")
    text = re.sub(r"[「」♪☆。、！？…・ー～〜\s]", "", text)
    return text


def report_group(label: str, values: list[tuple[str, str]]) -> list[tuple]:
    results = []
    for i, (left_label, left) in enumerate(values):
        for right_label, right in values[i + 1:]:
            ratio = SequenceMatcher(None, normalize(left), normalize(right)).ratio()
            if ratio >= THRESHOLD:
                results.append((ratio, label, left_label, right_label, left, right))
    return results


def main() -> None:
    lines = TARGET.read_bytes().decode("cp932").splitlines()
    blocks = {command: block for command, block in command_blocks(lines)}
    results = []
    simple_count = 0
    equip_count = 0
    custom_count = 0

    for command, block in blocks.items():
        variants = simple_variants(block)
        expected = {(relation, branch) for relation in ("恋人", "通常") for branch in (0, 1, 2)}
        actual = {(relation, branch) for relation, branch, _ in variants}
        if command in SIMPLE_TARGETS and actual == expected and len(variants) == 6:
            simple_count += 1
            for relation in ("恋人", "通常"):
                group = [(f"A{branch}", text) for rel, branch, text in variants if rel == relation]
                results.extend(report_group(f"COM{command} {relation}", group))

        dialogue = dialogue_lines(block)
        if command in EQUIP_TARGETS and len(dialogue) == 12:
            equip_count += 1
            labels = ["装着恋人", "装着通常", "取り外し恋人", "取り外し通常"]
            for index, label in enumerate(labels):
                group = [(f"A{branch}", dialogue[index * 3 + branch]) for branch in range(3)]
                results.extend(report_group(f"COM{command} {label}", group))

    for first, last, label in ((280, 284, "独自浮気"), (410, 414, "独自純愛")):
        for command in range(first, last + 1):
            if command not in blocks:
                continue
            dialogue = dialogue_lines(blocks[command])
            if len(dialogue) != 6:
                continue
            custom_count += 1
            results.extend(report_group(
                f"COM{command} {label} 恋人",
                [(f"A{branch}", dialogue[branch]) for branch in range(3)],
            ))
            results.extend(report_group(
                f"COM{command} {label} 通常",
                [(f"A{branch}", dialogue[3 + branch]) for branch in range(3)],
            ))

    results.sort(reverse=True)
    print(f"単純RAND3検査: {simple_count}ブロック")
    print(f"装着系検査: {equip_count}ブロック")
    print(f"独自RAND3検査: {custom_count}ブロック")
    print(f"近似候補>={THRESHOLD:.2f}: {len(results)}件")
    for ratio, label, left_label, right_label, left, right in results:
        print(f"{label} {left_label}/{right_label} similarity={ratio:.3f}")
        print(f"  {left_label}: {left}")
        print(f"  {right_label}: {right}")
    if results:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
