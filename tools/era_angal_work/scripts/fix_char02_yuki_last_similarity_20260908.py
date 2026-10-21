#!/usr/bin/env python3
"""CHAR02 北川ゆきに残ったかなえとの中程度類似2行を最終差別化する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_02_北川ゆき_COM.ERB"

REPLACEMENTS = {
    "……わかりました、飲みます。でも、変なことが起きたら、すぐそばにいてくださいね……":
        "……わかりました、飲みます。もしおかしくなったら……そのときは、先輩に最初に知らせますから……",
    "んっ……もう少し浅く……いえ、止めないで。今のは、忘れてください……♪":
        "んっ……浅いところでも、こんなに……。先輩、わたし、もう止めかたがわからないです……♪",
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    for old, new in REPLACEMENTS.items():
        if text.count(f"「{old}」") != 1:
            raise SystemExit(f"補正対象が一意ではありません: {old}")
        text = text.replace(f"「{old}」", f"「{new}」", 1)
    encoded = text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932")
    if b"\n" in encoded.replace(b"\r\n", b""):
        raise SystemExit("lone LF が混入しました")
    TARGET.write_bytes(encoded)
    print(f"updated {TARGET}")
    print(f"replacements {len(REPLACEMENTS)}")


if __name__ == "__main__":
    main()
