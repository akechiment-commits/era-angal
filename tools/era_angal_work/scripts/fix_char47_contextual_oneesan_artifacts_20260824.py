from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"


REPLACEMENTS = (
    ("んもう……わたしわたしだってば。", "んもう……わたしだってば。"),
    ("「やっ……んっ。お、わたしの胸で、", "「やっ……んっ。わたしの胸で、"),
    ("「あっ……ん。お、わたしの身体、", "「あっ……ん。わたしの身体、"),
)


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected exactly one occurrence ({count}): {old}")
        text = text.replace(old, new)
    TARGET.write_bytes(text.encode("cp932"))


if __name__ == "__main__":
    main()
