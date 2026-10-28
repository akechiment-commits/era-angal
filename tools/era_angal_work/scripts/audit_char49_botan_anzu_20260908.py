"""CHAR49ぼたんとCHAR72あんずの差別化・内部RAND・形式を再監査する。"""

from difflib import SequenceMatcher
from pathlib import Path
import re
import sys


sys.stdout.reconfigure(encoding="utf-8")
for candidate in Path(__file__).resolve().parents:
    if (candidate / "ERB" / "CHAR").is_dir():
        ROOT = candidate
        break
else:
    raise RuntimeError("ERB/CHARを含むプロジェクトルートを特定できません")
BOTAN_BASE = ROOT / "ERB/CHAR/CHAR_49_小松ぼたん.ERB"
BOTAN_COM = ROOT / "ERB/CHAR/CHAR_49_小松ぼたん_COM.ERB"
ANZU_COM = ROOT / "ERB/CHAR/CHAR_72_あんず_COM.ERB"


def read(path: Path) -> str:
    return path.read_bytes().decode("cp932")


def values(path: Path) -> dict[int, list[str]]:
    integrity_dir = ROOT / "tools" / "era_angal_work" / "misc"
    sys.path.insert(0, str(integrity_dir))
    from audit_koujo_integrity import extract_blocks  # noqa: PLC0415

    result: dict[int, list[str]] = {}
    for command, block in extract_blocks(read(path)).items():
        lines = [line.strip() for line in block.lines if line.strip().upper().startswith("PRINTFORM")]
        result[command] = lines
    return result


def normalize(value: str) -> str:
    value = re.sub(r"%[^%]+%", "", value)
    return re.sub(r"[「」。、，．！？!?♪☆…～〜ー・（）()\s]", "", value)


def main() -> None:
    botan = values(BOTAN_COM)
    anzu = values(ANZU_COM)
    pairs: list[tuple[float, int, str, str]] = []
    for command in sorted(set(botan) & set(anzu)):
        for left in botan[command]:
            for right in anzu[command]:
                left_norm = normalize(left)
                right_norm = normalize(right)
                if left_norm and right_norm:
                    pairs.append((SequenceMatcher(None, left_norm, right_norm).ratio(), command, left, right))
    print(
        "PAIR",
        len(pairs),
        *(f">={threshold} {sum(row[0] >= threshold for row in pairs)}" for threshold in (.99, .95, .90, .85, .80)),
    )
    for row in sorted(pairs, reverse=True)[:5]:
        print(f"  TOP {row[0]:.3f} COM{row[1]}: {row[2]} || {row[3]}")

    internal: list[float] = []
    for command, lines in botan.items():
        for offset in (0, 3):
            group = lines[offset : offset + 3]
            for first in range(len(group)):
                for second in range(first + 1, len(group)):
                    internal.append(SequenceMatcher(None, normalize(group[first]), normalize(group[second])).ratio())
    print(
        "INTERNAL",
        len(internal),
        *(f">={threshold} {sum(value >= threshold for value in internal)}" for threshold in (.99, .95, .90, .85, .80)),
    )

    base = read(BOTAN_BASE)
    com = read(BOTAN_COM)
    original_path = ROOT / "tools/era_angal_work/materials/output/ぼたん.txt"
    if not original_path.is_file():
        original_path = next((ROOT / "tools").rglob("ぼたん.txt"))
    original = original_path.read_text(encoding="utf-8")
    for token in ("わたし", "私", "うち", "あたし", "ふふ", "えへへ", "転校生くん", "君", "見ないで", "心の準備", "採点", "甘いもの", "ケーキ"):
        print("VOICE", token, "current", base.count(token) + com.count(token), "original", original.count(token))
    for path in (BOTAN_BASE, BOTAN_COM):
        raw = path.read_bytes()
        print("FORMAT", path.name, "CP932", end=" ")
        raw.decode("cp932")
        print("OK", "CRLF", raw.count(b"\r\n"), "LF", raw.count(b"\n"))


if __name__ == "__main__":
    main()
