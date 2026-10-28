from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")


COM90 = """;--- COM90 アナル愛撫させる ---
IF SELECTCOM == 90
\tIF TALENT:TARGET:153
\t\t;恋人
\t\tPRINTFORMW 「おまえのお尻、可愛がってやるぞ☆　んっ、ここをこうして……恋人の弱点、見つけちゃうもんね♪」
\tELSE
\t\t;通常
\t\tPRINTFORMW 「お尻を愛撫するのか☆　よぉし、私に任せろ……って、おまえもここ感じるんだな、ふむふむ、勉強だ転校生くん！」
\tENDIF
ENDIF
"""


ADDITIONAL10 = """;==============================================================
; CHAR67 追加10（助手・他キャラとの関係／通常と恋人 各RAND:3）
; 原作の「元気をお届け」「親睦」「愛情表現」を軸に、COMごとの参加者と視点を固定する。
;==============================================================
;--- COM60 助手にキスさせる ---
; 助手がましろにキスする。転校生くんは見守る側。
IF SELECTCOM == 60
\tCALL AITE_YOBI, 67, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「えっ、%LOCALS%に先を取られた!?　転校生くん、見ているなら笑うなよ……んむっ♪」
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
\t\tENDIF
\tENDIF
ENDIF

;--- COM62 ダブル素股 ---
; ましろと助手が、転校生くんを左右から挟む。三人の位置を混ぜない。
IF SELECTCOM == 62
\tCALL AITE_YOBI, 67, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「%LOCALS%と私で、転校生くんを左右から挟むのだな☆　愛の応援、二倍で行くぞっ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「んっ、%LOCALS%の動きに合わせるぞ……転校生くんの熱が真ん中で跳ね返って、私まで燃えてきた♪」
\t\tELSE
\t\t\tPRINTFORMW 「転校生くん、どちらの腰が好きか決めるなよ！　私たち二人でおまえを蕩かすのだからな☆」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「%LOCALS%と一緒に挟むのか!?　よし、足並みならチア部仕込みだ、転校生くんの熱を逃がすな！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「右へ動けば左が空く……ふむふむ、素股は隊列より難しいぞ！　でも、ちゃんと合わせてみせる☆」
\t\tELSE
\t\t\tPRINTFORMW 「おっとっとっと!?　転校生くんが真ん中で暴れるぞ！　%LOCALS%、私にぶつからないよう気をつけるのだ！」
\t\tENDIF
\tENDIF
ENDIF

;--- COM76 ダブルバイブ ---
; ましろと助手の女性二人が双頭バイブを使う。転校生くんは直接参加しない。
IF SELECTCOM == 76
\tCALL AITE_YOBI, 67, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「双頭バイブが%LOCALS%と私を同時に……っ。転校生くん、見ているなら、最後まで応援してくれ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひとつの道具で%LOCALS%とつながるのか……っ♪　私の身体、元気の出し方を間違えているのに止まらないぞ☆」
\t\tELSE
\t\t\tPRINTFORMW 「あぁっ、%LOCALS%と同じ刺激が奥まで来る……！　転校生くん、私の顔を見てくれ、まだ笑っていられるからな……っ♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ふむふむ、両側に入る道具か！　%LOCALS%、苦しくないか？　無理ならすぐ止めるぞ！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃあっ、同時に押されると声援の掛け声も出せないぞ!?　転校生くん、これは応援ではないな……！」
\t\tELSE
\t\t\tPRINTFORMW 「%LOCALS%と息を合わせるのだな……っ、よし、三つ数えるぞ！　いち、に……うわぁっ、もう無理だぁ！」
\t\tENDIF
\tENDIF
ENDIF

;--- COM78 授乳する ---
; 転校生くんが、ましろの胸から直接飲む。ましろが飲む側ではない。
IF SELECTCOM == 78
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「乳首をくわえて飲むのか……っ♪　転校生くんの口が触れると、母乳まで愛情みたいに熱くなるぞ☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ごく、ごくって音がする……私の胸をそんなに欲しがるなんて、可愛い恋人だな♪　もっと飲め！」
\t\tELSE
\t\t\tPRINTFORMW 「胸を空にするまで受け止めてやるぞ、転校生くん……っ。私の乳首、逃げないから、しっかり口をつけろ☆」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「えっ、胸から直接飲むのか!?　ふむ……乳首をくわえられると、体が勝手に反応するぞ……っ。」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ごくごく飲んでいるな……お腹は平気か？　私は平気だ、たぶん！　まだ応援できるぞ☆」
\t\tELSE
\t\t\tPRINTFORMW 「わっ、母乳が出てる!?　転校生くん、これは水分補給なのか、親睦なのか……どっちでも最後まで飲むのだな！」
\t\tENDIF
\tENDIF
ENDIF

;--- COM79 搾乳する ---
; 転校生くんが、ましろの胸を手で搾る。COM78の直接授乳と分ける。
IF SELECTCOM == 79
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「胸を手で搾るのか……っ、そこは乳首まで丁寧にだぞ？　転校生くんの手なら、任せてしまうな♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ぎゅっ、って押されるたびに母乳が……っ。私の胸をこんなに可愛がる恋人、好きだぞ☆」
\t\tELSE
\t\t\tPRINTFORMW 「飲む前に搾るのも愛情表現なのだな……転校生くん、もっと出してほしいなら、ちゃんと頼んでくれ♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「胸を手で扱うのか？　押す場所はそこではない……いや、そこだ！　ふむふむ、勉強になるな☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃっ、乳首をつまむと出るのか!?　な、なるほど、応援のようにリズムが大事なのだな……っ。」
\t\tELSE
\t\t\tPRINTFORMW 「わっ、手が母乳で濡れたぞ！　転校生くん、拭くものはあるか？　私が片づけるから気にするな！」
\t\tENDIF
\tENDIF
ENDIF

;--- COM84 Ｇスポット刺激 ---
; 転校生くんがましろのクリとおまんこを刺激する。受けているましろの声にする。
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
ENDIF

;--- COM86 強制放尿 ---
; ましろが放尿させられる。失敗を隠そうとするが、団長としての心が折れる。
IF SELECTCOM == 86
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「出てしまうところまで見ているのか、転校生くん……っ。恋人になら、団長の失敗も隠さず受け止めてほしいぞ……☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「止められない……っ、こんな情けない私でも愛してくれるか？　逃げるなよ、転校生くん……！」
\t\tELSE
\t\t\tPRINTFORMW 「うぅ、床に広がってしまう……っ。私は応援団長なのに、こんな姿を見せるのはおまえだけだからな……」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「ええっ、今ここで放尿!?　ま、待て転校生くん、これは団長命令で見ない……いや、もう出てしまうぞぉっ！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「うわぁぁん！　止められない、止められないぞ！　こんなことで負けるなんて、団長失格だぁっ！」
\t\tELSE
\t\t\tPRINTFORMW 「あっ、足元が濡れて……っ。笑うなよ、転校生くん！　私だって好きで漏らしているわけではないのだ！」
\t\tENDIF
\tENDIF
ENDIF

;--- COM202 胸同士 ---
; ましろと助手の女性二人が胸をこすり合わせる。転校生くんは直接参加しない。
IF SELECTCOM == 202
\tCALL AITE_YOBI, 67, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「%LOCALS%と胸を合わせるのか……っ♪　転校生くん、見ているだけでそんなに熱くなるのか？　私も負けないぞ☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「乳首が%LOCALS%に触れるたび、胸の奥まで弾む……っ。恋人への愛、二人分の勢いで届けるからな♪」
\t\tELSE
\t\t\tPRINTFORMW 「%LOCALS%の胸を押し返して……これは胸の親睦だぞ、転校生くん！　声援は胸の奥から出すのだ☆」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「おやっ、%LOCALS%と胸をこするのか!?　ふむふむ、チアの接触練習より近いな……っ。」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「乳首が当たると声が出るぞ!?　転校生くん、これは私たち二人の問題だから、変な声援は禁止だ！」
\t\tELSE
\t\t\tPRINTFORMW 「胸で押し合うのだな！　よし、負けない……って、%LOCALS%、そんなに強く押すと乳首が……ひゃあっ☆」
\t\tENDIF
\tENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; ましろは転校生くんに騎乗したまま、助手が転校生くんの顔に乗る。
IF SELECTCOM == 258
\tCALL AITE_YOBI, 67, ASSI
\tLOCALS '= @"%RESULTS%"
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「私は転校生くんに乗ったまま、%LOCALS%は顔の上か……っ♪　上下から愛されるなんて、私の元気が追いつかないぞ☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「腰を止められないのに、%LOCALS%まで近い……っ。転校生くん、私を見てくれ、恋人の顔でな♪」
\t\tELSE
\t\t\tPRINTFORMW 「んあっ、奥に当たるたび声が出る！　%LOCALS%に見られても、転校生くんの上から降りたくないぞ……っ♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「おっとっとっと!?　私は乗ったまま、%LOCALS%が転校生くんの顔に!?　これは隊列が近すぎるぞ！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「腰を動かしながら、下では顔を使わせるのか……っ。転校生くん、苦しくないか？　返事だけはしてくれ！」
\t\tELSE
\t\t\tPRINTFORMW 「わっ、私が騎乗位で、%LOCALS%が顔面騎乗……っ！　団長、どこを応援すればいいのだ、両方か!?」
\t\tENDIF
\tENDIF
ENDIF

;--- COM318 頭を撫でる ---
; ましろが転校生くんの頭を撫でる。撫でられる側をましろにしない。
IF SELECTCOM == 318
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「よしよし、転校生くん。今日もよく頑張ったな……私の手で、心の骨折を治してやるぞ♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「頭を撫でているだけなのに、こんなに近く感じるな。愛してるぞ、転校生くん……ぎゅうう☆」
\t\tELSE
\t\t\tPRINTFORMW 「こっちへ来い、転校生くん。私が頭を撫でて、元気をお届けするからな。泣いてもいいぞ♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「よしよし、転校生くん！　頭を撫でてやるから、ひとりで抱え込むなよ！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ふむふむ、肩が重いのか？　まずは頭からだな。心の病になる前に、私に話してくれ☆」
\t\tELSE
\t\t\tPRINTFORMW 「大丈夫、大丈夫だぞ！　私の手がここにある。落ち着いたら、またフレー！　フレー！　だ♪」
\t\tENDIF
\tENDIF
ENDIF

"""


def crlf(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\n", "\r\n")


text = PATH.read_bytes().decode("cp932")

assert text.count("IF SELECTCOM == 90") == 0, "CHAR67 COM90 already exists"
assert text.count(";--- COM110 クスコ ---") == 1, "CHAR67 COM110 anchor is not unique"
text = text.replace(
    ";--- COM110 クスコ ---",
    crlf(COM90) + ";--- COM110 クスコ ---",
    1,
)

assert text.count(";--- COM0 愛撫 ---") == 1, "CHAR67 COM0 anchor is not unique"
assert text.count("IF SELECTCOM == 60") == 0, "CHAR67 COM60 already exists"
text = text.replace(
    ";--- COM0 愛撫 ---",
    crlf(ADDITIONAL10) + ";--- COM0 愛撫 ---",
    1,
)

for command in (60, 62, 76, 78, 79, 84, 86, 90, 202, 258, 318):
    assert text.count(f"IF SELECTCOM == {command}") == 1, f"CHAR67 COM{command} was not inserted exactly once"

assert ADDITIONAL10.count("PRINTFORMW") == 60, "additional10 must contain exactly 60 lines"
PATH.write_bytes(text.encode("cp932"))
