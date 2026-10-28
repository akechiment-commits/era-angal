"""CHAR40 COM66のWフェラで助手名を解決する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_40_夜霧はやて_COM.ERB"
NEEDLE = "IF SELECTCOM == 66\n"
INSERT = "\tCALL AITE_YOBI, 40, ASSI\n\tLOCALS '= @\"%RESULTS%\"\n"


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932").replace("\r\n", "\n")
    start = text.index(NEEDLE)
    end = text.index("\n", start + len(NEEDLE))
    following = text[end + 1 :]
    if "CALL AITE_YOBI, 40, ASSI" in text[start : text.index("ENDIF", start)]:
        print("CHAR40 COM66の助手呼び出しは適用済みです。")
        return
    text = text[:end + 1] + INSERT + text[end + 1 :]
    TARGET.write_bytes(text.encode("cp932").replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    print("CHAR40 COM66に助手呼び出しを追加しました。")


if __name__ == "__main__":
    main()
