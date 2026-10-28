from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    old = '「あっ、ん……%LOCALS%の中、あったかい。力が返ってくると、わたしまでどきどきするね」'
    new = '「あっ、ん……%LOCALS%の中、きゅっとする。そんなに締めつけられたら、わたしまで夢中になるね」'
    start = text.index("IF SELECTCOM == 23")
    end = text.index("\nENDIF", start)
    block = text[start:end]
    if block.count(old) != 1:
        raise SystemExit("COM23 duplicate line not found exactly once")
    block = block.replace(old, new, 1)
    text = text[:start] + block + text[end:]
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
