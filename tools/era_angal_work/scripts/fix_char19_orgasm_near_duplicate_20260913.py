"""CHAR19みけの複絶頂に残った句読点違いの近似台詞を分離する。"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_19_猫塚みけ_COM.ERB"
BACKUP_DIR = ROOT / "tools" / "backups" / "CHAR19_before_orgasm_near_duplicate_fix_20260913"
BACKUP = BACKUP_DIR / TARGET.name

OLD = "「にゃあ……っ、力抜けちゃう……。せ、先輩……すごい……えへへ……」"
NEW = "「にゃあ……っ、足までふるふるする……。せ、先輩、あたし、まだ立てないよぉ……えへへ……」"
LINE_NUMBER = 5453


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    lines = text.splitlines(keepends=True)
    if BACKUP.exists():
        raise RuntimeError(f"backup already exists: {BACKUP}")
    line = lines[LINE_NUMBER - 1]
    if line.count(OLD) != 1:
        raise RuntimeError(f"line {LINE_NUMBER}: expected one old phrase, got {line.count(OLD)}")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, BACKUP)
    lines[LINE_NUMBER - 1] = line.replace(OLD, NEW, 1)
    TARGET.write_bytes("".join(lines).encode("cp932"))
    print(f"updated {TARGET}")
    print(f"backup {BACKUP}")
    print("changed_physical_lines 1")


if __name__ == "__main__":
    main()
