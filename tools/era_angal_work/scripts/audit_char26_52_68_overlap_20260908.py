"""CHAR26/52/68 の同一COM内発話重複を監査する。"""

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


def normalize(value: str) -> str:
    value = re.sub(r"%[^%]+%", "", value)
    value = re.sub(r"\{[^{}]*\}", "", value)
    return re.sub(r"[「」。、！？…・ー～〜♪☆★\s]", "", value)


def commands(path: Path) -> dict[int, list[str]]:
    lines = path.read_bytes().decode("cp932").splitlines()
    found: dict[int, list[str]] = {}
    command = None
    pending = None
    for line in lines:
        heading = re.match(r"^;--- COM(\d+)", line)
        if heading:
            command = int(heading.group(1))
            found.setdefault(command, [])
            pending = None
            continue
        if command is None:
            continue
        stripped = line.strip()
        if re.match(r"^PRINTFORML\b", stripped, re.I):
            pending = re.sub(r"^PRINTFORML\s*", "", stripped, flags=re.I)
        elif re.match(r"^PRINTFORMW\b", stripped, re.I):
            value = re.sub(r"^PRINTFORMW\s*", "", stripped, flags=re.I)
            found[command].append((pending or "") + value)
            pending = None
        elif pending is not None and stripped and not stripped.startswith(";"):
            # PRINTFORML の続きが通常のコード行にまたがる書式は対象外。
            pending = None
    return found


def main() -> int:
    data = {number: commands(path) for number, path in FILES.items()}
    candidates = []
    for command in sorted(set.intersection(*(set(value) for value in data.values()))):
        for left_number, right_number in ((26, 52), (26, 68), (52, 68)):
            left = data[left_number][command]
            right = data[right_number][command]
            for left_index, left_value in enumerate(left):
                for right_index, right_value in enumerate(right):
                    ratio = SequenceMatcher(None, normalize(left_value), normalize(right_value)).ratio()
                    if ratio >= 0.80:
                        candidates.append((ratio, command, left_number, left_index, right_number, right_index, left_value, right_value))
    candidates.sort(reverse=True)
    print("command counts:", ", ".join(f"CHAR{number:02d}={len(value)}" for number, value in data.items()))
    print("candidates >= .80:", len(candidates))
    for ratio, command, left_number, left_index, right_number, right_index, left_value, right_value in candidates[:160]:
        print(f"{ratio:.3f} COM{command} CHAR{left_number:02d}A{left_index} / CHAR{right_number:02d}A{right_index}")
        print("  L:", left_value)
        print("  R:", right_value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
