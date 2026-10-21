from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_33_柊るな_COM.ERB"


def indent_of(line: str) -> int:
    return len(line) - len(line.lstrip("\t "))


def branch_body(lines: list[str], start: int, branch_indent: int) -> tuple[str, ...]:
    body: list[str] = []
    for line in lines[start + 1 :]:
        stripped = line.strip()
        current_indent = indent_of(line)
        if current_indent == branch_indent and (
            re.fullmatch(r"ELSEIF A == 1", stripped)
            or stripped == "ELSE"
            or stripped == "ENDIF"
        ):
            break
        if stripped.startswith("PRINTFORM"):
            body.append(stripped)
    return tuple(body)


def main() -> None:
    text = TARGET.read_text(encoding="cp932")
    lines = text.splitlines()
    command = None
    rand_number = 0
    rand_line = 0
    group_number: dict[tuple[int, int], int] = {}
    for index, line in enumerate(lines):
        command_match = re.match(r"\s*(?:IF|ELSEIF) SELECTCOM == (\d+)", line)
        if command_match:
            command = int(command_match.group(1))
        if re.search(r"\bA\s*=\s*RAND:3\b", line):
            rand_number += 1
            rand_line = index + 1
        branch_match = re.match(r"(\s*)IF A == 0\s*$", line)
        if not branch_match or command is None or rand_number == 0:
            continue
        branch_indent = len(branch_match.group(1))
        values = {"A0": branch_body(lines, index, branch_indent)}
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
        for name in ("A1", "A2"):
            if name in branch_indexes:
                values[name] = branch_body(lines, branch_indexes[name], branch_indent)
        if len(values) == 3:
            key = (command, rand_line)
            group_number[key] = group_number.get(key, 0) + 1
            if len(set(values.values())) < 3:
                print(f"COM{command} RAND line {rand_line} group {group_number[key]}")
                for name, value in values.items():
                    print(f"  {name}: {' | '.join(value)}")
                print("  *** DUPLICATE BRANCH CONTENT ***")


if __name__ == "__main__":
    main()
