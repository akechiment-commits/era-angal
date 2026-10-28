from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")

old = """PRINTFORMW 「はぁ……っ、おまえのこと考えてたら、こんなに……っ。恋人くん、私の自慰、見ててくれるか……っ♪」
\t\t\tELSEIF A == 1
\t\t\t\t;恋人・ビデオ・2
\t\t\t\tPRINTFORMW 「あぁっ、おまえを想いながら指でいじると……っ、すぐイっちゃいそうだ……っ。早く会いたいぞ転校生くん♪」
\t\t\tELSE
\t\t\t\t;恋人・ビデオ・3
\t\t\t\tPRINTFORMW 「んっ、おまえの顔を思い浮かべると、止まらなくなっちゃう……っ。恋人くん、私のこと考えてくれてるか♪」"""
new = """PRINTFORMW 「はぁ……っ、カメラが回ってるのに、おまえのことを考えたら指が止まらない……っ。転校生くん、私の自慰、最後まで見ててくれ……っ♪」
\t\t\tELSEIF A == 1
\t\t\t\t;恋人・ビデオ・2
\t\t\t\tPRINTFORMW 「あぁっ、録画されながら指でいじると、いつもより恥ずかしいぞ……っ。転校生くんの恋人として、こんな姿まで残していいのか……っ♪」
\t\t\tELSE
\t\t\t\t;恋人・ビデオ・3
\t\t\t\tPRINTFORMW 「んっ、カメラに向かってるのに、転校生くんの顔を思い浮かべると止まらなくなっちゃう……っ。愛してるぞ、ちゃんと見ててくれ♪」"""

old = old.replace("\n", "\r\n")
new = new.replace("\n", "\r\n")
assert text.count(old) == 1, "CHAR67 COM3 lover video block is not unique"
PATH.write_bytes(text.replace(old, new, 1).encode("cp932"))
