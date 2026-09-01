from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_48_四方みつる_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR48_before_additional10_20260824" / TARGET.name


ADDITIONAL = r''';==============================================================
; CHAR48 標準追加10（原作照合後・恋人/通常 各RAND:3）
; ※「僕」＝王子様・副会長の公的な余裕。「わたし」＝本心が漏れる枝のみ。
;==============================================================
;--- COM60 助手にキスさせる ---
; ▼【視点】みつるが女性助手へキスする。PLAYERは見届ける側。
IF SELECTCOM == 60
	CALL AITE_YOBI, 48, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「%LOCALS%、こっちを向いて。……ちゅ。ふふ、転校生くんに見られながらだと、いつもの挨拶まで少し特別になるね♪」
		ELSEIF A == 1
			PRINTFORMW 「ん……もう一度？　いいよ。%LOCALS%の唇を味わってるところ、君にも見ていてほしいな……♪」
		ELSE
			PRINTFORMW 「ふふ、そんなに熱心に見てるのかい？　君の前でなら、僕も少し大胆になれる気がするよ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、僕が%LOCALS%に？　転校生くんが見てるのに……。ま、まぁ、挨拶くらいなら平気さ」
		ELSEIF A == 1
			PRINTFORMW 「ちゅ……っ。あ、あれ？　思っていたより、見る側がいちばん恥ずかしいね……」
		ELSE
			PRINTFORMW 「%LOCALS%、嫌じゃなければ、もう少しだけ付き合ってくれるかい？　転校生くんには、変な顔を見せたくないんだけどな」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
; ▼【視点】みつると女性助手が同じPLAYERへ素股をする。PLAYERを二人で挟む側。
IF SELECTCOM == 62
	CALL AITE_YOBI, 48, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「%LOCALS%と息を合わせて、君を挟むんだね。ふふ、どちらが先に君を参らせるか、競争してみようか♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ……動きが重なると、君の熱が二人ぶん返ってくるね。転校生くん、余裕の顔はもう終わりかな？」
		ELSE
			PRINTFORMW 「%LOCALS%、少しゆっくり。僕まで夢中になって、君をからかう余裕がなくなりそうだよ……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うわっ、二人がかりで？　転校生くん、ずいぶん贅沢なことを考えるね……」
		ELSEIF A == 1
			PRINTFORMW 「んっ、君が動くたびに%LOCALS%とぶつかる……。これ、思ったより息が合うと危険だね」
		ELSE
			PRINTFORMW 「ふふ、まだ僕は平気さ。……って、そんなに動かれたら、言い切れなくなるじゃないか」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; ▼【視点】みつると女性助手が一本の双頭バイブでつながる。PLAYERは当事者ではない。
IF SELECTCOM == 76
	CALL AITE_YOBI, 48, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「%LOCALS%の動きが、そのままこっちに返ってくる……。ふふ、離れてるのに、ずっと抱き合ってるみたいだね」
		ELSEIF A == 1
			PRINTFORMW 「んっ……今の、%LOCALS%が動いたんだね。こっちまで同じところが震えると、僕まで素直になってしまうよ……♪」
		ELSE
			PRINTFORMW 「だめ……もう少しだけ待って、%LOCALS%。君の動きと一緒に来ると、わたし、どちらを感じてるのかわからなくなる……」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、%LOCALS%と同じ道具を使うの？　……あ、今の震え、そっちから返ってきたんだね」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ……%LOCALS%、急に動かないで。こっちまで同じように揺れるから、心の準備が追いつかないよ……っ」
		ELSE
			PRINTFORMW 「女の子同士なら落ち着いていられると思ったのに……。ふふ、全然だね。ゆっくり合わせてくれるかい？」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
; ▼【視点】PLAYERがみつるの胸から飲む。みつるは飲ませる側。
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「ん……そんなに夢中になるんだね。ふふ、君に飲まれてると思うと、変に胸が熱くなるよ……♪」
		ELSEIF A == 1
			PRINTFORMW 「もう少しだけ、ゆっくりね。君の顔があまりにも嬉しそうで、わたし、離れてって言えなくなる……」
		ELSE
			PRINTFORMW 「……ふふ、甘えんぼうさん。僕のこと、ちゃんと女の子にしてくれるんだね？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、僕の胸から？　期待されると困るなぁ……って、もう飲んでるのかい？」
		ELSEIF A == 1
			PRINTFORMW 「あっ……そんなに吸うと、びっくりするよ。転校生くん、僕の顔を見て笑わないでくれたまえ……」
		ELSE
			PRINTFORMW 「まだ、離れないんだね。……まぁ、君が落ち着くなら、もう少しこのままでいようか」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
; ▼【視点】PLAYERがみつるの胸を搾る。みつるは搾られる側。
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「そこは、そんなふうに触るんだね……。君の手に僕の身体が慣れていくの、少し怖いけど嬉しいな」
		ELSEIF A == 1
			PRINTFORMW 「んっ……もう少し優しく。僕だって、君の前ではそんなに格好つけていられないよ……♪」
		ELSE
			PRINTFORMW 「出てくるたびに、そんな顔をするんだ。ふふ、わたしの身体で君が喜んでくれるの、好き……」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、搾るのかい？　ふふ、実験みたいに観察しないでよ。僕だって恥ずかしいんだから」
		ELSEIF A == 1
			PRINTFORMW 「あっ、そこは強いよ……。そんなに一生懸命にならなくても、ちゃんとわかってるからね」
		ELSE
			PRINTFORMW 「まだ続けるの？　……少しだけなら。妙に手慣れてくると、こっちまで意識しちゃうじゃないか」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
; ▼【視点】PLAYERがみつるのGスポットを刺激する。みつるは刺激を受ける側。
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「そこ……っ、君、もう見つけたのかい？　僕の弱いところ、そんなに簡単に見抜かないでほしいな……♪」
		ELSEIF A == 1
			PRINTFORMW 「ん、あ……っ、奥まで響く……。平気な顔をしていたいのに、わたしの声、聞こえてしまうね……」
		ELSE
			PRINTFORMW 「ひゃっ……そこはだめだよ。君の指だけで、頭のなかまで真っ白になりそう……っ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、そこを探してるの？　ち、違う、そこは……あれ、力が抜けるなぁ」
		ELSEIF A == 1
			PRINTFORMW 「ひっ……触るたびに身体が跳ねるよ。転校生くん、笑わないでくれたまえ……」
		ELSE
			PRINTFORMW 「ふふ、まだ平気……だと思う。いや、もう少しゆっくりにして。変な声が出そうだ」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
; ▼【視点】みつるが強制的に放尿させられる。制御喪失と羞恥を受ける側。
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「あ……っ、止まらない……。君の前でこんなふうになるなんて、わたし、もう隠せないよ……」
		ELSEIF A == 1
			PRINTFORMW 「や、だ……音まで聞こえるの？　お願い、手だけは離さないで。今は君に寄りかかっていたい……」
		ELSE
			PRINTFORMW 「僕の意志じゃ、どうにもならないんだね……。終わったあとも、隣にいてくれるかい？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、待って、これは……っ。僕、こんなつもりじゃ……止まらないよ……！」
		ELSEIF A == 1
			PRINTFORMW 「見ないでくれたまえって言いたいけど、もう遅いね……。転校生くん、今の顔は忘れてほしいな」
		ELSE
			PRINTFORMW 「うぅ……こんな失態、誰にも話さないでよ。僕と君だけの秘密にしておくれ……」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; ▼【視点】みつると女性助手が胸を合わせる。男性PLAYERは当事者ではない。
IF SELECTCOM == 202
	CALL AITE_YOBI, 48, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「%LOCALS%の胸、あったかいね……。女の子同士なのに、君に見られてると思うと余計にどきどきするよ♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ……動くたびに、胸の先が擦れるね。%LOCALS%、そんな顔で笑わないでよ。わたしまで意地悪したくなる……」
		ELSE
			PRINTFORMW 「ひゃっ……今の、思ったより深く響いた……。%LOCALS%、もう少しだけ、このままでいようか……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにっ？　%LOCALS%と胸を合わせるのかい？　大きさは期待しないでほしいなぁ……」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、急に押しつけないで。鼓動まで近くて、僕、落ち着いていられないよ～」
		ELSE
			PRINTFORMW 「ふふ、女の子同士なら平気だと思ったのに。……全然平気じゃないね、%LOCALS%？」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; ▼【視点】みつるがPLAYERに騎乗し、女性助手がPLAYERの顔に乗る。みつるも挿入を受ける側。
IF SELECTCOM == 258
	CALL AITE_YOBI, 48, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「僕が君に乗って、%LOCALS%は顔の上……。ふふ、二人ぶん受け止めてもらうんだから、ちゃんと僕を見ていてね♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ、下から来るのと%LOCALS%の動きが重なると……っ、わたし、どちらに合わせればいいのかわからないよ……」
		ELSE
			PRINTFORMW 「%LOCALS%ばかり見ないで。僕も君の上でちゃんと感じてるんだから……ほら、こっちを見て♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひゃっ……僕が乗るのかい？　しかも%LOCALS%まで顔の上だなんて、転校生くん、急すぎるよ……っ」
		ELSEIF A == 1
			PRINTFORMW 「あっ、揺らさないで……%LOCALS%も急に動かないでくれたまえ。上下から来たら、僕、落ち着けないじゃないか」
		ELSE
			PRINTFORMW 「ふふ、僕が主導権を取るつもりだったんだけど……二人とも好きに動かないでよ。わたしまで変になってしまう……っ」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; ▼【視点】みつるがPLAYERの頭を撫でる側。みつる自身が撫でられる側ではない。
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「よしよし、今日はよく頑張ったね。僕が撫でてあげるから、君は何も考えずに休んでいて♪」
		ELSEIF A == 1
			PRINTFORMW 「あれ、もう目を閉じたのかい？　ふふ、そんなに僕の手が気持ちいいなら、もう少し甘えていてくれたまえ」
		ELSE
			PRINTFORMW 「話したくないことは、今は話さなくていいよ。僕が隣にいるから……よしよし、眠るまで撫でてあげる」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「転校生くん、今日は疲れてるね。ほら、僕が撫でてあげるから、少し休もうか」
		ELSEIF A == 1
			PRINTFORMW 「うにっ？　そんなに素直に頭を預けるんだ……。ふふ、たまには先輩に甘えてもいいんだよ？」
		ELSE
			PRINTFORMW 「無理に話さなくて大丈夫。僕がちゃんと聞くからね。落ち着くまで、撫でていてあげるよ」
		ENDIF
	ENDIF
ENDIF
'''


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    if ";--- COM60 助手にキスさせる ---" in text:
        raise RuntimeError("CHAR48 additional10 already exists")
    marker = ";--- COM0 愛撫 ---"
    if marker not in text:
        raise RuntimeError("COM0 insertion marker not found")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        BACKUP.write_bytes(raw)
    normalized = text.replace("\r\n", "\n")
    normalized = normalized.replace(marker, ADDITIONAL + "\n" + marker, 1)
    TARGET.write_bytes(normalized.replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
