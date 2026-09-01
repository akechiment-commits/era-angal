from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_65_時国そら_COM.ERB"
BACKUP = ROOT / "tools" / "backups" / "CHAR65_before_additional10_20260824" / TARGET.name


ADDITIONAL = r''' ;==============================================================
; CHAR65 標準追加10（原作照合後・恋人/通常 各RAND:3）
; ※静かな表面と括弧の内面、「ゆん、ゆん」の交信音を分岐ごとに散らす。
;==============================================================
;--- COM60 助手にキスさせる ---
; ▼【視点】そらが女性助手へキスする。PLAYERは見届ける側。
IF SELECTCOM == 60
	CALL AITE_YOBI, 65, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「ゆん、ゆん……。%LOCALS%の唇、やわらかいね。あなたが見てると、いつもより音が近く聞こえる……」
		ELSEIF A == 1
			PRINTFORMW 「ん……ちゅ。……（あのひと、見てる。わたし、ちゃんと普通の女の子に見えてるかな……？）」
		ELSE
			PRINTFORMW 「%LOCALS%、もう少しだけ……。あなたの鼓動が聞こえると、離れるのが惜しくなるの」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひゃっ……わたしが先にするの？　あなた、見てる……。ゆん、ゆん……どうしよう」
		ELSEIF A == 1
			PRINTFORMW 「ん……っ、いまのは、挨拶じゃないね。%LOCALS%、笑わないで……。顔、熱いの」
		ELSE
			PRINTFORMW 「まだ、続けるのかな……。あなたの音が近すぎて、考えが聞こえそう……」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
; ▼【視点】そらと女性助手が同じPLAYERへ素股をする。PLAYERを二人で挟む側。
IF SELECTCOM == 62
	CALL AITE_YOBI, 65, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「%LOCALS%と息が重なると、あなたの熱が返ってくる……。わたし、少し嬉しい」
		ELSEIF A == 1
			PRINTFORMW 「ん……っ、あなたの鼓動、速い。%LOCALS%、急がなくていいよ……まだ、聴いていたいから」
		ELSE
			PRINTFORMW 「（あのひとの前で、こんなふうに……。恥ずかしいのに、離れたくない）……ゆん、ゆん」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひゃっ……%LOCALS%の気配、近いの。あなた、そんなに動くと……わたしまで、声が」
		ELSEIF A == 1
			PRINTFORMW 「ゆん、ゆん……。これは、わたしが聞いていたより、ずっと大きな音……」
		ELSE
			PRINTFORMW 「平気だと思ってたけど……もう、表の声だけじゃ足りないみたい」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; ▼【視点】そらと女性助手が一本の双頭バイブでつながる。PLAYERは当事者ではない。
IF SELECTCOM == 76
	CALL AITE_YOBI, 65, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「……いまの震え、%LOCALS%から？　離れているのに、わたしの中で返ってくる……ゆん、ゆん」
		ELSEIF A == 1
			PRINTFORMW 「んっ……また来た。%LOCALS%が息を変えると、こっちまでわかるの。あなたにも、聞こえてるかな」
		ELSE
			PRINTFORMW 「（ふたりで同じところを感じてる……。あのひとに見られると、心の中まで知られそう）」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひっ……今の、%LOCALS%？　わたしの中まで同じに……。ゆん、ゆん……怖くない、はず」
		ELSEIF A == 1
			PRINTFORMW 「ん、んぅ……動き、わかるよ。%LOCALS%、もう少しだけ、ゆっくり……」
		ELSE
			PRINTFORMW 「（声にしたら、届いちゃう。身体のことまで、聞かれちゃう）……あなた、見ないで」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
; ▼【視点】PLAYERがそらの胸から飲む。そらは飲ませる側。
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「ん……あなた、急がなくていいよ。飲んでる音も、鼓動も、ちゃんと聞こえるから」
		ELSEIF A == 1
			PRINTFORMW 「ゆん、ゆん……。そんなに安心した顔をされると、わたしも、あったかい」
		ELSE
			PRINTFORMW 「もう少し？　うん……あなたが欲しいなら、わたし、ここにいるの」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ……わたしの？　あなた、そんなに真っ直ぐ見るの……。困ったちゃん」
		ELSEIF A == 1
			PRINTFORMW 「あ……っ、急に吸わないで。音が近くて……わたし、何も考えられない」
		ELSE
			PRINTFORMW 「まだ離れないのかな……。いいよ、落ち着くまで。わたしも、動かないから」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
; ▼【視点】PLAYERがそらの胸を搾る。そらは搾られる側。
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「んっ……そこ、ゆっくり。あなたの手の音、近くで聞くと、身体まで眠くなる……」
		ELSEIF A == 1
			PRINTFORMW 「出るたび、あなたの息が変わるね。ふふ……わたしのことで、そんな顔をするの？」
		ELSE
			PRINTFORMW 「もう少しだけ、お願い。……（あのひとに触れられてる。うれしい）」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あっ……そこ、強い。わたし、音まで聞こえて……恥ずかしいの」
		ELSEIF A == 1
			PRINTFORMW 「ゆん、ゆん……。止まると、少し静かになるね。続けるなら、そっと……」
		ELSE
			PRINTFORMW 「まだ、するの？　嫌じゃないけど……あなたに見られてると、どこに顔を向けたらいいのかな」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
; ▼【視点】PLAYERがそらのGスポットを刺激する。そらは刺激を受ける側。
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「そこ……。あなた、わたしの揺れるところ、見つけたのね。ゆん、ゆん……近い」
		ELSEIF A == 1
			PRINTFORMW 「ん、あ……っ、聞こえる……あなたの心臓、速い。わたしのせいなのかな」
		ELSE
			PRINTFORMW 「（声、出したくないのに。気持ちいいって、もう聞かれてる）……もう少し、だけ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、そこを探すの？　……ひゃっ、力が抜ける。あなた、知らないふりして」
		ELSEIF A == 1
			PRINTFORMW 「ひっ……触れるたび、身体が跳ねる。ゆん、ゆん……わたし、変なのかな」
		ELSE
			PRINTFORMW 「平気、だと思う……たぶん。もう少し静かなら、まだ、話せるの」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
; ▼【視点】そらが強制的に放尿させられる。制御を失う側。
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「あ……止まらない。あなたの前で、こんなふうに……（見ないで、でも離れないで）」
		ELSEIF A == 1
			PRINTFORMW 「音、聞こえるね……。恥ずかしいけど、あなたの手、貸してほしい」
		ELSE
			PRINTFORMW 「ゆん、ゆん……終わった？　わたし、まだ震えてる。そばにいて」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、待って……わたしの声、聞こえてる？　止められないの……」
		ELSEIF A == 1
			PRINTFORMW 「見ないで、って言いたいけど……もう、遅いね。あなた、忘れてくれる？」
		ELSE
			PRINTFORMW 「（こんなの、知らない。知らないのに、身体だけ……）……誰にも、言わないで」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; ▼【視点】そらと女性助手が胸を合わせる。男性PLAYERは当事者ではない。
IF SELECTCOM == 202
	CALL AITE_YOBI, 65, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「%LOCALS%の鼓動、近いね。あなたが見てると、ふたりぶん聞こえてくるみたい……」
		ELSEIF A == 1
			PRINTFORMW 「んっ……そこ、触れる。%LOCALS%、いま笑った？　わたしまで、変な気持ちになる」
		ELSE
			PRINTFORMW 「（あのひとの前で、仲間とこんなに近く……。恥ずかしい。でも、嫌じゃない）」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%と、こんなに近くなるの……？　ゆん、ゆん……音が多い」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ……声、近いよ。わたし、何を言えばいいの……」
		ELSE
			PRINTFORMW 「気楽な触れ合いだと思ってた……。胸まで、落ち着かないね」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; ▼【視点】そらがPLAYERに騎乗し、女性助手がPLAYERの顔に乗る。そらは挿入を受ける側。
IF SELECTCOM == 258
	CALL AITE_YOBI, 65, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「んっ……あなたの鼓動、下から聞こえる。%LOCALS%の息も近い……わたし、どちらを聞けばいいのかな」
		ELSEIF A == 1
			PRINTFORMW 「あ……っ、重なると、身体の中まで響くね。あなた、わたしを見て……ゆん、ゆん」
		ELSE
			PRINTFORMW 「（こんな場所、誰にも見せられない。あのひとになら……見られていたい）……」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「わたしが、あなたの上に……？　そのうえ%LOCALS%まで。ひゃっ……音が、近すぎるよ」
		ELSEIF A == 1
			PRINTFORMW 「揺らさないで……。%LOCALS%、あなたの顔の上で、急がないでね。わたし、落ち着けないの」
		ELSE
			PRINTFORMW 「ゆん、ゆん……。ふたりぶんの気配、聞こえる。考える時間、なくなっちゃった」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; ▼【視点】そらがPLAYERの頭を撫でる側。そら自身が撫でられる側ではない。
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「よしよし……あなた、今日は疲れたのね。わたしの手、ここにあるから」
		ELSEIF A == 1
			PRINTFORMW 「目、閉じた？　（甘えてくれるの、うれしい。わたしだけが知っていたい）……ゆん、ゆん」
		ELSE
			PRINTFORMW 「話さなくていいよ。あなたの音、聞いてる。落ち着くまで、撫でてあげる」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「転校生くん、少し疲れてるね。……肩の力、抜いていいよ」
		ELSEIF A == 1
			PRINTFORMW 「わたしに頭を預けるの？　ゆん、ゆん……たまには、お姉さんみたいにしてあげる」
		ELSE
			PRINTFORMW 「無理に話さなくていいの。聞くから……あなたが眠るまで、ここにいるね」
		ENDIF
	ENDIF
ENDIF
'''


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    if ";--- COM60 助手にキスさせる ---" in text:
        raise RuntimeError("CHAR65 additional10 already exists")
    marker = ";--- COM0 愛撫 ---"
    if marker not in text:
        raise RuntimeError("COM0 insertion marker not found")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        BACKUP.write_bytes(raw)
    normalized = text.replace("\r\n", "\n")
    normalized = normalized.replace(marker, ADDITIONAL.lstrip() + "\n" + marker, 1)
    TARGET.write_bytes(normalized.replace("\n", "\r\n").encode("cp932"))
    print("CHAR65追加10を挿入しました。")


if __name__ == "__main__":
    main()
