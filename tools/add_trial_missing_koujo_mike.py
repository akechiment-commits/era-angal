from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_19_猫塚みけ_COM.ERB")
START = ";=== MIKE MISSING COMMAND TRIAL START ==="
END = ";=== MIKE MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_19"


BLOCK = r''';=== MIKE MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ん、ちゅ……にゃ。先輩の前でほかの子に懐くの、思ったより落ち着かないです……」
		ELSEIF A == 1
			PRINTFORMW 「うにゃ、唇が離れても顔が近いっ……！　先輩、そこでにゃふふって見てないで助けてくださいよ～っ」
		ELSE
			PRINTFORMW 「キスした相手にまでごろごろしたくなるの、猫の癖じゃないですからね？　あたしの癖です♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あたしからいきますよ。ホップ、ステップ……ちゅっ!?　うにゃ、勢いでやるものじゃなかったぁ！」
		ELSEIF A == 1
			PRINTFORMW 「そんな怯えなくても噛みませんって。……たぶん。うにゃ、冗談だから逃げないで～っ！」
		ELSE
			PRINTFORMW 「目ぇ閉じたらボールより距離感わかんない……。もうちょっと近づいて、そこから動かないでね？」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 19, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、レシーブみたいに合図でいきますよっ。先輩の弱いところ、ふたりで拾いますからね♪」
		ELSEIF A == 1
			PRINTFORMW 「うにゃっ、先輩の腰が追いかけてくる……！　ボールじゃないんだから、急に方向変えないでぇ！」
		ELSE
			PRINTFORMW 「先輩を挟んでるのに、%LOCALS%の脚まであったかい。三人って落ち着かないけど……嫌じゃないです」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「せーの、で動くの得意です！　ダブルダッチの要領で……うにゃ、先輩は縄じゃなかった！」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%、そっち逃がした！　あたしが追うから、次はしっかり挟んで～っ」
		ELSE
			PRINTFORMW 「脚がくっつくとじゃれたくなる……って今は真面目にやるんだった。はい、集中っ！」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：みけと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 19, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、逃げると追いかけたくなるから動かないで……んにゃっ、やっぱり動いてぇ！」
		ELSEIF A == 1
			PRINTFORMW 「声が向こうから震えてくる……。姿は見えてるのに、身体のなかで鳴いてるみたい」
		ELSE
			PRINTFORMW 「うにゃ、次に跳ねるまで三つ数えるよ。%LOCALS%、同時に声が出ても笑わないでね？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「片方が動くともう片方も追う……これ、猫じゃらしの気持ちがわかるかもっ」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%、今そっちから来たでしょ!?　不意打ちは反則……ひゃうっ！」
		ELSE
			PRINTFORMW 「あたしがじっとしてれば勝手に戻るかな……。うう、待ち伏せって苦手ぇ！」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩がこんなに近いと、胸が小さいのまで隠せない……うにゃ、笑わないって約束してくださいね？」
		ELSEIF A == 1
			PRINTFORMW 「飲まれるたび、胸よりお腹の奥がきゅっとする……。先輩、あたしの弱いとこ増やさないでぇ」
		ELSE
			PRINTFORMW 「ごろごろ言ってるの、喉じゃなくて胸の音です。先輩が近いから、勝手に鳴るんですよ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにゃ、猫のミルクじゃないですからね？　あたしは人間、これは人間のですっ！」
		ELSEIF A == 1
			PRINTFORMW 「あっ、そんな一気に吸ったら追いつかないです！　ちゃんと一口ずつ、休みながらっ」
		ELSE
			PRINTFORMW 「胸に顔を埋められると逃げ道ない……。でも、先輩の頭なら押し返せるかな。うにゃ、重い～っ」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩の指が来るたび逃げたいのに、胸だけ前に出ちゃう……。あたしの身体、飼い慣らされてません？」
		ELSEIF A == 1
			PRINTFORMW 「搾られてる間、先輩の膝から降りられない……。にゃふふ、今日は捕まっててあげますよ♪」
		ELSE
			PRINTFORMW 「最後の一滴まで欲しいなら、ちゃんと呼んでください。先輩の声なら、もう少し出るかも」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「丸い容器を目の前に置かないでくださいよ～。胸よりそっちに飛びつきそうになるから！」
		ELSEIF A == 1
			PRINTFORMW 「うにゃっ、急に飛んだ！　今のはあたしのせいじゃ……あたしの身体のせいではあるのかぁ」
		ELSE
			PRINTFORMW 「じっとしてるの苦手なんです。先輩、長引くならせめて尻尾……じゃなくて足は動かしていいですか？」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「にゃっ、そこ、だめぇ！　先輩、あたし、すぐ喉鳴っちゃ……んぁっ！」
		ELSEIF A == 1
			PRINTFORMW 「うにゃ、怖いのに腰が逃げない……っ！　先輩、もっと、捕まえててぇ！」
		ELSE
			PRINTFORMW 「せんぱいっ、そこ撫でるのずるい……！　あたし、もう人間の声でないぃっ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「みぎゃっ!?　なに今の、毛ぇ逆立ったぁ！」
		ELSEIF A == 1
			PRINTFORMW 「待って、レシーブ無理っ、奥から全部返ってくるぅ！」
		ELSE
			PRINTFORMW 「うにゃあっ、脚、勝手に丸まるっ！　お腹見せてる場合じゃないのにぃ！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「うにゃ……先輩の前だと、格好悪いとこまで隠せないですね。だったらもう、最後まで捕まってます」
		ELSEIF A == 1
			PRINTFORMW 「恥ずかしいのに、逃げたくない……。先輩の膝、ここだけはあたしの場所にしてて」
		ELSE
			PRINTFORMW 「音が止まるまで、先輩の心臓だけ聞いてます。そっちのほうが大きければ、まだ平気です」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにゃああ、身体が言うこと聞かない～っ！　こういうときの『待て』は誰が教えてくれるの!?」
		ELSEIF A == 1
			PRINTFORMW 「逃げたら余計に広がりそう……。じっとする、あたし今だけ置物の猫になりますっ！」
		ELSE
			PRINTFORMW 「泣いてないです、これはびっくりしただけっ！　終わるまで瞬きしないで耐えてやる～！」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：みけと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 19, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、そんな近くで顔見ないで……。ごろごろ言ったら、胸から伝わっちゃうでしょ」
		ELSEIF A == 1
			PRINTFORMW 「先っぽ同士が擦れるたび、あたしのほうが先に跳ねる……。うにゃ、逃げたら捕まえてね？」
		ELSE
			PRINTFORMW 「胸は小さいけど、%LOCALS%とくっつく場所はちゃんとあるもん。ほら、もう一回♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにゃっ、そこは猫の鼻より敏感なんだから！　%LOCALS%、最初はちょんってだけにして～っ」
		ELSEIF A == 1
			PRINTFORMW 「ふたりとも胸がないなら身軽でいいじゃん……って、%LOCALS%はあたしよりある!?　ずるい～！」
		ELSE
			PRINTFORMW 「じゃれ合うみたいで楽しいと思ったのに、これは笑うと余計に擦れるやつだぁ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：みけはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 19, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、先輩の顔は任せたっ……あたしはここで、んにゃっ、腰が勝手にぃ！」
		ELSEIF A == 1
			PRINTFORMW 「先輩が見えないと怖い……でも、なかで動いてるのはわかるっ、もっとこっちにも返事してぇ！」
		ELSE
			PRINTFORMW 「うにゃあっ、%LOCALS%、先輩の顔の上で揺れないでぇ……！　そのたび下から、あたしもう丸まれないぃ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%の腰が揺れたぶん、先輩の突き上げがこっちへ……！　これ、あたしが全部レシーブするのぉ!?」
		ELSEIF A == 1
			PRINTFORMW 「上に乗ったら有利だと思ったのに、下から突かれたら何もできないぃ！」
		ELSE
			PRINTFORMW 「先輩、顔が塞がってても腰は元気すぎですっ！　うにゃっ、また奥ぅ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：みけがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩の髪、毛繕いしてあげます。終わったらあたしも撫でてもらう、交代制ですよ♪」
		ELSEIF A == 1
			PRINTFORMW 「ごろごろするのは先輩の番です。あたしの膝、ちゃんと気持ちいいって顔してくださいね」
		ELSE
			PRINTFORMW 「撫でてると先輩が大人しくなる……にゃふふ、あたしだけの特技にしていいですか？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「転校生の先輩、頭下げてください。バレー部式、お疲れさまのわしゃわしゃですっ！」
		ELSEIF A == 1
			PRINTFORMW 「うにゃ、髪が丸まってる！　だめ、引っぱらないからちょっと触らせて～っ」
		ELSE
			PRINTFORMW 「先輩って撫でられると目ぇ細くなるんですね。猫じゃないって言い張る気持ち、ちょっとわかったかも♪」
		ENDIF
	ENDIF
ENDIF
;=== MIKE MISSING COMMAND TRIAL END ==='''


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
