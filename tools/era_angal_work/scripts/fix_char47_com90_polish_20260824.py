from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    old = '「君のお尻、いじるの……？　、転校生くんも、こんなとこで感じちゃうんだ……可愛いね♪」'
    new = '「君のお尻、ここを撫でるんだね。……あ、転校生くん、力が抜けてきた。可愛い♪」'
    start = text.index("IF SELECTCOM == 90")
    end = text.index("\nENDIF", start)
    block = text[start:end]
    if block.count(old) != 1:
        raise SystemExit("COM90 malformed line not found exactly once")
    block = block.replace(old, new, 1)
    text = text[:start] + block + text[end:]
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
