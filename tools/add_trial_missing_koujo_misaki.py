from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_08_丸子みさき_COM.ERB")
START = ";=== MISAKI MISSING COMMAND TRIAL START ==="
END = ";=== MISAKI MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_8"


BLOCK = r''';=== MISAKI MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「『ここで丸子みさき、まさかのキス～！』……先輩、実況してる場合じゃないって顔ですね？　妬いてるなら、あとで素直に言ってください♪」
		ELSEIF A == 1
			PRINTFORMW 「ん、ちゅ……。こ、これはラブじゃなくて交流です、交流！　（先輩の視線が熱い。嬉しいとか思うな、あたし～っ！）」
		ELSE
			PRINTFORMW 「相手の子に失礼だから、キス中はちゃんとそっちを見る。終わったら一番に先輩を見る……これなら公平ですよね？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「はいっ、突然ですがキスのお時間です☆　……って進行表にないんですけど!?　まぁ、やるなら楽しくいきましょ！」
		ELSEIF A == 1
			PRINTFORMW 「んむっ……あはは、ふたりとも目ぇ開けてた！　これじゃ照れ顔の観察会だよ。次はちゃんと閉じよっか？」
		ELSE
			PRINTFORMW 「そんなに固くならなくていいって。あたしも初めてみたいなもんだし、上手くいかなかったら一緒に笑おうよ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 8, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「『左右から息の合った攻め、先輩は逃げ場なし～！』……%LOCALS%、もう少し寄って。せっかくなら最高の放送……じゃなくて、最高の気分にしよ♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩、どっちが上手か採点は禁止ですよ？　（でも一番はあたしって言わせたい。競争じゃなくても、そこだけは譲れないっ！）」
		ELSE
			PRINTFORMW 「%LOCALS%と脚が触れるたび、先輩のがあたし側へ跳ねて……んっ。ふたり相手でも、あたしのこと見失わないでくださいね……？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%、あたしが合図するね。『いち、に、いち、に』……おぉっと先輩だけテンポアップ、現場が混乱しております！」
		ELSEIF A == 1
			PRINTFORMW 「三人の呼吸が合うと、ちょっと気持ちいいかも……♪　はい先輩、その調子！　%LOCALS%も笑ってないで動くっ！」
		ELSE
			PRINTFORMW 「息も笑い声も混ざって、三人で遊んでるみたい……♪　このまま誰が先に音を上げるか、最後までいきましょ☆」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：みさきと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 8, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の吐息、すぐそこ……っ。動く前から次が伝わるね。んあっ、もっと声聞かせて……あたしも返すから！」
		ELSEIF A == 1
			PRINTFORMW 「あたしが一回、%LOCALS%が一回……ひゃぁっ！　交互にしたら休めると思ったのに、奥ではずっと続いてるぅ……！」
		ELSE
			PRINTFORMW 「『ふたりの鼓動がひとつに――』なんて綺麗に言えな、あぁっ！　%LOCALS%、今の動きもう一回……っ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%が動くたび、あたしの余裕がどんどん消えてく～っ！　ひゃぁ、これほんとに声が隠せない！」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%、顔を見ればタイミングわかるよ。せぇの……んあっ！　あは、成功したけどふたりともすごい顔っ！」
		ELSE
			PRINTFORMW 「勝負じゃないから、先に止まっても負けじゃないよ。あたしはまだ……ひゃぅっ、続けたいけど、%LOCALS%はどう？」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ちいさな胸でも、先輩ひとりを満たすぶんはあるんですね。……ふふ、今日のこれは先輩だけの限定配信です♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ、吸う音まで聞こえる……。いつもは声を届けるあたしが、先輩に中身まで受け取ってもらうの、何だかいいなぁ」
		ELSE
			PRINTFORMW 「もっと飲んでいいですよ。先輩が頼ってくれるなら、たまにはあたしが支える側になったっていいでしょ？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「え、ここから直接!?　取材対象との距離が近すぎます！　……でも先輩、もう飲む気満々ですね。どうぞっ！」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、吸われると奥まできゅっとする……！　（胸の大きさより反応の大きさが問題だよ、あたし～っ！）」
		ELSE
			PRINTFORMW 「感想は正直にお願いしますね。放送部員はリスナーの声を大事にしますから……って、飲みながら返事は無理か♪」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩の手、思ったよりずっと丁寧……。あたし、任せるの苦手なんですけど、こういう任せかたなら悪くないかも」
		ELSEIF A == 1
			PRINTFORMW 「あっ、今ぴゅって出た！　そんな嬉しそうな顔されたら、あたしまで『もっと』って思っちゃうじゃないですか♪」
		ELSE
			PRINTFORMW 「いつも働きすぎって言われるあたしを、先輩が手入れしてくれてるみたい。……今日くらいは全部お願いします」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「そんな真剣な顔であたしの胸を搾るひと、学院広しといえど先輩くらいですよ。もう、笑えてきちゃった♪」
		ELSEIF A == 1
			PRINTFORMW 「そこを指で押すと出るんですね……おぉ、身体の仕組みって面白い！　あっ、取材みたいに観察しすぎないでくださいよ!?」
		ELSE
			PRINTFORMW 「先輩、黙って手元へ集中しすぎです。痛くないかとか、気持ちいいかとか、あたしにも聞いてくださいよ？」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩、そこは放送禁止……ひゃぁっ！　だめ、声、ぜんぶ拾われる……もっと、そこぉ……！」
		ELSEIF A == 1
			PRINTFORMW 「ラブじゃなくて、リスペ……んあぁっ！　無理、好きっ、先輩の指すきぃ……！」
		ELSE
			PRINTFORMW 「（考えられない、でも止めてほしくない――）あぁっ、先輩、もう一回っ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ひゃあっ!?　今のどこ、あたしの声が勝手に跳ねた！　先輩、確認って顔でもう一回押さないでぇ！」
		ELSEIF A == 1
			PRINTFORMW 「だ、大丈夫です、まだ喋れ……んあっ！　前言撤回、そこ続けたら何も説明できないですぅ！」
		ELSE
			PRINTFORMW 「人前に出るより緊張してるのに、身体は逃げるどころか指を追って……ひゃぅっ、それがあたしの本音みたいに見ないでぇ！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「放送事故なら音を切れますけど、先輩との時間は切りたくないです。……だからこれも、ふたりだけの記録にしてください」
		ELSEIF A == 1
			PRINTFORMW 「『丸子みさき、予想外の事態にも逃げません！』……先輩が受け止めてくれるなら、最後までここにいます」
		ELSE
			PRINTFORMW 「こんな姿で言うのも何ですけど、先輩に頼る練習だと思うことにします。あたし、何でもひとりでやろうとしすぎですから」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「緊急速報、丸子みさきの我慢が決壊しました～っ！　……自分で言うと少しだけ平気になるから、今は実況させてください！」
		ELSEIF A == 1
			PRINTFORMW 「くっ、こういうときまで先輩に気を遣わせたくない……！　いつもの調子でいてください、あたしもすぐ戻りますから！」
		ELSE
			PRINTFORMW 「終わったら、この件は編集で丸ごとカットです。あたしの記憶からは無理でも、先輩の口から外へ出すのは禁止っ！」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：みさきと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 8, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の鼓動、胸から直接聞こえる……。耳で聞くよりずっと近いね。あたしの音も伝わってる？」
		ELSEIF A == 1
			PRINTFORMW 「んっ、同じ場所が触れるたび、声まで重なる……♪　%LOCALS%、ふたりで綺麗な音にしよっか」
		ELSE
			PRINTFORMW 「大きさなんて比べなくていいからね。今は%LOCALS%のあったかさが伝われば、それで満点っ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「『本日のゲストと胸を合わせて親睦会～☆』……うわ、口に出すとすごい企画！　%LOCALS%、笑わないでよっ」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、先っぽ同士だと音もなく響く……。%LOCALS%も今ぞくってした？　顔に出てるよ♪」
		ELSE
			PRINTFORMW 「%LOCALS%、合わないなら角度を変えてみよ。せっかくだし、ふたりとも気持ちいい位置を探そうよ」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：みさきはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 8, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「『先輩の顔は%LOCALS%、腰はあたしが独占中～！』……ひゃぁっ、下から返事されたら、なか、深すぎますぅ！」
		ELSEIF A == 1
			PRINTFORMW 「顔が見えなくても、あたしが上で動いてるってわかりますよね……？　んあっ、先輩のそこ、あたしの奥ばっかり狙ってる……！」
		ELSE
			PRINTFORMW 「（%LOCALS%に妬いてる場合じゃない、あたし今すごい顔――）ひゃぁっ、先輩、腰で追いかけないでぇ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%が先輩の顔へ乗った衝撃、そのままあたしの奥へ直撃～っ！　んあぁ、説明する余裕もないですぅ！」
		ELSEIF A == 1
			PRINTFORMW 「先輩が息できてるか%LOCALS%に確認したいのに、下から突かれるたび言葉が……ひゃっ、途切れますぅ！」
		ELSE
			PRINTFORMW 「三人同時進行なんて台本にないですよぉ！　あっ、奥そこ……%LOCALS%、待って、あたしの腰が先に止まらないっ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：みさきがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ただいま放送終了、ここからは先輩ひとりだけの時間です。今日もお疲れさまでした……よしよし♪」
		ELSEIF A == 1
			PRINTFORMW 「あたしが先輩を甘やかしてるって、お嬢が知ったら驚くだろうなぁ。ふふ、これはふたりだけの秘密の休憩ですからね」
		ELSE
			PRINTFORMW 「頼るのが苦手なの、あたしだけじゃないんですね。じゃあ一緒に練習しましょ。今日は先輩が甘える番です♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「はい、働きすぎの先輩を確保～！　頭を撫でられてる間は次の仕事へ行っちゃ駄目ですからね？」
		ELSEIF A == 1
			PRINTFORMW 「髪、ちょっと乱れてますよ。あたし、こういう裏方仕事も得意なんです。じっとしててください♪」
		ELSE
			PRINTFORMW 「『本日の功労者には丸子みさきから、よしよし賞が贈られま～す☆』……あはは、先輩ほんとに嬉しそう！」
		ENDIF
	ENDIF
ENDIF
;=== MISAKI MISSING COMMAND TRIAL END ==='''


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
