from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_13_羽森つばさ_COM.ERB")
START = ";=== TSUBASA MISSING COMMAND TRIAL START ==="
END = ";=== TSUBASA MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_13"


BLOCK = r''';=== TSUBASA MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ、ちゅ……♪　ふふ、転校生殿には刺激が強かった？　あたしの唇、あとでちゃんと取り返しに来てね」
		ELSEIF A == 1
			PRINTFORMW 「女の子とのキスも絵になりますな～☆　でもこれはファンサじゃなくて、あたしがしたかっただけ」
		ELSE
			PRINTFORMW 「ちゅ……はい、敬礼～☆　任務完了っ。次は恋人の転校生殿に、もっと長いのをお願いしようかな♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ほほう、あたしから？　ではカメラなしの一回きり……んっ、ちゅ♪」
		ELSEIF A == 1
			PRINTFORMW 「あっ、同時に笑ったら唇ずれちゃった。あはは、こういう失敗ならもう一回できるね？」
		ELSE
			PRINTFORMW 「緊張してる？　あたし、舞台じゃないときのほうが優しいからさ。ほら、目ぇ閉じて♪」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 13, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、そのテンポで合わせて♪　転校生殿の熱、ふたりの腿の間でどんどん上がってるよ」
		ELSEIF A == 1
			PRINTFORMW 「転校生殿、どっちの脚が気持ちいいかなんて聞かないよ？　二人分まとめて好きにさせちゃうから☆」
		ELSE
			PRINTFORMW 「ほら、%LOCALS%と息がぴったり♪　転校生殿の反応まで、あたしたちの振り付けどおりだね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「自分が右舷、%LOCALS%が左舷を担当！　挟み込み作戦、開始であります～☆」
		ELSEIF A == 1
			PRINTFORMW 「わ、転校生殿の腰が跳ねた。今の気に入ったんだ？　%LOCALS%、もう一回同じリズムでいこう♪」
		ELSE
			PRINTFORMW 「二人分の脚って、思ったより隙間ないね～。転校生殿、顔に出てるよ。あはは♪」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：つばさと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 13, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ、%LOCALS%が動くと、あたしの奥も同じだけ揺れる……♪　これ、離れてるのに抱きあってるみたい」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、いいところ突いたね……！　じゃあ次はあたしから、%LOCALS%の奥へお返しっ☆」
		ELSE
			PRINTFORMW 「%LOCALS%、こっち見て。声も腰も同じ瞬間に揺れると、ひとりよりずっと気持ちいいよ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぁっ、片方の振動がこっちまで来た！　双方向通信、感度良好でありますっ……☆」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%、一回ずつ交代で動こう？　んっ……あはは、今のはふたり同時だったね」
		ELSE
			PRINTFORMW 「そんな真剣な顔しなくてもいいって。ほら、力抜いて……あっ、今の揺れ、すごくよかった♪」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生殿、そんな無防備な顔で飲むんだ……。ふふ、今のあたしだけが見られる限定映像だね♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ、吸うたび胸の奥まで熱くなる……。あたしのぶん、最後までちゃんと受け取ってね」
		ELSE
			PRINTFORMW 「おいで、転校生殿。今日はあたしが抱きしめる側だから、遠慮せずいっぱい甘えていいよ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ほ、本当に飲むの？　あたしも初めてなんだから、味の評価はお手柔らかにお願いしますっ」
		ELSEIF A == 1
			PRINTFORMW 「ふぁっ、舌使い上手すぎ……！　転校生殿、飲むよりあたしを感じさせる気でしょ？」
		ELSE
			PRINTFORMW 「は！　栄養補給の時間であります☆　……なんてね。こぼさないよう、もっと近くにおいで？」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生殿、一定のテンポを崩さないの上手いね……んっ。あたしまで呼吸合わせちゃう♪」
		ELSEIF A == 1
			PRINTFORMW 「わっ、すごい勢い♪　照明があったらきらきらして、変なところで映えそうだね」
		ELSE
			PRINTFORMW 「転校生殿が受け取ってくれるなら、これもあたしだけの差し入れってことで。味見の感想はあとでね♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「量は少なくても、集めればちゃんと一杯になるんだね。転校生殿、こぼしたらスタッフ失格だよ？」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、顔に飛んだ！　あはは、ごめん。これは放送事故じゃなくて完全にあたしの勝ち☆」
		ELSE
			PRINTFORMW 「搾られてる側は手持ち無沙汰ですな。転校生殿、終わるまで即興トークの相手を頼むよ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこっ、転校生殿……！　だめ、あたし、声ぜんぜん抑えられないっ……！」
		ELSEIF A == 1
			PRINTFORMW 「んぁっ、奥がまた跳ねるっ……！　好き、もっと、その指でぇ……！」
		ELSE
			PRINTFORMW 「転校生殿、そこばっかり……ひゃぁっ！　もう、立ってられないぃ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぁあっ!?　なに今の、身体の奥に直接きたっ……！」
		ELSEIF A == 1
			PRINTFORMW 「待って、そこ反則……んぁっ！　転校生殿、同じとこ続けないでっ……！」
		ELSE
			PRINTFORMW 「ひゃっ、脚が震える……！　任務続行、でも少しだけゆっくりぃ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あぁ、止まらない……。転校生殿の前じゃ、アイドルの顔も身体の秘密も丸裸だね……♪」
		ELSEIF A == 1
			PRINTFORMW 「ふふ、そんな優しい顔で見られたら、恥ずかしがるのも馬鹿らしくなるなぁ。最後まで受け止めてね」
		ELSE
			PRINTFORMW 「全部出たら、身体すっごく軽い……！　転校生殿だけの特別公開ってことで、感想は胸にしまっといて♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うわっ、本当に出た!?　こ、これは予定外だけど……こうなったら堂々と最後までいくから！」
		ELSEIF A == 1
			PRINTFORMW 「あはは、この音だけはライブじゃ聞かせられないな～。転校生殿だけのアンコールってことで♪」
		ELSE
			PRINTFORMW 「は！　緊急放水、止められませんっ☆　見届け役は転校生殿に一任するであります！」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：つばさと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 13, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の先っぽ、あたしのと擦れるたび熱くなる……。んっ、もっと胸ごと押しつけて♪」
		ELSEIF A == 1
			PRINTFORMW 「同じ瞬間に震えたね、%LOCALS%。ふふ、呼吸まで揃うとデュエットみたいで気持ちいい♪」
		ELSE
			PRINTFORMW 「離れるのはまだ早いよ。%LOCALS%の胸の鼓動、もう少し近くで感じさせて？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひゃっ、先っぽ同士は予想以上……！　%LOCALS%、次はゆっくり合わせてみよう？」
		ELSEIF A == 1
			PRINTFORMW 「あたしが押したら、%LOCALS%も押し返してね。胸と胸のフォーメーション、開始であります☆」
		ELSE
			PRINTFORMW 「あはは、ふたりとも同じ顔してる。恥ずかしさまでお揃いなら、もう笑って楽しもうよ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：つばさはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 13, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、転校生殿のお顔は任せた……！　あたしはここで、んぁっ、奥まで突かれてるぅ……！」
		ELSEIF A == 1
			PRINTFORMW 「顔が見えなくても、なかの転校生殿は元気すぎ……ひゃぁっ！　もっと、下から来てぇ……！」
		ELSE
			PRINTFORMW 「転校生殿、%LOCALS%ばっかり構わないで……んっ！　あたしの奥でも、もっと暴れてっ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%が動くと転校生殿の腰まで揺れて……ふぁっ、奥に何度も当たるっ！」
		ELSEIF A == 1
			PRINTFORMW 「あたしが上を担当します……って、ひゃぁっ！　転校生殿、下からの追撃は聞いてないっ！」
		ELSE
			PRINTFORMW 「上下同時でも鈍らないんだ……んぁっ、あたしのなか、ずっと深く突かれてるぅ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：つばさがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「お疲れさま、転校生殿。今だけはあたしの膝で、誰の期待にも応えなくていいからね……よしよし♪」
		ELSEIF A == 1
			PRINTFORMW 「転校生殿の髪、撫でてるとあたしまで落ち着くなぁ。ふたりだけの休演時間、もう少し延長しよっか？」
		ELSE
			PRINTFORMW 「本日の最前列はあたしのお膝です♪　恋人だけの特典だから、眠るまで好きに甘えてね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「は！　転校生殿の休養を確認。自分が責任を持って、頭から力を抜かせるであります～☆」
		ELSEIF A == 1
			PRINTFORMW 「癖のない髪って撫でやすいね～。あたしの跳ねた前髪と交換してほしいくらい。よしよし♪」
		ELSE
			PRINTFORMW 「あはは、撫でたら急に大人しくなった。こういう転校生殿は、あたしだけの特等席から眺めとくね」
		ENDIF
	ENDIF
ENDIF
;=== TSUBASA MISSING COMMAND TRIAL END ==='''


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
