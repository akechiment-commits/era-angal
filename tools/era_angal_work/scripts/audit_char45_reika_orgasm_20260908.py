"""CHAR45れいかの絶頂ブロック重複・RAND枝・人格語彙を再監査する。"""

from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
import re
import sys


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
COM = ROOT / "ERB/CHAR/CHAR_45_円城寺れいか_COM.ERB"
ORIGINAL = ROOT / "tools/output/れいか.txt"


def normalize(value: str) -> str:
    value = re.sub(r"%[^%]+%", "", value)
    return re.sub(r"[「」。、，．！？!?♪☆…～〜ー・（）()\s]", "", value)


def main() -> None:
    data = COM.read_bytes().decode("cp932")
    orgasm = data[data.index("@CHAR_ORGASM_45") :]
    orgasm_lines = [line.strip() for line in orgasm.splitlines() if "PRINTFORMW" in line and "「" in line]
    duplicates = Counter(normalize(line) for line in orgasm_lines)
    duplicate_values = {value: count for value, count in duplicates.items() if count > 1 and len(value) > 8}
    groups = [orgasm_lines[offset : offset + 3] for offset in range(0, len(orgasm_lines), 3)]
    ratios: list[float] = []
    for group in groups:
        if len(group) == 3:
            ratios.extend(
                SequenceMatcher(None, normalize(group[first]), normalize(group[second])).ratio()
                for first in range(3)
                for second in range(first + 1, 3)
            )
    print("ORGASM_LINES", len(orgasm_lines), "EXACT_DUPLICATES", len(duplicate_values), "EXTRA", sum(duplicate_values.values()) - len(duplicate_values))
    print("RAND_GROUPS", len(groups), "PAIRS", len(ratios), ">=.85", sum(value >= .85 for value in ratios), ">=.80", sum(value >= .80 for value in ratios), ">=.75", sum(value >= .75 for value in ratios))

    original = ORIGINAL.read_text(encoding="utf-8")
    for token in ("わたくし", "わたし", "れいか", "お兄さま", "あなた", "転校生くん", "坊や", "ふふ", "うふふ", "よろしくてよ", "あ゛", "ぁ゛", "く゛", "ん゛", "こわれ", "たすけて", "見ないで", "心の準備"):
        print("VOICE", token, "current", data.count(token), "original", original.count(token))
    print("FORMAT", "CP932", "OK", "CRLF", data.count("\r\n"), "LF", data.count("\n"))


if __name__ == "__main__":
    main()
