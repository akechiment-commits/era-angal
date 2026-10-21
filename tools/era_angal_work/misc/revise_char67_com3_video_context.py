from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")

old = """PRINTFORMW 「ふぁ……っ、ひとりでするところを撮るなんて……っ。でも、転校生くんの顔を思い浮かべると我慢できないんだ……っ♪」
\t\t\tELSEIF A == 1
\t\t\t\t;通常・ビデオ・2
\t\t\t\tPRINTFORMW 「あぁんっ、おまえの名前を呼びながら……っ。早く帰ってきてくれよ転校生くん、私、待ちきれないぞ……っ♪」
\t\t\tELSE
\t\t\t\t;通常・ビデオ・3
\t\t\t\tPRINTFORMW 「はぁ、はぁ……っ、イっちゃった……。転校生くんのことを考えると、すぐだなぁ……っ♪」"""
new = """PRINTFORMW 「ふぁ……っ、カメラに自慰を撮られてるのか……っ。転校生くん、こんな私を後で見るのか？　うぅ、変な声まで残るぞ……っ♪」
\t\t\tELSEIF A == 1
\t\t\t\t;通常・ビデオ・2
\t\t\t\tPRINTFORMW 「あぁんっ、録画中なのに止まらない……っ。転校生くんの名前を呼んだ声まで、ぜんぶ映像に残るのか……っ♪」
\t\t\tELSE
\t\t\t\t;通常・ビデオ・3
\t\t\t\tPRINTFORMW 「はぁ、はぁ……っ、イっちゃった……。カメラ、ちゃんと撮ったか？　転校生くんに見せるなら、笑うなよ……っ♪」"""

old = old.replace("\n", "\r\n")
new = new.replace("\n", "\r\n")
assert text.count(old) == 1, "CHAR67 COM3 non-lover video block is not unique"
PATH.write_bytes(text.replace(old, new, 1).encode("cp932"))
