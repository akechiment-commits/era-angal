from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_10_木之下ゆゆ_COM.ERB")
START = ";=== YUYU MISSING COMMAND TRIAL START ==="
END = ";=== YUYU MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_10"


BLOCK = r''';=== YUYU MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「えへへ、女の子の唇もやわらかいね～♪　でもゆゆ、おに～さんの唇がいちばん好き。あとで食べ比べさせてね？」
		ELSEIF A == 1
			PRINTFORMW 「ん～、ちゅっ♪　おに～さん、ちゃんと見てた？　ゆゆがほかの子に優しくできるところも、好きになってね」
		ELSE
			PRINTFORMW 「ヤキモチさんが出てきたら、三人で仲良くしたらいいよぉ。ゆゆ、好きなひとが増えるのは嬉しいもん♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぇ、キスするの？　いいよぉ♪　ほっぺとお口、どっちがいいか相手の子に選んでもらおう？」
		ELSEIF A == 1
			PRINTFORMW 「ちゅっ……えへへ～、くすぐったいねぇ。ふたりとも笑っちゃったから、もう一回やり直し～☆」
		ELSE
			PRINTFORMW 「怖くないよ、ゆゆがぎゅってしながらするからね。ほら、おいで～♪」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 10, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%とゆゆの脚で、おに～さんを両側からぎゅ～っ♪　えへへ、どっちが好きかなんて選ばなくていいんだよぉ」
		ELSEIF A == 1
			PRINTFORMW 「おに～さんの筋肉、ぴくぴくしてる～☆　%LOCALS%、今の擦りかた気持ちよかったみたい。もう一回しよ？」
		ELSE
			PRINTFORMW 「三人でくっつくと、あったかいねぇ。ゆゆ、おに～さんの顔も%LOCALS%の顔も見えるこの場所好き～♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%、せぇので脚を動かそうね。せぇの～……わぁ、おに～さんのが間でつるつるしてるよぉ☆」
		ELSEIF A == 1
			PRINTFORMW 「男のひとの骨格はこういうときに動くんだね～。%LOCALS%、腰のところ見て、面白いよぉ♪」
		ELSE
			PRINTFORMW 「ゆゆの脚ちいさいけど、%LOCALS%と合わせたらぴったり～♪　ふたりでおに～さんを喜ばせられたねっ」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：ゆゆと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 10, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%が動くと、ゆゆのなかにも同じのが来るねぇ……んっ♪　身体のなかでお話してるみたい」
		ELSEIF A == 1
			PRINTFORMW 「ひゃぅっ、ふたりの奥が一本で繋がってる～☆　%LOCALS%、ゆゆからも揺らすね。届いたぁ？」
		ELSE
			PRINTFORMW 「声も震えも混ざって、どっちのかわからないよぉ……♪　でも%LOCALS%と一緒なら、それでいいね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「わぁ、%LOCALS%が腰を動かすとゆゆまで跳ねる～！　不思議な仕組みだねぇ、もっと試してみよっか☆」
		ELSEIF A == 1
			PRINTFORMW 「ゆゆが一回、%LOCALS%が一回ね。んっ、交代で動くと、なかで波が行ったり来たりするよぉ♪」
		ELSE
			PRINTFORMW 「%LOCALS%、手ぇ繋ご～。怖いからじゃなくて、同じときに気持ちよくなったのがわかるように♪」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「おに～さん、ゆゆのミルクでおなかいっぱいになってね♪　ゆゆの身体の一部が、おに～さんの一部になるんだよぉ」
		ELSEIF A == 1
			PRINTFORMW 「んっ、ちゅうちゅうされると胸があったかくなる～。えへへ、飲ませてあげるのも抱っこみたいで好き♪」
		ELSE
			PRINTFORMW 「ダニエルには内緒の特別ミルクだよぉ。おに～さんだけにあげるから、ゆっくり味わってね？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「わぁ、本当にここから飲むんだね～☆　ゆゆ、身体が食器になるお話も書いてみたくなっちゃった♪」
		ELSEIF A == 1
			PRINTFORMW 「おに～さん、おいしい？　甘いかなぁ、しょっぱいかなぁ。ゆゆにもあとで教えてね～？」
		ELSE
			PRINTFORMW 「こぼれてるよぉ。ほら、もっとぴったりくっついて♪　せっかく出たの、ぜんぶ飲んでほしいもん」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「おに～さんの指に押されると、ゆゆのなかから白いのが出てくる～♪　身体って秘密の袋みたいだねぇ」
		ELSEIF A == 1
			PRINTFORMW 「一滴ずつ集めるの、ふたりの宝物みたいで楽しいね。えへへ、最後まで大事に搾ってね？」
		ELSE
			PRINTFORMW 「ゆゆの身体のこと、おに～さんがゆゆより詳しくなっちゃいそう。好きなひとになら、それも嬉しいよぉ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふあっ、そこ押すと出るんだぁ☆　おに～さん、もう一回同じところ！　ゆゆもちゃんと見てるから～♪」
		ELSEIF A == 1
			PRINTFORMW 「強く握ると痛いよぉ。果物みたいに潰れないから、指でやさしく押してね？」
		ELSE
			PRINTFORMW 「ぴゅって飛んだ～！　あはは、おに～さんの顔についたよぉ。取ってあげるね、ぺろっ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこ、ゆゆの好きなところぉ……ひゃぁっ！　おに～さん、もっと指で呼んでぇ……！」
		ELSEIF A == 1
			PRINTFORMW 「身体の奥でお花が潰れて、蜜がいっぱい出るみたい……んあぁっ、また潰してぇ……♪」
		ELSE
			PRINTFORMW 「おに～さん、すきっ……そこ触られると、ゆゆの声までとろとろになっちゃうぅ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふあぁっ!?　そこ押すと、ゆゆのおなかのなかが跳ねる～！　もう一回、今度は見てるからぁ……！」
		ELSEIF A == 1
			PRINTFORMW 「んひゃっ、指は一本なのに身体じゅうに来るよぉ！　おに～さん、すごい場所見つけたねぇ……！」
		ELSE
			PRINTFORMW 「待って待って、ゆゆも観察したいのに目ぇ閉じちゃう……んあっ！　身体のほうが先に楽しんでるぅ！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「おに～さん、ゆゆの身体が勝手に雨を降らせてるよぉ。こんな日も一緒に濡れてくれるなら、寂しくないね」
		ELSEIF A == 1
			PRINTFORMW 「身体のなかにこんなに溜めてたんだねぇ……。おに～さんには、ゆゆの秘密がどんどん見つかっちゃう♪」
		ELSE
			PRINTFORMW 「この場面もおとぎ話に書こうかなぁ。洪水のなかで、おに～さんとゆゆだけ手ぇ繋いでるの♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぇ、止められないよぉ……。でも笑っちゃ駄目なのは最初の一回だけね。ゆゆが笑ったら、おに～さんも笑っていいよ♪」
		ELSEIF A == 1
			PRINTFORMW 「これはゆゆの身体の観察会じゃないよ～？　見るなら、あとで何がわかったかちゃんと教えてね」
		ELSE
			PRINTFORMW 「むう、ゆゆが嫌って言ったことまで続けるのは駄目だよ。身体が止まらなくても、おに～さんのお耳は止まらないでね？」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：ゆゆと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 10, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の胸とゆゆの胸、くっつけるとひとつの身体みたい～♪　真ん中の線、消えちゃいそうだね」
		ELSEIF A == 1
			PRINTFORMW 「んっ、先っぽが擦れてふたりとも同じ声が出た～。えへへ、%LOCALS%とゆゆ、お揃いだねぇ♪」
		ELSE
			PRINTFORMW 「もっとぎゅってしよ、%LOCALS%。胸だけじゃなくて、ほっぺもおなかも全部くっつけたいよぉ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「わぁ、%LOCALS%の胸あったか～い♪　ゆゆのも同じ温度かなぁ、触り比べてみて？」
		ELSEIF A == 1
			PRINTFORMW 「乳首と乳首でご挨拶～☆　ちょん、ちょん……ひゃっ、くすぐったいけど気持ちいいねぇ」
		ELSE
			PRINTFORMW 「%LOCALS%が恥ずかしいなら、ゆゆが先に笑うね。えへへ～♪　ほら、楽しいことになったでしょ？」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：ゆゆはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 10, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%がおに～さんの顔に乗って、ゆゆは腰に乗ってる～♪　んあっ、下から動いたらゆゆの奥まで届くよぉ！」
		ELSEIF A == 1
			PRINTFORMW 「お顔が見えなくても、なかでおに～さんが元気なのわかるよぉ……ひゃんっ、ゆゆのこと追いかけてる～♪」
		ELSE
			PRINTFORMW 「%LOCALS%とゆゆで、おに～さんを上下からぎゅう～っ☆　あっ、奥で大きくなった……喜んでるねぇ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%が動くと、おに～さんの腰も揺れて、ゆゆのなかまでぐりってする～！　三人仕掛けのおもちゃみたい☆」
		ELSEIF A == 1
			PRINTFORMW 「ゆゆが上で腰を振るね。%LOCALS%はお顔のほうを……ひゃぅっ、おに～さんだけ別の動きしたぁ！」
		ELSE
			PRINTFORMW 「男のひとの筋肉、上と下を同時に動かせるんだねぇ……んあっ！　観察してたら奥に当たったよぉ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：ゆゆがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「いつも撫でてもらってるぶん、今日はゆゆがお返し～♪　おに～さんの髪も、ダニエルみたいにふわふわにしてあげるね」
		ELSEIF A == 1
			PRINTFORMW 「『ほっほっほ、おまえさまも甘えん坊じゃのう』……ダニエルもこう言ってるよぉ。ゆゆのお膝、好きに使ってね？」
		ELSE
			PRINTFORMW 「おに～さんが寂しいときは、ゆゆとダニエルがふたりで撫でるからね。だからひとりで隠れちゃ駄目だよぉ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「い～こい～こ♪　ふふ、おに～さんも撫でると目ぇ細くなるんだね。猫さんみたい～☆」
		ELSEIF A == 1
			PRINTFORMW 「頭の骨はこういう形なんだぁ……。あっ、解剖しないよぉ？　撫でながら触ってるだけ～♪」
		ELSE
			PRINTFORMW 「『働きすぎる者には休息が必要じゃ』だって。ダニエルのおばあちゃんの言うこと、ちゃんと聞こうね？」
		ENDIF
	ENDIF
ENDIF
;=== YUYU MISSING COMMAND TRIAL END ==='''


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
