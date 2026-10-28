"""CHAR07 高原ちあきの原作にない汎用語尾を、原作準拠の表記へ戻す。"""

from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_07_高原ちあき_COM.ERB"


REWRITES = {
    "ですよぉ～": "ですよ～",
    "ですよぉ……": "ですよ……",
    "ですよぉ！": "ですよ！",
    "ですよぉ♪": "ですよ♪",
    "ですよぉ、": "ですよ、",
    "ですよぉ」": "ですよ」",
    "ですよぉ?": "ですよ?",
    "ですよぉ!": "ですよ!",
    "ですぅ": "です",
}


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    counts = {}
    for old, new in REWRITES.items():
        counts[old] = text.count(old)
        text = text.replace(old, new)
    if sum(counts.values()) != 114:
        raise SystemExit(f"想定外の汚染語件数: {counts}")
    data = text.encode("cp932")
    if data.count(b"\r\n") != data.count(b"\n"):
        raise SystemExit("CRLF検査失敗")
    TARGET.write_bytes(data)
    print(f"CHAR07: 原作外語尾 {sum(counts.values())}件を是正: {counts}")


if __name__ == "__main__":
    main()
