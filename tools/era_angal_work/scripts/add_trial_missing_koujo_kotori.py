from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_14_花音ことり_COM.ERB")
START = ";=== KOTORI MISSING COMMAND TRIAL START ==="
END = ";=== KOTORI MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_14"


BLOCK = r''';=== KOTORI MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ、ちゅ……えへ、やわらけぇ唇だなぁ♪　転校生しゃんには、あとでもっと長いのしてやるだよ」
		ELSEIF A == 1
			PRINTFORMW 「おらから近づいたんだ、ちゃんと最後まで……んぅ♪　転校生しゃん、そんなに見惚れでどうしただ？」
		ELSE
			PRINTFORMW 「ちゅっ……♪　おらのキス、気に入っでもらえたみてぇだな。えへ、ちょっと自信ついだぞ☆」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふあっ、おらからするだか？　よぉし……目ぇ閉じでぐれ。んっ、ちゅ……♪」
		ELSEIF A == 1
			PRINTFORMW 「鼻がぶつかっちまっだなぁ。あはは、今度はおらが顔の向き合わせるがら、もう一回だぁ☆」
		ELSE
			PRINTFORMW 「そんなに固くならなくても大丈夫だぞ。おらも心臓ばぐばぐだがら、ふたりでゆっくりやるだ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 14, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、もう少しこっちさ寄っでぐれ♪　ふたりの腿で挟むと、転校生しゃんの熱がよくわかるだ」
		ELSEIF A == 1
			PRINTFORMW 「転校生しゃん、今の動きが好きだっただな？　えへ、%LOCALS%と息合わせで、もう一度だぁ♪」
		ELSE
			PRINTFORMW 「おらたちの間でこんなに硬くなっでる……。ふたりぶん大事にされで、嬉しいだろ？　転校生しゃん♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%、おらの足の動きに合わせでな。いち、に……うはぁ、綺麗に揃っただ☆」
		ELSEIF A == 1
			PRINTFORMW 「ふたりで擦ると、転校生しゃんの腰まで勝手に動ぐんだなぁ。わかりやすくで助かるだ♪」
		ELSE
			PRINTFORMW 「ダンスみてぇに呼吸が大事だな。%LOCALS%、次はゆっくり大きく動いでみるだよ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：ことりと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 14, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んぅっ、%LOCALS%が動ぐと、おらの奥まで同じ震えが来るだ……♪　離れでるのに近ぇなぁ」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、今のすげぇ……！　%LOCALS%、次はおらから動がすぞ。ちゃんと受け取っでな？」
		ELSE
			PRINTFORMW 「%LOCALS%、手ぇ繋いでぐれ。怖いんじゃねぇぞ、同じときに感じだのがわかるようにだぁ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うはぁ、片方を動がすとこっちまで来るだか！　%LOCALS%、不思議で面白ぇなぁ☆」
		ELSEIF A == 1
			PRINTFORMW 「おらがゆっくり腰を引ぐぞ……んっ。%LOCALS%の声まで振動で伝わっでくるだ♪」
		ELSE
			PRINTFORMW 「あはは、ふたりとも同時に跳ねちまっだな！　今度は抱きあっで、逃げねぇようにするだ☆」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生しゃん、ゆっくり飲んでいいだよ。おらが抱いでるがら、今日は好きなだけ甘えでな♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ、吸われるたび胸の奥がきゅうってするだ……。おらの身体で転校生しゃんを満たせるんだなぁ♪」
		ELSE
			PRINTFORMW 「残さなくていいぐらい、まだ出るだよ。えへ、おらが転校生しゃんにだけ作れるご馳走だぁ☆」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ほ、ほんとに飲むだか？　お味に自信はねぇげど……出したものは最後まで面倒みるだ！」
		ELSEIF A == 1
			PRINTFORMW 「ふぁっ、舌でそこ押されると勝手に出るだよぉ……！　転校生しゃん、飲みかた覚えるの早ぇなぁ」
		ELSE
			PRINTFORMW 「口の端からこぼれでるぞ。ほら、もっとおらにくっついで、しっかり飲んでぐれ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生しゃん、瓶の目盛りばっかり見ねぇで、おらの顔も見でぐれ……んっ。ひとりで頑張るより心強ぇだ♪」
		ELSEIF A == 1
			PRINTFORMW 「いつもは飯つくっで誰かの腹を満たす側だげど、今日はおらが世話されでるなぁ。えへ、たまにはいいだ♪」
		ELSE
			PRINTFORMW 「押されるたび胸は軽くなるのに、転校生しゃんの指のぬくもりだけ残るだ……不思議だなぁ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「一回目より二回目のほうが勢いあるぞ。身体にも順番があるんだなぁ、もう少し試しでみるだ☆」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、容器の外まで飛んだぁ！　次はおらが角度を直すがら、転校生しゃんはそのままだぞ」
		ELSE
			PRINTFORMW 「採れだぶん、何に使えばうめぇかなぁ。転校生しゃん、終わるまでに献立考えでぐれ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこっ、転校生しゃん……！　おら、すぐ駄目になっちまう、もっとぉ……！」
		ELSEIF A == 1
			PRINTFORMW 「んぁっ、奥が跳ねるだ……！　転校生しゃんの指、好き、離さねぇで……！」
		ELSE
			PRINTFORMW 「ひゃぁっ、またそこぉ……！　声、止められねぇ、転校生しゃんっ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おわひゃっ!?　何だいまの、身体の奥までびりって来ただ！」
		ELSEIF A == 1
			PRINTFORMW 「ま、待つだ、そこばっかりは……んぁっ！　腰が勝手に動ぐぅ……！」
		ELSE
			PRINTFORMW 「ふぁっ、脚に力入らねぇ……！　げど、その指はまだ離さねぇでぐれ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あぁ、ぜんぶ出ちまう……。転校生しゃんの前だと、身体まで隠しごとできねぇなぁ……♪」
		ELSEIF A == 1
			PRINTFORMW 「えへ、最後まで受け止めでくれるんだな。だったらおら、変に力入れねぇで任せるだよ」
		ELSE
			PRINTFORMW 「出し切ったら、身体がすっげぇ軽くなっただ☆　転校生しゃんに見守られだおかげだな♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うはぁ、本当に止まらねぇだ！　こうなったら最後まで、堂々と出し切るぞ～っ！」
		ELSEIF A == 1
			PRINTFORMW 「音まで聞こえで恥ずかしいげど……転校生しゃんが笑うなら、おらも笑っちまうだ♪」
		ELSE
			PRINTFORMW 「島の雨より勢いあるがもなぁ。あはは、身体って思ったより正直だぁ☆」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：ことりと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 14, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の先っぽ、おらのと擦れるたび熱くなるだ……。んっ、もう少し強く押しでぐれ♪」
		ELSEIF A == 1
			PRINTFORMW 「同じときに声出たな、%LOCALS%。えへ、胸の鼓動まで揃っでるみてぇだぁ♪」
		ELSE
			PRINTFORMW 「まだ離れなくていいだよ。%LOCALS%の温かさ、胸いっぱいに覚えでおきてぇだ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふあっ、先っぽ同士はこんなに敏感だか！　%LOCALS%、次はもっとゆっくりやるだ」
		ELSEIF A == 1
			PRINTFORMW 「おらが押したら、%LOCALS%も押し返しでな。んっ……あはは、いい勝負だぁ☆」
		ELSE
			PRINTFORMW 「ふたりとも同じ顔しでるなぁ。恥ずかしいなら、笑っで一緒に続けるだよ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：ことりはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 14, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、転校生しゃんの顔は頼むだ……！　おらはこっちで、んぁっ、奥まで来でるぅ……！」
		ELSEIF A == 1
			PRINTFORMW 「顔は隠れでるげど、転校生しゃんの腰の癖は間違えねぇ……ひゃぁっ、もっと下からぁ……！」
		ELSE
			PRINTFORMW 「転校生しゃん、%LOCALS%に夢中でも、おらの奥は休ませねぇで……んっ、もっとぉ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%が動ぐたび、転校生しゃんの腰まで……ふぁっ、奥に何度も当たるだ！」
		ELSEIF A == 1
			PRINTFORMW 「おらが上で動ぐぞ……ひゃぁっ！　転校生しゃん、下から急に突きあげるのはずりぃだ！」
		ELSE
			PRINTFORMW 「上下から忙しいのに、なかじゃ全然弱らねぇ……んぁっ、おらの奥ずっと擦られでるぅ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：ことりがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生しゃん、今日もよく頑張ったなぁ。おらの膝で、眠くなるまで撫ででやるだよ♪」
		ELSEIF A == 1
			PRINTFORMW 「こうしで髪に触れでると、転校生しゃんがちゃんと隣にいるってわかるだ。えへ、安心するなぁ♪」
		ELSE
			PRINTFORMW 「いつも守っでもらってるぶん、今日はおらが甘やかす番だぁ。遠慮しねぇで頭預けでな♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「疲れでる顔しでるぞ、転校生しゃん。ほら、頭こっちさ置いで、ちょっと休むだよ」
		ELSEIF A == 1
			PRINTFORMW 「おらの手、家事でちょっと硬ぇげど、撫でるときは優しくするがらな。よしよし♪」
		ELSE
			PRINTFORMW 「うはぁ、撫でたら急に大人しくなっただ☆　転校生しゃんにも、こんな顔があるんだなぁ」
		ENDIF
	ENDIF
ENDIF
;=== KOTORI MISSING COMMAND TRIAL END ==='''


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
