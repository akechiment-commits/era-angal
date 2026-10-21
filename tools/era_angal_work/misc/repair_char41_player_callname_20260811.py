"""CHAR41の今回追加ブロック内の主人公呼称を転校生さんへ統一する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_41_悠木ともこ_COM.ERB"
MARKER = ";=== TOMOKO RAND3 AND ADDITIONAL10 START ==="


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932").replace("\r\n", "\n")
    lines = text.split("\n")
    branch_indent = None
    branch = None
    count = 0
    for index, line in enumerate(lines):
        stripped = line.strip()
        indent = len(line) - len(line.lstrip("\t "))
        if stripped == "IF A == 0":
            branch_indent = indent
            branch = 0
            continue
        if branch_indent == indent and stripped == "ELSEIF A == 1":
            branch = 1
            continue
        if branch_indent == indent and stripped == "ELSE":
            branch = 2
            continue
        if branch_indent == indent and stripped == "ENDIF":
            branch_indent = None
            branch = None
            continue
        if branch in (1, 2) and stripped.startswith("PRINTFORM"):
            occurrences = line.count("あなた")
            if occurrences:
                lines[index] = line.replace("あなた", "転校生さん")
                count += occurrences
    result = "\n".join(lines).rstrip("\n") + "\n"
    TARGET.write_bytes(result.encode("cp932").replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    print(f"CHAR41のRAND枝内の呼称を{count}件修正しました。")


if __name__ == "__main__":
    main()
