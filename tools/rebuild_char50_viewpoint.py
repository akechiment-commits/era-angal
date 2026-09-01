"""CHAR50を加筆前バックアップから再構築し、視点修正版の加筆を再適用する。"""

from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_50_山條ぎん_COM.ERB"
SOURCE = ROOT / "tools" / "backups" / "CHAR50_before_rand3_and_additional10_20260813" / TARGET.name
SNAPSHOT = ROOT / "tools" / "backups" / "CHAR50_before_viewpoint_rebuild_20260813" / TARGET.name


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    if not SNAPSHOT.exists():
        SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
        SNAPSHOT.write_bytes(TARGET.read_bytes())
    TARGET.write_bytes(SOURCE.read_bytes())
    runpy.run_path(str(ROOT / "tools" / "add_missing_rand3_char50.py"), run_name="__main__")
    runpy.run_path(str(ROOT / "tools" / "repair_char50_voice.py"), run_name="__main__")
    print(f"視点修正版CHAR50を再構築: {TARGET}")


if __name__ == "__main__":
    main()
