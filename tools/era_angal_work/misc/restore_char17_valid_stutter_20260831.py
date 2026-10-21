from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "output" / "あずさ.txt"
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_17_小鳩あずさ_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR17_before_restore_valid_stutter_20260831" / TARGET.name


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    if not source_text.startswith("# あずさ（全1880件）"):
        raise RuntimeError("unexpected source header: あずさ.txt")

    data = TARGET.read_bytes()
    text = data.decode("cp932")
    old = "PRINTFORMW 「ひゃっ、撮らないでくださいっ……。あずさのこんな姿、残っちゃうなんてっ……恥ずかしいっ……」"
    new = "PRINTFORMW 「ひゃっ、と、撮らないでくださいっ……。あずさのこんな姿、残っちゃうなんてっ……恥ずかしいっ……」"
    if text.count(old) == 1 and text.count(new) == 0:
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        if not BACKUP.exists():
            shutil.copy2(TARGET, BACKUP)
        TARGET.write_bytes(text.replace(old, new).encode("cp932"))
        print("restored valid stutter:", TARGET)
        print("backup:", BACKUP)
        return
    if text.count(new) == 1 and text.count(old) == 1:
        print("unchanged: valid stutter is already restored")
        return
    raise RuntimeError(f"unexpected occurrence count: old={text.count(old)}, new={text.count(new)}")


if __name__ == "__main__":
    main()
