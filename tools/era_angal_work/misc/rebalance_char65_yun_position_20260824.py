import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_65_時国そら_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR65_before_yun_position_20260824" / TARGET.name
TOKEN = "ゆん、ゆん"
END_PAIR = re.compile(r"ゆん、ゆん(?P<tail>[……♪。！？?!〜」』）]*)$")

# 原作にある「文末のゆん、ゆん」に近い、短い余韻・喜び・交信の文だけ残す。
# それ以外は冒頭へ移す。同じ行の冒頭に既にある場合は文末側を落とす。
KEEP_END_LINES = {
    40, 185, 253, 359, 410, 483, 534, 573,
    624, 663, 736, 799, 902, 933, 1061, 1308,
    1491, 1548, 1582, 1722, 1770, 1898, 2106, 4725,
}


def insert_at_dialogue_start(line: str) -> str:
    for opener in ("「", "『", "（"):
        pos = line.find(opener)
        if pos >= 0:
            rest = line[pos + 1:].lstrip(" \u3000")
            if rest.startswith(("ゆん、ゆん", "ゆんゆん", "ゆ～ん")):
                return line
            return line[:pos + 1] + "ゆん、ゆん……。" + line[pos + 1:]
    marker = "PRINTFORMW "
    pos = line.find(marker)
    if pos >= 0:
        pos += len(marker)
        rest = line[pos:].lstrip(" \u3000")
        if rest.startswith(("ゆん、ゆん", "ゆんゆん", "ゆ～ん")):
            return line
        return line[:pos] + "ゆん、ゆん……。" + line[pos:]
    return "ゆん、ゆん……。" + line


def clean_tail(before: str, tail: str) -> str:
    closing = ""
    while tail and tail[-1] in "」』）":
        closing = tail[-1] + closing
        tail = tail[:-1]
    prefix = before.rstrip()
    if prefix.endswith(("？", "！", "。")):
        # 「？　♪」「。♪」のような、交信音を抜いた後の残骸を消す。
        tail = ""
    elif prefix.endswith("……") and tail.startswith("……"):
        # 既存の息継ぎと、ゆんに続いていた息継ぎを二重にしない。
        tail = tail[2:]
    return tail + closing


def main() -> None:
    source = BACKUP if BACKUP.exists() else TARGET
    raw = source.read_bytes()
    text = raw.decode("cp932")
    lines = text.splitlines(keepends=True)
    moved = 0
    removed = 0
    kept = 0

    for line_no, line in enumerate(lines, start=1):
        body = line.rstrip("\r\n")
        m = END_PAIR.search(body)
        if not m or line_no in KEEP_END_LINES:
            if m:
                kept += 1
            continue

        before = body[:m.start()].rstrip(" \u3000")
        tail = clean_tail(before, m.group("tail"))
        # 既に冒頭・文中に同じ交信音があるなら、重ねずに語尾側だけ削る。
        if TOKEN in before:
            new_body = before + tail
            removed += 1
        else:
            new_body = insert_at_dialogue_start(before + tail)
            moved += 1
        eol = "\r\n" if line.endswith("\r\n") else "\n"
        lines[line_no - 1] = new_body + eol

    new_text = "".join(lines)
    TARGET.write_bytes(new_text.encode("cp932"))
    print(f"yun_pair_terminal_kept={kept} moved_to_start={moved} removed_duplicate_tail={removed}")
    print(f"CRLF={new_text.count(chr(13)+chr(10))} bytes={TARGET.stat().st_size}")


if __name__ == "__main__":
    main()
