from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"


def remove_phrase(line: str, phrase: str) -> str:
    line = line.replace(f"{phrase}、", "")
    line = line.replace(f"{phrase}。", "")
    line = line.replace(f"{phrase}……", "")
    line = line.replace(f"、{phrase}", "")
    line = line.replace(f"。{phrase}", "。")
    line = line.replace(f"{phrase}♪", "♪")
    line = line.replace(phrase, "")
    line = line.replace("「、", "「")
    line = line.replace("。 、", "。")
    line = line.replace("、、", "、")
    return line


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    regular_fufu_seen = 0
    ehehe_seen = 0
    output = []
    for line in text.splitlines():
        if "PRINTFORM" in line:
            if "ふふ" in line and "ふふ～ん" not in line and "ふふふ" not in line:
                regular_fufu_seen += line.count("ふふ")
                # Keep alternating regular laughs; preserve the original teasing form ふふ～ん.
                if regular_fufu_seen % 2 == 0:
                    line = remove_phrase(line, "ふふ")
            if "えへへ" in line:
                ehehe_seen += line.count("えへへ")
                # Keep one of every three occurrences, preventing a fixed catchphrase.
                if ehehe_seen % 3 != 1:
                    line = remove_phrase(line, "えへへ")
        output.append(line)
    result = "\n".join(output) + ("\n" if text.endswith(("\n", "\r")) else "")
    TARGET.write_bytes(result.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
