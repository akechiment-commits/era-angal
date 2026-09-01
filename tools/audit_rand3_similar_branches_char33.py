from __future__ import annotations

import re
import sys
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_33_柊るな_COM.ERB"
PAIR_NAMES = (("A0", "A1"), ("A0", "A2"), ("A1", "A2"))


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip("\t "))


def branch_body(lines: list[str], start: int, branch_indent: int) -> tuple[str, ...]:
    body: list[str] = []
    for line in lines[start + 1 :]:
        stripped = line.strip()
        current_indent = indent_of(line)
        if current_indent == branch_indent and (
            stripped == "ELSEIF A == 1" or stripped == "ELSE" or stripped == "ENDIF"
        ):
            break
        if stripped.startswith("PRINTFORM"):
            body.append(stripped)
    return tuple(body)


def clean(text: str) -> str:
    text = re.sub(r"^PRINTFORM[LMW]?\s*", "", text)
    return re.sub(r"[\s「」。、，．！？!?♪☆…～〜ー・（）()]", "", text)


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    lines = TARGET.read_text(encoding="cp932").splitlines()
    command: int | None = None
    rand_line = 0
    groups: dict[tuple[int, int], int] = {}
    results: list[tuple[float, int, int, int, str, str, str]] = []
    for index, line in enumerate(lines):
        command_match = re.match(r"\s*(?:IF|ELSEIF) SELECTCOM == (\d+)", line)
        if command_match:
            command = int(command_match.group(1))
        if re.search(r"\bA\s*=\s*RAND:3\b", line):
            rand_line = index + 1
        branch_match = re.match(r"(\s*)IF A == 0\s*$", line)
        if not branch_match or command is None or rand_line == 0:
            continue
        branch_indent = len(branch_match.group(1))
        branch_indexes: dict[str, int] = {}
        for candidate_index in range(index + 1, len(lines)):
            candidate = lines[candidate_index]
            candidate_indent = indent_of(candidate)
            stripped = candidate.strip()
            if candidate_indent < branch_indent:
                break
            if candidate_indent != branch_indent:
                continue
            if stripped == "ELSEIF A == 1":
                branch_indexes["A1"] = candidate_index
            elif stripped == "ELSE":
                branch_indexes["A2"] = candidate_index
                break
            elif stripped == "ENDIF":
                break
        if set(branch_indexes) != {"A1", "A2"}:
            continue
        values = {
            "A0": branch_body(lines, index, branch_indent),
            "A1": branch_body(lines, branch_indexes["A1"], branch_indent),
            "A2": branch_body(lines, branch_indexes["A2"], branch_indent),
        }
        key = (command, rand_line)
        groups[key] = groups.get(key, 0) + 1
        group = groups[key]
        for left, right in PAIR_NAMES:
            left_text = " ".join(values[left])
            right_text = " ".join(values[right])
            left_clean = clean(left_text)
            right_clean = clean(right_text)
            if not left_clean or not right_clean:
                continue
            matcher = SequenceMatcher(None, left_clean, right_clean)
            ratio = matcher.ratio()
            block = max(matcher.get_matching_blocks(), key=lambda item: item.size)
            common = left_clean[block.a : block.a + block.size]
            if ratio >= 0.56 and block.size >= 12:
                results.append((ratio, block.size, command, rand_line, group, f"{left}/{right}", common))
    for ratio, block_size, command, rand_line, group, pair, common in sorted(results, reverse=True):
        print(
            f"COM{command} line {rand_line} group {group} {pair} "
            f"ratio={ratio:.3f} common={block_size}: {common}"
        )


if __name__ == "__main__":
    main()
