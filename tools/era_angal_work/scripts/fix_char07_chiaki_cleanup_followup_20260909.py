"""ラクロス比喩整理で増えた汎用羞恥語を追加整理する。"""

from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_07_高原ちあき_COM.ERB"
REPLACEMENTS = {
    "「お尻まで来ると、あたし、身体が勝手に跳ねちゃいます～っ！　見ないでください、お兄ちゃん先輩……！」":
        "「お尻まで来ると、あたし、身体が勝手に跳ねちゃいます～っ！　そんな顔で見ないで、お兄ちゃん先輩……！」",
    "「うう、お兄ちゃん先輩～！　足に力が入らないですぅ……こんなふうに使うために鍛えたんじゃないですよ～!?」":
        "「うう、お兄ちゃん先輩～！　足に力が入らないです～……こんなふうに使うために鍛えたんじゃないですよ～!?」",
    "「針を使うなら、先に狙いを教えてください！　いきなりは、心の準備ができないですよ～っ！」":
        "「針を使うなら、先に狙いを教えてください！　いきなりだと、声が出ちゃいますよ～っ！」",
    "「うひゃっ、そんなに急がないでください！　あたし、まだ心の準備ができてないですよ～っ！」":
        "「うひゃっ、そんなに急がないでください！　あたし、まだ気持ちが追いついてないですよ～っ！」",
}


def main() -> int:
    text = TARGET.read_bytes().decode("cp932")
    for old, new in REPLACEMENTS.items():
        if text.count(old) != 1:
            raise RuntimeError(f"expected one occurrence, got {text.count(old)}: {old}")
        text = text.replace(old, new, 1)
    TARGET.write_bytes(text.encode("cp932"))
    print(f"follow-up rewrote {len(REPLACEMENTS)} lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
