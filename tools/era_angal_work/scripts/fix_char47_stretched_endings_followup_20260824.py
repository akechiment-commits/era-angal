from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"

REPLACEMENTS = {
    "身体が跳ねるよぉ。": "身体が跳ねるよ。",
    "見ないでよぉ。わたしだって": "見ないでよ。わたしだって",
    "落ち着かないよ～」": "落ち着かないよ」",
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    start = text.index(";--- COM60 助手にキスさせる ---")
    end = text.index("\n@TRAIN_MESSAGE_B280_47", start)
    block = text[start:end]
    for old, new in REPLACEMENTS.items():
        count = block.count(old)
        if count != 1:
            raise SystemExit(f"expected one occurrence in CHAR47 additional block: {old!r} ({count})")
        block = block.replace(old, new, 1)
    text = text[:start] + block + text[end:]
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
