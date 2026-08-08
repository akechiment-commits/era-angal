from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_11_氷野くるみ_COM.ERB")
START = ";=== KURUMI MISSING COMMAND TRIAL START ==="
END = ";=== KURUMI MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_11"


BLOCK = r''';=== KURUMI MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ……やわらかくて、甘いキスでした～♪　先輩にもあとで、わたしの唇がどんな味になったか確かめてもらいましょう☆」
		ELSEIF A == 1
			PRINTFORMW 「んっ……ちゅ♪　びっくりしました？　わたし、好きなひとには出し惜しみしない主義なんです～」
		ELSE
			PRINTFORMW 「先輩、そんなに真剣に見つめなくても大丈夫ですよ～？　キスしたぶん、わたしから先輩にもお裾分けしますから♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぇっ、わたしからですか？　ではでは、まずは笑顔でご挨拶して……その次に、ちゅ～っ♪」
		ELSEIF A == 1
			PRINTFORMW 「鼻がぶつかっちゃいました～！　あはは、今度はふたりで反対に傾けて、もう一回やってみましょう☆」
		ELSE
			PRINTFORMW 「緊張してるんですか～？　大丈夫、わたしも初めてみたいにどきどきしてます。お揃いですよ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 11, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、もう少しこっちへ～♪　ふたりの脚で先輩を挟むと、ぴったり重なって気持ちいいですね☆」
		ELSEIF A == 1
			PRINTFORMW 「先輩が熱くなるたび、わたしたちの腿までぽかぽかします～。えへへ、三人で同じ温度ですね♪」
		ELSE
			PRINTFORMW 「今の動き、先輩が好きみたいです！　%LOCALS%、せぇので同じところを、もう一度～♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「右は%LOCALS%、左はわたしが担当します！　息を合わせて、いち、にぃ……わぁ、つるんって動きました～☆」
		ELSEIF A == 1
			PRINTFORMW 「ふたり分の柔らかさなら効果も二倍ですね～？　先輩の顔、さっきよりずっと元気そうです♪」
		ELSE
			PRINTFORMW 「あっ、急に跳ねました！　%LOCALS%、いまの場所を忘れないうちに、もう一往復してみましょう～♪」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：くるみと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 11, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んぅっ、%LOCALS%が揺れるたび、わたしの奥まで響きます～……♪　ちゃんと繋がってるんですね」
		ELSEIF A == 1
			PRINTFORMW 「ひゃぅっ！　そんなに動いたら、わたしからも返しちゃいますよ～？　んっ、えいっ……☆」
		ELSE
			PRINTFORMW 「%LOCALS%、手を貸してください～。腰だけじゃなくて指まで繋いだら、もっと一緒に感じられます♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぇぇ、片方が動くともう片方も勝手に……！　%LOCALS%、これ、ふたりで上手になる道具なんですね～☆」
		ELSEIF A == 1
			PRINTFORMW 「次はわたしがゆっくり動かしますね～。んっ……%LOCALS%の声、こっちまで振動で伝わってきます♪」
		ELSE
			PRINTFORMW 「あはは、ふたりとも同時に腰が逃げちゃいました～！　今度は逃げないように、ぎゅっと抱きあいましょう☆」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩、慌てなくてもたくさんありますよ～♪　わたしが抱っこしてますから、ゆっくり飲んでくださいね」
		ELSEIF A == 1
			PRINTFORMW 「んっ、吸われるたび胸の奥がきゅうってします……。先輩のお腹を満たせるなら、何だか誇らしいです～☆」
		ELSE
			PRINTFORMW 「わたしから出たものを先輩が飲んでくれるって、不思議なくらい嬉しいですね。残さずどうぞ～♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「本当に飲めるんですね～！　お味はどうですか？　健康状態も含めて、詳しい感想をお願いします☆」
		ELSEIF A == 1
			PRINTFORMW 「ふぁっ、そこを舌で押されると勝手に出ちゃいます～。先輩、もう飲みかたを覚えたんですか？」
		ELSE
			PRINTFORMW 「あっ、口の端からこぼれてますよ～？　もったいないですから、もっと深くくわえてください♪」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「一押しごとに、先輩とわたしで作ったぶんが増えていきます～♪　この瓶いっぱい、ふたりの成果ですね☆」
		ELSEIF A == 1
			PRINTFORMW 「先輩が触る前と後で、胸の張りがぜんぜん違います～。恋人効果って、観察記録に書いてもいいですか？」
		ELSE
			PRINTFORMW 「先輩の手のなかで、少しずつ空っぽになっていくの、落ち着きます～。終わったらぎゅっとしてくださいね♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「右と左で勢いが違います～！　右、左、右って交互に押したら、どちらが先に空になるでしょう☆」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、まっすぐ飛びました～！　身体は素直ですけど、狙いをつけるのは難しいですね？」
		ELSE
			PRINTFORMW 「採れた量と回数、あとで記録してもいいですか～？　次は水分量を変えて再実験です☆」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこ、だめ……っ、先輩の指、好きすぎます～！　もっと、同じところっ……！」
		ELSEIF A == 1
			PRINTFORMW 「ひゃぁっ、奥が跳ねて……笑っていられません～っ！　先輩、もう一回……！」
		ELSE
			PRINTFORMW 「せんぱい、せんぱいっ……そこ押されると、わたし、すぐ変になっちゃいます～っ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぇっ、なに今のっ……！　お腹の奥から、びりってきました～っ！」
		ELSEIF A == 1
			PRINTFORMW 「ひゃううっ！　そこだけ反応が違います、先輩っ、もう少しゆっくり～っ！」
		ELSE
			PRINTFORMW 「んぁっ、足に力が入りません～！　でも、その指は離さないでくださいっ……！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あぁ～、ぜんぶ出ちゃいました……！　先輩の前だと、身体まで隠しごとができませんね～♪」
		ELSEIF A == 1
			PRINTFORMW 「ふふ、すごい勢いですね～。先輩が受け止めてくれるなら、最後まで力を抜いちゃいます☆」
		ELSE
			PRINTFORMW 「止まらないものは止まらないです～！　こうなったら先輩、一緒に最後まで見届けてくださいね♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うわぁ、我慢しようとすると余計に出ます～！　身体の仕組みって、思いどおりにはいきませんねぇ」
		ELSEIF A == 1
			PRINTFORMW 「おお～、思ったより長く続きますね！　先輩、わたしの水分補給がばっちりだった証拠ですよ～☆」
		ELSE
			PRINTFORMW 「あはは、こんなに出たらもう笑うしかありません～！　わたし、最後まで堂々としてますね♪」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：くるみと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 11, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の先っぽ、わたしのとぴったり重なります～♪　んっ、同じところが一緒に熱くなりますね」
		ELSEIF A == 1
			PRINTFORMW 「もう少し強く押しても大丈夫ですよ～。ふぁっ、そうそう……ふたりの胸がひとつみたいです☆」
		ELSE
			PRINTFORMW 「%LOCALS%が笑うと、胸まで震えてくすぐったいです～♪　わたしも笑ったら、お返しになりますか？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふぇっ、先っぽ同士ってこんなに敏感なんですか～！　%LOCALS%、もう一度そっと擦ってみましょう☆」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%の胸、あったかいですね～♪　押したり離したりすると、ちくちくがだんだん気持ちよくなります」
		ELSE
			PRINTFORMW 「恥ずかしくなったら顔を見てください～。ほら、ふたりでやると何だか楽しいでしょう？」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：くるみはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 11, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、先輩のお顔はお願いします～！　わたしはこっちで……ひゃぁっ、奥まで来ましたっ！」
		ELSEIF A == 1
			PRINTFORMW 「先輩の顔が見えなくても、なかで全部わかります～っ！　んぁっ、そんなに突きあげたら……！」
		ELSE
			PRINTFORMW 「上下からふたりがかりですね～♪　あっ、先輩っ、わたしの奥でも元気になってます～っ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%が動くたび先輩の腰まで……ひゃうっ！　わたしのなか、急に深くなりました～っ！」
		ELSEIF A == 1
			PRINTFORMW 「わたしが上で動きますね～。んっ、先輩、下から別の動きを足すのは反則です～っ！」
		ELSE
			PRINTFORMW 「ふぇぇ、奥を何度もこすられて……！　%LOCALS%、先輩のお顔で何をしたんですか～っ？」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：くるみがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「今日もいっぱい頑張りましたね、先輩♪　わたしの膝で、頭の力までぜ～んぶ抜いてください」
		ELSEIF A == 1
			PRINTFORMW 「よしよし～☆　先輩が元気になるまで、何時間でも撫でますよ。こういうお世話なら大得意です♪」
		ELSE
			PRINTFORMW 「先輩の髪、撫でるたび指に馴染みますね～。えへへ、好きなひとの頭って愛おしいです♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「はい、保健委員式の休憩です～。目を閉じて、わたしに頭を預けてくださいね♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩にも撫でられると眠くなる場所があるんでしょうか～？　このへんかな、よしよし☆」
		ELSE
			PRINTFORMW 「笑顔が足りないときは、頭から補給です～♪　なでなで、にこにこ、元気にな～れ！」
		ENDIF
	ENDIF
ENDIF
;=== KURUMI MISSING COMMAND TRIAL END ==='''


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
