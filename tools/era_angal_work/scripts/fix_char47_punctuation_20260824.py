from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    lines = []
    for line in text.splitlines():
        if "PRINTFORM" in line:
            line = line.replace("　、", "　")
            line = line.replace("「ふふ、？", "「ふふ？")
            line = line.replace("?", "？")
        lines.append(line)
    result = "\n".join(lines) + ("\n" if text.endswith(("\n", "\r")) else "")
    TARGET.write_bytes(result.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
