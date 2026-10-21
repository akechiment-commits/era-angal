from __future__ import annotations

import difflib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "tools/backups/assistant_locals_viewpoint_20260904"
TARGETS = [27, 52, 53, 54, 55, 56, 57, 59, 60]


def main() -> int:
    for number in TARGETS:
        current = next(ROOT.glob(f"ERB/CHAR/CHAR_{number:02d}_*_COM.ERB"))
        backup = BACKUP_DIR / current.name
        old = backup.read_bytes().decode("cp932").replace("\r\n", "\n").splitlines()
        new = current.read_bytes().decode("cp932").replace("\r\n", "\n").splitlines()
        changed = []
        for line in difflib.unified_diff(old, new, lineterm=""):
            if line.startswith(("---", "+++", "@@")):
                continue
            if any(token in line for token in ("%LOCALS%", "%CALLNAME:ASSI%", "CALL AITE_YOBI", "つゆりちゃん", "さくらさん")):
                changed.append(line)
        if changed:
            print(f"--- CHAR{number:02d} ---")
            print("\n".join(changed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
