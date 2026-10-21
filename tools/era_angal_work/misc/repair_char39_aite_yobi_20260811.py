from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COM_PATH = ROOT / "ERB/CHAR/CHAR_39_冴木もも_COM.ERB"
OLD = "CALL AITE_YOBI, 34, ASSI"
NEW = "CALL AITE_YOBI, 39, ASSI"


def main() -> None:
    raw = COM_PATH.read_bytes()
    text = raw.decode("cp932")
    old_count = text.count(OLD)
    if old_count == 0:
        print("CHAR39の助手解決はCASE39です。無変更で終了します。")
        return
    if old_count != 5:
        raise ValueError(f"CHAR39追加ブロックのCASE34残存数が想定外です: {old_count}")
    COM_PATH.write_bytes(text.replace(OLD, NEW).encode("cp932").replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    print("CHAR39追加助手5枠のAITE_YOBIをCASE39へ修正しました。")


if __name__ == "__main__":
    main()
