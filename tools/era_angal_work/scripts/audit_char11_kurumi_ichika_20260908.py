"""CHAR11の人格汚染、CHAR12との同一COM重複、RAND枝重複を再監査する。"""

from difflib import SequenceMatcher
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from audit_koujo_integrity import extract_blocks, read_cp932  # noqa: E402


KURUMI_BASE = ROOT / "ERB/CHAR/CHAR_11_氷野くるみ.ERB"
KURUMI_COM = ROOT / "ERB/CHAR/CHAR_11_氷野くるみ_COM.ERB"
ICHIKA_COM = ROOT / "ERB/CHAR/CHAR_12_神樹いちか_COM.ERB"


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
    kurumi = dialogue_values(KURUMI_COM)
    ichika = dialogue_values(ICHIKA_COM)
    pair_ratios: list[tuple[float, int, str, str]] = []
    for command in sorted(set(kurumi) & set(ichika)):
        for kurumi_line in kurumi[command]:
            for ichika_line in ichika[command]:
                left = normalize(kurumi_line)
                right = normalize(ichika_line)
                if left and right:
                    pair_ratios.append((SequenceMatcher(None, left, right).ratio(), command, kurumi_line, ichika_line))
    print("PAIR", len(pair_ratios), ">=.99", sum(row[0] >= .99 for row in pair_ratios), ">=.95", sum(row[0] >= .95 for row in pair_ratios), ">=.90", sum(row[0] >= .90 for row in pair_ratios), ">=.85", sum(row[0] >= .85 for row in pair_ratios), ">=.80", sum(row[0] >= .80 for row in pair_ratios))
    for ratio, command, kurumi_line, ichika_line in sorted(pair_ratios, reverse=True)[:5]:
        print(f"  TOP {ratio:.3f} COM{command}: {kurumi_line} || {ichika_line}")

    internal: list[float] = []
    for command, block in extract_blocks(read_cp932(KURUMI_COM)).items():
        lines = [line.strip() for line in block.lines if line.strip().upper().startswith("PRINTFORM")]
        for offset in (0, 3):
            group = lines[offset : offset + 3]
            if len(group) != 3:
                continue
            for first in range(3):
                for second in range(first + 1, 3):
                    internal.append(SequenceMatcher(None, normalize(group[first]), normalize(group[second])).ratio())
    print("INTERNAL", len(internal), ">=.99", sum(value >= .99 for value in internal), ">=.90", sum(value >= .90 for value in internal), ">=.75", sum(value >= .75 for value in internal), ">=.70", sum(value >= .70 for value in internal))

    base = read_cp932(KURUMI_BASE)
    com = read_cp932(KURUMI_COM)
    original = (ROOT / "tools/output/くるみ.txt").read_text(encoding="utf-8")
    for token in ("わたし", "私", "あたし", "僕", "ぼく", "ですＹＯ", "ですぅ", "ですよぉ", "えへへ", "心の準備", "見ないで", "お兄ちゃん"):
        print("VOICE", token, "current", base.count(token) + com.count(token), "original", original.count(token))
    for path in (KURUMI_BASE, KURUMI_COM):
        data = path.read_bytes()
        data.decode("cp932")
        print("FORMAT", path.name, "CRLF", data.count(b"\r\n") == data.count(b"\n"), "LF", data.count(b"\n"))


if __name__ == "__main__":
    main()
