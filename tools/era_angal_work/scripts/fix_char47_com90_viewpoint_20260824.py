from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"

REPLACEMENTS = {
    '「ひゃっ……っ、そんなところ触られたら、くすぐったいよ。急に入れないでね……」': '「ひゃっ……っ、ここを撫でると、転校生くんの息が変わるね。急にはしないから、力を抜いて」',
    '「んぅ……っ、そこはまだ慣れてないよ。わたしが見てるから、無理はしないでね……」': '「んぅ……っ、まだ力が入ってるね。わたしの手、ちゃんと感じてる？　無理はしないで、ゆっくりでいいよ」',
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    start = text.index("IF SELECTCOM == 90")
    end = text.index("\nENDIF", start)
    block = text[start:end]
    for old, new in REPLACEMENTS.items():
        if block.count(old) != 1:
            raise SystemExit(f"expected one occurrence in COM90: {old}")
        block = block.replace(old, new, 1)
    text = text[:start] + block + text[end:]
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
