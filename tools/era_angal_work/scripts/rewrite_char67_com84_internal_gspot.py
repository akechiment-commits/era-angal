from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")

old = """; 転校生くんがましろのクリとおまんこを刺激する。受けているましろの声にする。
IF SELECTCOM == 84
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「クリをなぞるだけで、こんなに……っ。転校生くん、そこは恋人の弱点だ、覚えておけ……あぁっ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「おまんこを指で探られると、応援の声が裏返る……っ。私をここまで崩せるのは、おまえだけだぞ☆」
\t\tELSE
\t\t\tPRINTFORMW 「奥の気持ちいいところ、もっと押してくれ……っ。攻めるつもりだったのに、私のほうが転校生くんを求めてる♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ふぇっ？　そこはクリだぞ!?　なぜ変な声を!?　転校生くん、どこか痛いのか……あっ、違うのか!?」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「おまんこを指で……っ、うわぁ、考えるより先に腰が跳ねた！　これは応援されている側なのか!?」
\t\tELSE
\t\t\tPRINTFORMW 「んんっ、奥を押すな、いや待て、やっぱりもう一度……っ！　私、指一本でこんなに負けるのかぁっ!?」
\t\tENDIF
\tENDIF
ENDIF"""
new = """; 転校生くんがましろのおまんこの奥、上側を刺激する。受けているましろの声にする。
IF SELECTCOM == 84
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「中の上側をなぞられるだけで、こんなに……っ。転校生くん、そこは恋人の弱点だ、覚えておけ……あぁっ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「おまんこの奥を指で探られると、応援の声が裏返る……っ。私をここまで崩せるのは、転校生くんだけだぞ☆」
\t\tELSE
\t\t\tPRINTFORMW 「奥の気持ちいいところ、もっと上を押してくれ……っ。攻めるつもりだったのに、私のほうが転校生くんを求めてる♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ふぇっ？　おまんこの奥の上側を押すのか!?　なぜ変な声を!?　転校生くん、どこか痛いのか……あっ、違うのか!?」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「おまんこの中を指で……っ、うわぁ、考えるより先に腰が跳ねた！　これは応援されている側なのか!?」
\t\tELSE
\t\t\tPRINTFORMW 「んんっ、奥の上側を押すな、いや待て、やっぱりもう一度……っ！　私、指一本でこんなに負けるのかぁっ!?」
\t\tENDIF
\tENDIF
ENDIF"""

old = old.replace("\n", "\r\n")
new = new.replace("\n", "\r\n")
assert text.count(old) == 1, "CHAR67 COM84 block is not unique"
PATH.write_bytes(text.replace(old, new, 1).encode("cp932"))
