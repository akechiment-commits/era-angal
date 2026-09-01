from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_58_天宮るり_COM.ERB"


REPLACEMENTS = [
    (
        '「ふぅむ、わたしの髪質、観測データに追加します。意外と、扱いやすいですね♪」',
        '「ふぅむ、るりの髪質、観測データに追加します。意外と、扱いやすいですね♪」',
    ),
    (
        '「この櫛、いい仕事するでしょ♪　わたしの髪、つやつやになぁれ……るるる☆」',
        '「この櫛、いい仕事するでしょ♪　あたしの髪、つやつやになぁれ……るるる☆」',
    ),
    (
        '「できた♪　わたしの髪、宇宙でいちばん整ってる……あなたに梳いてもらえて、嬉しいです、るるる☆」',
        '「できた♪　あたしの髪、宇宙でいちばん整ってる……あなたに梳いてもらえて、嬉しいです、るるる☆」',
    ),
    (
        '「ふぅむ、わたしの手つき、丁寧でしょう。観測データに追加します……心地よい、です♪」',
        '「ふぅむ、るりの手つき、丁寧でしょう。観測データに追加します……心地よい、です♪」',
    ),
    (
        '「櫛で、ですか。るるる、道具を使えば、より精密に……あたしの髪、ゆっくり梳いてください、転校生のひと☆」',
        '「櫛で、ですか。るるる、道具を使えば、より精密に……るりの髪、ゆっくり梳いてください、転校生のひと☆」',
    ),
    (
        '「あなた、少し肩に力が入っています。……ほら、息を吐いて。あたしが撫でていますから」',
        '「あなた、少し肩に力が入っています。……ほら、息を吐いて。るりが撫でていますから」',
    ),
]


def main() -> None:
    text = PATH.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    changed = 0
    for old, new in REPLACEMENTS:
        old_count = text.count(old)
        new_count = text.count(new)
        if old_count == 1 and new_count == 0:
            text = text.replace(old, new, 1)
            changed += 1
        elif old_count == 0 and new_count == 1:
            continue
        else:
            raise RuntimeError(f"unexpected match counts for {old!r}: old={old_count}, new={new_count}")
    PATH.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print(f"updated CHAR58 voice tier: {changed} replacements")


if __name__ == "__main__":
    main()
