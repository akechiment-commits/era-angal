"""2026-09-04に補完したRAND3 5枠の枝数と近似重複を検査する。"""

from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CASES = {
    30: ("ゆう", 17),
    44: ("ひよの", 17),
    45: ("れいか", 17),
    46: ("みづき", 17),
    67: ("ましろ", 90),
}
THRESHOLD = 0.45


def command_span(text: str, command: int) -> tuple[int, int]:
    marker = f";--- COM{command}"
    start = text.index(marker)
    next_heading = re.search(r"^;--- COM", text[start + len(marker):], re.MULTILINE)
    heading_end = start + len(marker) + next_heading.start() if next_heading else len(text)
    next_return = re.search(r"^RETURN 0\s*$", text[start:heading_end], re.MULTILINE)
    end = start + next_return.start() if next_return else heading_end
    return start, end


def prints(block: str) -> list[str]:
    return [
        line.strip() for line in block.splitlines()
        if "「" in line and re.match(r"^PRINTFORM(?:L|W)?\b", line.strip(), re.I)
    ]


def normalize(text: str) -> str:
    text = re.sub(r"%[^%]+%", "", text)
    return re.sub(r"[「」。、！？…・ー～〜\s]", "", text)


def main() -> int:
    failures = []
    for number, (name, command) in CASES.items():
        target = next(ROOT.glob(f"ERB/CHAR/CHAR_{number:02d}_*_COM.ERB"))
        text = target.read_bytes().decode("cp932")
        start, end = command_span(text, command)
        values = prints(text[start:end])
        expected = 12 if command == 17 else 6
        if len(values) != expected:
            raise RuntimeError(f"CHAR{number:02d} COM{command}: 台詞数 {len(values)} != {expected}")
        groups = (("装着恋人", 0), ("装着通常", 3), ("取り外し恋人", 6), ("取り外し通常", 9)) if command == 17 else (("恋人", 0), ("通常", 3))
        for label, offset in groups:
            group = values[offset:offset + 3]
            if len(group) != 3:
                raise RuntimeError(f"CHAR{number:02d} COM{command} {label}: RAND3枝不足")
            for left_index, left in enumerate(group):
                for right_index, right in enumerate(group[left_index + 1:], left_index + 1):
                    ratio = SequenceMatcher(None, normalize(left), normalize(right)).ratio()
                    if ratio >= THRESHOLD:
                        failures.append((ratio, number, command, label, left_index, right_index, left, right))
        print(f"CHAR{number:02d} {name} COM{command}: {len(values)}枝確認")
    failures.sort(reverse=True)
    print(f"近似候補>={THRESHOLD:.2f}: {len(failures)}件")
    for ratio, number, command, label, left_index, right_index, left, right in failures:
        print(f"CHAR{number:02d} COM{command} {label} A{left_index}/A{right_index} similarity={ratio:.3f}")
        print(f"  A{left_index}: {left}")
        print(f"  A{right_index}: {right}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
