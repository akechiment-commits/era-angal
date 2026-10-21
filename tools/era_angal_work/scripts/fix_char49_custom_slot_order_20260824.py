from pathlib import Path
import re


TARGET = Path(r"ERB/CHAR/CHAR_49_小松ぼたん_COM.ERB")


def reorder_group(
    text: str,
    start_marker: str,
    end_marker: str,
    order: list[int],
    source_order: list[int],
) -> str:
    start = text.index(start_marker)
    end = text.index(end_marker, start)
    segment = text[start:end]
    lines = segment.splitlines(keepends=True)
    codes = set(order)
    code_re = re.compile(r"^(?:IF|ELSEIF) SELECTCOM == (\d+)\s*$")
    code_rows: list[tuple[int, int, int]] = []
    for i, line in enumerate(lines):
        code_match = code_re.match(line.rstrip("\r\n"))
        if not code_match:
            continue
        code = int(code_match.group(1))
        if code in codes:
            branch_start = i
            if i > 0 and lines[i - 1].lstrip().startswith(";◆地の文"):
                branch_start = i - 1
            code_rows.append((code, branch_start, i))
    if {code for code, _, _ in code_rows} != codes or len(code_rows) != len(order):
        raise RuntimeError(f"custom branch detection failed: {code_rows}")
    code_rows.sort(key=lambda row: row[1])
    top_end = None
    for i in range(code_rows[-1][2] + 1, len(lines)):
        if lines[i].rstrip("\r\n") == "ENDIF":
            top_end = i
            break
    if top_end is None:
        raise RuntimeError("outer ENDIF not found")

    header = lines[:code_rows[0][1]]
    branch_data: dict[int, tuple[list[str], int]] = {}
    for pos, (code, branch_start, code_row) in enumerate(code_rows):
        branch_end = code_rows[pos + 1][1] if pos + 1 < len(code_rows) else top_end
        branch = lines[branch_start:branch_end]
        branch_data[code] = (branch, code_row - branch_start)
    branches: dict[int, list[str]] = {}
    for pos, target_code in enumerate(order):
        source_code = source_order[pos]
        branch, code_offset = branch_data[source_code]
        old_line = branch[code_offset]
        branch[code_offset] = (
            ("IF" if pos == 0 else "ELSEIF")
            + f" SELECTCOM == {target_code}"
            + ("\r\n" if old_line.endswith("\r\n") else "\n")
        )
        branches[target_code] = branch
    tail = lines[top_end:]
    rebuilt = "".join(header + [line for code in order for line in branches[code]] + tail)
    return text[:start] + rebuilt + text[end:]


def group_has_expected_scenes(text: str, expected: dict[int, str]) -> bool:
    for code, scene in expected.items():
        pattern = (
            rf"(?m)^(?:IF|ELSEIF) SELECTCOM == {code}\s*$"
            rf"\r?\n\s*;◆地の文（場面: {re.escape(scene)}）\s*$"
        )
        if re.search(pattern, text) is None:
            return False
    return True


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    expected_ufufu = {
        280: "穴場シャワー室",
        281: "夜の旧校舎",
        282: "貸切露天の二人",
        283: "家庭科室の戯れ",
        284: "ケーキ屋の密会",
    }
    expected_pure = {
        410: "思い出の和菓子屋",
        411: "温泉饅頭デート",
        412: "海の思い出",
        413: "ケーキパーティ",
        414: "だらだら甘味三昧",
    }
    if not group_has_expected_scenes(text, expected_ufufu):
        text = reorder_group(
            text,
            ";--- COM280-284 独自ウフフ ---",
            ";--- COM410-414 独自純愛 ---",
            [280, 281, 282, 283, 284],
            [283, 284, 280, 281, 282],
        )
    if not group_has_expected_scenes(text, expected_pure):
        text = reorder_group(
            text,
            ";--- COM410-414 独自純愛 ---",
            ";==============================================================\r\n; えっち系・よく使うコマンド",
            [410, 411, 412, 413, 414],
            [412, 410, 414, 411, 413],
        )
    replacements = {
        "「離れないで、ではありません……でも、同時に動かれたら合図が届かないでしょ！」":
            "「離れないでって意味じゃないけど……同時に動かれたら、合図も届かないでしょ！」",
        "「撫でられているうちに、わたしまで肩の力が抜けた……。君が眠るまで動かないよ」":
            "「撫でているうちに、わたしまで肩の力が抜けた……。君が眠るまで手を止めないよ」",
    }
    for old, new in replacements.items():
        old_count = text.count(old)
        new_count = text.count(new)
        if old_count == 1 and new_count == 0:
            text = text.replace(old, new)
        elif old_count == 0 and new_count == 1:
            continue
        else:
            raise RuntimeError(
                f"expected one old or one new form for {old!r}, got old={old_count}, new={new_count}"
            )
    encoded = text.encode("cp932")
    TARGET.write_bytes(encoded)
    print("verified/reordered custom slots: 280-284 and 410-414")
    print("fixed COM76 normal A2 wording and COM318 lover A2 viewpoint")
    crlf = encoded.count(b"\r\n")
    lf = encoded.count(b"\n")
    print(f"CP932 bytes: {len(encoded)}; CRLF: {crlf}; LF: {lf}")


if __name__ == "__main__":
    main()
