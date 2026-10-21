"""CHAR34 COM307から視点整理時に落ちた呼称を復元する。"""

from __future__ import annotations

from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_34_桐島かいり_COM.ERB"
OLD = "PRINTFORMW 「今日は桐島家の櫛で梳いていただけるんですの？　……ふふ、丁寧にお願いしますわ♪」"
NEW = "PRINTFORMW 「今日は桐島家の櫛で梳いていただけるんですの？　……お祖母さま譲りの逸品ですから、丁寧にお願いしますわ♪」"


def main() -> int:
    text = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n")
    count = text.count(OLD)
    if count == 0 and text.count(NEW) == 1:
        print("CHAR34 COM307の呼称: 変更なし")
        return 0
    if count != 1:
        raise ValueError(f"CHAR34 COM307の復元対象が一意でない: {count}")
    TARGET.write_bytes(text.replace(OLD, NEW).replace("\n", "\r\n").encode("cp932"))
    print("CHAR34 COM307のお祖母さま呼びを復元")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
