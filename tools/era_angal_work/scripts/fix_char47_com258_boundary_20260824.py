from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    start = text.index(";--- COM258 助手顔面騎乗 ---")
    end = text.index("\n;--- COM318 頭を撫でてもらう ---", start)
    block = text[start:end]
    if block.rstrip().endswith("ENDIF\nENDIF") or block.rstrip().endswith("ENDIF\r\nENDIF"):
        raise SystemExit("COM258 boundary already has both ENDIF lines")
    if not block.rstrip().endswith("ENDIF"):
        raise SystemExit("unexpected COM258 block ending")
    block = block.rstrip("\r\n") + "\nENDIF\n"
    text = text[:start] + block + text[end:]
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
