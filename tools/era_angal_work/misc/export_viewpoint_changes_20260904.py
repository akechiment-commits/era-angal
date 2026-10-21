from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_koujo_integrity import char_number, extract_blocks, read_cp932  # noqa: E402
import fix_all_char_sweet_words_viewpoint_20260904 as sweet  # noqa: E402
import fix_hair_viewpoint_batch_20260904 as hair  # noqa: E402
import fix_other_viewpoint_batch_20260904 as other  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]


def target(number: int) -> Path:
    return next(ROOT.glob(f"ERB/CHAR/CHAR_{number:02d}_*_COM.ERB"))


def emit_dialogue(label: str, cases: dict[int, dict], backup_dir: str, default_command: int | None = None) -> None:
    print(f"### {label}")
    for number, case in cases.items():
        path = target(number)
        backup = ROOT / "tools/backups" / backup_dir / path.name
        current = read_cp932(path)
        before = read_cp932(backup)
        blocks = extract_blocks(current)
        entries: list[tuple[int, str]] = []
        for new in case["rewrites"].values():
            if current.count(new) <= before.count(new):
                continue
            commands = [
                block.number
                for block in blocks.values()
                if new in block.body
            ]
            command = commands[0] if commands else default_command
            entries.append((command or 0, new))
        if not entries:
            continue
        print(f"\nCHAR{number:02d} {case['source']}" )
        for command, text in entries:
            print(f"COM{command}")
            print(text)


def main() -> int:
    emit_dialogue("COM311 甘い言葉", sweet.CASES, "sweet_words_viewpoint_20260904", 311)
    emit_dialogue("髪梳き・頭撫で", hair.CASES, "hair_viewpoint_batch_20260904")
    emit_dialogue("COM30・COM90・COM312", other.CASES, "other_viewpoint_batch_20260904")
    path = target(63)
    blocks = extract_blocks(read_cp932(path))
    print("\n### CHAR63 ちづる COM194 呼称補正")
    for line in blocks[194].lines:
        if "%LOCALS%" in line and line.lstrip().startswith("PRINTFORM"):
            print(line.strip())
    print("\n### 助手参加枠の変数補正")
    print("CHAR52: COM60/62/76/202/258")
    print("CHAR53: COM202/258")
    print("CHAR54: COM60/62/76/202/258")
    print("CHAR55/56/57/59: COM258")
    print("各枠で %CALLNAME:ASSI% → %LOCALS%、必要箇所に CALL AITE_YOBI と LOCALS 初期化を追加")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
