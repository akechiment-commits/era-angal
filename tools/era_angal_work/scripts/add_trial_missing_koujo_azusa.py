from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_17_小鳩あずさ_COM.ERB")
START = ";=== AZUSA MISSING COMMAND TRIAL START ==="
END = ";=== AZUSA MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_17"


BLOCK = r''';=== AZUSA MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ、ちゅ……☆　ちゃんと笑えてました？　転校生の先輩を見たら、急に胸がちくってしたんですけどっ」
		ELSEIF A == 1
			PRINTFORMW 「ふあっ、唇が離れたら、今度は先輩のところへ戻りたくなっちゃいました。あずさ、欲張りですねっ☆」
		ELSE
			PRINTFORMW 「この子には優しく、先輩には特別に……同じキスじゃないです。そこは間違えないでくださいねっ☆」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「笑ってたらキスできませんよね。あずさ、ちょっとだけキラキラ笑顔をお休みします……んっ」
		ELSEIF A == 1
			PRINTFORMW 「あずさから近づきますねっ☆　……あれ、目を閉じたら急に距離がわからなく……手、握ってくださいっ」
		ELSE
			PRINTFORMW 「唇って、こんなに柔らかいんですね……って、あずさ何を観察してるんでしょうっ。もう一回は観察じゃないですよ☆」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 17, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、あずさが右を受け持ちますっ☆　……転校生の先輩、どちらかだけ見つめるのは禁止ですよ？」
		ELSEIF A == 1
			PRINTFORMW 「ひゃわんっ、脚がもつれ……！　転校生の先輩、笑う前に支えてください～っ☆」
		ELSE
			PRINTFORMW 「三人の呼吸が揃うたび、先輩の熱が強くなる……。あずさ、ちゃんと役に立ててますねっ☆」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あずさ、テニスのペアより連携が不安ですっ☆　%LOCALS%、転んだら一緒に受け止めてくださいね！」
		ELSEIF A == 1
			PRINTFORMW 「せぇのっ……あれ、あずさだけ逆でした!?　次は声を出して合わせましょうっ☆」
		ELSE
			PRINTFORMW 「先輩の顔が真っ赤です。保健委員としては休ませたいですけど……まだ続けたい顔ですねっ？」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：あずさと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 17, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、あずさが笑ってる間は大丈夫ですっ☆　……ひゃわん、今のはちょっと笑えませんでしたぁ！」
		ELSEIF A == 1
			PRINTFORMW 「離れたところまで同じ震えが届くなんて、独りぼっちじゃない証拠みたいですね……手、離さないでくださいっ」
		ELSE
			PRINTFORMW 「%LOCALS%が息を止めると、あずさまで苦しくなります。声、我慢しないで一緒に出しましょうっ☆」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「右を動かしたら左が……ひゃわんっ！　あずさの身体、説明書どおりに動いてくれません～っ」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%、次はあずさが止まってます。どっちの震えか、ちゃんと確かめたいですっ☆」
		ELSE
			PRINTFORMW 「ふたりで腰が逃げてたら、ずっと終わりませんよね……。せぇので、今度こそ前へっ！」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「今日は先輩が患者さんですっ☆　あずさの胸に顔を埋めて、元気になるまで退院禁止ですよ？」
		ELSEIF A == 1
			PRINTFORMW 「飲んでくれるたび、あずさのなかの寂しいところまで満たされます……おかしいですね、あげてるのはあずさなのに」
		ELSE
			PRINTFORMW 「先輩の髪が頬に当たって、くすぐったいですっ。動かないでください、もう少しこのままがいいです☆」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「味も体温も、あずさには測れませんっ☆　先輩、飲み終わったら患者さん目線で報告してくださいね？」
		ELSEIF A == 1
			PRINTFORMW 「ひゃわんっ、吸う力って思ったより強いんですね！　あずさ、笑顔の準備が間に合いませんでした～っ☆」
		ELSE
			PRINTFORMW 「こぼしたぶんは拭けば大丈夫です。焦らないで、ちゃんと息継ぎしてくださいねっ☆」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩が搾るたび、胸の張りと一緒に強がりまで抜けてくみたいです……。最後まで笑っていられるかな」
		ELSEIF A == 1
			PRINTFORMW 「あずさの身体から出たものを、先輩と一緒に集めてる……ふたりだけの秘密が形になったみたいですねっ☆」
		ELSE
			PRINTFORMW 「まだ終わらないでください。こうして先輩の手を独り占めできる時間、あずさ好きですからっ☆」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「胸を押されると、くすぐったい場所と力が抜ける場所が違います。これはカルテに……書けませんねっ☆」
		ELSEIF A == 1
			PRINTFORMW 「ひゃわんっ、白衣だったら今ので汚れてました～！　先輩、あずさの制服は狙わないでくださいっ☆」
		ELSE
			PRINTFORMW 「あずさが合図するまで手を止めないでください。途中で止まるほうが、むずむずして困りますっ」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ひゃわんっ、そこは笑顔、むり……！　先輩、あずさの顔見ないで、でも手はそのままぁっ！」
		ELSEIF A == 1
			PRINTFORMW 「お兄ちゃん、そこ、もうわかっちゃったんですか……っ？　だめ、あずさ、すぐへなへなにぃ……！」
		ELSE
			PRINTFORMW 「先輩っ、ひとりにしないで……！　指、もっと奥、あずさを捕まえてぇっ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ふあ～んっ!?　今の、手当てじゃ治らないやつですぅっ！」
		ELSEIF A == 1
			PRINTFORMW 「待って、身体が勝手に笑っ……違う、これ笑顔じゃないですっ、ひゃぁん！」
		ELSE
			PRINTFORMW 「脚が言うこと聞きません～っ！　転校生の先輩、あずさが倒れる前に支えてぇっ！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「キラキラ笑顔で乗り切るつもりだったのに……先輩、今だけは笑えなくても、ここにいてください」
		ELSEIF A == 1
			PRINTFORMW 「あずさの身体、先輩には秘密をつくらせてくれないんですね……。もう、笑うしかないですっ☆」
		ELSE
			PRINTFORMW 「全部出たら、ちゃんと顔を上げます。先輩の恋人ですから、俯いたままにはなりませんっ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひゃわん、止めるほうに力を入れると脚まで震えます～っ！　こうなったら、倒れないことを優先します！」
		ELSEIF A == 1
			PRINTFORMW 「保健委員なのに自分の身体の合図を無視しました……。これは反省です、恥ずかしいけど覚えておきますっ」
		ELSE
			PRINTFORMW 「音に負けないくらい喋ってれば平気ですっ☆　先輩、何か質問してください、早く～っ！」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：あずさと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 17, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、胸の大きさより顔の近さが恥ずかしいですっ。そんなに見つめたら笑顔が崩れちゃいますよ～！」
		ELSEIF A == 1
			PRINTFORMW 「先っぽが触れるたび、%LOCALS%の息まで跳ねますね。あずさだけじゃないって、ちょっと安心ですっ☆」
		ELSE
			PRINTFORMW 「ふたりの間に隙間がなくなると、独りぼっちだったことまで遠くなります……もう少しくっついててください」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひゃわんっ、あずさのほうが大きいぶん先に当たっちゃいます！　%LOCALS%、位置を教えてください～っ」
		ELSEIF A == 1
			PRINTFORMW 「くすぐったくて笑ったら胸まで揺れちゃいましたっ☆　%LOCALS%も笑ったから、おあいこですね！」
		ELSE
			PRINTFORMW 「触れてるのは先っぽだけなのに、背中までぞわぞわします……。保健委員でも理由がわかりませんっ」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：あずさはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 17, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、先輩が苦しそうなら合図してくださいっ……！　あずさは上で転ばないように……ひゃわん、下からぁっ！」
		ELSEIF A == 1
			PRINTFORMW 「先輩の顔が見えないと、あずさだけ置いてかれたみたいで……んぁっ、腰でちゃんとここにいるって教えてぇ！」
		ELSE
			PRINTFORMW 「お兄ちゃんっ、お顔のほうに夢中になってないで……ふあぁっ！　あずさのなかも、もっと構ってぇっ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「上の%LOCALS%が体勢を変えると、その揺れが先輩の腰を伝って……ひゃぁっ、あずさ、バランス取れません～っ！」
		ELSEIF A == 1
			PRINTFORMW 「上から押さえるつもりが、下から何度も……！　先輩、そんなに器用にならなくていいですぅっ！」
		ELSE
			PRINTFORMW 「脚に力が入らないっ、%LOCALS%、あずさの手を引っ張って！　先輩のお顔から落ちないでぇ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：あずさがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩、今日の診察はここまでですっ☆　最後にあずさの膝で、よく頑張りましたの撫で撫でですよ♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩が目を閉じるまで撫でますね。眠ったら、あずさが独り占めしてたことは秘密ですっ☆」
		ELSE
			PRINTFORMW 「お兄ちゃん、たまには誰かに守られてください。あずさの手じゃ小さくても、頭くらいは包めますから」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「転校生の先輩、考えごとで眉間が固いです。ここを撫でたら、少しはほどけますか？」
		ELSEIF A == 1
			PRINTFORMW 「髪に寝癖発見ですっ☆　直すついでに撫でてるだけですから、照れなくていいですよ？」
		ELSE
			PRINTFORMW 「患者さんは安静にっ。あずさが三十数えるまで、膝から起きちゃ駄目ですっ☆」
		ENDIF
	ENDIF
ENDIF
;=== AZUSA MISSING COMMAND TRIAL END ==='''


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
