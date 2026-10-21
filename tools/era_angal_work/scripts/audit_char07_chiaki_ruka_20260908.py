"""CHAR07の人格汚染、CHAR09との同一COM重複、RAND枝重複を再監査する。"""

from difflib import SequenceMatcher
from pathlib import Path
import re

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from audit_koujo_integrity import extract_blocks, read_cp932  # noqa: E402


CHIAKI_COM = ROOT / "ERB/CHAR/CHAR_07_高原ちあき_COM.ERB"
CHIAKI_BASE = ROOT / "ERB/CHAR/CHAR_07_高原ちあき.ERB"
RUKA_COM = ROOT / "ERB/CHAR/CHAR_09_月永るか_COM.ERB"


def dialogue_values(path: Path) -> dict[int, list[str]]:
    result: dict[int, list[str]] = {}
    for command, block in extract_blocks(read_cp932(path)).items():
        values: list[str] = []
        pending: str | None = None
        for line in block.lines:
            stripped = line.strip()
            if stripped.upper().startswith("PRINTFORML"):
                if pending is not None:
                    values.append(pending)
                pending = re.sub(r"^PRINTFORML\s*", "", stripped, flags=re.I)
            elif stripped.upper().startswith("PRINTFORMW"):
                value = re.sub(r"^PRINTFORMW\s*", "", stripped, flags=re.I)
                if pending is not None:
                    values.append(pending + value)
                    pending = None
                else:
                    values.append(value)
        if pending is not None:
            values.append(pending)
        result[command] = values
    return result


def normalize(value: str) -> str:
    value = re.sub(r"%[^%]+%", "", value)
    return re.sub(r"[「」。、，．！？!?♪☆…～〜ー・（）()\s]", "", value)


def main() -> None:
    chiaki = dialogue_values(CHIAKI_COM)
    ruka = dialogue_values(RUKA_COM)
    pair_ratios: list[tuple[float, int, int, int, str, str]] = []
    for command in sorted(set(chiaki) & set(ruka)):
        for chiaki_index, chiaki_line in enumerate(chiaki[command], 1):
            for ruka_index, ruka_line in enumerate(ruka[command], 1):
                left = normalize(chiaki_line)
                right = normalize(ruka_line)
                if left and right:
                    pair_ratios.append((SequenceMatcher(None, left, right).ratio(), command, chiaki_index, ruka_index, chiaki_line, ruka_line))
    print("PAIR", len(pair_ratios), ">=.99", sum(row[0] >= .99 for row in pair_ratios), ">=.95", sum(row[0] >= .95 for row in pair_ratios), ">=.90", sum(row[0] >= .90 for row in pair_ratios), ">=.85", sum(row[0] >= .85 for row in pair_ratios), ">=.80", sum(row[0] >= .80 for row in pair_ratios))
    for ratio, command, chiaki_index, ruka_index, chiaki_line, ruka_line in sorted(pair_ratios, reverse=True)[:5]:
        print(f"  TOP {ratio:.3f} COM{command} C{chiaki_index}/R{ruka_index}: {chiaki_line} || {ruka_line}")

    internal_ratios: list[float] = []
    for command, block in extract_blocks(read_cp932(CHIAKI_COM)).items():
        lines = [line.strip() for line in block.lines if line.strip().upper().startswith("PRINTFORM")]
        for offset in (0, 3):
            group = lines[offset : offset + 3]
            if len(group) != 3:
                continue
            for first in range(3):
                for second in range(first + 1, 3):
                    internal_ratios.append(SequenceMatcher(None, normalize(group[first]), normalize(group[second])).ratio())
    print("INTERNAL", len(internal_ratios), ">=.99", sum(value >= .99 for value in internal_ratios), ">=.90", sum(value >= .90 for value in internal_ratios), ">=.75", sum(value >= .75 for value in internal_ratios), ">=.70", sum(value >= .70 for value in internal_ratios))

    base = read_cp932(CHIAKI_BASE)
    com = read_cp932(CHIAKI_COM)
    original = (ROOT / "tools/output/ちあき.txt").read_text(encoding="utf-8")
    for token in ("私", "わたし", "僕", "ぼく", "ですぅ", "ですよぉ", "ふむ", "見ないで", "心の準備", "えへへ", "ふっふっふ"):
        print("VOICE", token, "current", base.count(token) + com.count(token), "original", original.count(token))
    for path in (CHIAKI_BASE, CHIAKI_COM):
        data = path.read_bytes()
        print("FORMAT", path.name, "cp932", end=" ")
        data.decode("cp932")
        print("ok", "CRLF", data.count(b"\r\n") == data.count(b"\n"), "LF", data.count(b"\n"))


if __name__ == "__main__":
    main()
