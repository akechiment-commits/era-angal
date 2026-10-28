from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_18_熊沢ひめの_COM.ERB"
SOURCE_BACKUP = ROOT / "tools/backups/CHAR18_before_rand3_20260831/CHAR_18_熊沢ひめの_COM.ERB"
RECOVERY_BACKUP = ROOT / "tools/backups/CHAR18_before_script_recovery_20260831/CHAR_18_熊沢ひめの_COM.ERB"


def main() -> None:
    original = SOURCE_BACKUP.read_bytes()
    original.decode("cp932")
    if not original:
        raise RuntimeError("empty CHAR18 RAND3 backup")
    current = TARGET.read_bytes()
    if current != original:
        RECOVERY_BACKUP.parent.mkdir(parents=True, exist_ok=True)
        if not RECOVERY_BACKUP.exists():
            shutil.copy2(TARGET, RECOVERY_BACKUP)
        TARGET.write_bytes(original)
        print("restored pre-RAND3 target:", TARGET)
        print("recovery backup:", RECOVERY_BACKUP)
    else:
        print("unchanged: target already matches pre-RAND3 backup")


if __name__ == "__main__":
    main()
