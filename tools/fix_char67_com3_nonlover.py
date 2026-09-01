from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")

old1 = "PRINTFORMW 「ふぁ……っ、恋人がいるのに自分でしちゃうなんて……っ。でも、おまえを想うと我慢できないんだ……っ♪」"
new1 = "PRINTFORMW 「ふぁ……っ、ひとりでするところを撮るなんて……っ。でも、転校生くんの顔を思い浮かべると我慢できないんだ……っ♪」"
old2 = "PRINTFORMW 「はぁ、はぁ……っ、イっちゃった……。えへへ、おまえのこと考えると、すぐだなぁ……愛してるぞ恋人くん♪」"
new2 = "PRINTFORMW 「はぁ、はぁ……っ、イっちゃった……。転校生くんのことを考えると、すぐだなぁ……っ♪」"

assert text.count(old1) == 1, "CHAR67 COM3 non-lover video line 1 is not unique"
assert text.count(old2) == 1, "CHAR67 COM3 non-lover video line 3 is not unique"
text = text.replace(old1, new1, 1).replace(old2, new2, 1)
PATH.write_bytes(text.encode("cp932"))
