"""CHAR16 RAND3化の作業前バックアップへ一度だけ戻す。"""

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_16_大虎いさみ_COM.ERB"
BACKUP = ROOT / "tools/backups/CHAR16_before_rand3_20260831/CHAR_16_大虎いさみ_COM.ERB"


def main() -> int:
    if not BACKUP.exists():
        raise FileNotFoundError(BACKUP)
    shutil.copy2(BACKUP, TARGET)
    print("CHAR16をRAND3化前バックアップへ復元")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
