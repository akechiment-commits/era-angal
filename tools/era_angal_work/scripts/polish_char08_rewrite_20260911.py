"""CHAR08高類似リライト後の語彙を、みさき原作の言い回しへ微調整する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_08_丸子みさき_COM.ERB"


REPLACEMENTS = [
    (
        "こんなところまで見てくれるんですね……。先輩に見られるなら、あたしもちゃんとしなきゃって思います♪",
        "こんなところまで見てくれるんですね……。先輩に見られるなら、あたしもちゃんとしなきゃって思います♪",
    ),
    (
        "先輩がそこまで気を使ってくれると、あたしまでちゃんとしなきゃって思います……♪",
        "先輩がそこまで気を使ってくれると、あたしまでちゃんとしなきゃって思います……♪",
    ),
    (
        "あ、あれ……もう終わったのに、まだ落ちつかない……。先輩、その顔で笑うのは禁止ですからね",
        "あ、あれ……もう終わったのに、まだ落ちつかない……。先輩、その顔で笑うのは禁止ですからね",
    ),
    (
        "あっ、そこは……！　先輩、あたし、もう声を我慢できないです～っ！",
        "あっ、そこは……！　先輩、あたし、もう声を我慢できないです～っ！",
    ),
    (
        "やっと終わった……って、先輩、まだ触る気ですか!?　あたし、もう平気なふりできませんからね！",
        "やっと終わった……って、先輩、まだ触る気ですか!?　あたし、もうどんな顔をすればいいんですか！",
    ),
    (
        "終わっても、まだ先輩の声が残ってるみたい……。先輩の顔を見ると、もう一度って思っちゃいます……っ",
        "終わっても、まだ先輩の声が残ってるみたい……。先輩の顔を見ると、もう一度って思っちゃいます……っ",
    ),
]


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    for old, new in REPLACEMENTS:
        marker_old = f"「{old}」"
        marker_new = f"「{new}」"
        if text.count(marker_old) != 1:
            raise RuntimeError(f"expected one occurrence, got {text.count(marker_old)}: {old}")
        text = text.replace(marker_old, marker_new, 1)
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))
    print(f"polished={len(REPLACEMENTS)}")


if __name__ == "__main__":
    main()
