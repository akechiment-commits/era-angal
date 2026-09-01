from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGETS = [
    ROOT / "ERB/CHAR/CHAR_31_夢路まりあ_COM.ERB",
    ROOT / "ERB/CHAR/CHAR_31_夢路まりあ.ERB",
]

# 「はわたくし」「はわかります」などの単語内部は対象外。
# 原作にある「はわ、わっ」はそのまま残し、それ以外の独立した「はわ」だけを
# 「はわわ」にする。既存の「はわわ」は (?!わ) で二重化しない。
INTERJECTION = re.compile(
    r"(?<![ぁ-んァ-ヶ一-龠])はわ(?!わ)(?!、わっ)(?=[、。！？…♪」』】っ]|$)"
)


def main() -> None:
    for target in TARGETS:
        raw = target.read_bytes()
        text = raw.decode("cp932")
        updated, count = INTERJECTION.subn("はわわ", text)
        target.write_bytes(updated.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))
        print(f"{target.name}: {count} interjections normalized")


if __name__ == "__main__":
    main()
