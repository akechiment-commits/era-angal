from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_29_春風なな_COM.ERB")
START = ";=== NANA MISSING COMMAND TRIAL START ==="
END = ";=== NANA MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_29"


BLOCK = r''';=== NANA MISSING COMMAND TRIAL START ===
; 追加10コマンド：ななの応援気質／初心の反応を各3分岐

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	CALL AITE_YOBI, 29, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%さんと、こんなふうに唇を重ねるんですかーっ!?　うわぁ、転校生くんに見られたら応援どころじゃないですよーっ……でも、もう一回だけっ♪」
		ELSEIF A == 1
			PRINTFORMW 「ちゅっ……。ほっぺたにするつもりだったのに、あたし、勢いがついちゃいましたーっ☆　%LOCALS%さん、びっくりしました？」
		ELSE
			PRINTFORMW 「あたし、逃げないでファイトしますーっ……！　%LOCALS%さん、今度はゆっくりですよーっ。あ、あんまり見つめないでくださいっ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、%LOCALS%さんと口づけですかーっ!?　う、うわぁ、心の準備が全然できてませんよーっ……転校生くんに見られたら、顔が真っ赤ですーっ！」
		ELSEIF A == 1
			PRINTFORMW 「ちゅ、ってしただけなのに、心臓がチアの太鼓みたいですーっ……。あたし、次に何をしたらいいんでしょうかーっ!?」
		ELSE
			PRINTFORMW 「ま、まだ近づくんですかーっ!?　あたし、逃げませんけど、逃げませんけど……足が言うことを聞かないですよーっ！」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 29, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%さん、せーのっ、ですよーっ……！　転校生くんの熱が一緒に来ると、あたしの脚まで応援みたいに動いちゃいますーっ♪」
		ELSEIF A == 1
			PRINTFORMW 「ふたりで挟むなんて、息を合わせる競技みたいですねーっ☆　転校生くん、あたしのほうもちゃんと見て、ファイトって言ってくださいっ♪」
		ELSE
			PRINTFORMW 「あっ、速いですーっ！　%LOCALS%さんの熱と転校生くんの熱、どっちも応援したくなって……あたし、笑ってごまかせませんよーっ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%さん、もう少しゆっくりですよーっ……！　転校生くんまで揺れちゃって、あたし、脚の置き場所がわからないですーっ!?」
		ELSEIF A == 1
			PRINTFORMW 「うわぁ、あたしの脚、見ないでくださいーっ！　ふたり分の視線が集まったら、応援の掛け声も出てこないですよーっ……！」
		ELSE
			PRINTFORMW 「うひゃっ、誰の動きに合わせたらいいんですかーっ!?　止まるのも怖いですけど、急に来るのも心臓に悪いですよーっ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
	CALL AITE_YOBI, 29, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%さん、手をつないでてくださいねーっ。ふたりで同じように震えると、ひとりで応援してるんじゃないみたいで安心しますーっ♪」
		ELSEIF A == 1
			PRINTFORMW 「ひゃあっ、速度が上がりましたーっ!?　声が出ちゃっても、%LOCALS%さんのせいじゃないですよーっ……あたし、ファイトで受け止めますからっ！」
		ELSE
			PRINTFORMW 「女の子と、こんなに近くで一緒に頑張るなんて思いませんでしたーっ……。%LOCALS%さんとなら、もう少しだけ続けてもいいですかーっ？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ!?　%LOCALS%さんが動くたび、あたしの中まで同じように跳ねますーっ……逃げ道がないですよーっ！」
		ELSEIF A == 1
			PRINTFORMW 「ま、待ってください、急に強くしたら……あっ、また来ましたーっ!?　いまの声は応援の掛け声じゃないですからねーっ！」
		ELSE
			PRINTFORMW 「どっちが動いたのか、もうわからないですよーっ……。%LOCALS%さん、手は離さないでください。怖いですけど、ひとりになるほうが嫌ですーっ……」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生くん、そんなに一生懸命なんですかーっ……。あたしで元気になってくれるなら、今日はいっぱい甘えていいですよーっ♪」
		ELSEIF A == 1
			PRINTFORMW 「吸われるたび、胸の奥がくすぐったくなりますーっ……。恥ずかしいのに、転校生くんが嬉しそうだと、ストップって言えなくなっちゃいますねーっ☆」
		ELSE
			PRINTFORMW 「おいしいかどうか、そんな顔で聞かなくてもわかりますよーっ？　でも、ちゃんと教えてくれないと、あたし、応援の仕方を迷っちゃいますっ……」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、ほんとに飲むんですかーっ!?　あたし、まだ心の準備が……っ。そんなに待たれたら、ダメって言えないですよーっ……！」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、吸われると胸の奥まできゅーってしますーっ……。見られるだけでも恥ずかしいのに、こんなの、どんな顔をすればいいんですかーっ!?」
		ELSE
			PRINTFORMW 「ゆっくりですよーっ、むせたら大変ですからねっ……って、あたしが世話を焼いてる場合じゃないですよーっ！　声、変になっちゃいますーっ……」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生くんの手、やさしいですねーっ……。そんなに大事そうにしてくれたら、あたしのほうから、もっとファイトってお願いしちゃいますよーっ♪」
		ELSEIF A == 1
			PRINTFORMW 「こんなに出るんですねーっ……。恥ずかしいですけど、転校生くんが受け取ってくれるなら、あたし、ちゃんと最後まで応援しますーっ☆」
		ELSE
			PRINTFORMW 「あっ、そこは少し強いですよーっ……！　痛いんじゃなくて、身体の奥までわかっちゃうんですっ。もう少しゆっくり、お願いしますーっ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、量まで見るんですかーっ!?　うわぁ、数字にされると恥ずかしいですよーっ……体重の話と同じで、聞かなかったことにしてくださいっ！」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、手際がよすぎますーっ！　作業みたいにしないでくださいよーっ、見られてるあたしのほうが、どきどきしちゃいますっ……！」
		ELSE
			PRINTFORMW 「あぅ……絞られるたび、胸の奥がきゅっとしますーっ……。こんな顔、誰にも見せたことないのに、あたし、ファイトって言える状態じゃないですよーっ……」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ひゃっ、そこですーっ……！　転校生くん、止め……あ、あれっ、止めないでくださいっ！　あたし、言ってることがバラバラですよーっ!?」
		ELSEIF A == 1
			PRINTFORMW 「またそこを押すんですかーっ!?　お腹の奥が勝手にきゅっとして、脚に力が入りませんっ……でも、転校生くんの応援、聞こえてますーっ☆」
		ELSE
			PRINTFORMW 「好きなひとに触ってもらえるのは嬉しいはずなのに、そこだけは、あかんって言いたくなりますーっ……身体が先に返事しちゃいますよーっ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ!?　そこ、まだ知らない場所ですよーっ！　いったん止まって、あたしに考える時間を……って、考えられないですーっ!?」
		ELSEIF A == 1
			PRINTFORMW 「あ、あたしの腰、勝手に跳ねましたーっ!?　動かしたのはあたしじゃないですからねっ……もう、言い訳もできないですよーっ……！」
		ELSE
			PRINTFORMW 「ひぃん……怖いのに、離れたら足りないみたいで、変な感じですーっ……。あたし、どんな顔でファイトって言えばいいんですかーっ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生くんの前では、ちゃんとしていたかったんですよーっ……。見ないでって言うと、余計に見てほしいみたいになるから、もう、どうしましょうーっ!?」
		ELSEIF A == 1
			PRINTFORMW 「身体がいうことを聞かないの、怖いですーっ……。でも、転校生くんが黙ってそばにいてくれるなら、あたし、逃げずに最後まで頑張りますっ……」
		ELSE
			PRINTFORMW 「恥ずかしくて泣きそうですけど、嫌いにならないでくださいなんて言えませんーっ……！　ただ、手だけは握っててくださいねーっ……」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ!?　ま、待ってください、急すぎますーっ！　止めるって言っても身体が聞いてくれないですーっ……団長にばれたら、応援どころじゃないですよーっ!?」
		ELSEIF A == 1
			PRINTFORMW 「見ないでくださいーっ！　あたしが片づけますから、笑わないでくださいねっ……足に力が入らなくて、いま動けないんですーっ……！」
		ELSE
			PRINTFORMW 「あ、間に合わないですーっ……！　我慢できなかったんじゃなくて、身体が勝手に……でも、あたし、ここから逃げませんからーっ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
	CALL AITE_YOBI, 29, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%さんの胸、あったかいですねーっ……。あたし、いつも元気にしてるつもりなのに、こんなふうにくっつくと、ふにゃってしちゃいますーっ♪」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、先っぽが触れましたーっ……！　%LOCALS%さん、もう一回だけですよーっ？　あたしからお願いするなんて、応援部失格かもしれませんっ……」
		ELSE
			PRINTFORMW 「胸を比べたいんじゃなくて、%LOCALS%さんとくっついていたいんですーっ……。あたしの気持ち、ちゃんと伝わってますかーっ？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、顔がこんなに近いんですかーっ!?　胸を合わせるだけだと思ってたのに、%LOCALS%さんの目まで見えますーっ……どこを見ればいいんですかーっ!?」
		ELSEIF A == 1
			PRINTFORMW 「あぅっ、擦れるたびにぞくってしますーっ……。平気なつもりだったあたしが、いちばん平気じゃないですよーっ……！」
		ELSE
			PRINTFORMW 「比べないでくださいねーっ？　あたし、胸のことは……ひゃっ、急に押しつけたら、恥ずかしいって言う暇もないですよーっ!?」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
	CALL AITE_YOBI, 29, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%さんが近づくたび、転校生くんの中まで揺れるんですねーっ……！　あたし、ふたりとも応援しなきゃなのに、どっちも見られませんよーっ……！」
		ELSEIF A == 1
			PRINTFORMW 「転校生くん、腰、止めないでくださいねーっ……。%LOCALS%さんに見られてるのに、あたし、気持ちいいって顔を隠せなくなっちゃいましたーっ！」
		ELSE
			PRINTFORMW 「%LOCALS%さん、そんな声で煽らないでくださいよーっ……！　転校生くんに奥を突かれるたび、あたしまで返事しちゃいますーっ。もう、平気なふりできないですーっ……」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ、%LOCALS%さんが動いたら、下の転校生くんまで揺れますーっ!?　あたしの身体、上下から忙しくされて、どこに応援を送ればいいんですかーっ!?」
		ELSEIF A == 1
			PRINTFORMW 「ま、待ってください、入ったまま腰を動かしたら……あっ、脚に力が入りませんーっ！　転校生くんの上から落ちたら大変ですよーっ!?」
		ELSE
			PRINTFORMW 「上も下も一度に来たらダメですーっ……！　%LOCALS%さん、転校生くん、どっちか止まって……あ、でも止まると寂しいって何ですかーっ!?」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：なながプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生くん、今日はよく頑張りましたーっ☆　ほら、頭をこっちに……あたしが撫でて、元気を満タンにしますからねーっ♪」
		ELSEIF A == 1
			PRINTFORMW 「髪に触れてると、練習のあとに団長を励ましてるみたいで落ち着きますーっ……。転校生くんが眠るまで、あたし、ここにいますよーっ♪」
		ELSE
			PRINTFORMW 「いつも助けてもらってばかりですから、今日はあたしの番ですーっ☆　元気になるまで撫でますから、逃げちゃダメですよーっ？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「転校生くん、今日は静かですねーっ……。撫でられると困るんですか？　あたしも慰めるのは得意じゃないですけど、元気のないひとを放っておけないんですよーっ……」
		ELSEIF A == 1
			PRINTFORMW 「よしよしですよーっ……。うまい慰め方はわからないですけど、手なら動かせますからっ。少しだけ、あたしに任せてくださいねーっ」
		ELSE
			PRINTFORMW 「失敗したんですかーっ？　そんな顔をしても、星は一晩曇ったくらいで消えませんよーっ。ほら、転校生くんも少し休みましょうっ？」
		ENDIF
	ENDIF
ENDIF
;=== NANA MISSING COMMAND TRIAL END ==='''


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    # AITE_YOBI/LOCALS already contains the complete character-specific
    # address, including any honorific.  Keep generated ERB from appending
    # a second honorific if an older draft string still contains one.
    block = BLOCK.replace("\n", "\r\n").replace("%LOCALS%さん", "%LOCALS%")

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
