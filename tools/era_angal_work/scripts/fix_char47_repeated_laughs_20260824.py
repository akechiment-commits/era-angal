from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"


def strip_extra_laughs(line: str, keep_first: bool) -> tuple[str, bool]:
    if "PRINTFORM" not in line or "ふふ" not in line or "ふふ～ん" in line:
        return line, keep_first
    if "ふふふ" in line:
        return line, keep_first
    if not keep_first:
        keep_first = True
        first = line.find("ふふ")
        line = line[:first + 2] + line[first + 2:].replace("ふふ", "")
    else:
        line = line.replace("ふふ", "")
    # Removing a laugh must not leave an artificial leading comma or a doubled pause.
    line = line.replace("「、", "「")
    line = line.replace("「……、", "「……")
    line = line.replace("。 、", "。")
    line = line.replace("。、", "。")
    line = line.replace("、、", "、")
    line = line.replace("……♪", "……♪")
    return line, keep_first


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    lines = text.splitlines()
    kept = False
    output = []
    for line in lines:
        stripped = line.strip()
        if re.match(r"(?:IF|ELSEIF) SELECTCOM == \d+", stripped):
            kept = False
        line, kept = strip_extra_laughs(line, kept)
        output.append(line)
    result = "\n".join(output) + ("\n" if text.endswith(("\n", "\r")) else "")
    TARGET.write_bytes(result.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
