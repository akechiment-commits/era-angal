"""残っていた独自枠の場面違い枝を削除し、かえでの見回り台詞を補う。"""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CHAR_DIR = ROOT / "ERB" / "CHAR"


def command_ranges(lines: list[str], start: int, end: int) -> dict[int, tuple[int, int]]:
    starts: list[tuple[int, int]] = []
    for i in range(start, end):
        match = re.match(r"^\s*(?:IF|ELSEIF) SELECTCOM == (\d+)", lines[i])
        if match:
            starts.append((i, int(match.group(1))))
    return {
        command: (line_no, starts[pos + 1][0] if pos + 1 < len(starts) else end)
        for pos, (line_no, command) in enumerate(starts)
    }


def group_range(lines: list[str], first: int, last: int) -> tuple[int, int]:
    start_marker = f";--- COM{first}-{last}"
    start = next(i for i, line in enumerate(lines) if start_marker in line)
    end_marker = ";--- COM410-414" if first == 280 else ";--- COM0 "
    end = next(i for i in range(start + 1, len(lines)) if end_marker in lines[i])
    return start, end


def branch_slots(lines: list[str], start: int, end: int) -> list[dict[str, int]]:
    a0_markers = [i for i in range(start, end) if lines[i].strip() == "IF A == 0"]
    if len(a0_markers) != 2:
        raise RuntimeError(f"expected two talent branches at line {start + 1}, got {len(a0_markers)}")

    result: list[dict[str, int]] = []
    for a0 in a0_markers:
        indent = len(lines[a0]) - len(lines[a0].lstrip())
        a1 = next(
            i for i in range(a0 + 1, end)
            if len(lines[i]) - len(lines[i].lstrip()) == indent
            and lines[i].strip() == "ELSEIF A == 1"
        )
        a2 = next(
            i for i in range(a1 + 1, end)
            if len(lines[i]) - len(lines[i].lstrip()) == indent
            and lines[i].strip() == "ELSE"
        )
        end_if = next(
            i for i in range(a2 + 1, end)
            if len(lines[i]) - len(lines[i].lstrip()) == indent
            and lines[i].strip() == "ENDIF"
        )
        result.append({"a0": a0, "a1": a1, "a2": a2, "end": end_if})
    return result


def remove_nonzero_branches(
    lines: list[str], start: int, end: int, keep_a2: set[int] | None = None
) -> None:
    keep_a2 = keep_a2 or set()
    slots = branch_slots(lines, start, end)
    for branch_index in reversed(range(2)):
        slot = slots[branch_index]
        if branch_index in keep_a2:
            # Retain the existing A==2 text as one safe A==1 branch; A==2 now
            # deliberately produces no additional scene-mismatched text.
            del lines[slot["a1"] : slot["a2"]]
            lines[slot["a2"]] = lines[slot["a2"]].replace("ELSE", "ELSEIF A == 1", 1)
        else:
            del lines[slot["a1"] : slot["end"]]


def set_print_line(line: str, text: str) -> str:
    if "「" not in line:
        raise RuntimeError(f"not a dialogue line: {line!r}")
    return line.split("「", 1)[0] + "「" + text + "」"


def rewrite_four_branches(lines: list[str], start: int, end: int, texts: list[str]) -> None:
    slots = branch_slots(lines, start, end)
    indices: list[int] = []
    for slot in slots:
        a1_lines = [
            i for i in range(slot["a1"] + 1, slot["a2"])
            if "PRINT" in lines[i] and "「" in lines[i]
        ]
        a2_lines = [
            i for i in range(slot["a2"] + 1, slot["end"])
            if "PRINT" in lines[i] and "「" in lines[i]
        ]
        if len(a1_lines) != 1 or len(a2_lines) != 1:
            raise RuntimeError("expected one PRINT line in each RAND3 nonzero branch")
        indices.extend((a1_lines[0], a2_lines[0]))
    if len(texts) != 4:
        raise RuntimeError("expected four replacement texts")
    for index, text in zip(indices, texts):
        lines[index] = set_print_line(lines[index], text)


def process_yako(path: Path) -> None:
    text = path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    # やこ：下町の屋台飯に屋上の追加枝が入っているため、非ゼロ枝を削除。
    start, end = group_range(lines, 410, 414)
    command = command_ranges(lines, start, end)[410]
    remove_nonzero_branches(lines, *command)
    path.write_bytes("\r\n".join(lines).encode("cp932"))


def process_mari(path: Path) -> None:
    text = path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    # まり：シャワー室は全追加枝が夜のコートなので削除。純愛2枠は、
    # 散歩／ラリーに通る通常側の一枝だけを残す。
    start, end = group_range(lines, 280, 284)
    command = command_ranges(lines, start, end)[281]
    remove_nonzero_branches(lines, *command)
    start, end = group_range(lines, 410, 414)
    ranges = command_ranges(lines, start, end)
    remove_nonzero_branches(lines, *ranges[411], keep_a2={1})
    start, end = group_range(lines, 410, 414)
    ranges = command_ranges(lines, start, end)
    remove_nonzero_branches(lines, *ranges[412], keep_a2={1})
    path.write_bytes("\r\n".join(lines).encode("cp932"))


def process_kaede(path: Path) -> None:
    text = path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")

    # かえで：COM410「風紀の見回りデート」の追加4枝を場面に合わせて書き直す。
    start, end = group_range(lines, 410, 414)
    command = command_ranges(lines, start, end)[410]
    rewrite_four_branches(
        lines,
        *command,
        [
            "ふん、見回りのはずなのに……あんたが隣にいると、誰かに見つかりそうで落ち着かないじゃない♪",
            "手、つなぐならさりげなくしなさいよ……っ。……離れたら、それはそれで気になるでしょうが♪",
            "ちょっと、勝手に先へ行かない！　見回りはあたしの隣、ほら、そこにいなさいよ！",
            "寄り道は終わり。……あんたと歩くのが嫌なんじゃなくて、巡回の時間が押してるだけなんだからねっ！",
        ],
    )
    path.write_bytes("\r\n".join(lines).encode("cp932"))


def main() -> None:
    yako = next(CHAR_DIR.glob("CHAR_52_*_COM.ERB"))
    mari = next(CHAR_DIR.glob("CHAR_53_*_COM.ERB"))
    kaede = next(CHAR_DIR.glob("CHAR_60_*_COM.ERB"))
    process_yako(yako)
    process_mari(mari)
    process_kaede(kaede)


if __name__ == "__main__":
    main()
