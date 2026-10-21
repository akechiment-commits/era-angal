#!/usr/bin/env python3
"""CHAR02 COM196の差別化後台詞に混入した相手呼称を視点に合わせて補正する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_02_北川ゆき_COM.ERB"
OLD = "やっ……抜けると、急に寒くなる……っ。まだ、身体が先輩を探してるみたいで……"
NEW = "やっ……抜けると、急に寒くなる……っ。まだ、身体が%LOCALS%を探してるみたいで……"


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    if text.count(f"「{OLD}」") != 1:
        raise SystemExit("COM196の補正対象が一意ではありません")
    text = text.replace(f"「{OLD}」", f"「{NEW}」", 1)
    encoded = text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932")
    if b"\n" in encoded.replace(b"\r\n", b""):
        raise SystemExit("lone LF が混入しました")
    TARGET.write_bytes(encoded)
    print(f"updated {TARGET}")


if __name__ == "__main__":
    main()
