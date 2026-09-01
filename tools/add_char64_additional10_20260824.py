from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_64_峰山しおん_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR64_before_additional10_20260824" / TARGET.name


ADDITIONAL = r''' ;==============================================================
; CHAR64 標準追加10（原作照合後・恋人/通常 各RAND:3）
; ※観察者の余裕を核にしつつ、親密になるほど自分が物語へ引き込まれる声へ。
;==============================================================
;--- COM60 助手にキスさせる ---
; ▼【視点】しおんが女性助手へキスする。PLAYERは見届ける側。
IF SELECTCOM == 60
	CALL AITE_YOBI, 64, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「ふむ……%LOCALS%の唇は、思ったより素直な味がするね。少年、そんなに見つめると、こちらまで意識してしまうよ」
		ELSEIF A == 1
			PRINTFORMW 「ん……ちゅ。もう一度、かい？　君の前で読者の顔をしているのも、そろそろ難しくなってきたね♪」
		ELSE
			PRINTFORMW 「失敬、少し長くなったかな。%LOCALS%が離れてくれないものだから……いや、私も望んでいたのだけれどね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ええと……私が先に近づくのかい？　少年、見ているだけのつもりなら、そんな顔をしないでくれたまえ」
		ELSEIF A == 1
			PRINTFORMW 「ん……っ、待って、いまのは挨拶では済まないね。%LOCALS%、もう笑わないでくれ」
		ELSE
			PRINTFORMW 「ふむ、こういう展開は本の中だけだと思っていたよ。続けるなら……せめて、急かさないでくれたまえ」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
; ▼【視点】しおんと女性助手が同じPLAYERへ素股をする。PLAYERを二人で挟む側。
IF SELECTCOM == 62
	CALL AITE_YOBI, 64, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「%LOCALS%と息が重なるたび、少年の熱がこちらへ返ってくるね……。ふふ、これは一人で読む物語ではないらしい」
		ELSEIF A == 1
			PRINTFORMW 「んっ……そんなに動かれると、%LOCALS%の呼吸まで近くなる。どちらに合わせても、私のほうが先に乱れそうだよ」
		ELSE
			PRINTFORMW 「少年、余裕の顔をしているね。こちらはもう、勝敗を論じる気分ではないのだけれど……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おや……二人がかりとは、ずいぶん大胆な筋書きだね。私はまだ、その頁を開く覚悟が……」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ……%LOCALS%とぶつかるたび、声が勝手に……。少年、今のは聞かなかったことにしたまえ」
		ELSE
			PRINTFORMW 「ふむ、平静を装うのもここまでか。%LOCALS%、もう少し呼吸を合わせてくれないかい」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; ▼【視点】しおんと女性助手が一本の双頭バイブでつながる。PLAYERは当事者ではない。
IF SELECTCOM == 76
	CALL AITE_YOBI, 64, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「……いまの震え、%LOCALS%から届いたのかい。離れているのに、私の内側で返事をされると、妙に近く感じるね」
		ELSEIF A == 1
			PRINTFORMW 「んっ……あ、また来た。%LOCALS%が動くたび、同じところまで揺れる……これは、なかなか抗いがたいよ」
		ELSE
			PRINTFORMW 「ふふ、互いの息まで伝わってくるようだ。少年、私がどちらを見ているかは、訊かないでくれたまえ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひっ……いまのは%LOCALS%のほうかい？　私の身体まで同じように震えるのは、少し心の準備が……」
		ELSEIF A == 1
			PRINTFORMW 「ん、んぅ……その動き、こちらまで来るよ。%LOCALS%、もう少しゆっくりなら、まだ考えられるのだけれど」
		ELSE
			PRINTFORMW 「ふむ……平気な顔をしていたかったが、今のは無理だね。声まで返ってしまいそうだよ」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
; ▼【視点】PLAYERがしおんの胸から飲む。しおんは飲ませる側。
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「ん……そんなに急がなくていいよ。君が夢中になっているのを見ていると、私まで胸の奥が温かくなるね」
		ELSEIF A == 1
			PRINTFORMW 「ふふ、甘え上手だね、少年。もう少し欲しいなら、そう言葉にしてみたまえ」
		ELSE
			PRINTFORMW 「そこまで大切そうに扱われると、読書よりこちらを選びたくなるではないか……困ったものだよ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、私から？　……いや、構わないが、そんなにまっすぐ見上げられると落ち着かないね」
		ELSEIF A == 1
			PRINTFORMW 「あ……っ、そんなに吸われるとは思わなかったよ。少年、私の顔を観察して楽しんでいるのかい？」
		ELSE
			PRINTFORMW 「まだ離れないのだね。ふむ……君が安心するなら、もう少しこのままでもいいよ」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
; ▼【視点】PLAYERがしおんの胸を搾る。しおんは搾られる側。
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「んっ……そこは丁寧に。君の手つきに慣れてしまうと、私まで続きを期待してしまうではないか」
		ELSEIF A == 1
			PRINTFORMW 「あ、出るたびに嬉しそうな顔をするね。私の身体でそんな顔をされると、悪い気はしないよ♪」
		ELSE
			PRINTFORMW 「もう少しだけ……。ふふ、こうして頼む側になるのは、読者でいるよりずっと落ち着かないね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おや、ずいぶん熱心だね……っ。研究対象のように眺められると、さすがに恥ずかしいよ」
		ELSEIF A == 1
			PRINTFORMW 「あっ、そこは少し強い……。君の手が止まらないと、こちらの思考まで散ってしまうね」
		ELSE
			PRINTFORMW 「まだ続けるのかい？　……いや、嫌だとは言っていないよ。どうにも断る文句が見つからなくてね」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
; ▼【視点】PLAYERがしおんのGスポットを刺激する。しおんは刺激を受ける側。
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「そこ……っ、君はもう見つけたのかい。私の余裕まで読み解かれるとは、なかなかの観察眼だね」
		ELSEIF A == 1
			PRINTFORMW 「ん、あ……っ、深く響くね。言葉を選んでいる暇がなくなるほど、君の指は正直だよ」
		ELSE
			PRINTFORMW 「ひゃっ……そこは、まだ読者に見せる場面ではないのだけれど。君だけなら……続きを許してしまいそうだ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、そこを探しているのかい？　ま、待ちたまえ……あ、もう、力が抜けてしまうじゃないか」
		ELSEIF A == 1
			PRINTFORMW 「ひっ……触れるたびに身体が跳ねるよ。少年、笑わないでくれたまえ、これは私の意思では……」
		ELSE
			PRINTFORMW 「ふむ、まだ平気だと思っていたのだがね。もう少し静かにされると、取り繕う言葉がなくなりそうだ」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
; ▼【視点】しおんが強制的に放尿させられる。制御を失う側。
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「あ……止まらないね。君の前でこんな失態を晒すとは、私のほうが物語に呑まれてしまったようだよ」
		ELSEIF A == 1
			PRINTFORMW 「音まで聞こえてしまうのかい……。せめて手を貸してくれたまえ、今は君の隣から離れたくない」
		ELSE
			PRINTFORMW 「ふふ、見られたくないのに、君には隠せないね。終わったあとも、何も言わずそばにいてくれるかい？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、待ちたまえ……っ、これは私の意志ではないよ。止めようとしても、身体のほうが先に……」
		ELSEIF A == 1
			PRINTFORMW 「見ないでくれたまえ、と言うには遅すぎるね。少年、今のことは忘れてくれるかい」
		ELSE
			PRINTFORMW 「うぅ……こんな頁は本に挟んで隠しておきたいよ。誰にも話さないでくれたまえ」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; ▼【視点】しおんと女性助手が胸を合わせる。男性PLAYERは当事者ではない。
IF SELECTCOM == 202
	CALL AITE_YOBI, 64, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「%LOCALS%の肌が触れると、思ったより息が近くなるね……。少年、そんなに興味深そうに見ないでくれたまえ♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ……いまの重なり方は、少し意地が悪いよ。%LOCALS%、君もわざとではないだろうね？」
		ELSE
			PRINTFORMW 「ふふ、胸の鼓動まで伝わってくる。こういう一節なら、観察するだけではもったいないな」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「おや……%LOCALS%と、こうして近づくのかい？　平静にしていれば済むと思ったのだが……」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、そこは……っ。声が近すぎて、何を言えばいいのか忘れてしまったよ」
		ELSE
			PRINTFORMW 「ふむ、気楽なじゃれ合いと思っていたのだけれどね。予想外に息が上がるよ」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; ▼【視点】しおんがPLAYERに騎乗し、女性助手がPLAYERの顔に乗る。しおんは挿入を受ける側。
IF SELECTCOM == 258
	CALL AITE_YOBI, 64, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「んっ……下から来るたび、%LOCALS%の気配まで重なってくる。少年、今は私を見ていたまえ」
		ELSEIF A == 1
			PRINTFORMW 「あ、そこ……。%LOCALS%の動きと重なると、どちらに息を合わせればいいのか、わからなくなるよ」
		ELSE
			PRINTFORMW 「ふふ、私が物語を解説する余裕は、もう残っていないね。君の上でこんな声を出すとは……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ええと……私が君の上に？　そのうえ%LOCALS%まで……。読む前から筋書きが過激すぎないかい」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ……揺らさないでくれたまえ、落ち着いて座っていられないよ。%LOCALS%、君も急がないで……」
		ELSE
			PRINTFORMW 「ふむ、主導権を取るつもりだったのだがね。二人に挟まれると、考える時間さえ与えてもらえないらしい」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; ▼【視点】しおんがPLAYERの頭を撫でる側。しおん自身が撫でられる側ではない。
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「よしよし、今日はよく頑張ったね。私の手でよければ、少し眠るといいよ」
		ELSEIF A == 1
			PRINTFORMW 「おや、もう目を閉じたのかい？　ふふ、君がこうして素直に甘えるのは、私だけが知っていれば十分だね」
		ELSE
			PRINTFORMW 「話したくないことは、今は話さなくていい。読書の続きは後回しにして、君が落ち着くまでここにいるよ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「転校生くん、少し疲れているようだね。ほら、肩の力を抜きたまえ」
		ELSEIF A == 1
			PRINTFORMW 「ふむ、私に頭を預けるとは……。たまには先輩を頼ってくれてもいいのだよ」
		ELSE
			PRINTFORMW 「無理に話さなくていいさ。聞くくらいなら私にもできる。落ち着くまで、ここにいようじゃないか」
		ENDIF
	ENDIF
ENDIF
'''


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    if ";--- COM60 助手にキスさせる ---" in text:
        raise RuntimeError("CHAR64 additional10 already exists")
    marker = ";--- COM0 愛撫 ---"
    if marker not in text:
        raise RuntimeError("COM0 insertion marker not found")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        BACKUP.write_bytes(raw)
    normalized = text.replace("\r\n", "\n")
    normalized = normalized.replace(marker, ADDITIONAL.lstrip() + "\n" + marker, 1)
    TARGET.write_bytes(normalized.replace("\n", "\r\n").encode("cp932"))
    print("CHAR64追加10を挿入しました。")


if __name__ == "__main__":
    main()
