from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")


def crlf(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\n", "\r\n")


old = """\t\t\tPRINTFORMW 「えっ、%LOCALS%に先を取られた!?　転校生くん、見ているなら笑うなよ……んむっ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ちゅ、ちゅう……っ。%LOCALS%の唇、元気すぎるぞ……私の頬まで熱くなってきた♪」
\t\tELSE
\t\t\tPRINTFORMW 「転校生くんへの愛は揺るがないが、%LOCALS%との親睦も大切……んむ、って近いぞぉっ☆」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「おやっ、%LOCALS%からキスの応援か!?　ふむふむ、仲間の士気を上げるには……んむっ!?」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ちゅっ……ええと、これは挨拶だな！　転校生くん、変な顔をするな、親睦の一環だぞ☆」
\t\tELSE
\t\t\tPRINTFORMW 「んん～？　唇を重ねると声援より伝わるのか……%LOCALS%、もう一度だけ実験するか？」
\t\tENDIF"""

new = """\t\t\tPRINTFORMW 「%LOCALS%、こっちへ来い！　転校生くんが見ていても、親睦のキスくらい堂々とするぞ……ちゅっ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「んむっ、%LOCALS%の唇は元気がいいな♪　私からもう一度いくぞ、転校生くん、目をそらすなよ☆」
\t\tELSE
\t\t\tPRINTFORMW 「転校生くんへの愛は揺るがないからな！　だから%LOCALS%にも応援の気持ちを……むっちゅ♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「%LOCALS%、挨拶のキスだぞ！　転校生くん、これは仲間の親睦であって、変な意味では……んむっ☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ちゅっ……おやっ、唇を重ねると声援より伝わるのか？　%LOCALS%、もう一度試してみるか！」
\t\tELSE
\t\t\tPRINTFORMW 「転校生くん、見ているか？　私から%LOCALS%へ元気をお届けだ！　んっ、ちゅう……♪」
\t\tENDIF"""

old = crlf(old)
new = crlf(new)

assert text.count(old) == 1, "CHAR67 COM60 old dialogue block is not unique"
text = text.replace(old, new, 1)
PATH.write_bytes(text.encode("cp932"))
