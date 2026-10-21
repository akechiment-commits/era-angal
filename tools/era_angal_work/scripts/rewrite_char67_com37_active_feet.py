from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")

old = """PRINTFORMW 「あぁっ、おまえの足で私のを……っ♪　恋人にこんなことされると、変な気分になっちゃうなぁ……っ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「んっ、足のあいだでおまえの熱が返ってくる……じれったいけど、息が合うと楽しいな☆」
\t\tELSE
\t\t\tPRINTFORMW 「ふぁ……指よりゆっくりなのに、待たされるぶん身体が熱くなるぞ♪」
\t\tENDIF
\tELSE
\t\t;通常
\t\tA = RAND:3
\t\tIF A == 0
\t\t\tPRINTFORMW 「わっ、足でこするのか!?　……んっ、こ、こんなやり方があるのか……っ、変だけど気持ちいいぞ転校生くん☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「わっ、足を重ねるだけでこんなに熱いのか！？　うう、変な感じだぞ……！」
\t\tELSE
\t\t\tPRINTFORMW 「んっ、足の力まで見られてるみたいで恥ずかしいけど、離すのは惜しいな」
\t\tENDIF"""
new = """PRINTFORMW 「あぁっ、私の足で転校生くんのを……っ♪　恋人にこんなふうにしてやると、変な気分になっちゃうなぁ……っ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「んっ、私の足のあいだで転校生くんの熱が返ってくる……じれったいけど、息が合うと楽しいな☆」
\t\tELSE
\t\t\tPRINTFORMW 「ふぁ……指よりゆっくり、私の足でこするのは難しいのに、待たされるぶん身体が熱くなるぞ♪」
\t\tENDIF
\tELSE
\t\t;通常
\t\tA = RAND:3
\t\tIF A == 0
\t\t\tPRINTFORMW 「わっ、私の足でこするのか!?　……んっ、こ、こんなやり方があるのか……っ、変だけど気持ちいいぞ転校生くん☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「わっ、私の足を重ねるだけでこんなに熱いのか！？　うう、変な感じだぞ……！」
\t\tELSE
\t\t\tPRINTFORMW 「んっ、私の足の力まで見られてるみたいで恥ずかしいけど、離すのは惜しいな転校生くん……っ。」
\t\tENDIF"""

old = old.replace("\n", "\r\n")
new = new.replace("\n", "\r\n")
assert text.count(old) == 1, "CHAR67 COM37 block is not unique"
PATH.write_bytes(text.replace(old, new, 1).encode("cp932"))
