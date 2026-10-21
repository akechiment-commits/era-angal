"""CHAR27のつゆり専用特殊分岐を、助手一般化前の固定呼称へ戻す。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_27_夏野ゆり_COM.ERB"
BACKUP = ROOT / "tools/backups/assistant_locals_viewpoint_20260904" / TARGET.name
START = ";=== NATSUNO YURI TSUYURI TRAINER SPECIAL START ==="
END = ";=== NATSUNO YURI TSUYURI TRAINER SPECIAL END ==="


def main() -> int:
    current = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n")
    original = BACKUP.read_bytes().decode("cp932").replace("\r\n", "\n")
    current_start = current.index(START)
    current_end = current.index(END, current_start) + len(END)
    original_start = original.index(START)
    original_end = original.index(END, original_start) + len(END)
    current_special = current[current_start:current_end]
    original_special = original[original_start:original_end]
    if current_special == original_special:
        print("CHAR27つゆり専用分岐: 変更なし")
        return 0
    restored = current[:current_start] + original_special + current[current_end:]
    TARGET.write_bytes(restored.replace("\n", "\r\n").encode("cp932"))
    print(
        f"CHAR27つゆり専用分岐を復元: %LOCALS% {current_special.count('%LOCALS%')}件を除去、"
        f"つゆりちゃん {original_special.count('つゆりちゃん')}件を維持"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
