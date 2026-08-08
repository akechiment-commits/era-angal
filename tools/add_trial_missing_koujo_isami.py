from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_16_大虎いさみ_COM.ERB")
START = ";=== ISAMI MISSING COMMAND TRIAL START ==="
END = ";=== ISAMI MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_16"


BLOCK = r''';=== ISAMI MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ、ちゅ……♪　柔らかくて、いい匂いするっすね。先輩にはあとで、もっと甘いのあげるっす」
		ELSEIF A == 1
			PRINTFORMW 「あたいから近づいたんすから、途中で逃げないっすよ……んぅ♪　えへへ、ちゃんとできたっす」
		ELSE
			PRINTFORMW 「先輩、そんなに見つめられると照れるっすよ。キスしたぶん、あとであたいをかわいがってくださいね♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、あたいからっすか？　お、押忍……こういうときこそ女らしく、んっ、ちゅ♪」
		ELSEIF A == 1
			PRINTFORMW 「わわっ、力入りすぎて肩まで掴んじゃったっす！　今度はもっと柔らかく、もう一回いいっすか？」
		ELSE
			PRINTFORMW 「緊張してるの、あたいも同じっす。えへへ、ふたりで目ぇ閉じれば怖くないっすよ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 16, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%と脚を重ねると、先輩の硬さが真ん中でよくわかるっす。焦らさず温めますね♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩が跳ねても逃がさないっすよ。あたいと%LOCALS%で、優しくしっかり包みますから♪」
		ELSE
			PRINTFORMW 「今の擦りかた、先輩が好きみたいっす。%LOCALS%、力じゃなくて呼吸を合わせて、もう一度っ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あたいが強く挟みすぎないよう支えるっす。%LOCALS%はそのままゆっくり動いてください♪」
		ELSEIF A == 1
			PRINTFORMW 「おわっ、先輩の腰が急にっ！　にひひ、ちゃんと効いてるなら安心したっす☆」
		ELSE
			PRINTFORMW 「柔らかさなら%LOCALS%に任せて、あたいは温かく包む係っすね。ふたりでちょうどいいっす♪」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：いさみと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 16, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ、%LOCALS%が動くと、あたいの奥にも同じ震えが……♪　身体のなかで抱きあってるみたいっすね」
		ELSEIF A == 1
			PRINTFORMW 「ひぁいっ、急に引いたら奥まで来るっすよ！　……じゃあ次は、あたいからお返しっす♪」
		ELSE
			PRINTFORMW 「%LOCALS%、手ぇ握っていいっすか？　力は入れないから、同じときに感じたら握り返してください♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うわっ、片方の動きがこっちまで来るんすか!?　%LOCALS%、面白いけど油断できないっすね」
		ELSEIF A == 1
			PRINTFORMW 「次はあたいがゆっくり動かすっす。んっ……%LOCALS%の反応、奥からちゃんと伝わったっすよ♪」
		ELSE
			PRINTFORMW 「あはは、ふたり揃って腰が逃げたっすね。今度は抱きあって、もう少し近くで試しましょう♪」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩、慌てなくていいっすよ。あたいが抱いてますから、お腹いっぱいになるまで飲んでください♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩の口が動くたび、胸がじんじん熱くなるっす……。あたいからあげられるものがあるって、嬉しいっすね♪」
		ELSE
			PRINTFORMW 「いつも食べさせる側っすけど、こんなふうに飲ませるのも悪くないっす。えへへ、もっとどうぞ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ほ、本当に飲むんすか？　味は保証できないっすけど……先輩のお口なら、ちゃんと受け止めてほしいっす」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、そこ舐められると乳首が震えて、どんどん出るっす……！　先輩、飲みかた上手すぎません？」
		ELSE
			PRINTFORMW 「こぼれてるっすよ。ほら、あたいがもっと近くに抱き寄せるから、しっかり飲んでください♪」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あたいの胸からこんなに出るんすね……。女らしいところ、先輩がまたひとつ見つけてくれたっす♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩の手、あたいを壊れ物みたいに扱うんすね。そんなに大事にされると、胸より顔が熱くなるっす……♪」
		ELSE
			PRINTFORMW 「胸の張りがほどけるたび、先輩の手に身体を預けてる感じがするっす。もっと力抜いていいっすか？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あたいなら力入れると思ったっすか？　これは勝負じゃないんで、先輩のやりかたに合わせますよ♪」
		ELSEIF A == 1
			PRINTFORMW 「おわっ、思ったより量が多いっすね！　燃費だけじゃなく生産量まで大虎級っすか……あはは」
		ELSE
			PRINTFORMW 「あたいの手じゃ加減が難しいんで、先輩の指先だけ見て真似するっす。もう一度お願いします♪」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこっ、先輩……！　あたい、力抜ける、もっと同じとこぉ……！」
		ELSEIF A == 1
			PRINTFORMW 「んぁっ、奥がまた跳ねるっ……！　先輩の指、好き、止めないでぇ……！」
		ELSE
			PRINTFORMW 「ひゃぁっ、そこばっかり……！　もう、あたい、立ってられないっ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おわっ!?　何すかそこ、身体の芯まで響いたっす！」
		ELSEIF A == 1
			PRINTFORMW 「ま、待って先輩、そこ続けると……んぁっ、膝が勝手に崩れるっす！」
		ELSE
			PRINTFORMW 「痛くないのに力が入らない……！　先輩、もう一回だけ、そこお願いしますっ！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あぁ、全部出ちゃうっす……。先輩の前じゃ、あたいの身体も格好つけられないっすね……♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩が平気な顔で受け止めてくれるなら、あたいも最後まで任せるっす。もう力抜きますね」
		ELSE
			PRINTFORMW 「はふぅ、出し切ったら身体が軽いっす♪　これなら先輩を抱えて帰れそうっすね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うわっ、本当に止まらないっす！　こうなったら腹括って、最後まで堂々といくっすよ」
		ELSEIF A == 1
			PRINTFORMW 「あはは、すごい音っすね。先輩が驚いてるなら、あたいだけ恥ずかしがるのも変っすよね♪」
		ELSE
			PRINTFORMW 「これだけ出るってことは、身体の巡りは絶好調っすね。にひひ、丈夫さには自信あるっす☆」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：いさみと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 16, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の先っぽ、あたいのと擦れて熱いっす……。んっ、胸ごともう少し近くに来てください♪」
		ELSEIF A == 1
			PRINTFORMW 「同じときに震えたっすね、%LOCALS%。えへへ、こうしてると大きさなんて気にならないっす♪」
		ELSE
			PRINTFORMW 「あたいの胸、重かったら言ってくださいね。でも今は、もう少しこのままくっついてたいっす♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひゃっ、先っぽ同士は思ったより敏感っす！　%LOCALS%、次はそっと擦りましょう」
		ELSEIF A == 1
			PRINTFORMW 「あたいが押しすぎたら止めてくださいね。%LOCALS%の力に合わせて、ゆっくり動くっす♪」
		ELSE
			PRINTFORMW 「あはは、ふたりとも照れてるっすね。顔見て笑えたなら、もう恥ずかしくないっす♪」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：いさみはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 16, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、上はお願いするっす……！　あたい、先輩を腰で受け止めて、んぁっ、いちばん奥までぇ……！」
		ELSEIF A == 1
			PRINTFORMW 「先輩、上も忙しいはずなのに、あたいのなかじゃ元気すぎるっす……ひゃぁっ、また深くぅ……！」
		ELSE
			PRINTFORMW 「先輩、%LOCALS%だけじゃなく、あたいの奥ももっと構って……んっ、強くぅ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%が動くと先輩の腰まで揺れて……ふぁっ、あたいの奥に何度も当たるっす！」
		ELSEIF A == 1
			PRINTFORMW 「あたいが上で支えるっす……ひぁいっ！　先輩、下から急に突きあげないでぇ！」
		ELSE
			PRINTFORMW 「あたいの腿で支えてるのに、先輩の腰が止まらない……んぁっ、何度も芯に当たるぅ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：いさみがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩、今日はあたいに甘えていいっすよ。眠るまで、優しく撫でてあげますから♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩の髪、撫でてるとあたいまで落ち着くっす。大事なひとがここにいるって、手のひらでわかるっすね」
		ELSE
			PRINTFORMW 「あたいの膝、丈夫で柔らかいっすよ♪　恋人だけの特等席なんで、好きなだけ使ってください」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「先輩、ちょっと疲れてるっすね。頭こっちに置いて、あたいに世話焼かせてください♪」
		ELSEIF A == 1
			PRINTFORMW 「力仕事の手でも、撫でるときは優しくできるっすよ。ほら、よしよし……どうっすか？」
		ELSE
			PRINTFORMW 「わわっ、撫でたら先輩が大人しくなったっす。にひひ、この顔はあたいだけの秘密にしときますね♪」
		ENDIF
	ENDIF
ENDIF
;=== ISAMI MISSING COMMAND TRIAL END ==='''


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
