from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tools" / "output" / "あずさ.txt"
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_17_小鳩あずさ_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR17_before_shooting_typo_20260831" / TARGET.name


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    if not source_text.startswith("# あずさ（全1880件）"):
        raise RuntimeError("unexpected source header: あずさ.txt")

    data = TARGET.read_bytes()
    text = data.decode("cp932")
    replacements = {
        (
            "PRINTFORMW 「ひゃうっ、と、撮影しながらなんてっ……。あずさ、恥ずかしくて消えたいですっ……んっ……」",
            "PRINTFORMW 「ひゃうっ、撮影しながらなんてっ……。あずさ、恥ずかしくて消えたいですっ……んっ……」",
        ),
        (
            "PRINTFORMW 「はぁ……っ、あずさが上だと、全部見られちゃいますっ……。は、恥ずかしいけと、止まれないっ……」",
            "PRINTFORMW 「はぁ……っ、あずさが上だと、全部見られちゃいますっ……。は、恥ずかしいけど、止まれないっ……」",
        ),
        (
            "こんなの恥ずかしいけと、止まらないですっ……っ」",
            "こんなの恥ずかしいけど、止まらないですっ……っ」",
        ),
    }

    changed = False
    for old, new in replacements:
        old_count = text.count(old)
        new_count = text.count(new)
        if old_count == 0 and new_count == 1:
            continue
        if old_count != 1 or new_count != 0:
            raise RuntimeError(
                f"unexpected occurrence count: old={old_count}, new={new_count}: {old}"
            )
        text = text.replace(old, new)
        changed = True

    if not changed:
        print("unchanged: all known CHAR17 typos are already corrected")
        return

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)
    TARGET.write_bytes(text.encode("cp932"))
    print("updated:", TARGET)
    print("backup:", BACKUP)


if __name__ == "__main__":
    main()
