from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_28_星海こよい_COM.ERB")
START = ";=== KOYOI MISSING COMMAND TRIAL START ==="
END = ";=== KOYOI MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_28"


BLOCK = r''';=== KOYOI MISSING COMMAND TRIAL START ===
; 追加10コマンド：こよいの恋慕／非恋慕を各3分岐

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%と、こんなふうにしてるとこ……転校生くんに見られたら、うち、何て言うたらえぇのん？　……でも、離れたない」
		ELSEIF A == 1
			PRINTFORMW 「ん……っ。唇、重ねるだけやと思てたのに、胸の奥まで転校生くんに隠しごとできへんくなるみたい……」
		ELSE
			PRINTFORMW 「つゆちゃんに仕込まれたんやなくて、うちが望んだんやから……%LOCALS%、もう一回だけ、ゆっくりして？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、%LOCALS%と口……!?　うち、ほっぺたやと思て心の準備してへんのに、転校生くんに見られたら……あかん、顔あげられへん」
		ELSEIF A == 1
			PRINTFORMW 「ちゅ、ってしただけやのに、何でこんなに心臓うるさいん……。うち、ほんま人見知りやのに、知らんふりできへんわぁ」
		ELSE
			PRINTFORMW 「もう終わりやんな？　……えっ、まだ顔を近づけるん？　あかんて、うち、逃げる場所もあらへんよ～っ」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 28, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、転校生くんの腰、うちに合わせてくれる？　……ひゃっ、先に動かれたら、うちの脚まで勝手に追いかけてまう」
		ELSEIF A == 1
			PRINTFORMW 「ふたりに挟まれた転校生くん、嬉しそうやなぁ……。うちのこともちゃんと見ててや？　見られへんと、どない動いたらえぇかわからへん」
		ELSE
			PRINTFORMW 「せーの……っ、あかん、%LOCALS%の熱と転校生くんの熱がいっぺんに来て……うち、笑ってごまかせへんよぉ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%、もうちょっとだけゆっくりにして……。転校生くんの腰まで揺れるから、うち、どこに力入れたらえぇのん？」
		ELSEIF A == 1
			PRINTFORMW 「うちの脚、そんな見んといてや……！　ふたり分の視線が集まったら、友達づくりどころやあらへん、頭真っ白やわぁ」
		ELSE
			PRINTFORMW 「うひゃっ、誰の動きやのん!?　転校生くん、急に合わせようとせんでえぇから……あっ、でも止まるのも、ちょっと怖いねん」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
	CALL AITE_YOBI, 28, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、手ぇ……握ってて。うちが震えたら、そっちまで同じように動いてまうんやね……ふふ、ひとりやないみたい」
		ELSEIF A == 1
			PRINTFORMW 「あ、あかん……速ぅなったら、声、隠せへん……。%LOCALS%が頑張ってるん、わかるから、うちも離れへんけど……っ」
		ELSE
			PRINTFORMW 「女の子と、こんな近ぅなるなんて思てへんかった……でも、%LOCALS%となら、もう少しだけ、このままがえぇねん」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ!?　%LOCALS%が動くたび、うちの中まで同じように跳ねるん……。これ、別々のはずやのに、逃げ道があらへんよぉ」
		ELSEIF A == 1
			PRINTFORMW 「ま、待ってや、いきなり強ぅしたら……あっ、また来たっ！　うちの声、聞かんかったことにしてぇ……」
		ELSE
			PRINTFORMW 「どっちが動いたんか、もうわからへん……。%LOCALS%、お願いやから手ぇ離さんといて。怖いのに、ひとりになるほうが嫌やねん」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生くん、そんなに一生懸命……。うちの身体でほっとしてくれるんやったら、今日は好きなだけ甘えてえぇよ」
		ELSEIF A == 1
			PRINTFORMW 「吸われるたび、胸の奥がくすぐったぁなって……。見られるんは恥ずかしいのに、転校生くんが嬉しそうやと、止めてって言えへんわぁ」
		ELSE
			PRINTFORMW 「おいしいかどうか、そんな顔で聞かんでもわかるやろ……。でも、ちゃんと伝えてくれへんと、うち、また不安になるねん」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、ほんまに飲むのん!?　うち、まだ心の準備が……っ。そんな顔で待たれたら、あかんって言えへんやん」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、吸うたら胸の奥まできゅうってする……。うち、見られるだけでも人見知りするのに、こんなん、どないしたらえぇのん」
		ELSE
			PRINTFORMW 「ゆっくりしてや？　むせたら大変やもん……って、うちが世話焼いてる場合ちゃうなぁ。飲まれるたび、声、変になってまう……」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生くんの手、やさしすぎて……そこまで大事そうに扱われたら、うちのほうが、もっとしてって言うてまうやん」
		ELSEIF A == 1
			PRINTFORMW 「こんなに溜まってたんや……。数字にしたら恥ずかしいから見んといて。でも、転校生くんが受け取ってくれるなら、捨てんといてな」
		ELSE
			PRINTFORMW 「あっ、そこはちょっと強ぅ……っ。痛いんとちゃう、ただ、身体の奥までわかってまうから……転校生くん、もう少しだけ、ゆっくり」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「け、計るん？　量まで見られるん!?　うち、体重と同じで、そういう数字は聞かんかったことにしてほしいわぁ……」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、手際よすぎるやん……！　牛さんやないねんから、そんなに作業みたいにせんといて。見られてるこっちが恥ずかしいやろ」
		ELSE
			PRINTFORMW 「あぅ……絞られるたび、胸の奥がきゅっとして、白いのが止まらへん……。うち、こんな顔、誰にも見せたことあらへんのに」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ひゃっ、そこ……っ！　転校生くん、指、止め……あかん、止めんといて……うち、言うてること自分でもわからへん！」
		ELSEIF A == 1
			PRINTFORMW 「また、そこ押すん……？　お腹の奥が勝手に締まって、足、力入らへん……転校生くん、顔、見んといてやぁ……！」
		ELSE
			PRINTFORMW 「好きやから、触れられるんが嬉しいはずやのに……そこばっかりは、あかん、あかんて言うても、身体が先に返事してまう……っ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ!?　そこは、まだ知らんとこやのに……！　転校生くん、いったん止まって、うちに考える時間を……あっ、考えられへん！」
		ELSEIF A == 1
			PRINTFORMW 「あ、あかん、腰が勝手に跳ねた……。うちが動かしたんちゃうからな!?　ほんまに、そっちが勝手に……もう、言い訳もでけへん」
		ELSE
			PRINTFORMW 「ひぃん……そこ、怖いのに、離れたら足りへんみたいで……。こんなん、うち、どないしたらえぇのん……声、止められへんよぉ」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「うち、転校生くんの前でだけは、ちゃんとしていたかったのに……。あかん、見んといてって言うたら、余計に見てほしいみたいになるし……どないしょ」
		ELSEIF A == 1
			PRINTFORMW 「こんなふうに身体に裏切られるん、怖いわぁ……でも、転校生くんが黙ってそばにおってくれるなら、うち、逃げんとここにおる」
		ELSE
			PRINTFORMW 「恥ずかしくて死にそうやけど……嫌いにならんといて、とは言えへん。そんなこと言うほど、うち、子どもやないもん……ただ、手ぇだけ握ってて」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ!?　ま、待って、そんな急に……！　止めるから、って言うても身体が聞いてくれへん……お父やんにばれたら、ほんまに死ぬわぁ」
		ELSEIF A == 1
			PRINTFORMW 「見んといてや……！　うち、ひとりで片づけるから……って、足に力入らへん。こないなとこで困り顔を笑わんといてな……」
		ELSE
			PRINTFORMW 「あかん、間にあわへん……。これ、我慢できへんかったんやなくて、うちの身体が勝手に……せやけど、もう逃げへんって決めたから、最後までここにおる……」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
	CALL AITE_YOBI, 28, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の胸、あったかい……。普段は人の目が怖いのに、%LOCALS%になら、もうちょっと近ぅてもえぇと思てまう」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、先っぽが触れた……！　%LOCALS%、もう一回だけ。うち、女の子同士でこんなお願いするなんて、知らんかったわぁ」
		ELSE
			PRINTFORMW 「胸の大きさ比べてるんやなくて、%LOCALS%とくっついてたいねん……。うち、ちゃんと伝えられてる？　……あかん、聞く前から恥ずかしい」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、顔こんな近いのん!?　胸を合わせるだけやと思てたのに、%LOCALS%の目まで見えて……うち、どこ見たらえぇんやろ」
		ELSEIF A == 1
			PRINTFORMW 「あぅっ、先っぽが擦れるたび、ぞくってする……。女の子同士やから平気やと思てたうちが、いちばんあかんかったわぁ」
		ELSE
			PRINTFORMW 「比べんといてな？　うち、胸のことは……。ひゃっ、急に押しつけたら、恥ずかしいって言う暇もあらへんやん」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
	CALL AITE_YOBI, 28, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%が顔を近づけるたび、転校生くんの中まで揺れるん……っ。うち、ふたりとも見なあかんのに、どっちも見られへんよぉ」
		ELSEIF A == 1
			PRINTFORMW 「転校生くん、腰、止めんといて……。%LOCALS%に見られてるのに、うち、気持ちえぇって顔を隠せへん……！」
		ELSE
			PRINTFORMW 「%LOCALS%、そんな声で煽らんといてや……っ。転校生くんに奥を突かれるたび、うちまで返事してまう。もう、ふたりの前で平気なふりなんてでけへんよぉ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ、%LOCALS%が動いたら、下の転校生くんまで揺れるやん!?　うちの身体、上下からせわしなくされて、どないしたらえぇのん！」
		ELSEIF A == 1
			PRINTFORMW 「ま、待ってや、入ったまま腰を動かしたら……あっ、脚に力入らへん！　転校生くんの上から落ちたら、ほんまに死ぬぅ……！」
		ELSE
			PRINTFORMW 「上も下も、いっぺんに来たらあかんて……！　%LOCALS%、転校生くん、どっちかだけでも止まって……あ、でも止まったら寂しいって何でやのん！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：こよいがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生くん、今日はよう頑張ったんやね。ほら、頭こっち……うちが撫でたるから、何もしゃべらんでえぇよ」
		ELSEIF A == 1
			PRINTFORMW 「髪に触れてると、屋上で星見てるときみたいに落ちつくわぁ。転校生くんが眠るまで、うち、ここにおるねん」
		ELSE
			PRINTFORMW 「いつも助けてもろてばっかりやから、今日はうちの番やで。えへへ、元気になるまで撫でるって決めたから、逃げたらあかんよ？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ん？　転校生くん、今日は静かやなぁ。……何や、撫でられると困るん？　うちも人見知りやけど、元気ないひと放っておけへんねん」
		ELSEIF A == 1
			PRINTFORMW 「よしよし……。うち、話すん苦手やから、うまい慰め方は知らへんけど、手ぇなら動かせるよってな」
		ELSE
			PRINTFORMW 「失敗したん？　そないな顔せんでも、星は一晩曇ったぐらいで消えへんよ。ほら、転校生くんも、ちょっとだけ休み？」
		ENDIF
	ENDIF
ENDIF
;=== KOYOI MISSING COMMAND TRIAL END ==='''


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
