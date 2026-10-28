from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_02_北川ゆき_COM.ERB")
START = ";=== YUKI MISSING COMMAND TRIAL START ==="
END = ";=== YUKI MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_2"


BLOCK = r''';=== YUKI MISSING COMMAND TRIAL START ===
; 試作：未実装10コマンド（ユーザー指定どおり、恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%と口づけるだけ……なのに。先輩が見てると、悪いことをしてるみたいで……目をそらさないでください。余計に、寂しいから」
		ELSEIF A == 1
			PRINTFORMW 「先輩は、わたしが誰とキスしても平気なんですね。……むう。終わったら、いちばん長いのを先輩にしてもらいますから」
		ELSE
			PRINTFORMW 「うまく言葉がでてこないぶん、触れることは大事だって思ってたけど……。これは、先輩に伝えたい気持ちとはちがいます」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あ、あの、%LOCALS%。合図を決めませんか？　三つ数えたら目を閉じて……終わったら、何もなかった顔をするんです」
		ELSEIF A == 1
			PRINTFORMW 「近い、です……。画面越しなら平気なのに、息が触れる距離だと、どこを見ればいいのかわかりません」
		ELSE
			PRINTFORMW 「……ん。い、今のは命令どおりにしただけですから。変な意味を探して、わたしの顔を見ないでください」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	; 三人コマンドなので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 2, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、もうすこしこっちへ。……先輩のためなら、こうして息を合わせるくらいできます。たぶん」
		ELSEIF A == 1
			PRINTFORMW 「先輩、どちらが上手か見比べるのは禁止です。わたし、勝ち負けにすると本気になって……たぶん、優しくできなくなるから」
		ELSE
			PRINTFORMW 「ふたりの間で、先輩の呼吸だけが近くなって……。変ですね、三人なのに、先輩とふたりきりみたいに感じます」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%、わたしに合わせなくて大丈夫です。こういう協力プレイは……下手なほうが、上手なひとを真似したほうが早いですから」
		ELSEIF A == 1
			PRINTFORMW 「あっ、待って。一度止まりましょう。先輩の顔が苦しそうで……わたし、役に立つどころか邪魔になってませんか？」
		ELSE
			PRINTFORMW 「三人ぶんの体温が混ざると、誰に触れてるのかわからなくなります。……せめて、先輩は手を離さないでください」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
	; 助手調教専用なので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 2, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%が動くたび、わたしの奥にも返ってきます……。離れてるのに繋がってるみたいで、なんだか、嬉しいです」
		ELSEIF A == 1
			PRINTFORMW 「声を我慢しなくていいですよ。%LOCALS%の声が聞こえると、わたしだけじゃないって思えて……もうすこし、頑張れますから」
		ELSE
			PRINTFORMW 「あっ……今、わざと動きましたね？　だったらわたしも返します。こういう勝負、手加減できませんから……っ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あの、%LOCALS%。目を閉じてもらえませんか？　顔を見られると、失敗しちゃいけない気がして……身体が、固まるんです」
		ELSEIF A == 1
			PRINTFORMW 「どちらかが焦ると、もう片方にも伝わるんですね。……だいじょうぶ。ゆっくり、一緒に慣れていきましょう」
		ELSE
			PRINTFORMW 「んっ……言葉にしなくても、%LOCALS%が次に動くのがわかります。こういう会話なら、わたしにもできるのかも」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩は、いつも誰かを助けてばかりだから。今だけは何も考えないで、わたしに甘えてください……♪」
		ELSEIF A == 1
			PRINTFORMW 「飲んでくれるんですね。わたしの身体にも、先輩にあげられるものがあった……。えへへ、なんだか安心しました」
		ELSE
			PRINTFORMW 「先輩の髪、触ってもいいですか？　こうしてると、わたしのほうがお姉さんみたいで……すこしだけ、頼もしくなれた気がします」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「そ、そんなに急がなくても、なくなりませんから。むせたら困ります……わたしにも、ちゃんと世話をさせてください」
		ELSEIF A == 1
			PRINTFORMW 「味を聞かれても、わたしにはわかりません。……先輩の顔を見るかぎり、悪い出力ではなさそうですけど」
		ELSE
			PRINTFORMW 「こんなふうに誰かを満たせるなんて、変な感じです。いつも役に立てないって思ってたから……ちょっとだけ、嬉しいかも」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「量なんて記録しないでください。先輩に触れられて、どれだけ出たかまで残ったら……あとで見返して、眠れなくなります」
		ELSEIF A == 1
			PRINTFORMW 「先輩の手で絞られるたび、わたしのものが少しずつ溜まっていく……。捨てないでくださいね。恥ずかしくても、ぜんぶわたしですから」
		ELSE
			PRINTFORMW 「綺麗に着飾ったところだけ、見てほしかったのに。こんな格好まで大事そうに見られたら……隠れてる意味、なくなっちゃいます」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ちょ、ちょっと待って。容器と布と、それから戸締まりを確認します。途中で誰かに見られたら、もう学校に来られません」
		ELSEIF A == 1
			PRINTFORMW 「数字にするのはやめましょう。正しい出力でも、見られたくないデータはあるんです……先輩には、わからないかもしれませんけど」
		ELSE
			PRINTFORMW 「そんな真剣な顔でしないでください。笑われるよりはいいけど……大切な作業みたいに扱われると、もっと恥ずかしいです」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あっ、そこ……先輩には、見つけてほしくなかったです。もう強がっても、どこを触れば崩れるか知られちゃったから……」
		ELSEIF A == 1
			PRINTFORMW 「や、やめてとは言いません。先輩になら、隠せないところまで知られても……嫌われないって、信じてみたいです」
		ELSE
			PRINTFORMW 「身体は、正しい入力に正しい出力を返すだけなのに……先輩の指だと思うと、嬉しいまで混ざるのは、ずるいです」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「い、今の声は忘れてください。わたしにも予想できなかった反応で……再現しようとしないでっ」
		ELSEIF A == 1
			PRINTFORMW 「そこを触られると、頭のなかが真っ白になります。何か言わなくちゃいけないのに……言葉が、ぜんぶ消えて……っ」
		ELSE
			PRINTFORMW 「先輩、わたしの顔ばかり見てますよね。反応を確かめなくても、当たってます……だから、すこし目を閉じてください」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「操作は受けつけないのに、声だけはまだ届くんですね……。先輩、返事してください。通信まで切れたら、わたし……耐えられない」
		ELSEIF A == 1
			PRINTFORMW 「ゲームなら直前のデータをロードできます。でも……先輩とここにいたことまで消えるなら、やり直したくないです」
		ELSE
			PRINTFORMW 「強制イベントでも、先輩の服を掴んだのはわたしの入力です。……そこだけは、勝手に起きたことにしないでください」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「待って、操作不能の表示もなしですか……!?　原因も対処法もわからないまま進むの、いちばん苦手なのに……！」
		ELSEIF A == 1
			PRINTFORMW 「バグだと思えたら楽なのに、身体は正常なんですよね。正常に、わたしの言うことだけ聞かない……それが、すごく怖いです」
		ELSE
			PRINTFORMW 「今の記憶、頭のなかで何度も自動再生されそう……。先輩、何かどうでもいい話をしてください。上書きできるくらい、たくさん」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
	; 助手調教専用なので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 2, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の鼓動、胸から直接伝わってきます。わたしと同じくらい速くて……ふふ、ちょっと安心しました」
		ELSEIF A == 1
			PRINTFORMW 「もうすこし近くに来てください。……うまく言えないぶん、触れていたいです。%LOCALS%が嫌でなければ」
		ELSE
			PRINTFORMW 「そんなに優しくされたら、勝負にもできないじゃないですか。……今日は、負けてもいいって思ってるのに」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あの、胸より顔が近いです。%LOCALS%に見つめられると、どこを合わせるのかもわからなくなります……」
		ELSEIF A == 1
			PRINTFORMW 「比べたり、しませんよね？　わたし、そういう視線には慣れてるつもりでしたけど……今は、すごく落ち着かないです」
		ELSE
			PRINTFORMW 「ひゃっ……触れただけで、ふたりとも同時に震えましたね。ご、ごめんなさい。なんだかおかしくて……ふふ」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
	; 三人コマンドなので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 2, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、先輩の顔、見えますか？　返事はできなくても……手を握れば、だいじょうぶってわかりますから」
		ELSEIF A == 1
			PRINTFORMW 「先輩は、またふたりとも支えるつもりなんですね。……だったら、わたしも逃げません。せめて重さを分けあいます」
		ELSE
			PRINTFORMW 「先輩、苦しかったら二回叩いてください。……一回は、続けてほしい合図です。わたしだって、そのくらいは欲張ります」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ま、待って、%LOCALS%。急に動くと先輩が苦しそうです。こういうときまで我慢して、平気なふりをしますから」
		ELSEIF A == 1
			PRINTFORMW 「上下から別々に動いたら、先輩が困ります。三人の協力プレイなんですから、せめて合図くらい決めましょう」
		ELSE
			PRINTFORMW 「先輩、無理をしてませんか？　……わたしじゃ頼りないでしょうけど、苦しいときくらい、ちゃんと教えてほしいです」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：ゆきがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩が『大丈夫』って言ってくれたから、わたしは外に出られました。今度は、わたしが言います。……大丈夫です、先輩」
		ELSEIF A == 1
			PRINTFORMW 「うまく言葉がでてこないぶん、せめて触れていたいです。先輩が眠るまで、ずっとこうしてますから」
		ELSE
			PRINTFORMW 「いつも自分のことを後回しにして、誰かを助けてばかり……。今日はわたしが離しません。すこしくらい、頼ってください」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「事情は、話したくなってからでいいです。わたしも言葉にするのが遅いから……待つことなら、上手です」
		ELSEIF A == 1
			PRINTFORMW 「あの、力加減はこれで合ってますか？　誰かを慰めるの、まだ慣れてなくて……でも、途中で投げだしたりはしません」
		ELSE
			PRINTFORMW 「先輩は、あったかいです。……触れていれば、同じ現実にいるってわかります。だから、落ち着くまでここにいてください」
		ENDIF
	ENDIF
ENDIF
;=== YUKI MISSING COMMAND TRIAL END ==='''


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
