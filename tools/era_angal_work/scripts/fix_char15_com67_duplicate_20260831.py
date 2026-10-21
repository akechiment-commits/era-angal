"""CHAR15 COM67の誤って重複した一方の分岐だけを分離する。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_15_長町やえ_COM.ERB"


OLD = "「足を重ねたまま動けないっ……。おに～さんの熱がじわじわ伝わって、顔まで真っ赤だよぉ……！」"
NEW = "「足の甲でゆっくり押すと、おに～さんの息が変わるっ……。あたし、手ぇを使わなくても感じさせられるんだねっ♪」"


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    count = text.count(OLD)
    if count != 2:
        raise RuntimeError(f"COM67重複台詞の出現数が不正です: {count}件")
    text = text.replace(OLD, NEW, 1)
    TARGET.write_bytes(text.encode("cp932"))
    print("CHAR15 COM67の重複台詞を1分岐だけ改稿: 1件")


if __name__ == "__main__":
    main()
