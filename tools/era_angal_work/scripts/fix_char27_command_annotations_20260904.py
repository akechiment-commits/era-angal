from __future__ import annotations

import argparse
import re
from pathlib import Path

from restore_command_annotations import template_names


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_27_夏野ゆり_COM.ERB"
SELECTOR_RE = re.compile(
    r"^\s*(?:IF|ELSEIF)\s+SELECTCOM\s*==\s*(\d+)\b", re.IGNORECASE
)
HEADER_RE = re.compile(r"^\s*;---\s*COM\s*(\d+)(?:\s|-)" , re.IGNORECASE)

CUSTOM_NAMES = {
    280: "独自ウフフ（音楽室）",
    281: "独自ウフフ（楽器庫）",
    282: "独自ウフフ（掃除用具室）",
    283: "独自ウフフ（早朝の教室）",
    284: "独自ウフフ（屋上）",
    410: "独自純愛（クレーンゲーム）",
    411: "独自純愛（動物カフェ）",
    412: "独自純愛（グッズ屋めぐり）",
    413: "独自純愛（帰り道）",
    414: "独自純愛（花火の帰り）",
}


def command_names() -> dict[int, str]:
    names = template_names()
    names.update(CUSTOM_NAMES)
    return names


def has_nearby_header(lines: list[str], index: int, command: int) -> bool:
    for line in lines[max(0, index - 12) : index]:
        match = HEADER_RE.match(line)
        if match and int(match.group(1)) == command:
            return True
    return False


def build_lines(lines: list[str]) -> tuple[list[str], list[tuple[int, int, str]]]:
    names = command_names()
    output: list[str] = []
    inserted: list[tuple[int, int, str]] = []
    for line_number, line in enumerate(lines, 1):
        match = SELECTOR_RE.match(line)
        if match:
            command = int(match.group(1))
            if command not in names:
                raise SystemExit(f"名称未登録のSELECTCOM: {command}行目 COM{command}")
            if not has_nearby_header(lines, line_number - 1, command):
                header = f";--- COM{command} {names[command]} ---"
                output.append(header)
                inserted.append((line_number, command, header))
        output.append(line)
    return output, inserted


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    lines = TARGET.read_bytes().decode("cp932").splitlines()
    new_lines, inserted = build_lines(lines)
    print(f"対象: {TARGET}")
    print(f"追加予定注釈: {len(inserted)}件")
    for line_number, command, header in inserted:
        print(f"L{line_number}: COM{command} {header}")
    if args.dry_run:
        return
    TARGET.write_bytes(("\r\n".join(new_lines) + "\r\n").encode("cp932"))
    print("反映しました")


if __name__ == "__main__":
    main()
