from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_27_夏野ゆり_COM.ERB"


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    start = text.index(";=== NATSUNO YURI TSUYURI TRAINER SPECIAL START ===")
    end = text.index(";=== NATSUNO YURI TSUYURI TRAINER SPECIAL END ===", start)
    block = text[start:end]
    old = "    ELSEIF SELECTCOM == 258\r\n"
    new = "    ELSEIF SELECTCOM == 258 && ASSIPLAY == 0\r\n"
    if block.count(old) != 1:
        raise SystemExit(f"expected one unconditional 258 branch, found {block.count(old)}")
    block = block.replace(old, new, 1)
    TARGET.write_bytes((text[:start] + block + text[end:]).encode("cp932"))


if __name__ == "__main__":
    main()
