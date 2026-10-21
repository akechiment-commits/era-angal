from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"
SOURCE = ROOT / "tools" / "backups" / "CHAR47_before_full_voice_audit_20260824" / TARGET.name
CURRENT_BACKUP = ROOT / "tools" / "backups" / "CHAR47_before_mechanical_revert_20260824" / TARGET.name


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"restore source not found: {SOURCE}")
    CURRENT_BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not CURRENT_BACKUP.exists():
        shutil.copy2(TARGET, CURRENT_BACKUP)
    shutil.copy2(SOURCE, TARGET)
    restored = TARGET.read_bytes()
    if restored != SOURCE.read_bytes():
        raise SystemExit("restore verification failed")
    print(f"restored {TARGET} from {SOURCE}")


if __name__ == "__main__":
    main()
