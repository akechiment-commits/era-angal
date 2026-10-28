from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_07_高原ちあき_COM.ERB")
START = ";=== CHIAKI MISSING COMMAND TRIAL START ==="
END = ";=== CHIAKI MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_7"


BLOCK = r''';=== CHIAKI MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「この子、先輩より緊張してますよ。まずあたしが落ち着かせますから……そのあとで、先輩の難しい顔も何とかします」
		ELSEIF A == 1
			PRINTFORMW 「お兄ちゃん先輩、そうやって黙ると本当のお兄ちゃんみたいですよ。妹の交友関係を見守る顔……あたしが欲しいの、それじゃないのにな」
		ELSE
			PRINTFORMW 「ちゅっ……。嫉妬するか試したかったわけじゃないです。あたし、先輩の気持ちを試すようなやり方は嫌いですから」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「いやいやいや、本人たちより周りが先に盛り上がらないでください！　ほら、そっちも嫌なら今のうちに言ってね？」
		ELSEIF A == 1
			PRINTFORMW 「んむっ……うひゃ、ごめん！　痛くなかった？　ちょっと唇見せて。キスの続きより、まず怪我してないか確認！」
		ELSE
			PRINTFORMW 「ふたりとも真っ赤で、見てるほうまで黙っちゃって……。もう、誰かひとりくらい普通に喋ってくださいよ。あたしも無理ですけど！」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 7, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「どうして妬いてるあたしが、%LOCALS%との呼吸まで整えてあげてるんでしょうね……。先輩、あとで埋め合わせしてくださいよ？」
		ELSEIF A == 1
			PRINTFORMW 「先輩、どっちにも遠慮して中途半端に動くのやめてください。優しさのつもりでも、あたしたち二人とも調子が狂うんですから」
		ELSE
			PRINTFORMW 「%LOCALS%の脚が震えてる……支えるから寄りかかって。んっ、先輩はそのまま……あたしまで擦れるから、少しだけゆっくり……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「三人とも相手に合わせようとして、誰も動けてないじゃないですか！　もう、あたしが数えるから二人ともちゃんと聞いて！」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、先輩だけ先走らないでください！　%LOCALS%まで驚いてるでしょ。まず全員の顔を見てから動く！」
		ELSE
			PRINTFORMW 「%LOCALS%、無理ならすぐ言ってね。先輩も気持ちよさより安全優先！　……なんでこんな格好であたしが進行役なんですかぁ！」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：ちあきと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 7, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、目、そらさないで……っ。そっちが動くたび、あたしの奥まで、んあぁっ……一緒に感じてる顔、見せて……！」
		ELSEIF A == 1
			PRINTFORMW 「ひぃっ、待って、今の深い……！　あたしが止まったら、%LOCALS%も止めて……だめ、勝手に腰、動くぅ……！」
		ELSE
			PRINTFORMW 「手、握って……っ。平気って言いたいのに、なか、きゅって……あぁっ！　%LOCALS%、離れないで……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃぁっ!?　%LOCALS%、急に動かしたでしょ！　こっちの奥まで響くんだから、合図してよぉ……！」
		ELSEIF A == 1
			PRINTFORMW 「大丈夫です大丈夫ですダイジョウブ……ひぃいっ、全然だいじょばない！　%LOCALS%、ちょっと休憩っ！」
		ELSE
			PRINTFORMW 「あたしが合わせるから、%LOCALS%は無理しないで……んあっ、や、気遣ってる場合じゃ、奥、当たってるぅ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そんなに夢中で飲まれると、胸だけじゃなくて心臓まで吸われそうです……。お兄ちゃん先輩、あたしの顔も見てください」
		ELSEIF A == 1
			PRINTFORMW 「んっ、そこ強く吸うと出ちゃう……！　ふふ、先輩を甘やかすの、嫌いじゃないですけど……今の顔は誰にも見せませんからね」
		ELSE
			PRINTFORMW 「お腹いっぱいになるまでどうぞ。妹みたいだからじゃなくて……好きな人に、あたしのものを飲んでほしいんです」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ、直接飲むんですか!?　水分補給ならもっと普通の方法が……ひゃぅ、もう吸ってるし！」
		ELSEIF A == 1
			PRINTFORMW 「こぼさないように、ちゃんと口をつけてくださいね。……って、なんであたしがこんなに世話慣れた感じ出してるんだろ」
		ELSE
			PRINTFORMW 「んっ……おいしいですか？　先輩がほっとした顔してると、恥ずかしいのに止めづらいじゃないですか」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「手つき、ずいぶん上手くなりましたね……。ちょっと複雑ですけど、お兄ちゃん先輩になら任せます」
		ELSEIF A == 1
			PRINTFORMW 「あっ、そこ押されると、ぴゅって……！　もう、面白がってません？　先輩の顔、完全にいたずらっ子ですよ」
		ELSE
			PRINTFORMW 「溜まって苦しかったの、気づいてくれたんですね。こういう時だけは……お兄ちゃん先輩って呼んでてよかったな」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「いやいや、牛じゃないんですから！　そんな真剣な顔で搾られると、あたしの立場がないですよぉ！」
		ELSEIF A == 1
			PRINTFORMW 「んっ、指で根元から押すと……あ、出た。先輩、顔を近づけすぎると飛びますよ？」
		ELSE
			PRINTFORMW 「痛くはないです。でも、じっと見られるほうが恥ずかしいかも……手元だけ見ててください、手元だけ！」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこ覚えてたなんて、ほんと世話焼かせるの上手……ひゃぁっ！　だめ、今はあたしが何もしてあげられな……！」
		ELSEIF A == 1
			PRINTFORMW 「お兄ちゃん……っ！　あ、先輩って、つけなきゃ……ひぃっ、無理、今だけちゃんと呼べないぃ……！」
		ELSE
			PRINTFORMW 「先輩に余裕ない顔を見せるの、悔しいのに……っ。んあぁ、そこ、もう格好つけられないからぁ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「いやいやいや、指でそこを押すのは聞いてませんって……うひゃぁっ！　説明してる途中にもう一回は駄目ぇ！」
		ELSEIF A == 1
			PRINTFORMW 「大丈夫です、これくらい……ひぅっ！　はい嘘です、全然大丈夫じゃない！　あたしのこと支えてくださいっ！」
		ELSE
			PRINTFORMW 「身体ってこんな正直なんだ……っ。口では文句言ってるのに、なかは先輩の指、待って……ひゃぁっ！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「『大丈夫』って、あたしが言うときは誰かを安心させたいときなんです……。今度は先輩が、あたしに言ってください」
		ELSEIF A == 1
			PRINTFORMW 「妹みたいな子の失敗で済ませないでくださいね。こんなときでも、あたしは先輩に女の子として見てほしいんです……変ですけど」
		ELSE
			PRINTFORMW 「あとで慰めるなら、頭を撫でるのは禁止です。妹扱いじゃなくて……ちゃんと恋人みたいに、キスしてください」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ちょっと、これは悪ふざけで済ませる線を越えてます！　あたしが止めてって言ったら、そこはちゃんと聞いてください！」
		ELSEIF A == 1
			PRINTFORMW 「自分の限界くらいわかってるつもりだったのに……他人の心配ばっかりして、自分の身体は後回しにしてた罰かなぁ」
		ELSE
			PRINTFORMW 「こういうときまであたしが場をまとめるんですか!?　お兄ちゃん先輩、せめて何か気の利いたこと……やっぱ今は黙っててください！」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：ちあきと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 7, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、もっと近く……。胸の大きさなんて関係ないよ、ここが触れると……んっ、ちゃんと気持ちいいから」
		ELSEIF A == 1
			PRINTFORMW 「あっ、今お互い同じところで震えた……。ふふ、顔までこんな近いと、隠し事できないね」
		ELSE
			PRINTFORMW 「%LOCALS%の音、胸から直接伝わってくる……。もう少しだけ、このままくっついててもいい？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「いやいや、胸を合わせるって聞いたけど、こんなぴったり!?　%LOCALS%、顔まで赤いよ……あたしもだけど！」
		ELSEIF A == 1
			PRINTFORMW 「んっ、乳首同士が引っかかって……うひゃ、今のなし！　%LOCALS%、笑ったら怒るからね！」
		ELSE
			PRINTFORMW 「%LOCALS%、痛くない？　じゃあ、もう少しだけ擦ってみよっか。あたしが速すぎたらすぐ言ってね」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：ちあきはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 7, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「妹分じゃ、こんなふうに先輩の上では動きませんよ……っ。%LOCALS%で顔が見えなくても、あたしを女の子として感じて……んあっ！」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%のことも支えて、先輩の腰にも合わせて……ひゃぁっ、二人ぶんの面倒なんて、今は見きれないですぅ！」
		ELSE
			PRINTFORMW 「お兄ちゃん先輩、声が出せないなら手を……あっ、届かない！　じゃあ腰で……ひゃぁっ、それは強すぎますってぇ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%、先輩の呼吸はちゃんと見てて！　あたしは下のほうを……ひぃっ、こっちはあたしが見られてる側でしたぁ！」
		ELSEIF A == 1
			PRINTFORMW 「一人ずつならちゃんと気を配れるのに、二人同時は無理です！　先輩まで下から自己主張しないで、んあぁっ！」
		ELSE
			PRINTFORMW 「あたしが転びそうになったら%LOCALS%は先に降りてね……って、先輩、そこで深くしたら指示が飛びますぅ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：ちあきがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「よしよし、大丈夫だよ……って、先輩には子供扱いですかね。でも今日は、あたしに甘やかされてください」
		ELSEIF A == 1
			PRINTFORMW 「お兄ちゃん先輩って呼んでますけど、本当のお兄ちゃんにこんなふうにはしませんよ。……意味、わかってくださいね？」
		ELSE
			PRINTFORMW 「先輩が頑張ってるの、あたしはちゃんと知ってます。だから今は何も説明しなくていいですよ……よしよし」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「お疲れさまです、お兄ちゃん先輩。ほら、ここ座って。元気が戻るまで、あたしがよしよししてあげます」
		ELSEIF A == 1
			PRINTFORMW 「いつも誰かの頭を撫でる役ですから、けっこう上手いんですよ？　眠くなったら、そのまま寝てもいいですからね」
		ELSE
			PRINTFORMW 「無理に笑わなくて大丈夫です。そばにいるくらいなら、あたしにもできますから……よしよし、大丈夫だよ」
		ENDIF
	ENDIF
ENDIF
;=== CHIAKI MISSING COMMAND TRIAL END ==='''


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
