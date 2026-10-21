"""CHAR07ベース口上に残る原作外語尾を是正する。"""

from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_07_高原ちあき.ERB"


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    count = text.count("ですよぉ")
    if count != 3:
        raise SystemExit(f"想定外のベース汚染語件数: {count}")
    text = text.replace("ですよぉ～", "ですよ～")
    text = text.replace("ですよぉ……", "ですよ……")
    text = text.replace("ですよぉ！", "ですよ！")
    text = text.replace("ですよぉ♪", "ですよ♪")
    data = text.encode("cp932")
    if data.count(b"\r\n") != data.count(b"\n"):
        raise SystemExit("CRLF検査失敗")
    TARGET.write_bytes(data)
    print(f"CHAR07 base: 原作外語尾 {count}件を是正")


if __name__ == "__main__":
    main()
