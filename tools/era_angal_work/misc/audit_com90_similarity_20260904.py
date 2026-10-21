"""COM90のキャラ内・キャラ間の近似台詞を監査する。"""

from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_koujo_integrity import char_files, char_number, extract_blocks, read_cp932  # noqa: E402


def dialogue_prints(path: Path) -> list[str]:
    block = extract_blocks(read_cp932(path)).get(90)
    if block is None:
        return []
    dialogues: list[str] = []
    pending: str | None = None
    for line in block.lines:
        if line.lstrip().startswith("PRINTFORML"):
            if pending is not None:
                dialogues.append(pending)
            pending = re.sub(r"^PRINTFORML\s*", "", line.strip(), flags=re.I)
        elif line.lstrip().startswith("PRINTFORMW"):
            value = re.sub(r"^PRINTFORM(?:L|W)?\s*", "", line.strip(), flags=re.I)
            if pending is not None:
                dialogues.append(pending + value)
                pending = None
            else:
                dialogues.append(value)
    if pending is not None:
        dialogues.append(pending)
    return dialogues


def normalize(line: str) -> str:
    value = line
    for token in ("PRINTFORMW", "PRINTFORML", "「", "」", "…", "♪", "☆", "っ", "～"):
        value = value.replace(token, "")
    return value.replace(" ", "").replace("　", "")


def main() -> int:
    rows = [(char_number(path), path, dialogue_prints(path)) for path in char_files() if char_number(path) != 27]
    rows = [(number, path, lines) for number, path, lines in rows if lines]
    print("COM90対象:", len(rows), "CHAR")
    print("枝数:", ", ".join(f"CHAR{n:02d}={len(lines)}" for n, _, lines in rows))
    candidates: list[tuple[float, str, str]] = []
    for number, _, lines in rows:
        normalized = [normalize(line) for line in lines]
        for first in range(len(normalized)):
            for second in range(first + 1, len(normalized)):
                ratio = SequenceMatcher(None, normalized[first], normalized[second]).ratio()
                if ratio >= 0.65:
                    candidates.append((ratio, f"CHAR{number:02d}枝{first + 1}", f"CHAR{number:02d}枝{second + 1}"))
    for first_index, (number_a, _, lines_a) in enumerate(rows):
        for number_b, _, lines_b in rows[first_index + 1 :]:
            for index_a, line_a in enumerate(lines_a):
                for index_b, line_b in enumerate(lines_b):
                    ratio = SequenceMatcher(None, normalize(line_a), normalize(line_b)).ratio()
                    if ratio >= 0.72:
                        candidates.append((ratio, f"CHAR{number_a:02d}枝{index_a + 1}", f"CHAR{number_b:02d}枝{index_b + 1}"))
    candidates.sort(reverse=True)
    print("近似候補:", len(candidates))
    for ratio, first, second in candidates[:120]:
        print(f"{ratio:.3f} {first} / {second}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
