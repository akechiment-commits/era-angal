#!/usr/bin/env python3
"""CHAR02 COM187の未差別化行を、ゆきの不安と先輩への依存へ補正する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_02_北川ゆき_COM.ERB"
OLD = "ごくっ……。これで大丈夫なんですか？　次からは、もっと気をつけてください……っ"
NEW = "ごくっ……。あの、これで心配はなくなったんですよね？　次からは、先輩も忘れないでください……っ"


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    if text.count(f"「{OLD}」") != 1:
        raise SystemExit("COM187の補正対象が一意ではありません")
    text = text.replace(f"「{OLD}」", f"「{NEW}」", 1)
    encoded = text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932")
    if b"\n" in encoded.replace(b"\r\n", b""):
        raise SystemExit("lone LF が混入しました")
    TARGET.write_bytes(encoded)
    print(f"updated {TARGET}")


if __name__ == "__main__":
    main()
