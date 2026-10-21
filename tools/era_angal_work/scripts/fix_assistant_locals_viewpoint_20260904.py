"""助手参加COMの相手呼称を、各ブロック内の%LOCALS%へ統一する。"""

from __future__ import annotations

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "tools/backups/assistant_locals_viewpoint_20260904"
TARGETS = {
    27: {60, 62, 76, 202, 258},
    52: {60, 62, 76, 202, 258},
    53: {202, 258},
    54: {60, 62, 76, 202, 258},
    55: {258},
    56: {258},
    57: {258},
    59: {258},
    60: {202},
}
SPECIAL_CHAR27 = {60, 62, 76, 202, 258}


def command_span(text: str, command: int) -> tuple[int, int]:
    marker = f";--- COM{command}"
    start = text.index(marker)
    next_heading = text.find(";--- COM", start + len(marker))
    next_return = text.find("\nRETURN 0", start)
    ends = [x for x in (next_heading, next_return) if x >= 0]
    return start, min(ends) if ends else len(text)


def fix_block(block: str, number: int, command: int) -> tuple[str, int]:
    body_start = block.index(f"IF SELECTCOM == {command}")
    line_end = block.index("\n", body_start)
    body = block[body_start:]
    changed = 0
    if "CALL AITE_YOBI" not in body:
        body = body[: line_end - body_start + 1] + f"\tCALL AITE_YOBI, {number}, ASSI\n\tLOCALS '= @\"%RESULTS%\"\n" + body[line_end - body_start + 1:]
        changed += 1
    body = body.replace("%CALLNAME:ASSI%", "%LOCALS%")
    if "%LOCALS%" in body:
        changed += 1
    return block[:body_start] + body, changed


def fix_char27_special(text: str) -> tuple[str, int]:
    """つゆり専用分岐は固有呼称・固有構造を維持し、一般化しない。"""
    return text, 0


def main() -> int:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    changed = 0
    for number, commands in TARGETS.items():
        target = next(ROOT.glob(f"ERB/CHAR/CHAR_{number:02d}_*_COM.ERB"))
        backup = BACKUP_DIR / target.name
        if not backup.exists():
            shutil.copy2(target, backup)
        text = target.read_bytes().decode("cp932").replace("\r\n", "\n")
        for command in sorted(commands):
            start, end = command_span(text, command)
            block = text[start:end]
            replacement, count = fix_block(block, number, command)
            text = text[:start] + replacement + text[end:]
            changed += count
        target.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print(f"助手呼称・%LOCALS%補正: {changed}件")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
