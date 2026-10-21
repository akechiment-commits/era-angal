from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"


REWRITTEN = r''';--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	CALL AITE_YOBI, 47, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の顔、真っ赤だね。ふふ、転校生くんに見られてるからかな。もう少しだけ、このままでいよ♪」
		ELSEIF A == 1
			PRINTFORMW 「ん……ちゅ。%LOCALS%の唇、やわらかいね。転校生くん、そんな顔をするなら、ちゃんと見ていてよ♪」
		ELSE
			PRINTFORMW 「もう一度？　いいよ、%LOCALS%。終わったら、転校生くんのところへ戻るからね……ふふ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、わたしが%LOCALS%に？　転校生くんが見てるのに……先に言ってくれたら、心の準備くらいできたのに」
		ELSEIF A == 1
			PRINTFORMW 「ちゅ……っ。触れただけなのに、緊張するね。転校生くん、そんなにじっと見ないでよ」
		ELSE
			PRINTFORMW 「%LOCALS%、もう少しだけなら……。転校生くんの前でこんなことするの、変な感じだね」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 47, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あっ……%LOCALS%と息が合うと、転校生くんの熱まで近くなるね。ふふ、負けたくないな♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ……%LOCALS%、そのまま。転校生くん、そんなに嬉しそうな顔をしないで。わたしまで調子に乗るから」
		ELSE
			PRINTFORMW 「あ、だめ……っ。わたしのほうが先に力が抜けそう。%LOCALS%、置いていかないでね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃあっ!?　%LOCALS%まで一緒なの？　転校生くん、いつの間にこんな話になったの？」
		ELSEIF A == 1
			PRINTFORMW 「ん、あ……っ。ちょっと待って、早いよ。%LOCALS%、わたしの息に合わせてね」
		ELSE
			PRINTFORMW 「ふふ、平気な顔をしてみたけど、もうばれたよね。転校生くん、笑ったらだめだからね」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
	CALL AITE_YOBI, 47, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ……%LOCALS%の息、聞こえるね。動くたびにわたしまで揺れて……もう少し、そばにいて」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%、いまの、わたしにも来たよ。離れてるのに、同じところで声が出そう……ふふ」
		ELSE
			PRINTFORMW 「ひゃわわわっ!?　待って。気持ちいいのが重なると、自分の声までわからなくなるね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにっ……%LOCALS%？　ごめん、いまの声、忘れて。こんなに近いと、変な気分になるね」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、そんなに動いたら……っ。%LOCALS%、手、貸して。ちょっとだけ、ぎゅってしてて」
		ELSE
			PRINTFORMW 「女の子同士なら平気だと思ったのに。%LOCALS%、わたし、今すごく変な顔してない？」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ん……っ、そんなに夢中になってくれると、嬉しくなるよ。胸のことは、あんまり見ないでね♪」
		ELSEIF A == 1
			PRINTFORMW 「ふふ、甘えん坊さんだね。飲んでる顔を見てると、わたしまでお姉さんになった気分……えへへ♪」
		ELSE
			PRINTFORMW 「まだ離れなくていいよ。転校生くんが落ち着くまで、わたしもこうしてるからね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、わたしの胸から？　これで足りるのかな。……って、もう飲んでるんだね」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ……顔、近いよ。胸が小さいの、見ればわかるでしょ？　そんなに一生懸命にならなくても……」
		ELSE
			PRINTFORMW 「ん……っ、急に吸うと驚くよ。そんな顔をされたら、止めてとは言いにくいな」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこ、もう慣れたんだね。ふふ、わたしの反応を覚えられるのは恥ずかしいけど……嫌じゃないよ」
		ELSEIF A == 1
			PRINTFORMW 「あっ、そこは少しやさしくね。胸のこと、そんなに丁寧にしてくれるんだ……ふふ」
		ELSE
			PRINTFORMW 「出てくるの、そんなに嬉しい？　……なら、もう少しだけ付き合うよ。転校生くんの顔、好きだから」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにっ!?　搾るって、そういうことなの？　手つきまで確認するの、なんだか実験みたいだね」
		ELSEIF A == 1
			PRINTFORMW 「あっ、強いよ……っ。そんなに頑張られると、くすぐったくて、どこを見ればいいかわからなくなるな」
		ELSE
			PRINTFORMW 「まだ続けるんだね。……量を数えるのはやめてね。恥ずかしくなるから」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこ……っ、もう見つけたの？　転校生くんに触られると、すぐわかっちゃうんだね……止めなくていいよ」
		ELSEIF A == 1
			PRINTFORMW 「んっ、あ……っ。奥まで響く……。お姉さんだよって言ってたのに、もう声が隠せないね」
		ELSE
			PRINTFORMW 「ひゃわわわっ!?　だめ、頭が真っ白……っ。転校生くん、ぎゅっとしてて。どこにも行かないで♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、そこ……？　違うよ、そんなところじゃ……っ。あれ、力が入らないな」
		ELSEIF A == 1
			PRINTFORMW 「ひ、ひゃっ……っ。触られるたびに身体が跳ねる……。転校生くん、笑わないでね」
		ELSE
			PRINTFORMW 「ふふ……まだ平気、だよね。……うそ、もう少しゆっくりにして。変な声、聞かれたくないから」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あ……止まらない……。転校生くんの前で、こんなところまで見せるんだね。笑わないで、そばにいて」
		ELSEIF A == 1
			PRINTFORMW 「や、だ……っ。音まで聞こえるの、恥ずかしいよ……手、離さないでね」
		ELSE
			PRINTFORMW 「ひゃっ……わたし、もう止められないんだね。終わったあとも、ちゃんと隣にいてくれる？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、ちょっと待って……っ。なにこれ、止まらないよ。わたし、こんなつもりじゃ……」
		ELSEIF A == 1
			PRINTFORMW 「うぅ……見ないで、とは言えないけど……今の顔、覚えないでね」
		ELSE
			PRINTFORMW 「みづちゃんに知られたら、絶対からかわれる……。転校生くん、今のことは秘密にしてね」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
	CALL AITE_YOBI, 47, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の胸、あったかい……。顔まで近いと、余計にどきどきするね♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ……%LOCALS%、そこ、擦れる……。ふふ、そんな顔をされたら、わたしまで意地悪したくなるね」
		ELSE
			PRINTFORMW 「ひゃっ……っ、胸の先、そこに当たってる。%LOCALS%、もう少しだけ、このままでいよ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにっ？　%LOCALS%と胸を合わせるの？　近いね……わたし、どんな顔をしてればいいのかな」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、急に押しつけないで……っ。鼓動まで聞こえると、落ち着かないよ」
		ELSE
			PRINTFORMW 「ふふ、平気だと思ったのに……。%LOCALS%、ゆっくりなら、もう少し続けてもいいよ」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
	CALL AITE_YOBI, 47, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ……下からも、%LOCALS%の動きも……っ。転校生くん、二人分は、わたしには多いよ……♪」
		ELSEIF A == 1
			PRINTFORMW 「あ、また揺れた……。%LOCALS%、そんなに動かなくても、もう十分伝わってるよ」
		ELSE
			PRINTFORMW 「%LOCALS%ばかり見ないで……っ。わたしのことも忘れないで、こっちを見てよ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひゃわわわっ!?　わたしが上なの？　%LOCALS%まで顔の上って、転校生くん、急すぎるよ……っ」
		ELSEIF A == 1
			PRINTFORMW 「あっ、揺らさないで……っ。%LOCALS%も、そんなに動かないで。下から来ると、わたし、もう……」
		ELSE
			PRINTFORMW 「ふふ～ん、わたしが合わせてあげる……って、二人とも待って。これじゃわたしまで余裕なくなるよっ」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「よしよし。今日はよく頑張ったね。わたしが撫でてあげるから、今は休んでて♪」
		ELSEIF A == 1
			PRINTFORMW 「ふふ、もう目を閉じたんだ。眠くなるまで、もう少しこうしてようね」
		ELSE
			PRINTFORMW 「話したくないことは、今は話さなくていいよ。わたし、隣にいるからね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「転校生くん、今日は疲れた顔してるね。ほら、わたしに任せて」
		ELSEIF A == 1
			PRINTFORMW 「うにっ？　そんなに素直に頭を預けるんだ……。ふふ、たまには甘えていいんだよ？」
		ELSE
			PRINTFORMW 「無理に話さなくて大丈夫。わたし、ちゃんと聞くからね。眠るまで撫でてあげるよ」
		ENDIF
	ENDIF
ENDIF
'''


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    start = text.index(";--- COM60 助手にキスさせる ---")
    end = text.index("\n@TRAIN_MESSAGE_B280_47", start)
    text = text[:start] + REWRITTEN + text[end:]
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
