import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_65_時国そら_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR65_before_yun_cleanup_20260824" / TARGET.name
# 「ゆん、ゆん」「ゆんゆん」の後半を単独扱いしない。
BAD = re.compile(r"(?<!ゆん)(?<!、)ゆん(?![、ゆ～])")


# 強い反応・柔らかな呼気・神秘的な場面で、原作にある変化形を少量だけ使う。
# 指定しない箇所は基本形「ゆん、ゆん」へ戻す。
VARIANT_BY_LINE = {
    547: "ゆ～ん",
    601: "ゆんゆん",
    1173: "ゆんゆん",
    1460: "ゆんゆん",
    1519: "ゆ～ん",
    2352: "ゆんゆん",
    2508: "ゆ～ん",
    2618: "ゆんゆん",
    2706: "ゆんゆん",
    2805: "ゆんゆん",
    2910: "ゆんゆん",
    3371: "ゆんゆん",
    3744: "ゆんゆん",
    3983: "ゆんゆん",
    4185: "ゆんゆん",
    4424: "ゆんゆん",
    4943: "ゆんゆん",
    5205: "ゆんゆん",
    5474: "ゆんゆん",
    5748: "ゆんゆん",
    5868: "ゆんゆん",
    5946: "ゆんゆん",
}

# 「ゆん……ゆん……」は二つの単音を並べず、原作にもある連続音へまとめる。
FULL_REPLACEMENTS = {
    1033: ("ゆん……ゆん……", "ゆんゆん……"),
    1531: ("ゆん……ゆん……", "ゆんゆん……"),
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    direct_before = text
    text = text.replace("ゆん、ゆんって返して", "ゆん、ゆん……って返して")
    lines = text.splitlines(keepends=True)
    before = len(BAD.findall(text))
    if before == 0 and text == direct_before:
        print("CHAR65の単独ゆんは既に0件です。")
        return
    if not BACKUP.exists():
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        BACKUP.write_bytes(raw)

    changed_lines = 0
    for line_no, line in enumerate(lines, start=1):
        if not BAD.search(line):
            continue
        original = line
        if line_no in FULL_REPLACEMENTS:
            old, new = FULL_REPLACEMENTS[line_no]
            if line.count(old) != 1:
                raise RuntimeError(f"line {line_no}: expected one full replacement")
            line = line.replace(old, new, 1)
        else:
            variant = VARIANT_BY_LINE.get(line_no, "ゆん、ゆん")
            line = BAD.sub(variant, line)
        if BAD.search(line):
            raise RuntimeError(f"line {line_no}: lone ゆん remains")
        lines[line_no - 1] = line
        if line != original:
            changed_lines += 1

    new_text = "".join(lines)
    after = len(BAD.findall(new_text))
    if after:
        raise RuntimeError(f"lone ゆん remains after rewrite: {after}")
    TARGET.write_bytes(new_text.encode("cp932"))
    print(f"lone_yun_before={before} after={after} changed_lines={changed_lines}")
    print(f"CRLF={new_text.count(chr(13)+chr(10))} bytes={TARGET.stat().st_size}")


if __name__ == "__main__":
    main()
