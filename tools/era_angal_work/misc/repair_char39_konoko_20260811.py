from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COM_PATH = ROOT / "ERB/CHAR/CHAR_39_冴木もも_COM.ERB"
OLD = "その子が困ってるなら、顔を見て加減して。あたし、黙って見ていられるほど器用じゃないよ……っ"
NEW = "%CALLNAME:ASSI%が困ってるなら、顔を見て加減して。あたし、黙って見ていられるほど器用じゃないよ……っ"


def main() -> None:
    raw = COM_PATH.read_bytes()
    text = raw.decode("cp932")
    old_count = text.count(OLD)
    if old_count == 0:
        print("CHAR39の「その子」混入は見つかりません。無変更で終了します。")
        return
    if old_count != 1:
        raise ValueError(f"想定外の置換件数: {old_count}")
    COM_PATH.write_bytes(text.replace(OLD, NEW).encode("cp932").replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    print("CHAR39 COM56の「その子」を助手名参照へ修正しました。")


if __name__ == "__main__":
    main()
