"""CHAR53まりの絶頂ブロック重複・RAND枝・人格語彙を監査する。"""

from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
import re
import sys


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
COM = ROOT / "ERB/CHAR/CHAR_53_花丘まり_COM.ERB"
ORIGINAL = ROOT / "tools/output/まり.txt"


def normalize(value: str) -> str:
    value = re.sub(r"%[^%]+%", "", value)
    return re.sub(r"[「」。、，．！？!?♪☆…～〜ー・（）()\s]", "", value)


def main() -> None:
    data = COM.read_bytes().decode("cp932")
    lines = data.splitlines()
    start = next(index for index, line in enumerate(lines) if "@CHAR_ORGASM_53" in line)
    orgasm = [(index + 1, line.strip()) for index, line in enumerate(lines[start:], start) if "PRINTFORMW" in line and "「" in line]
    counts = Counter(normalize(line) for _, line in orgasm)
    duplicates = {value: count for value, count in counts.items() if count > 1 and len(value) > 8}
    print("ORGASM_LINES", len(orgasm), "DUP_KEYS", len(duplicates), "EXTRA", sum(count - 1 for count in duplicates.values()))
    for value, count in sorted(duplicates.items(), key=lambda item: (-item[1], item[0])):
        locations = [line_number for line_number, line in orgasm if normalize(line) == value]
        print("DUP", count, "LINES", locations, value)

    values = [line for _, line in orgasm]
    groups = [values[offset : offset + 3] for offset in range(0, len(values), 3)]
    ratios: list[float] = []
    for group in groups:
        if len(group) == 3:
            ratios.extend(
                SequenceMatcher(None, normalize(group[first]), normalize(group[second])).ratio()
                for first in range(3)
                for second in range(first + 1, 3)
            )
    print("RAND_GROUPS", len(groups), "PAIRS", len(ratios), ">=.85", sum(value >= .85 for value in ratios), ">=.80", sum(value >= .80 for value in ratios), ">=.75", sum(value >= .75 for value in ratios))

    original = ORIGINAL.read_text(encoding="utf-8")
    for token in ("あたし", "あたしゃ", "わたし", "私", "ねぇ", "おやまぁ", "やれやれ", "飴ちゃん", "転校生くん", "あんた", "見ないで", "心の準備", "ん゛", "えへへ"):
        print("VOICE", token, "current", data.count(token), "original", original.count(token))
    print("FORMAT", "CP932", "OK", "CRLF", data.count("\r\n"), "LF", data.count("\n"))


if __name__ == "__main__":
    main()
