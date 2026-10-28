from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_04_早川きこ_COM.ERB")
START = ";=== KIKO MISSING COMMAND TRIAL START ==="
END = ";=== KIKO MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_4"


BLOCK = r''';=== KIKO MISSING COMMAND TRIAL START ===
; 試作：未実装10コマンド（ユーザー指定どおり、恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「おろろ、%LOCALS%とキスしたら、あたしまで浮気者ですか？　先輩、あとでちゃんと上書きしてくださいね～？」
		ELSEIF A == 1
			PRINTFORMW 「ん、ちゅ……。あれ、先輩の顔どっちですか？　よく見えないけど、なんだかすっごく見られてる気がします～っ」
		ELSE
			PRINTFORMW 「恋バナは見るほうが楽しいのに、自分が見られるとこんなに恥ずかしいんですね……。先輩、笑ってませんよね？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「お、おろろ～？　%LOCALS%と口でですかっ？　ほっぺじゃ駄目なんでしょうか、あたしキスとかよくわかんなくて～っ！」
		ELSEIF A == 1
			PRINTFORMW 「んむっ……あ痛っ！　ご、ごめんなさい、歯がぶつかっちゃいました！　キスでもドジるなんてぇ……！」
		ELSE
			PRINTFORMW 「%LOCALS%、ごめんね？　あたし、緊張すると力加減がわかんなくて……唇、痛くしなかった？」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	; 三人コマンドなので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 4, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「おろろっ、%LOCALS%と息を合わせる前に、先輩が腰を動かすから……！　あたしの脚、もうついていけません～っ！」
		ELSEIF A == 1
			PRINTFORMW 「ふたりがかりなのに、先輩まだ余裕そう……。むう、%LOCALS%、今度こそ一緒にぎゅって挟みましょうっ」
		ELSE
			PRINTFORMW 「ひゃっ、先輩のが脚の間を擦って……%LOCALS%の肌まで当たってますっ。あたし、どっちに合わせたらいいのぉ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「三人で動くなんて無理ですよ～っ！　右脚と左脚だけでも、あたしはよく絡まって転ぶのにぃ！」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%、せぇので動こう？　せぇの……おろろっ、先輩が逆に動いたら、もう何が何だか～っ！」
		ELSE
			PRINTFORMW 「ひゃあっ、どっちの脚が触ってるんですか!?　先輩、そんな嬉しそうな顔してないで教えてくださいよぉ！」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
	; 助手調教専用なので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 4, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、手ぇ握ってて……。そっちが震えるたび、あたしのなかにも来て……おろ、ろ……っ」
		ELSEIF A == 1
			PRINTFORMW 「待って、今いっぺんに動いたら……ひゃぁあっ！　もう、わざとでしょ～……あたし、力入らないよぉ……！」
		ELSE
			PRINTFORMW 「%LOCALS%の声、近くで聞こえる……。あたしも我慢できないから、一緒に……あっ、また奥、揺れてぇ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「お、おろろっ!?　%LOCALS%が動くと、こっちまで勝手に……ひぃっ、次に来るのが見えなくて怖いよぉ！」
		ELSEIF A == 1
			PRINTFORMW 「ゆっくり、同じ速さで動こう？　あっ……だ、駄目、いま止まって！　身体が追いつかないのぉ……！」
		ELSE
			PRINTFORMW 「ごめんね%LOCALS%、怖くて脚を閉じたら、そっちまで引っぱっちゃう……！　うぇ～ん、どうすればいいのぉ!?」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「おいしいですか、先輩？　あたしでも、ちゃんと先輩の役に立ててるんですね……えへへ、もっと飲んでください♪」
		ELSEIF A == 1
			PRINTFORMW 「胸はあんまり感じないはずなのに……先輩が夢中で飲んでるのを見てると、そこだけ熱くなるんです。おろろ……？」
		ELSE
			PRINTFORMW 「こぼさず飲めて偉いですね～♪　なんて、あたしがお母さんみたい……。先輩、笑わないでくださいよぉ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ほ、本当にそこから飲むんですか!?　おろろ～、あたしより先輩のほうが覚悟決まりすぎですよぉ！」
		ELSEIF A == 1
			PRINTFORMW 「あぅ、吸われてる感じはするけど……おいしいんですか？　変な味だったらごめんなさい、って謝ることなのかなぁ？」
		ELSE
			PRINTFORMW 「そんなに急いだらむせちゃいますよ？　ほら、ゆっくり……って、どうして飲まれてるあたしが世話を焼いてるんでしょう～？」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩、意外と手つきが上手ですね～……。あたしの胸から、白いのがどんどん溜まってくの、不思議です」
		ELSEIF A == 1
			PRINTFORMW 「おろろ、こんなに出るとは思わなかったです！　せっかく先輩が集めてくれたんだし、ひと滴も無駄にしないでくださいね？」
		ELSE
			PRINTFORMW 「胸は鈍いほうなのに、先輩の指を見てると落ち着かないです……。次にどこを搾られるか、わかっちゃうからかなぁ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「お、おろろ～？　そんなに真剣な顔で搾らないでくださいっ。量まで見られるの、何だか恥ずかしいですよぉ！」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、容器をあたしに持たせるんですか？　だ、駄目ですよ、こういうときほど絶対こぼしますから～っ！」
		ELSE
			PRINTFORMW 「痛くはないですけど、もうすこし優しくしてください。あたしが平気でも、胸が取れちゃいそうで怖いです～っ！」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ひゃぁっ、そこ、またっ……！　先輩、待って、あたし……おろろも、言えな……あぁっ！」
		ELSEIF A == 1
			PRINTFORMW 「せんぱい、指、曲げないで……っ！　なか、びくびくして……脚、もう力はいらないよぉ……！」
		ELSE
			PRINTFORMW 「好き、好きですからぁ……そこばっかり、だめぇっ！　あたし、先輩の前で、おかしくなっちゃう……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おろっ、そこ何ですかっ!?　ひゃぁあっ、もう一回は駄目、身体が勝手に跳ねちゃうぅ！」
		ELSEIF A == 1
			PRINTFORMW 「やっ、怖い、指が来るのわかるのに避けられない……！　あぅっ、またそこぉ……！」
		ELSE
			PRINTFORMW 「ひぃん、止めてくださ……あっ、声、勝手にっ！　あたし、こんなの知らないよぉ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「目が悪くてよかったって、初めて思いました……。でも先輩の顔が見えないと、怒ってないかもわからなくて……困ります」
		ELSEIF A == 1
			PRINTFORMW 「おろろ……こぼすのは慣れてるつもりだったのに、自分までこぼれちゃうなんて……こんなドジ、笑いかたもわからないです」
		ELSE
			PRINTFORMW 「先輩、いつもの『またやったな』って顔してください……。特別にかわいそうな子を見るみたいにされたら、そっちのほうが泣いちゃいます」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おろろろっ、転んでないのに水たまりができてますぅ!?　あたし、とうとう何もないところで身体まで滑らせましたぁ!?」
		ELSEIF A == 1
			PRINTFORMW 「コンタクトなら落としても拾えますけど、これは拾えないですぅ！　先輩、そこで探すみたいに下を見ないでぇ！」
		ELSE
			PRINTFORMW 「いつもの失敗なら、あとで笑い話にできますけど……これはまだ無理です。だから先輩、今は笑うの、ちょっと待ってくださいね……？」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
	; 助手調教専用なので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 4, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の顔、近いね……。胸の感触より、息が当たるほうがドキドキするかも。えへへ、変なの～♪」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、%LOCALS%はそんなに感じるの？　あたし、ちょっと鈍いみたいで……同じくらい気持ちよくなれなくて、ごめんね？」
		ELSE
			PRINTFORMW 「おろろ、こすってるうちにずれてきちゃった。%LOCALS%、もう一回くっつけて？　今度は離れないように抱きしめるから♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「お、おろろ～？　胸を比べるだけじゃなくて、先っぽまで合わせるんですか？　顔も近くて落ち着かないよぉ！」
		ELSEIF A == 1
			PRINTFORMW 「あっ、いま擦れた……。あたしは平気だけど、%LOCALS%は大丈夫？　痛かったらすぐ言ってね？」
		ELSE
			PRINTFORMW 「ごめんね、力加減がわからなくて！　あたしがあんまり感じないからって、ぎゅうぎゅう押しすぎちゃった～っ！」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
	; 三人コマンドなので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 4, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ひゃぁっ、%LOCALS%が動くたび、先輩の腰まで揺れて……なか、擦れてっ……あたし、座ってられないよぉ！」
		ELSEIF A == 1
			PRINTFORMW 「先輩、下から突かないでぇ……！　脚、もうへなへなで……%LOCALS%の前なのに、声、止まらな……あぁっ！」
		ELSE
			PRINTFORMW 「せんぱい、奥、だめぇっ……！　上も動いて、あたしまで揺れて……好き、だから、もう落ちても離れないでぇ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おろろっ、%LOCALS%が腰を動かすと、先輩まで下で……ひゃぁっ、なかに当たってますぅ！」
		ELSEIF A == 1
			PRINTFORMW 「ま、待ってください、入ったまま揺らしたら……脚に力、入らないっ！　あたし、先輩の上から転びます～っ！」
		ELSE
			PRINTFORMW 「上と下で別々に動かないでぇ！　どっちに合わせれば……あぅっ、奥、こすれて頭まっしろですぅ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：きこがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「いつも転んだあたしを起こしてくれるでしょう？　今日は、あたしが先輩を元気にする番です。よしよし～♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩はあんまり喋らないから、平気な顔してても心配なんです。元気になるまで、こうしててもいいですか？」
		ELSE
			PRINTFORMW 「大丈夫ですよ。あたしが何度転んでも先輩が見放さなかったみたいに、あたしもずっとそばにいますから……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おろろ、先輩が元気ないなんて珍しいですね？　こういうときは頭を撫でるといいって、あたし知ってますよ～♪」
		ELSEIF A == 1
			PRINTFORMW 「よしよし。いつも助けてもらってばかりですから、たまにはあたしにも頼ってください。転ばないよう座ってますし！」
		ELSE
			PRINTFORMW 「はい、良い子良い子～♪　あっ、先生をお母さんって呼ぶみたいに、先輩を子供扱いしちゃってますね。ごめんなさい！」
		ENDIF
	ENDIF
ENDIF
;=== KIKO MISSING COMMAND TRIAL END ==='''


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
