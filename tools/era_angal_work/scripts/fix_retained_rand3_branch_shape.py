"""まりの残存1枝を A == 1 の単独枝として整形する。"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from repair_remaining_unique_scene_branches import command_ranges, group_range  # noqa: E402


def fix(command: int) -> None:
    path = next((ROOT / "ERB" / "CHAR").glob("CHAR_53_*_COM.ERB"))
    lines = path.read_bytes().decode("cp932").replace("\r\n", "\n").split("\n")
    start, end = group_range(lines, 410, 414)
    block_start, block_end = command_ranges(lines, start, end)[command]
    a0 = [i for i in range(block_start, block_end) if lines[i].strip() == "IF A == 0"]
    if len(a0) != 2:
        raise RuntimeError(f"COM{command}: expected two A == 0 branches")
    indent = len(lines[a0[1]]) - len(lines[a0[1]].lstrip())
    candidates = [
        i for i in range(a0[1] + 1, block_end)
        if len(lines[i]) - len(lines[i].lstrip()) == indent and lines[i].strip() == "ELSE"
    ]
    if len(candidates) != 1:
        raise RuntimeError(f"COM{command}: retained branch marker is ambiguous")
    lines[candidates[0]] = lines[candidates[0]].replace("ELSE", "ELSEIF A == 1", 1)
    path.write_bytes("\r\n".join(lines).encode("cp932"))


if __name__ == "__main__":
    fix(411)
    fix(412)
