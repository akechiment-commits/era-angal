from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_15_長町やえ_COM.ERB")
START = ";=== YAE MISSING COMMAND TRIAL START ==="
END = ";=== YAE MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_15"


BLOCK = r''';=== YAE MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ、ちゅ～っ♪　あはは、キスするとふたりとも元気になるねっ！　おに～さんにもあとで分けてあげるっ☆」
		ELSEIF A == 1
			PRINTFORMW 「あたしからいくよっ……ちゅ♪　ふふん、ちゃんとできたっ！　おに～さん、見直したでしょっ？」
		ELSE
			PRINTFORMW 「唇やわらかくて、ちょっと離れがたいねっ……♪　でも次はおに～さんの番だから、ちゃんと待っててっ☆」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あたしからっ？　いいよいいよっ、何ごとも全力で挑戦だ～っ！　んっ、ちゅ♪」
		ELSEIF A == 1
			PRINTFORMW 「わっ、歯が当たっちゃった！　あははっ、失敗したらもう一回できるからお得だねっ☆」
		ELSE
			PRINTFORMW 「ふたりともどきどきしてるなら条件は同じっ！　せぇので目ぇ閉じよっ、せぇの～♪」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 15, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、左右からぴったり挟むよっ♪　おに～さんの熱、あたしたちの腿にどんどん伝わってくるねっ」
		ELSEIF A == 1
			PRINTFORMW 「おに～さん、今ので腰が跳ねたっ！　%LOCALS%、弱点発見だよっ、もう一往復～っ☆」
		ELSE
			PRINTFORMW 「ふたりがかりで嬉しそうだねっ、おに～さん♪　どっちも選ばなくていいから、まとめて感じてっ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%、あたしがテンポ取るねっ！　いち、にっ、いち、にっ……わぁ、綺麗に動いたっ♪」
		ELSEIF A == 1
			PRINTFORMW 「あたしの脚だけじゃ足りなくても、%LOCALS%と一緒なら隙間なしっ！　チームワークの勝利だねっ☆」
		ELSE
			PRINTFORMW 「おに～さんの顔、どんどん緩んでるよっ？　あははっ、効いてるならもっと正直に声出してっ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：やえと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 15, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ、%LOCALS%が動くたび、あたしの奥にも届くよっ……♪　身体のなかで合図しあってるみたいっ」
		ELSEIF A == 1
			PRINTFORMW 「わひゃっ、急に大きく動いたねっ！　じゃあ今度はあたしから、%LOCALS%にお返し～っ☆」
		ELSE
			PRINTFORMW 「%LOCALS%、顔見せてっ。どっちが先に声を我慢できなくなるか、勝負しよっ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにゅっ、片方を引いたらこっちまでっ!?　%LOCALS%、これ、ふたりで探検する道具だねっ☆」
		ELSEIF A == 1
			PRINTFORMW 「次はあたしがゆっくり動かすよっ。んっ……%LOCALS%の反応、振動ですぐわかるねっ♪」
		ELSE
			PRINTFORMW 「あははっ、同時に腰が逃げちゃったっ！　今度は手ぇ繋いで、最後まで踏ん張ろうねっ☆」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「おに～さん、あたしが抱っこしてあげるっ♪　いつも助けてもらってるぶん、今日は好きなだけ甘えてねっ」
		ELSEIF A == 1
			PRINTFORMW 「んっ、吸われると胸の奥まできゅうってするっ……。おに～さんを満たせるの、すっごい幸せだよっ♪」
		ELSE
			PRINTFORMW 「まだまだ出るから慌てなくていいよっ。あたしのぶん、元気百倍になるまで飲んでっ☆」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ほぇ、本当にここから飲むのっ？　よぉし、あたしがちゃんと支えるから、思いきってどうぞっ！」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、舌で押すの上手っ！　おに～さん、あたしより先に攻略しちゃったねっ？」
		ELSE
			PRINTFORMW 「こぼれてるこぼれてるっ！　もっとぴったりくっつけば大丈夫っ、ほらこっち～♪」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「一回出るたび、おに～さんの顔が嬉しそうになるっ♪　じゃあもっと喜ばせるから、どんどんいこうっ！」
		ELSEIF A == 1
			PRINTFORMW 「こんなちっちゃな胸でも、おに～さんに渡せるものがあるんだねっ。えへへ、ちょっと誇らしいっ♪」
		ELSE
			PRINTFORMW 「搾られるの、くすぐったいより気持ちいいっ……。おに～さんの手が離れたら、たぶん寂しくなるねっ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「一押しごとに、ぴゅっ、ぴゅっ♪　ピッチングみたいに同じリズムでいくと調子いいねっ！」
		ELSEIF A == 1
			PRINTFORMW 「今の、ここからあそこまで飛んだよっ！　目印つけといて、次に抜けるか挑戦しよっ☆」
		ELSE
			PRINTFORMW 「あたしの手ちっちゃいから、おに～さんの指の間からお手伝いするっ♪　二人羽織みたいだねっ」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこっ、おに～さん……！　あたし、すぐいっちゃう、もっとぉ……！」
		ELSEIF A == 1
			PRINTFORMW 「んぁっ、奥が跳ねるっ……！　おに～さんの指、止めないでぇ……！」
		ELSE
			PRINTFORMW 「ひゃぁっ、またそこぉっ！　だめ、声も腰も止まらないよぉ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「わひゃあっ!?　なに今のっ、身体じゅうに響いたよっ！」
		ELSEIF A == 1
			PRINTFORMW 「待って待って、そこ連打は反則っ……んぁっ！　脚、力入らないっ！」
		ELSE
			PRINTFORMW 「うにゅぅっ、あたしが先に降参しそうっ……！　でも、もう一回そこぉっ！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あぁ～、止まらないっ……！　おに～さんの前じゃ、身体までまっすぐ正直だねっ♪」
		ELSEIF A == 1
			PRINTFORMW 「おに～さんが受け止めてくれるなら、あたし最後まで力抜くよっ。ちゃんと見守っててねっ」
		ELSE
			PRINTFORMW 「全部出たら、すっごい身軽になったっ☆　今ならどこまでだって走れそうだよっ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うわぁ、本当に出た出たっ！　こうなったら勢いよく、最後までいっちゃえ～っ☆」
		ELSEIF A == 1
			PRINTFORMW 「あははっ、おに～さんまでびっくりしてるっ！　その顔見たら恥ずかしさ吹き飛んじゃったっ♪」
		ELSE
			PRINTFORMW 「これだけ出るなら水分補給は大成功っ！　身体の調子は絶好調だねっ☆」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：やえと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 15, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の先っぽ、あたしのと擦れて熱いっ……♪　もっと胸ごとぎゅ～ってしてっ」
		ELSEIF A == 1
			PRINTFORMW 「同時に声出ちゃったねっ、%LOCALS%♪　ふたりの弱いところ、お揃いみたいっ」
		ELSE
			PRINTFORMW 「まだ離れたくないなっ。%LOCALS%の鼓動、胸をくっつけてもう少し聞かせてっ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「わひゃっ、先っぽ同士は刺激が強いっ！　%LOCALS%、次はゆっくりねっ？」
		ELSEIF A == 1
			PRINTFORMW 「胸の大きさじゃなくて、くっつきかたが大事っ！　%LOCALS%、ぴったり合わせてみよっ☆」
		ELSE
			PRINTFORMW 「あははっ、ふたりとも真っ赤っかだねっ♪　こうなったら笑って続けちゃおっ！」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：やえはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 15, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、おに～さんの顔は任せたっ……！　あたしはここで、んぁっ、奥まで突かれてるぅ！」
		ELSEIF A == 1
			PRINTFORMW 「おに～さんの顔は見えないけど、なかでびくびくしてるの全部わかるっ……ひゃぁっ！」
		ELSE
			PRINTFORMW 「おに～さん、%LOCALS%ばっかり構わないでっ……んっ！　あたしの奥でももっと動いてぇ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%が動くたび、おに～さんの腰まで揺れて……ふぁっ、奥に当たるっ！」
		ELSEIF A == 1
			PRINTFORMW 「あたしが上で全力っ……わひゃぁっ！　おに～さん、下から突きあげるのは聞いてないよぉ！」
		ELSE
			PRINTFORMW 「上下同時でもまだ硬いっ……んぁっ、あたしのなか、ずっと深く擦られてるぅ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：やえがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「いつもみんなを助けてるおに～さんに、今日はあたしがご褒美っ♪　眠るまで撫でてあげるねっ」
		ELSEIF A == 1
			PRINTFORMW 「おに～さんの髪、撫でてるとあたしまで元気になるっ。大好きなひとがここにいるってわかるからっ♪」
		ELSE
			PRINTFORMW 「あたしのお膝はおに～さん専用っ☆　今日は何にも頑張らなくていいから、いっぱい甘えてねっ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おに～さん、ちょっと休憩っ！　頭こっちに置いて、あたしが元気を注入してあげるっ♪」
		ELSEIF A == 1
			PRINTFORMW 「よしよしっ、撫でると目ぇ細くなるんだねっ。あははっ、大きな動物みたいでかわいいっ☆」
		ELSE
			PRINTFORMW 「あたしの手ちっちゃいけど、頭ぜんぶ撫でるまで何往復でもするよっ♪」
		ENDIF
	ENDIF
ENDIF
;=== YAE MISSING COMMAND TRIAL END ==='''


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    block = BLOCK.replace("\n", "\r\n")
    if START in text:
        start = text.index(START)
        end = text.index(END, start) + len(END)
        text = text[:start] + block + text[end:]
    else:
        if ANCHOR not in text:
            raise RuntimeError(f"insertion anchor not found: {TARGET}")
        text = text.replace(ANCHOR, block + "\r\n\r\n" + ANCHOR, 1)
    TARGET.write_bytes(text.encode("cp932"))


if __name__ == "__main__":
    main()
