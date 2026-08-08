from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_06_藍乃あいか_COM.ERB")
START = ";=== AIKA MISSING COMMAND TRIAL START ==="
END = ";=== AIKA MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_6"


BLOCK = r''';=== AIKA MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「相手の子のほうが震えてる……。安心させなきゃって思ったら、先輩に見られてることまで忘れられました。少しだけですけど」
		ELSEIF A == 1
			PRINTFORMW 「ん、ちゅ……。キスしてる間は何も言えないんですね。先輩に聞きたいことばかり浮かぶのに、唇が塞がってる……」
		ELSE
			PRINTFORMW 「嫉妬を試して恋が深まる、なんて本にはありますけど……わたしは試したくないです。先輩の気持ち、本物だから怖いんです」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぁっ、わたしが相手でいいんですか？　あの、嫌という意味じゃなくて……まず、そっちも困ってないか知りたくて」
		ELSEIF A == 1
			PRINTFORMW 「んむ……ひゃっ。いま謝りそうになったけど、キスされて謝るのも変ですよね。……もう一度なら、今度は黙ってできます」
		ELSE
			PRINTFORMW 「ふたりとも目を閉じるタイミングを逃しちゃった……。ふふ、変な顔。笑えたから、さっきより怖くないです」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 6, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%とふたりで先輩を……。こんな場面、小説にも書いたことないです。ひゃっ、急に腰を動かさないでください！」
		ELSEIF A == 1
			PRINTFORMW 「先輩のが脚の間を通るたび、%LOCALS%の肌まで擦れて……。わたし、どこを見ればいいんですか……？」
		ELSE
			PRINTFORMW 「もう息が上がっちゃいました……。でも先輩が気持ちよさそうだから、あと少しだけ……%LOCALS%、支えてくれる？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「わ、わたし運動は苦手なのに、三人で息を合わせるなんて無理です……！　%LOCALS%、置いていかないでね？」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、先輩が動くと脚に当たって……。ごめんなさい、止まっちゃった。わたしのせいで調子が狂いましたよね」
		ELSE
			PRINTFORMW 「%LOCALS%、もう少しゆっくり……。わたし、脚が震えて先輩を挟んでるのか、寄りかかってるのかわからないよぉ……」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
	CALL AITE_YOBI, 6, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%が動くたび、わたしのなかまで……ひゃぁっ！　同じものを感じてるって思うと、怖いのに離したくない……っ」
		ELSEIF A == 1
			PRINTFORMW 「待って、速い……っ！　あっ、でも止まったら寂しいなんて、わがままですよね……ひゃぅっ！」
		ELSE
			PRINTFORMW 「%LOCALS%、手を……。わたし、もう息が続かなくて……なか、また締まっ、あぁっ……一緒にいて……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うぴいっ!?　%LOCALS%が動いたのに、どうしてわたしの奥まで……！　やだ、次が来るの怖いっ！」
		ELSEIF A == 1
			PRINTFORMW 「ゆっくり、お願い……っ。わたし体力ないから、もう震えが止まらなくて……あっ、動かさないでぇ！」
		ELSE
			PRINTFORMW 「ごめんね%LOCALS%、わたしが力を抜けないせいで、そっちまで苦しいよね……。でも、怖くて緩められないの……！」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「こんな小さな胸でも、先輩を満たせるんですね……。えへへ。わたしにも、あげられるものがあってよかった♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ、吸われるたびに胸の奥が引っぱられて……。先輩、そんなに夢中だと、わたしまで離れたくなくなります」
		ELSE
			PRINTFORMW 「物語なら、きっと穏やかで綺麗な場面なのに……現実は息づかいまで聞こえて、こんなに恥ずかしいんですね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ほ、本当に飲むんですか？　わたしのなんて、おいしくないかもしれないのに……あとで後悔しても知りませんからね？」
		ELSEIF A == 1
			PRINTFORMW 「ふぁっ、そこを吸われると、身体の力まで抜けちゃう……。すみません、少し肩を貸してもらっていいですか？」
		ELSE
			PRINTFORMW 「むせてないですか？　無理しなくていいですよ。残されたら寂しいけど……先輩が苦しくなるほうが嫌ですから」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩の手、優しいですね……。搾られてるのに、頭を撫でられたときみたいに安心するの、何だか変です」
		ELSEIF A == 1
			PRINTFORMW 「あっ、また出た……。そんな大事そうに集めてもらうと、わたしまで自分の身体を嫌わずにすみそうです」
		ELSE
			PRINTFORMW 「もう出ないと思います……。それでも先輩が触っていたいなら、わたしは……もう少しだけ、このままでいいです」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひゃっ、そんなに見つめないでください……！　小さい胸からどれだけ出るか、数えられてるみたいで落ち着かないです」
		ELSEIF A == 1
			PRINTFORMW 「痛っ……ご、ごめんなさい、大声出して。わたし痛いのに弱いから、もう少しだけ優しくしてもらえますか？」
		ELSE
			PRINTFORMW 「容器、いっぱいになってきましたね……。わたしが持つと落としそうなので、最後まで先輩が持っていてください」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「こんなの、言葉にして覚えておけない……っ。先輩、わたしが忘れても、どこが好きだったか……覚えててぇ……！」
		ELSEIF A == 1
			PRINTFORMW 「せんぱい、せんぱい……っ。名前しか出てこない……ひゃぁっ、でも呼んだら返事して、置いてかないでぇ……！」
		ELSE
			PRINTFORMW 「やめてって言ってるのに、止まったら寂しいって思ってる……っ。こんなわがまま、わたしにもわからないよぉ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うぴいっ!?　い、今ので息のしかた忘れました……！　先輩、次に触る前に、ちゃんと呼吸させて……っ！」
		ELSEIF A == 1
			PRINTFORMW 「痛いのと気持ちいいの、区別できない……っ。わたし痛いの苦手なのに、身体は先輩の指を追いかけてる……！」
		ELSE
			PRINTFORMW 「ごめんなさ……ひゃぁっ！　謝るのも最後まで言えない……先輩、わたし、もう何もちゃんとできな……っ！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「小説なら、こういう時間は一行あけて飛ばすんです……。でも現実のわたしは、その空白のなかにもずっといるんですね」
		ELSEIF A == 1
			PRINTFORMW 「頭のなかで、先輩に嫌われる結末ばかり浮かびます……。お願い、その先を先輩の言葉で書きかえてください」
		ELSE
			PRINTFORMW 「身体にまで置いていかれるなんて思わなかった……。先輩、わたしの声だけは置いていかないで。ちゃんと聞いていてください……っ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「恋愛小説がこういうことを書かない理由、やっとわかりました……。綺麗じゃないからじゃなくて、本人には長すぎるからです……っ」
		ELSEIF A == 1
			PRINTFORMW 「謝っても止まらないし、我慢しても止まらない……わたし、こういうとき何を言えばいいのか、本当に知らないです……！」
		ELSE
			PRINTFORMW 「ひとりなら毛布をかぶって、なかったことにできたのに……。先輩がいると恥ずかしい。でも、ひとりよりは怖くないです」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
	CALL AITE_YOBI, 6, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の胸、あったかい……。わたしのは小さくて合わせづらいのに、離さないでいてくれるんだね」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、先っぽ同士が擦れると、そこだけぞくって……。%LOCALS%も同じ顔してる。えへへ、少し安心した♪」
		ELSE
			PRINTFORMW 「こんなに近いと、胸より顔のほうが気になります……。%LOCALS%、目を逸らさないで。わたしも頑張るから」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「わ、わたしの胸、小さいから合わせにくいですよね……。ごめんね%LOCALS%、無理に押しつけなくていいから」
		ELSEIF A == 1
			PRINTFORMW 「ふぁっ、いま擦れた……！　女の子同士なのに、こんな声が出るんだ。%LOCALS%も、びっくりした？」
		ELSE
			PRINTFORMW 「%LOCALS%、痛くない？　わたし、力加減がよくわからなくて……嫌だったら、ちゃんと言ってね？」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
	CALL AITE_YOBI, 6, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩の顔が見えないのに、なかにはずっといる……っ。変です、こんなに繋がってるのに、ひとりみたいで怖い……！」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%に触る手はあるのに、わたしを支える手がない……っ。先輩、せめて腰で、ここにいるって教えて……ひゃぁっ！」
		ELSE
			PRINTFORMW 「物語のヒロインなら綺麗に腰を揺らすのに……わたし、先輩にしがみつくことしか、あぁっ、できない……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「わひっ、%LOCALS%、急に動かないで……！　わたしのなかの先輩までずれて、どこにも力を逃がせないの……！」
		ELSEIF A == 1
			PRINTFORMW 「もう脚が保たないです……。落ちたら先輩を痛くしそうで、それが怖い……%LOCALS%、肩だけ貸して……！」
		ELSE
			PRINTFORMW 「ふたりの息づかいが別々に聞こえて、頭が追いつかない……っ。わたし、どっちにも迷惑かけないなんて無理ですぅ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：あいかがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「いつもは子供あつかいしないでって怒るのに、今日はわたしが撫でる側ですね。えへへ……先輩、良い子です♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩が無理してるの、ちゃんと気づきたいんです。手遅れになってから後悔するのは……もう、嫌ですから」
		ELSE
			PRINTFORMW 「何も話さなくていいです。わたしも、黙ったままそばにいてもらって救われたことがありますから……」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あの……頭、撫でてもいいですか？　いつも助けてもらってるから、わたしにも少しくらいお返しさせてください」
		ELSEIF A == 1
			PRINTFORMW 「よしよし……。ふふ、先輩が静かにしてると、本を読んでる猫みたいです。今のは誰にも言わないでくださいね？」
		ELSE
			PRINTFORMW 「元気が出るまで、ここにいます。迷惑じゃなければ……ひとりにされる寂しさは、わたしも知ってますから」
		ENDIF
	ENDIF
ENDIF
;=== AIKA MISSING COMMAND TRIAL END ==='''


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
