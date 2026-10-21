"""ちあきの追加整理で、汎用的な「見ないで」を増やさない。"""

from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_07_高原ちあき_COM.ERB"
OLD = "「お尻まで来ると、あたし、身体が勝手に跳ねちゃいます～っ！　そんな顔で見ないで、お兄ちゃん先輩……！」"
NEW = "「お尻まで来ると、あたし、身体が勝手に跳ねちゃいます～っ！　そんなに見つめられたら、余計に止まらないですよ、お兄ちゃん先輩……！」"


def main() -> int:
    text = TARGET.read_bytes().decode("cp932")
    if text.count(OLD) != 1:
        raise RuntimeError(f"expected one occurrence, got {text.count(OLD)}")
    TARGET.write_bytes(text.replace(OLD, NEW, 1).encode("cp932"))
    print("removed added generic 見ないで from CHAR07")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
