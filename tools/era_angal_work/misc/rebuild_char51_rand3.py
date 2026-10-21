"""CHAR51の追加10/RAND3口上をバックアップから再生成する。"""

from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COM_PATH = ROOT / "ERB" / "CHAR" / "CHAR_51_御影かすみ_COM.ERB"
BACKUP_PATH = ROOT / "tools" / "backups" / "CHAR51_before_rand3_and_additional10_20260813" / COM_PATH.name
SCRIPT_PATH = ROOT / "tools" / "add_missing_rand3_char51.py"


def main() -> None:
    if not BACKUP_PATH.exists():
        raise FileNotFoundError(f"backup not found: {BACKUP_PATH}")
    COM_PATH.write_bytes(BACKUP_PATH.read_bytes())
    runpy.run_path(str(SCRIPT_PATH), run_name="__main__")
    print(f"CHAR51を再構築: {COM_PATH}")


if __name__ == "__main__":
    main()
