from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_09_月永るか_COM.ERB"
BACKUP = ROOT / "tools/backups/CHAR09_com61_before_repair_20260828" / TARGET.name

OLD = "「んっ、動くと顔が近すぎます！　ぼくまで緊張して、舌がうまく動かないですよぉ～っ！」"
NEW = "「んっ、動かないでください。ぼく、舌を迷わせたくないので、じっとしていてください……」"
OLD2 = "「んっ、動かないでください。ぼく、舌を迷わせたくないので、じっとしていてください……」"
NEW2 = "「んっ、動かないでください。ぼく、ゆっくり舐めますから、力を抜いてください……」"


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932").replace("\r\n", "\n")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        BACKUP.write_bytes(raw)
    if text.count(OLD) == 1:
        text = text.replace(OLD, NEW)
    elif text.count(OLD2) == 1:
        text = text.replace(OLD2, NEW2)
    else:
        raise RuntimeError(f"COM61の対象文が見つかりません: OLD={text.count(OLD)}, OLD2={text.count(OLD2)}")
    TARGET.write_bytes((text.rstrip("\n") + "\n").replace("\n", "\r\n").encode("cp932"))
    print("CHAR09 COM61: 曖昧な『顔が近い』を、舌で愛撫中の反応へ修正")


if __name__ == "__main__":
    main()
