from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")

old = """PRINTFORMW 「あぁっ、おまえの足で私のを……っ♪　恋人にこんなふうにされると、変な気分になっちゃうなぁ……っ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「足の裏で熱が返ってくるな。いつもの応援とは違うけど、これはこれで効くぞ☆」
\t\tELSE
\t\t\tPRINTFORMW 「ふぁ……じれったいのに、ゆっくりだから余計に待ってしまうな♪」
\t\tENDIF
\tELSE
\t\t;通常
\t\tA = RAND:3
\t\tIF A == 0
\t\t\tPRINTFORMW 「わっ、足でこするのか!?　……んっ、こ、こんなやり方、初めてで……っ、変だけど気持ちいいぞ転校生くん☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃっ、足で！？　うう、こんな触り方があるとは知らなかったぞ……！」
\t\tELSE
\t\t\tPRINTFORMW 「んっ、足の力まで見られてるみたいで恥ずかしい。だが、離すとは言ってないぞ」
\t\tENDIF"""
new = """PRINTFORMW 「あぁっ、転校生くんの足が私のに……っ♪　恋人に足で扱かれると、いつもの応援とは違う熱が来るなぁ……っ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「んっ、足の裏で擦られるたび、私のが跳ねる……じれったいのに、転校生くんの足から離れたくないぞ☆」
\t\tELSE
\t\t\tPRINTFORMW 「ふぁ……指よりゆっくりなのに、転校生くんの足で待たされるぶん、身体の奥まで熱くなるな♪」
\t\tENDIF
\tELSE
\t\t;通常
\t\tA = RAND:3
\t\tIF A == 0
\t\t\tPRINTFORMW 「わっ、転校生くんの足で私のをこするのか!?　……んっ、こ、こんな受け方があるのか……っ、変だけど気持ちいいぞ☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃっ、足の裏で挟まれてる!?　うう、動かれるたびに私のが反応するぞ……！」
\t\tELSE
\t\t\tPRINTFORMW 「んっ、転校生くんの足で扱かれるところまで見られるのか……恥ずかしいのに、離れろとは言えないぞ……っ。」
\t\tENDIF"""

old = old.replace("\n", "\r\n")
new = new.replace("\n", "\r\n")
assert text.count(old) == 1, "CHAR67 COM67 block is not unique"
PATH.write_bytes(text.replace(old, new, 1).encode("cp932"))
