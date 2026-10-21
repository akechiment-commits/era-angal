from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CHAR_DIR = ROOT / "ERB" / "CHAR"
TEMPLATE = CHAR_DIR / "CHAR_TEMPLATE_COM.ERB"


EXTRA_NAMES = {
    11: "バイブ",
    13: "アナルバイブ",
    14: "クリキャップ",
    15: "ニプルキャップ",
    16: "搾乳器",
    17: "オナホール",
    60: "助手にキスさせる",
    62: "ダブル素股",
    76: "双頭バイブ",
    78: "母乳飲み",
    79: "乳搾り",
    84: "Gスポット刺激",
    86: "強制放尿",
    202: "乳首合わせ",
    258: "助手顔面騎乗",
    318: "頭を撫でてもらう",
}

CUSTOM_NAMES = {
    280: "茶道部の部室",
    281: "放課後の生徒指導室",
    282: "取り締まり中の屋上",
    283: "両親不在の実家の自室",
    284: "風紀委員会の指導室",
    410: "風紀の見回りデート",
    411: "茶道部でお茶",
    412: "実家でママの手料理",
    413: "花を愛でる散歩デート",
    414: "れいか様お茶会のお供",
}


def template_names():
    names = {}
    for line in TEMPLATE.read_bytes().decode("cp932").splitlines():
        match = re.match(r"^;---\s*COM\s*(\d+)(?:\s+(.*?)\s*)?---\s*$", line.strip(), re.I)
        if match:
            names[int(match.group(1))] = match.group(2)
    names.update(EXTRA_NAMES)
    return names


def header_match(line):
    return re.match(r"^(;---\s*COM\s*)(\d+)(\s+.*?\s*---\s*)$", line.strip(), re.I)


def exact_header_mentions(line, command):
    return re.match(
        rf"^;---\s*COM\s*{command}(?:\s|$)", line.strip(), re.I
    ) is not None


def is_transparent(line):
    stripped = line.strip()
    return (
        not stripped
        or re.match(r"^(?:ENDIF|ELSE|ELSEIF\b|RETURN 0)\b", stripped, re.I) is not None
    )


def repair_file(path, names):
    lines = path.read_bytes().decode("cp932").splitlines()
    changed = False

    # Independent slots are character-specific. Do not leave Kaede's
    # scenario names on other characters; their group annotation and the
    # per-branch scene comments are the authoritative labels.
    custom_headers = {
        f";--- COM{command} {name} ---"
        for command, name in CUSTOM_NAMES.items()
    }
    custom_headers.update({
        ";--- COM280 -284 独自ウフフ ---",
        ";--- COM410 -414 独自純愛 ---",
    })
    filtered = [line for line in lines if line.strip() not in custom_headers]
    if len(filtered) != len(lines):
        lines = filtered
        changed = True

    # Replace generic labels such as "追加口上" with the actual command name.
    for i, line in enumerate(lines):
        match = header_match(line)
        if not match:
            continue
        command = int(match.group(2))
        if command not in names:
            continue
        expected = f";--- COM{command} {names[command]} ---"
        if line.strip() != expected:
            lines[i] = expected
            changed = True

    # Restore a command header when the top-level command has no annotation.
    i = 0
    while i < len(lines):
        match = re.match(r"^IF SELECTCOM == (\d+)\s*$", lines[i].strip(), re.I)
        if not match:
            i += 1
            continue
        command = int(match.group(1))
        if command not in names:
            i += 1
            continue

        has_header = False
        j = i - 1
        for _ in range(12):
            if j < 0:
                break
            if exact_header_mentions(lines[j], command):
                has_header = True
                break
            if is_transparent(lines[j]) or lines[j].lstrip().startswith(";"):
                j -= 1
                continue
            break

        if not has_header:
            lines.insert(i, f";--- COM{command} {names[command]} ---")
            changed = True
            i += 1
        i += 1

    if changed:
        path.write_bytes(("\r\n".join(lines) + "\r\n").encode("cp932"))
    return changed


def main():
    names = template_names()
    changed = []
    for path in sorted(CHAR_DIR.glob("*_COM.ERB")):
        if repair_file(path, names):
            changed.append(path.relative_to(ROOT).as_posix())
    print(f"updated {len(changed)} files")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
