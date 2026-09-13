"""CHAR19みけの裸の「うにゃ、」を、原作に沿う語尾付き表記へ分散する。"""

from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_19_猫塚みけ_COM.ERB"
BACKUP_DIR = ROOT / "tools" / "backups" / "CHAR19_before_unya_suffix_normalization_20260913"
BACKUP = BACKUP_DIR / TARGET.name
OLD = "うにゃ、"
BARE_RE = re.compile(r"うにゃ(?![あ～〜っんーぁ])")

SOFT_RE = re.compile(
    r"嬉|好き|しあわせ|安心|ありがとう|お昼寝|日なた|お外|お散歩|"
    r"リラックス|あったか|甘やか|デート|一緒|隣|寝ちゃ|ごろごろ|特別|楽しい"
)
SHARP_AFTER_RE = re.compile(
    r"^(?:こ|怖|こわ|痛|やだ|止め|見ない|恥ずかし|不安|嫌|苦し|逃げ|捕ま|"
    r"急|びっくり|驚|不意|いきなり|叩|噛|縛|目隠|口枷)"
)


def suffix_for(line: str, line_number: int) -> str:
    position = line.find(OLD)
    after = line[position + len(OLD):position + len(OLD) + 18] if position >= 0 else line
    if SHARP_AFTER_RE.search(after):
        return "うにゃっ、"
    if SOFT_RE.search(line):
        return "うにゃ～、"
    return "うにゃあ、" if line_number % 3 else "うにゃ～、"


def main() -> None:
    if BACKUP.exists():
        raw = BACKUP.read_bytes()
    else:
        raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    lines = text.splitlines(keepends=True)
    targets = [
        index for index, line in enumerate(lines)
        if "PRINTFORM" in line and OLD in line and BARE_RE.search(line)
    ]
    if len(targets) != 258:
        raise RuntimeError(f"expected 258 bare comma forms, got {len(targets)}")
    if not BACKUP.exists():
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(TARGET, BACKUP)
    counts = {"うにゃあ、": 0, "うにゃ～、": 0, "うにゃっ、": 0}
    for index in targets:
        line_number = index + 1
        replacement = suffix_for(lines[index], line_number)
        lines[index] = lines[index].replace(OLD, replacement, 1)
        counts[replacement] += 1
    TARGET.write_bytes("".join(lines).encode("cp932"))
    print(f"updated {TARGET}")
    print(f"backup {BACKUP}")
    print("changed_physical_lines", len(targets))
    print("replacement_counts", counts)


if __name__ == "__main__":
    main()
