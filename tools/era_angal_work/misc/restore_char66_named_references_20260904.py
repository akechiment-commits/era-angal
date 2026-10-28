"""CHAR66 COM312から視点整理時に落ちた固有名を復元する。"""

from __future__ import annotations

from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_66_曽根セイラ_COM.ERB"
OLD = "「えっ、頭、撫でてくれるの……？　はうう、こうして甘やかされるの、なんだか新鮮だけれど～♪」"
NEW = "「えっ、頭、撫でてくれるの……？　はうう、クロちゃんやルカちゃんを撫でるときとは違って、こうして甘やかされるの、なんだか新鮮だけれど～♪」"


def main() -> int:
    text = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n")
    count = text.count(OLD)
    if count == 0 and text.count(NEW) == 1:
        print("CHAR66 COM312の固有名: 変更なし")
        return 0
    if count != 1:
        raise ValueError(f"CHAR66 COM312の復元対象が一意でない: {count}")
    TARGET.write_bytes(text.replace(OLD, NEW).replace("\n", "\r\n").encode("cp932"))
    print("CHAR66 COM312のクロちゃん・ルカちゃん呼びを復元")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
