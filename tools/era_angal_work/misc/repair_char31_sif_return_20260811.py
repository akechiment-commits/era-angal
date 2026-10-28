from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COM_PATH = ROOT / "ERB/CHAR/CHAR_31_夢路まりあ_COM.ERB"
SIF = "SIF TEQUIP:45 && SELECTCOM != 45"


def main() -> None:
    raw = COM_PATH.read_bytes()
    text = raw.decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    indexes = [i for i, line in enumerate(lines) if line.strip() == SIF]
    if len(indexes) != 1:
        raise ValueError(f"CHAR31のSIF件数が想定外です: {len(indexes)}")
    index = indexes[0]
    if index + 1 < len(lines) and lines[index + 1].strip() == "RETURN 0":
        print("CHAR31のSIF直後はRETURN 0です。無変更で終了します。")
        return
    lines.insert(index + 1, "\tRETURN 0")
    result = "\r\n".join(lines).rstrip("\r\n") + "\r\n"
    COM_PATH.write_bytes(result.encode("cp932"))
    print("CHAR31のSIF直後へRETURN 0を復元しました。")


if __name__ == "__main__":
    main()
