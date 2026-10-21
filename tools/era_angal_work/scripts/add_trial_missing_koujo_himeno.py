from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_18_熊沢ひめの_COM.ERB")
START = ";=== HIMENO MISSING COMMAND TRIAL START ==="
END = ";=== HIMENO MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_18"


BLOCK = r''';=== HIMENO MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んぅ……♪　キスって力加減を考えなくていいから、好きだなあ。唇だけなら誰も壊れないもんねえ」
		ELSEIF A == 1
			PRINTFORMW 「ちゅ……ん。離れたあとも顔が近いままだねえ。えへへ、この子も照れてるみたいだよお♪」
		ELSE
			PRINTFORMW 「先輩、そんなに目を丸くしなくてもお。わたしだって、やさしいキスぐらいできますよお♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「唇なら、ぎゅっとしないほうがいいんだよねえ？　それじゃあ、そおっと……ちゅ♪」
		ELSEIF A == 1
			PRINTFORMW 「あれえ、わたしより相手の子のほうが固まってるう。大丈夫、噛んだりしないよお？」
		ELSE
			PRINTFORMW 「てへ、ぺろっ……は、キスのあとだと紛らわしいかなあ。普通に笑っとくねえ、えへへ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 18, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、わたしの腿には力を入れないからあ、先輩を真ん中で迷子にしないよう寄っててねえ♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩の腰、わたしたちの間で忙しそうだねえ。ふふふ、急がなくても逃げませんよお♪」
		ELSE
			PRINTFORMW 「わたしが支えるから、%LOCALS%は動くほうをお願いねえ。役割分担すると安心だなあ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃあ、ちょっと挟んだだけで先輩が潰れそうな顔してるう!?　力、もっと抜きますねえ！」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%と脚の速さが違うねえ。わたし、のんびり合わせるから先に動いていいよお♪」
		ELSE
			PRINTFORMW 「ふたりでやると力が半分で済むんだねえ。これはわたし向きかもしれないなあ、えへへ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：ひめのと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 18, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、好きなときに動いていいよお。わたしはゆっくり受け取るから……ひゃあ、ちゃんと届いたあ♪」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%の声が震えると、わたしまで守ってあげたくなるねえ。んっ……動けないから、名前を呼ぶねえ」
		ELSE
			PRINTFORMW 「これなら抱きつかなくても、%LOCALS%を近くに感じるねえ……ふふふ、変なのお♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「わたしが動くと、そっちまで強くなっちゃうのお？　じゃあ今日は、のんびりが正解だねえ」
		ELSEIF A == 1
			PRINTFORMW 「うひゃあっ、%LOCALS%が跳ねたらわたしまで……！　ごめんねえ、今のはわたしじゃないよお!?」
		ELSE
			PRINTFORMW 「力加減より、動かない加減のほうが難しいなあ。%LOCALS%、いったん休もお？」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩の頬、わたしの胸にぴったり収まるねえ。小さいのも、今日は悪くないかなあ♪」
		ELSEIF A == 1
			PRINTFORMW 「んぅっ、そんなに強く吸ったら、乳首がすぐ固くなっちゃうよお……ゆっくり飲んでえ」
		ELSE
			PRINTFORMW 「七夕セブンからの元気のお届けですう♪　飲み終わったら、先輩のお願いもひとつ聞くねえ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あれえ、出る場所が小さいと飲みにくいかなあ？　顔、もっと近くにしていいですよお」
		ELSEIF A == 1
			PRINTFORMW 「うひゃあっ、舌が当たるたび力が入っちゃう！　先輩を抱き潰す前に、腕は後ろに置いとくねえ」
		ELSE
			PRINTFORMW 「飲んでる顔って、こんなに静かなんだねえ。ふふふ、ちょっと眠そうでかわいいなあ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「わたしの身体なのに、先輩の手のほうが言うことを聞かせるの上手だねえ……ちょっと悔しいなあ♪」
		ELSEIF A == 1
			PRINTFORMW 「こんな小さなところに、まだ残ってたんだねえ。先輩の手って、隠しものを見つけるの得意だなあ」
		ELSE
			PRINTFORMW 「搾られてると、抱きしめる側じゃなくて抱かれてる気分になるのお。先輩、後ろから支えててねえ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あれえ、わたしが瓶を持ったら割っちゃいそうだねえ。先輩、そっちは任せましたよお♪」
		ELSEIF A == 1
			PRINTFORMW 「胸より先に、握ってるシーツが破れそう……。うひゃあ、手をどこに置けばいいのお？」
		ELSE
			PRINTFORMW 「出たぶんだけ軽くなるはずなのに、乳首はどんどん重たく感じるよお。不思議だねえ」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこおっ……先輩、わたし、力が……！　抱いたら壊しちゃう、手ぇ押さえててぇ！」
		ELSEIF A == 1
			PRINTFORMW 「んぁっ、もう、のんびりできないよお……！　もっと、早く、そこぉっ！」
		ELSE
			PRINTFORMW 「先輩、目ぇ開いちゃう……っ！　怖い顔でも逃げないで、そこ、続けてぇ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃあっ、そこ何ぃ!?　おまんこ、勝手にぎゅってなるよおっ！」
		ELSEIF A == 1
			PRINTFORMW 「だめ、シーツ破れちゃう……っ！　でも手を離したら、先輩を掴んじゃうう！」
		ELSE
			PRINTFORMW 「待ってえ、身体のなかから押し返されるうっ！　わたし、どうすればいいのお!?」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩の前でまで我慢しなくていいって、身体が勝手に決めちゃったみたいだねえ……えへへ」
		ELSEIF A == 1
			PRINTFORMW 「止めようとすると、またどこか壊しそうで……。今日は力を抜くほうを、先輩に手伝ってほしいなあ」
		ELSE
			PRINTFORMW 「全部終わるまで、わたしの手だけ握っててえ。今なら壊さないくらい、弱く握れそうだからあ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あれえ、床がどんどん遠く見える……。目ぇ開けてるのに、恥ずかしくて何も見えないよお」
		ELSEIF A == 1
			PRINTFORMW 「わたしの力でも、出るものは止められないんだねえ。うう、初めて自分より強いもの見つけたあ」
		ELSE
			PRINTFORMW 「うひゃあ、勢いにびっくりして目ぇ開いちゃった！　先輩まで怖い顔しないでよお、わたしも驚いてるんだからあ」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：ひめのと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 18, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の胸に隠れちゃいそうだねえ、わたしの。でも先っぽはちゃんと見つけてもらえたあ♪」
		ELSEIF A == 1
			PRINTFORMW 「んぅっ、重ねたまま抱きつきたい……。%LOCALS%、強くしないから腕まわしていいかなあ？」
		ELSE
			PRINTFORMW 「同じところが熱くなると、どっちの鼓動かわからないねえ。ふふふ、どっちでもいいかあ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃあ、ちょんってしただけで乳首がびりびりするう！　%LOCALS%、わたしここ弱いみたいだよお」
		ELSEIF A == 1
			PRINTFORMW 「押し返したら強すぎるよねえ。わたしはじっとしてるから、%LOCALS%の好きな速さでどうぞお」
		ELSE
			PRINTFORMW 「胸は小さくても、近づくのに邪魔がなくて便利だねえ。えへへ、負け惜しみじゃないよお？」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：ひめのはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 18, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、先輩のお顔にしっかり座っててねえ。わたしは潰さないように、んぁっ、腰だけ動かすからあ！」
		ELSEIF A == 1
			PRINTFORMW 「先輩、顔が見えなくても力は抜いてますよお……ひゃあっ、下からそんなに突かないでぇ！」
		ELSE
			PRINTFORMW 「先輩の顔の上で%LOCALS%がもぞっとしたら、先輩のが奥にっ……！　わたし、抱きしめるものがないと壊れちゃうう！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「わたしが上で支えたら安定するはずなのにい……うひゃっ、先輩の腰のほうが強いよお！」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%、急に動いたらだめえ！　先輩が跳ねて、わたしのなかまでびっくりするうっ！」
		ELSE
			PRINTFORMW 「下半身だけ全力って難しいなあ……んぁっ、先輩、わたしの腿を押さえててぇ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：ひめのがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩、今日はわたしが撫で撫でする番ですよお。痛かったら三回叩いて教えてねえ？」
		ELSEIF A == 1
			PRINTFORMW 「髪って、力を入れなくても指の間を通ってくれるんだねえ。こういう触りかた、わたし好きだなあ♪」
		ELSE
			PRINTFORMW 「眠ったら抱っこして運んであげますねえ。起きたときも、わたしの膝だから安心してえ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「お礼に頭を撫で撫でしてあげますねえ。照れなくていいのに、先輩ってシャイだなあ♪」
		ELSEIF A == 1
			PRINTFORMW 「うひゃ、髪が一本ひっかかった！　ごめんなさあい、今度は指先だけでそおっとするねえ」
		ELSE
			PRINTFORMW 「肩揉みは怖がられるから、今日は頭だけにしましたあ。これなら気持ちいいでしょう？」
		ENDIF
	ENDIF
ENDIF
;=== HIMENO MISSING COMMAND TRIAL END ==='''


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
