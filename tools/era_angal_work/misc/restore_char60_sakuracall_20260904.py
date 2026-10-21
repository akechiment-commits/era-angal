"""CHAR60 COM202の既存固有名「さくらさん」を復元する。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_60_瀬川かえで_COM.ERB"
BACKUP = ROOT / "tools/backups/assistant_locals_viewpoint_20260904" / TARGET.name
OLD = "「んっ、柔らかいものが重なると……っ。%LOCALS%には絶対に言わないでよね」"
NEW = "「んっ、柔らかいものが重なると……っ。さくらさんには絶対に言わないでよね」"


def main() -> int:
    text = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n")
    backup = BACKUP.read_bytes().decode("cp932").replace("\r\n", "\n")
    expected = backup.count(NEW)
    current = text.count(OLD)
    if current == 0 and text.count(NEW) == expected:
        print("CHAR60 COM202のさくらさん呼び: 変更なし")
        return 0
    if current != 1 or expected != 1:
        raise ValueError(f"CHAR60 COM202の復元対象が一意でない: current={current}, backup={expected}")
    text = text.replace(OLD, NEW)
    TARGET.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print("CHAR60 COM202のさくらさん呼びを復元")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
