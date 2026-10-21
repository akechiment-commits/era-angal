from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_46_双葉みづき_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR46_before_additional10_20260822" / TARGET.name


ADDITIONAL = r''';--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	CALL AITE_YOBI, 46, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%とキスしてるところ、わたしに見せつける気かよ……っ。ふふん、そういう儀式なら最後まで見届けてやるぞ☆」
		ELSEIF A == 1
			PRINTFORMW 「ちゅ……っ、近い近い！　転校生、そんな顔で見るなよ。わたしまで変な魔力に巻き込まれるだろ……♪」
		ELSE
			PRINTFORMW 「もう一回って、%LOCALS%に頼むのか？　……べつに止めないけど、終わったらわたしのところへ戻ってこいよ☆」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おわっ、%LOCALS%にいきなり!?　な、なんだその実験、わたしを立会人にするなよ～っ！」
		ELSEIF A == 1
			PRINTFORMW 「ん……っ、見てるだけなのに変な感じだぞ。転校生、こっちを試験管みたいに観察するな～っ」
		ELSE
			PRINTFORMW 「%LOCALS%、顔が真っ赤じゃんか。……その、嫌じゃないなら続けてもいいけど、わたしは知らないからな☆」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 46, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%と息が重なるたび、転校生の反応が跳ね返ってくる……っ。ふふ、三人分の魔力、受け止めてみろよ♪」
		ELSEIF A == 1
			PRINTFORMW 「ん、そこ……っ、%LOCALS%と動きがずれると余計に変になるだろ。わたしのほう見て、ちゃんとついてこい……☆」
		ELSE
			PRINTFORMW 「あはっ、そんな顔するんだな。わたしまで意地悪したくなる……っ、まだ逃げるなよ、使い魔♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ、二人がかりって聞いてないぞ～っ！　%LOCALS%、急に合わせるな、こっちまで変な声が出るだろ！」
		ELSEIF A == 1
			PRINTFORMW 「ちょ、ちょっと待て……っ、熱がぶつかって、頭が追いつかない。転校生、わたしを巻き込むなよ～っ」
		ELSE
			PRINTFORMW 「ふ、ふふん……まだ平気だぞ。%LOCALS%も、わたしの合図を聞け。……って、聞けって言ってるのにっ！」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
	CALL AITE_YOBI, 46, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の震えが、そのままわたしの奥へ返ってくる……っ。ひとつの術式みたいで、離れるほうが惜しいぞ♪」
		ELSEIF A == 1
			PRINTFORMW 「あっ……%LOCALS%、そこまで動いたら、わたしまで力抜ける……っ。顔を見るな、いまのは魔力の暴走だ☆」
		ELSE
			PRINTFORMW 「ん、んぅ……っ、同じ振動でつながってるの、ずるいな。%LOCALS%が乱れると、わたしも隠せなくなる……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「わひゃっ……これ、%LOCALS%が動くとこっちにも来るのか!?　な、なかなか厄介な呪具だぞ～っ！」
		ELSEIF A == 1
			PRINTFORMW 「待て、急に強くするなっ……ひぃっ、同じところまで震える。%LOCALS%、わたしの顔を見るな～っ！」
		ELSE
			PRINTFORMW 「ふふん、女同士なら平気だと思ったのに……っ。%LOCALS%、手、握ってろよ。ちょっとだけ、頭がくらくらする」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ん……そんなに夢中になるなよ。わたしの胸に魔力があるみたいで、変に嬉しくなるだろ……♪」
		ELSEIF A == 1
			PRINTFORMW 「ふふ、飲む音まで聞こえる……。転校生、甘えすぎだぞ。……でも、離れろとは言わない☆」
		ELSE
			PRINTFORMW 「まだ欲しいのか？　まったく、使い魔は欲深いな……っ。わたしが許すまで、ゆっくりしてろよ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、わたしの胸から!?　ち、違うぞ、これは神秘の調査で……って、もう飲んでるじゃんか～っ！」
		ELSEIF A == 1
			PRINTFORMW 「ひぃっ、そんな顔で見上げるなよ……っ。わたしだって、どこ見ればいいかわからなくなるだろ！」
		ELSE
			PRINTFORMW 「ん……っ、急に吸うな、びっくりする。……でも、そんなに嬉しそうにするなよ、断れなくなるじゃんか☆」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこ、そう……っ。おまえの手つき、もう覚えちゃったんだな。わたしの反応まで見抜くなよ、恥ずかしいだろ♪」
		ELSEIF A == 1
			PRINTFORMW 「あ……っ、急に強くするな。そんなに欲しそうな顔をされると、わたしまで意地悪したくなるぞ☆」
		ELSE
			PRINTFORMW 「ふふん、ちゃんとわたしを扱えてるじゃん。……褒めてやるから、そのままもう少し続けろ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おわっ、搾るってそういう意味か!?　転校生、わたしを実験動物みたいに見るな～っ！」
		ELSEIF A == 1
			PRINTFORMW 「あっ、そこは強いっ……。わ、わたしの顔を見ながら加減するなよ、余計に何も言えなくなるだろ！」
		ELSE
			PRINTFORMW 「そんなに一生懸命になるなって……っ。べつに、少しくらいなら、付き合ってやるけどさ☆」
		ENDIF
	ENDIF
ENDIF

;--- COM84 クリ刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「っ、そこ……っ、わたしが隠してた場所、もう見つけたのかよ。転校生、そんな得意そうな顔するな……でも、止めるな♪」
		ELSEIF A == 1
			PRINTFORMW 「ん、んぅっ……指が触れるたび、背中までぞくっとする。わたしの魔力、ぜんぶおまえに持っていかれそうだぞ……☆」
		ELSE
			PRINTFORMW 「あ、ぁ……っ、声、変になる……っ。ふふんって笑う余裕、もう残ってない。だから、ちゃんと最後まで責任取れよ……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「んぎょっ!?　そこ、何を探してるんだよっ！　わたしの弱点を呪具みたいに扱うな～っ！」
		ELSEIF A == 1
			PRINTFORMW 「ひ、ひぃっ……っ、触るたびに息が止まる。転校生、わたしの顔見て笑うなよ、ほんとに……っ」
		ELSE
			PRINTFORMW 「わ、わたしは平気……っ、平気だぞ。……うそ、もう少しだけ、ゆっくりなら……その、続けてもいい」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あ……っ、止まらない……。おまえに見られてるのに、力が抜ける。笑うなよ、これは信頼の証なんだからな……♪」
		ELSEIF A == 1
			PRINTFORMW 「や、だ……っ、こんな音まで聞かせるなよ……。転校生、目を逸らすなとは言わないけど、手だけは離すな……っ」
		ELSE
			PRINTFORMW 「ひぃっ……もう、わたしの意志じゃ止められない。呪うぞ……って言いたいのに、声が震えて言えないじゃんか……☆」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「な、何してるんだよ!?　待て、これは儀式じゃない、事故だぞ！　見るな、いや、見ても笑うな～っ！」
		ELSEIF A == 1
			PRINTFORMW 「ひぃっ……っ、やだ、止まらないっ。転校生、そんなにじっと見るなよ……っ、わたし、呪うからな……！」
		ELSE
			PRINTFORMW 「うぅ……最悪だ。こんなの、みなちゃんにも知られたら終わりだぞ……。だから、今のは忘れろ、絶対だ！」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
	CALL AITE_YOBI, 46, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の胸、あったかい……っ。こうして触れ合ってると、ふたり分の鼓動がひとつの術式みたいに重なるな♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ……%LOCALS%、そんなに押しつけるなよ。……いや、離れろじゃなくて、その、もう少しだけこのまま☆」
		ELSE
			PRINTFORMW 「ひゃっ、そこが擦れると……っ、わたしまで素直になるだろ。%LOCALS%、いまの顔は見ないでくれ……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、胸を合わせるのか!?　%LOCALS%、近いって……っ。わたし、こういう呪術は専門外だぞ～っ！」
		ELSEIF A == 1
			PRINTFORMW 「わひゃっ……いきなり押すなよ。%LOCALS%の鼓動まで聞こえると、こっちまで落ち着かなくなるじゃんか！」
		ELSE
			PRINTFORMW 「ふ、ふふん……女同士なら平気、平気だぞ。……でも%LOCALS%、ちょっとだけゆっくりにしてくれ」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
	CALL AITE_YOBI, 46, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「わたしが転校生に跨がって、%LOCALS%は顔の上……っ。ふふ、二方向から攻めるなんて、ずいぶん贅沢な儀式だな♪」
		ELSEIF A == 1
			PRINTFORMW 「ん、揺れる……っ。下からも顔のほうからも来ると、わたし、どっちに合わせればいいんだよ……っ☆」
		ELSE
			PRINTFORMW 「%LOCALS%ばっかり見てると、わたしが拗ねるぞ。ちゃんとこっちも感じてるって、顔を上げて確かめろ……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おわっ、わたしが乗るのか!?　しかも%LOCALS%まで顔の上って、転校生、何の召喚陣を開いたんだよ～っ！」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ……下で動くな、%LOCALS%も急に来るなっ。わたし、落ちる……いや、落ちないけど頭が追いつかない！」
		ELSE
			PRINTFORMW 「ふ、ふふん、わたしが主導権を握るぞ。……って、二人とも好きにするなよっ、これじゃわたしまで乱れるだろ～っ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ほら、今日はよく頑張ったな。わたしが撫でてやるから、転校生は黙って甘えてろ♪」
		ELSEIF A == 1
			PRINTFORMW 「そんなに目を閉じるなら、もう少し続けてやる。……ふふん、わたしの手は特別製だからな☆」
		ELSE
			PRINTFORMW 「みなちゃんを守るのはわたしの役目だけど、おまえが疲れたときくらいは、わたしがそばにいるぞ。ほら、頭を上げるな♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「転校生、今日は顔が死んでるぞ。ほら、わたしが撫でてやるから、少しくらい力を抜けよ」
		ELSEIF A == 1
			PRINTFORMW 「おわっ、素直に預けてくるのか……。べつに嫌じゃないけど、変な期待をするなよ？　ゆっくりしてろ☆」
		ELSE
			PRINTFORMW 「話したくないなら、今は話さなくていいぞ。わたしが聞くから……って、寝るなよ、最後まで撫でてやるんだからな」
		ENDIF
	ENDIF
ENDIF
'''


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    marker = "\n@TRAIN_MESSAGE_B280_46"
    if marker not in text:
        raise SystemExit("insertion marker not found")
    if ";--- COM60 助手にキスさせる ---" in text:
        raise SystemExit("CHAR46 additional block already exists")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        BACKUP.write_bytes(raw)
    text = text.replace(marker, "\n" + ADDITIONAL + marker, 1)
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
