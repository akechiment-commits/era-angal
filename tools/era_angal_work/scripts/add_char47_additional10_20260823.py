from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR47_before_additional10_20260823" / TARGET.name


ADDITIONAL = r''';--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	CALL AITE_YOBI, 47, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%にキスしてるところ、転校生くんに見せちゃうね♪　ふふ、今日はお姉さんの余裕を見せる日だから」
		ELSEIF A == 1
			PRINTFORMW 「ん……ちゅ。%LOCALS%の唇、やわらかいね。転校生くん、そんな顔をするなら、もっと近くで見ていてよ♪」
		ELSE
			PRINTFORMW 「もう一度？　いいよ、%LOCALS%。でも終わったら、ちゃんと転校生くんのところへ戻るからね……ふふ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、わたしが%LOCALS%にするの？　転校生くんが見てるのに……お、お姉さんだから平気だけどねっ」
		ELSEIF A == 1
			PRINTFORMW 「ちゅ……っ。あ、あれ、思ったより緊張するなぁ。転校生くん、そんなにじっと見ないでよ～」
		ELSE
			PRINTFORMW 「%LOCALS%、嫌じゃないなら、もう少しだけ……。転校生くんには、ちゃんと見届けてもらうんだからね」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 47, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%と一緒に、転校生くんを挟むの……。ふふ、どっちのほうが夢中にさせられるか、競争してみよっか♪」
		ELSEIF A == 1
			PRINTFORMW 「あっ……%LOCALS%、動きが重なると、わたしまで熱くなるよ。転校生くん、まだ余裕なんて顔しないでね？」
		ELSE
			PRINTFORMW 「ん、んぅ……っ、そんなに揺れたら、わたしのほうが先に負けちゃう。%LOCALS%、もう少しだけ合わせて……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃあっ!?　二人でって、そんなの聞いてないよ～っ！　%LOCALS%、急に近づかないで、びっくりするから！」
		ELSEIF A == 1
			PRINTFORMW 「あ、あのね……っ、二人分の熱が返ってくると、どうしたらいいのかな。転校生くん、わたしまで困らせないでよぉ」
		ELSE
			PRINTFORMW 「ふふ～ん、まだ平気だよ？　%LOCALS%も、わたしが合図するまでゆっくりね。……あっ、もう、息が合いすぎだよ～っ」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
	CALL AITE_YOBI, 47, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の動きが、こっちまで返ってくる……。ふたりで同じ熱を分け合うの、思ってたよりずっと近いね♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ……%LOCALS%、いま動いた？　また来たよ、わたしの中まで……。顔、見ないでね、変になっちゃうから」
		ELSE
			PRINTFORMW 「ひゃわわわっ……っ、同じ震えでつながってるの、ずるいなぁ。%LOCALS%が乱れると、わたしまで隠せなくなるよ……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにっ……いまの、%LOCALS%から返ってきたの？　同じところが震えるなんて、変な呪具だねぇ……っ」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、急に強くしないでよぉ……っ。%LOCALS%、わたしまで力が抜けちゃうから、手を握ってて」
		ELSE
			PRINTFORMW 「女の子同士なら平気かなって思ったのに……。ふふ、全然平気じゃないね。%LOCALS%、もう少しゆっくりにしよ？」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ん……そんなに夢中になってくれるんだね。胸に自信はないけど、転校生くんが嬉しそうなら、もう少しあげる♪」
		ELSEIF A == 1
			PRINTFORMW 「ふふ、甘えんぼさんだなぁ。飲んでる顔を見てると、わたしまでお姉さんになった気分……えへへ♪」
		ELSE
			PRINTFORMW 「まだ離れなくていいよ。わたしのこと、ちゃんと欲しがってくれてるの、少し嬉しいから……ゆっくりね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、わたしの胸から飲むの？　あんまり期待されても困るよぉ……って、もう始めてるし！」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ……そんなに見上げないでよ。貧相なの、知ってるでしょ？　……でも、嫌とは言ってないからね」
		ELSE
			PRINTFORMW 「ん……っ、急に吸うとびっくりするよぉ。そんなに嬉しそうにされたら、止めてって言えなくなるじゃん……」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこを、そうやって……。ふふ、転校生くんの手、ずいぶん慣れたね。わたしの反応まで覚えないでよ、恥ずかしいなぁ♪」
		ELSEIF A == 1
			PRINTFORMW 「あっ……もう少しやさしくね。小さいからって、乱暴に扱ったら、お姉さんでも拗ねちゃうよ？」
		ELSE
			PRINTFORMW 「出てくるところ、そんなに嬉しそうに見るんだ……。ふふ、じゃあ今日は、転校生くんの好きなだけ付き合ってあげる♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにっ!?　搾るって、手でそうするの!?　転校生くん、わたしを何かの実験みたいに見ないでよ～っ！」
		ELSEIF A == 1
			PRINTFORMW 「あっ、そこは強いよぉ……っ。わたし、胸は大きくないんだから、そんなに一生懸命にならなくても……」
		ELSE
			PRINTFORMW 「んもう、まだ続けるの？　……少しだけならいいけど、数字を数えたりはしないでね。変に恥ずかしいから」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこ……っ、転校生くん、もう見つけたの？　わたしの弱いところ、そんなに簡単に見抜かないでよ……でも、止めないで♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ、あ……っ、奥まで響く……。お姉さんだから平気って言いたいのに、声が勝手に幼くなるよぉ……」
		ELSE
			PRINTFORMW 「ひゃわわわっ!?　だめ、そこは、頭の中まで真っ白になる……っ。転校生くん、もう少しだけ、わたしを離さないで……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、そこを探してるの？　ち、違うよ、そこは別に……っ、あれ、力が入らないなぁ……」
		ELSEIF A == 1
			PRINTFORMW 「ひ、ひゃっ……っ、触るたびに身体が跳ねるよぉ。転校生くん、笑わないで……わたし、ちゃんとお姉さんなのに」
		ELSE
			PRINTFORMW 「ふふ……まだ平気、だよね。……うそ、もう少しゆっくりにして。わたし、変な声が出ちゃうから……」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あ……っ、止まらないよぉ……。転校生くんの前で、こんなに無防備になるなんて。笑わないで、ね……？」
		ELSEIF A == 1
			PRINTFORMW 「や、だ……っ、音まで聞こえるの、恥ずかしいよ……。でも、手は離さないで。今だけ、甘えてもいいよね？」
		ELSE
			PRINTFORMW 「ひゃっ……もう、わたしの意志じゃどうにもならないんだね……。転校生くん、終わったあとも、ちゃんと隣にいてくれる？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、ちょっと待って、なにこれ……っ。わたし、こんなつもりじゃないのに、止まらないよぉ～っ！」
		ELSEIF A == 1
			PRINTFORMW 「うぅ……見ないでって言いたいけど、もう遅いよね。転校生くん、お願いだから、今の顔は覚えないで……」
		ELSE
			PRINTFORMW 「みづちゃんに知られたら、絶対にからかわれる……っ。ね、今のことは、わたしと転校生くんだけの秘密にしてね？」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
	CALL AITE_YOBI, 47, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の胸、あったかいね……。こうしてくっついてると、女の子同士なのに、変にどきどきしてくるよ♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ……%LOCALS%、少し動くたびに、そこが擦れるね。ふふ、そんな顔をされたら、わたしまで意地悪したくなるなぁ」
		ELSE
			PRINTFORMW 「ひゃっ……っ、胸の先が触れると、思ったより敏感なんだね。%LOCALS%、もうちょっとだけ、このままでいよ……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにっ？　%LOCALS%と胸を合わせるの？　あんまり大きくないから、期待されると困るんだけどなぁ……」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、いきなり押しつけないでよぉ……っ。%LOCALS%の鼓動まで近くて、落ち着かないよ～」
		ELSE
			PRINTFORMW 「ふふ～ん、女の子同士なら平気……。あれ、全然平気じゃないね。%LOCALS%、ゆっくりにしてくれる？」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
	CALL AITE_YOBI, 47, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「わたしが転校生くんに乗って、%LOCALS%は顔の上なんだね……。ふふ、二人で甘やかしてあげるから、ちゃんと受け止めてよ♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ、下から来るのと、%LOCALS%の動きが重なると……っ、わたし、どっちに合わせればいいのかな……」
		ELSE
			PRINTFORMW 「%LOCALS%ばかり見ないでよぉ。わたしだって、ちゃんと感じてるんだから……ほら、こっちも見て、転校生くん♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひゃわわっ!?　わたしが乗るの？　しかも%LOCALS%まで顔の上って……転校生くん、急にお姉さんを困らせないでよ～っ！」
		ELSEIF A == 1
			PRINTFORMW 「あっ、揺らさないで……っ、%LOCALS%も急に動かないでよぉ。下からも上からも来たら、わたし、落ち着けないじゃん……」
		ELSE
			PRINTFORMW 「ふふ～ん、わたしが主導権を取るからね。……って、二人とも好きにしないでっ、これじゃわたしまで変になっちゃうよ～っ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「よしよし、今日はよく頑張ったね。ほら、わたしが撫でてあげるから、転校生くんは力を抜いていいよ♪」
		ELSEIF A == 1
			PRINTFORMW 「あれ、もう目を閉じちゃうの？　ふふ、そんなに気持ちいいなら、もう少しお姉さんに甘えててね」
		ELSE
			PRINTFORMW 「話したくないことは、今は話さなくていいよ。わたしが隣にいるから……ほら、頭を上げないで、よしよし」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「転校生くん、今日はちょっと疲れてるね。ほら、わたしが撫でてあげるから、少し休もうか」
		ELSEIF A == 1
			PRINTFORMW 「うにっ？　そんなに素直に頭を預けるんだ……。ふふ、たまにはお姉さんに甘えてもいいんだよ？」
		ELSE
			PRINTFORMW 「無理に話さなくて大丈夫。わたし、ちゃんと聞くからね。眠るまでくらい、ずっと撫でてあげるよ」
		ENDIF
	ENDIF
ENDIF
'''


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    marker = "\n@TRAIN_MESSAGE_B280_47"
    if marker not in text:
        raise SystemExit("insertion marker not found")
    if ";--- COM60 助手にキスさせる ---" in text:
        raise SystemExit("CHAR47 additional block already exists")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        BACKUP.write_bytes(raw)
    text = text.replace(marker, "\n" + ADDITIONAL + marker, 1)
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
