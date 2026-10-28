"""CHAR20しずくに残ったLOCALS代入の不要なバックスラッシュを除去する。"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_20_藤猪しずく_COM.ERB"
BACKUP_DIR = ROOT / "tools" / "backups" / "CHAR20_before_locals_escape_fix_20260912"
BACKUP = BACKUP_DIR / TARGET.name


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    bad = "LOCALS " + chr(92) + chr(39) + "="
    good = "LOCALS " + chr(39) + "="
    count = text.count(bad)
    if count != 10:
        raise RuntimeError(f"expected 10 malformed LOCALS assignments, got {count}")
    if BACKUP.exists():
        raise RuntimeError(f"backup already exists: {BACKUP}")

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, BACKUP)
    updated = text.replace(bad, good)
    TARGET.write_bytes(updated.encode("cp932"))
    print(f"updated {TARGET}")
    print(f"backup {BACKUP}")
    print(f"fixed_assignments {count}")


if __name__ == "__main__":
    main()
