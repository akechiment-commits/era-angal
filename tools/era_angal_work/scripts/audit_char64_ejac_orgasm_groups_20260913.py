"""CHAR64しおんの射精・絶頂フックを関数単位で分け、RAND:3の類似枝を監査する。"""

from __future__ import annotations

import re
import sys
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_64_峰山しおん_COM.ERB"
LABELS = (
    "@CHAR_EJAC_64",
    "@CHAR_EJAC_MOUTH_64",
    "@CHAR_EJAC_IN_64",
    "@CHAR_ORGASM_64",
)


def normalize(text: str) -> str:
    text = re.sub(r"%[^%]+%", "%X%", text)
    return re.sub(r"[「」。、！？…・ー～〜\s]", "", text)


def speech(lines: list[str]) -> str:
    values = []
    for line in lines:
        if "PRINTFORM" in line:
            values.append(line.split("PRINTFORM", 1)[1].strip())
    return " ".join(values)


def find_groups(lines: list[str], start: int, end: int) -> list[dict[str, object]]:
    groups = []
    i = start
    while i < end:
        if lines[i].strip() != "IF A == 0":
            i += 1
            continue
        indent = len(lines[i]) - len(lines[i].lstrip())
        branches = [(i, 0)]
        j = i + 1
        while j < end:
            stripped = lines[j].strip()
            candidate_indent = len(lines[j]) - len(lines[j].lstrip())
            if candidate_indent == indent and stripped == "ELSEIF A == 1":
                branches.append((j, 1))
            elif candidate_indent == indent and stripped == "ELSE":
                branches.append((j, 2))
            elif candidate_indent == indent and stripped == "ENDIF":
                break
            j += 1
        if len(branches) == 3 and j < end:
            values = []
            for position, (branch_start, branch) in enumerate(branches):
                branch_end = branches[position + 1][0] if position + 1 < len(branches) else j
                values.append(speech(lines[branch_start + 1:branch_end]))
            ratios = [
                SequenceMatcher(None, normalize(values[left]), normalize(values[right])).ratio()
                for left in range(3)
                for right in range(left + 1, 3)
            ]
            groups.append({"line": i + 1, "values": values, "ratio": max(ratios)})
        i = max(i + 1, j + 1)
    return groups


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    lines = TARGET.read_bytes().decode("cp932").splitlines()
    label_positions = {label: lines.index(label) for label in LABELS}
    sections = []
    for index, label in enumerate(LABELS):
        start = label_positions[label]
        end = label_positions[LABELS[index + 1]] if index + 1 < len(LABELS) else next(
            (i for i in range(start + 1, len(lines)) if lines[i].startswith("@TRAIN_MESSAGE_B280_64")),
            len(lines),
        )
        groups = find_groups(lines, start, end)
        sections.append((label, groups))

    print("CHAR64_EJAC_ORGASM_RAND3_AUDIT")
    print(f"FUNCTIONS={len(sections)}")
    print(f"RAND3_GROUPS={sum(len(groups) for _, groups in sections)}")
    print("GROUPS_WITH_SIMILARITY_GE_045")
    for label, groups in sections:
        for group in groups:
            if float(group["ratio"]) < 0.45:
                continue
            print(f"{label} line={group['line']} max_similarity={float(group['ratio']):.3f}")
            for branch, value in enumerate(group["values"]):
                print(f"  A{branch}: {value}")
    print("SECTION_SUMMARY")
    for label, groups in sections:
        literary = sum(
            any(re.search(r"文学|物語|文献|書誌|章|頁|精読|記録|連載|作家|詩|図像|観察席", value) for value in group["values"])
            for group in groups
        )
        print(f"{label}\tgroups={len(groups)}\tliterary_groups={literary}")


if __name__ == "__main__":
    main()
