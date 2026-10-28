from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_46_双葉みづき_COM.ERB"

REPLACEMENTS = {
    '「%LOCALS%とキスしてるところ、わたしに見せつける気かよ……っ。ふふん、そういう儀式なら最後まで見届けてやるぞ☆」': '「%LOCALS%にキスするところ、転校生に見せつける気かよ……っ。ふふん、そういう儀式なら最後まで見届けてやるぞ☆」',
    '「ちゅ……っ、近い近い！　転校生、そんな顔で見るなよ。わたしまで変な魔力に巻き込まれるだろ……♪」': '「ちゅ……っ、%LOCALS%の唇、やわらか……って、転校生が見てるのか。そ、そういう魔力観測は近すぎるだろ……♪」',
    '「もう一回って、%LOCALS%に頼むのか？　……べつに止めないけど、終わったらわたしのところへ戻ってこいよ☆」': '「もう一回って、%LOCALS%に頼むのか？　……べつに止めないけど、転校生はちゃんと見てろよ。わたしの勝ちだからな☆」',
    '「おわっ、%LOCALS%にいきなり!?　な、なんだその実験、わたしを立会人にするなよ～っ！」': '「おわっ、%LOCALS%にキスしてるところを転校生に見られるのか!?　な、なんだその実験、わたしを立会人にするなよ～っ！」',
    '「ん……っ、見てるだけなのに変な感じだぞ。転校生、こっちを試験管みたいに観察するな～っ」': '「ん……っ、%LOCALS%の唇、思ったより近い……。転校生、こっちを観察するなよ。わたしまで変な感じになるだろ～っ」',
    '「%LOCALS%、顔が真っ赤じゃんか。……その、嫌じゃないなら続けてもいいけど、わたしは知らないからな☆」': '「%LOCALS%、顔が真っ赤じゃんか。……その、嫌じゃないなら続けてもいいけど、転校生はよそ見するなよ☆」',
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    for old, new in REPLACEMENTS.items():
        if text.count(old) != 1:
            raise SystemExit(f"expected one occurrence: {old}")
        text = text.replace(old, new, 1)
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
