from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_35_梅園かな_COM.ERB"
OLD = "CALL AITE_YOBI, 34, ASSI"
NEW = "CALL AITE_YOBI, 35, ASSI"


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    count = text.count(OLD)
    if count != 5:
        raise ValueError(f"CHAR35の助手呼称固定値が想定外です: {count}")
    text = text.replace(OLD, NEW)
    encoded = text.replace("\r\n", "\n").replace("\r", "\n").encode("cp932")
    TARGET.write_bytes(encoded.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    print("CHAR_35のAITE_YOBI CASEを34から35へ修正しました。")


if __name__ == "__main__":
    main()
