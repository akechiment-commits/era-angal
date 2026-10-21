"""CHAR63ちづるの絶頂反復ビート・RAND枝・人格語彙を監査する。"""

from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
import re
import sys


sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
COM = ROOT / "ERB/CHAR/CHAR_63_八雲ちづる_COM.ERB"
ORIGINAL = ROOT / "tools/output/ちづる.txt"


def normalize(value: str) -> str:
    value = re.sub(r"%[^%]+%", "", value)
    return re.sub(r"[「」。、，．！？!?♪☆…～〜ー・（）()\s]", "", value)


def main() -> None:
    data = COM.read_bytes().decode("cp932")
    lines = data.splitlines()
    start = next(index for index, line in enumerate(lines) if "@CHAR_ORGASM_63" in line)
    end = next(index for index, line in enumerate(lines[start:], start) if line.strip() == "RETURN 0")
    orgasm = [(index + 1, line.strip()) for index, line in enumerate(lines[start:end], start) if "PRINTFORMW" in line and "「" in line]
    counts = Counter(normalize(line) for _, line in orgasm)
    duplicates = {value: count for value, count in counts.items() if count > 1 and len(value) > 8}
    groups = [orgasm[offset : offset + 3] for offset in range(0, len(orgasm), 3)]
    ratios: list[float] = []
    for group in groups:
        if len(group) == 3:
            ratios.extend(
                SequenceMatcher(None, normalize(group[first][1]), normalize(group[second][1])).ratio()
                for first in range(3)
                for second in range(first + 1, 3)
            )
    print("ORGASM_LINES", len(orgasm), "EXACT_DUP_KEYS", len(duplicates), "EXTRA", sum(count - 1 for count in duplicates.values()))
    print("RAND_GROUPS", len(groups), "PAIRS", len(ratios), ">=.85", sum(value >= .85 for value in ratios), ">=.80", sum(value >= .80 for value in ratios), ">=.75", sum(value >= .75 for value in ratios))

    original = ORIGINAL.read_text(encoding="utf-8")
    for token in ("わたし", "あたし", "私", "かなって", "おね～さん", "きゃ～", "にゅふふ", "えへへ", "転校生くん", "きみ", "ヘルプマン", "見ないで", "心の準備", "身体が熱い", "息が追いつかない", "声が変"):
        print("VOICE", token, "current", data.count(token), "original", original.count(token))
    print("FORMAT", "CP932", "OK", "CRLF", data.count("\r\n"), "LF", data.count("\n"))


if __name__ == "__main__":
    main()
