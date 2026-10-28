from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_03_小野ちよ_COM.ERB")
START = ";=== CHIYO MISSING COMMAND TRIAL START ==="
END = ";=== CHIYO MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_3"


BLOCK = r''';=== CHIYO MISSING COMMAND TRIAL START ===
; 試作：未実装10コマンド（ユーザー指定どおり、恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%とキスするんですか？　いいですけど……あとで、お兄ちゃん先輩にも同じことしてもらいますからね？」
		ELSEIF A == 1
			PRINTFORMW 「ん……。あっ、お兄ちゃん先輩、そんなにじっと見ないでください。何だか、悪いことしてる気分になりますよぉ……」
		ELSE
			PRINTFORMW 「あ、甘い味がします。さっきのお菓子かな……？　でも、わたしが知りたいのは、お兄ちゃん先輩の味なんですけどね……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、%LOCALS%と？　女の子同士で、ほっぺじゃなくて……く、口ですか？　ふぇぇ、急ですね～っ!?」
		ELSEIF A == 1
			PRINTFORMW 「ん、ちゅ……。わわっ、目を開けてたんですか？　恥ずかしいから、そこは閉じててくださいよぉ！」
		ELSE
			PRINTFORMW 「……終わり、ですよね？　%LOCALS%、そんな名残惜しそうにされると、もう一回しなくちゃいけない気がするんですけど……」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	; 三人コマンドなので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 3, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「むう。お兄ちゃん先輩、ふたりに挟まれて嬉しそう……。わたしの脚のほうが気持ちいいって、ちゃんと言わせますからね？」
		ELSEIF A == 1
			PRINTFORMW 「ひゃんっ、先輩のが、太ももの間で……。%LOCALS%と擦れるたび、わたしまでぞくぞくしますぅ……」
		ELSE
			PRINTFORMW 「せぇの、で動きますよ。せぇ……あぅっ、先輩が先に動いたら、息なんて合わせられませんよぉ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%、もうすこしゆっくり……ひゃっ！　わたし、こういう運動は得意じゃないんです～っ！」
		ELSEIF A == 1
			PRINTFORMW 「脚がやわらかい？　そ、それは遠回しに太いって……ふぇっ、今そこを擦らないでくださいっ！」
		ELSE
			PRINTFORMW 「あぅ、三人で動くと、どこが誰に触れてるのか……。お兄ちゃん先輩、急に腰を揺らさないでぇ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
	; 助手調教専用なので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 3, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、手ぇ握って……。動くたび、そっちの震えまで奥にくるんです。ひゃぁ、また……っ」
		ELSEIF A == 1
			PRINTFORMW 「ま、待って、いま速くしたら……あぅっ！　こっちにも返ってくるって、知っててやりましたね～っ？」
		ELSE
			PRINTFORMW 「そんなに声を我慢しなくていいよ……。わたしも、もう無理だから。いっしょに、いっぱい声だそ……？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぇぇ、%LOCALS%が動くと、わたしのなかまで……！　い、いきなり来るから怖いですぅっ！」
		ELSEIF A == 1
			PRINTFORMW 「あっ、止まって……。だいじょうぶ、すこしびっくりしただけ。今度は、ゆっくりいっしょに動こうね？」
		ELSE
			PRINTFORMW 「ひゃんっ！　いま、どっちが動いたの？　もう、わからないよぉ……身体が勝手に揺れちゃう……っ」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「おいしいですか、お兄ちゃん先輩？　えへへ……わたしの身体から出たもので笑ってくれるの、何だか嬉しいです♪」
		ELSEIF A == 1
			PRINTFORMW 「そんなに夢中で飲まれると、胸の奥までくすぐったいです……。今日は、いっぱい甘えていいですからね？」
		ELSE
			PRINTFORMW 「お兄ちゃん先輩に食べてもらうの、大好きですけど……これはいつもの試食より、ずっと恥ずかしいですね……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぇっ、ほんとに飲むんですか？　残すのはもったいないですけど……心の準備くらい、させてくださいよぉ」
		ELSEIF A == 1
			PRINTFORMW 「あぅ、吸うたびに胸がきゅって……。お、おいしいならいいですけど、感想は小声でお願いします～っ」
		ELSE
			PRINTFORMW 「ゆっくり飲んでくださいね。むせたりしたら大変ですから……って、どうしてわたしが落ち着かせてるんでしょう？」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ひゃっ……絞るたび、胸が熱くなります。お兄ちゃん先輩、そんなに丁寧にされたら、もっと出ちゃいますよぉ……」
		ELSEIF A == 1
			PRINTFORMW 「わたしのもの、こんなに溜まったんですね……。捨てないでください。先輩に、ぜんぶ飲んでほしいです」
		ELSE
			PRINTFORMW 「あぅっ、そこは強すぎます……！　味見したいなら、もうすこし優しくしてくださいよぉ、お兄ちゃん先輩……」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「け、計量カップまで用意したんですか？　量は数えないでください、体重と同じくらい知りたくない数字ですぅ！」
		ELSEIF A == 1
			PRINTFORMW 「ひゃんっ！　牛さんみたいに手際よくしないでください。褒めてませんからね、お兄ちゃん先輩～っ！」
		ELSE
			PRINTFORMW 「あぅ……胸を揉まれるたび、白いのが出て……。そんなに近くで見られたら、恥ずかしいですよぉ」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ひゃっ、そこ、だめぇ！　お兄ちゃん先輩、指、止め……あぁっ、止めないでぇ……！」
		ELSEIF A == 1
			PRINTFORMW 「あっ、またそこっ……！　お腹の奥、きゅうって……ふぇぇ、先輩の顔、見てられないよぉ……！」
		ELSE
			PRINTFORMW 「せんぱい、好き、です……だから、そこばっかり、こすらないで……っ！　わたし、変になっちゃう……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぇっ!?　い、今のところ、もう触らないで……ひゃぁっ、言ったそばからぁ！」
		ELSEIF A == 1
			PRINTFORMW 「あぅっ、身体が勝手に跳ねちゃう……！　ち、ちがうんです、わたしが動いたんじゃなくてぇ……！」
		ELSE
			PRINTFORMW 「ひぃん、そこ怖いですぅ……！　頭、真っ白になって……声、止められないよぉっ！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「おばあちゃんは『強くなければ生きていけない』って言ってたけど……お兄ちゃん先輩、今日だけは弱いまま、ここにいてもいいですか……？」
		ELSEIF A == 1
			PRINTFORMW 「わたし、食べたぶんだけ幸せになれる身体は好きです。でも今は、その身体が言うことを聞かないのが……くやしいです」
		ELSE
			PRINTFORMW 「強くなければ、の続きは『優しくなければ』なんです……。お兄ちゃん先輩、今はわたしの代わりに、優しくしてください……っ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「人間の身体って、我慢すれば何でもできるようにはできてないんですよぉ！　そんなの、断食のときにもう学びましたぁ……！」
		ELSEIF A == 1
			PRINTFORMW 「こ、これ、ふくよかだから多いわけじゃないですからね!?　ひぃん、こんなときまでそこを気にする自分が嫌ですぅ……！」
		ELSE
			PRINTFORMW 「『奇跡は起きるんじゃなくて、起こすもの』……止める奇跡は無理でしたけど、泣かずに立ってるくらいは……やってみせます！」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
	; 助手調教専用なので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 3, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の胸、あったかい……。こうしてくっつくと、抱きしめるより近いですね……えへへ♪」
		ELSEIF A == 1
			PRINTFORMW 「ひゃんっ、先っぽ同士、こすれちゃった……。%LOCALS%、もう一回して。今の、気持ちよかったから……」
		ELSE
			PRINTFORMW 「わたしのほうがふくよか？　そ、それは褒めてますよね？　むう……じゃあ、もっと押しつけちゃいます♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぇっ、%LOCALS%、顔が近いよぉ……。胸よりそっちのほうが恥ずかしいです～っ」
		ELSEIF A == 1
			PRINTFORMW 「あぅ、先っぽが触れるたび、ぞくってします……。女の子同士でも、こんなになるんですね」
		ELSE
			PRINTFORMW 「く、比べないでね？　わたし、自分の身体にはちょっと自信が……ひゃっ、急に擦らないで～っ！」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
	; 三人コマンドなので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 3, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あっ、先輩、下から突きあげないでぇ！　腰、止まらなく……%LOCALS%の前で、こんな声ぇ……！」
		ELSEIF A == 1
			PRINTFORMW 「ひゃぁっ、奥まで入ってるぅ……！　%LOCALS%も先輩の顔で動いて……わたし、どっち見たらいいのぉ……！」
		ELSE
			PRINTFORMW 「せんぱい、好きぃ……もっと、下から……っ！　ふぇぇ、%LOCALS%に聞かれてるのに、止められないよぉ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぇっ、%LOCALS%が動くと、その下のお兄ちゃん先輩まで……ひゃんっ！　なか、擦れてますぅ！」
		ELSEIF A == 1
			PRINTFORMW 「ま、待ってください、入ったまま揺らしたら……あぅっ！　脚に力、入らないよぉ……！」
		ELSE
			PRINTFORMW 「ひぃん、上も下も動かないでぇ……！　こんなに突かれたら、わたし、先輩の上から落っこちちゃいますぅ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：ちよがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「お兄ちゃん先輩、今日もお疲れさまです。いつもがんばってるぶん、わたしが良い子良い子してあげますね～♪」
		ELSEIF A == 1
			PRINTFORMW 「お兄ちゃん先輩の髪、あったかい……。眠ってもいいですよ。起きるまで、ずっと撫でてますから」
		ELSE
			PRINTFORMW 「いつもわたしのお菓子を食べて、笑ってくれるでしょう？　今日はそのお礼です。元気になるまで、離しませんよ～♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「何か失敗しちゃったんですか？　まあまあ、なるようになりますよ。良い子、良い子～♪」
		ELSEIF A == 1
			PRINTFORMW 「よしよし……。お腹も空いてませんか？　落ち着いたら、甘いものをつくってあげますね」
		ELSE
			PRINTFORMW 「事情は聞きませんけど、元気がないひとは放っておけません。泣きたいなら、わたしの胸も貸しますよ？」
		ENDIF
	ENDIF
ENDIF
;=== CHIYO MISSING COMMAND TRIAL END ==='''


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
