"""CHAR26/52/68の各RAND:3枝内の内容近似を監査する。"""

from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
FILES = {
    26: ROOT / "ERB/CHAR/CHAR_26_堀田さあや_COM.ERB",
    52: ROOT / "ERB/CHAR/CHAR_52_湖南やこ_COM.ERB",
    68: ROOT / "ERB/CHAR/CHAR_68_深鳥ふみ_COM.ERB",
}


def indent(line: str) -> int:
    return len(line) - len(line.lstrip("\t "))


def clean(value: str) -> str:
    value = re.sub(r"%[^%]+%", "", value)
    return re.sub(r"[「」。、！？…・ー～〜♪☆★\s]", "", value)


def body(lines: list[str], start: int, level: int) -> str:
    values = []
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if indent(line) == level and stripped in {"ELSEIF A == 1", "ELSE", "ENDIF"}:
            break
        if stripped.upper().startswith("PRINTFORM"):
            values.append(stripped)
    return "".join(values)


def groups(path: Path) -> list[tuple[int, int, list[str]]]:
    lines = path.read_bytes().decode("cp932").splitlines()
    command = None
    results = []
    for index, line in enumerate(lines):
        heading = re.match(r"^;--- COM(\d+)", line)
        if heading:
            command = int(heading.group(1))
        if command is None or not re.search(r"\bA\s*=\s*RAND:3\b", line):
            continue
        for start in range(index + 1, min(index + 100, len(lines))):
            match = re.match(r"^(\s*)IF A == 0\s*$", lines[start])
            if not match:
                continue
            level = len(match.group(1))
            branches = [(start, body(lines, start, level))]
            for candidate in range(start + 1, min(start + 100, len(lines))):
                if indent(lines[candidate]) != level:
                    continue
                stripped = lines[candidate].strip()
                if stripped == "ELSEIF A == 1":
                    branches.append((candidate, body(lines, candidate, level)))
                elif stripped == "ELSE":
                    branches.append((candidate, body(lines, candidate, level)))
                    break
                elif stripped == "ENDIF":
                    break
            if len(branches) == 3 and all(value for _, value in branches):
                results.append((command, index + 1, [value for _, value in branches]))
            break
    return results


def main() -> int:
    all_results = []
    for number, path in FILES.items():
        found = groups(path)
        print(f"CHAR{number:02d}: RAND groups={len(found)}")
        for command, line, values in found:
            for left, right in ((0, 1), (0, 2), (1, 2)):
                ratio = SequenceMatcher(None, clean(values[left]), clean(values[right])).ratio()
                all_results.append((ratio, number, command, line, left, right, values[left], values[right]))
        for row in sorted((item for item in all_results if item[1] == number), reverse=True)[:8]:
            ratio, _, command, line, left, right, first, second = row
            print(f"  COM{command} line {line} A{left}/A{right} ratio={ratio:.3f}")
            print("   ", first)
            print("   ", second)
    high = sorted((item for item in all_results if item[0] >= 0.75), reverse=True)
    print(f"all internal pairs={len(all_results)}; >=.75={len(high)}; >=.80={sum(item[0] >= .80 for item in all_results)}; >=.85={sum(item[0] >= .85 for item in all_results)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
