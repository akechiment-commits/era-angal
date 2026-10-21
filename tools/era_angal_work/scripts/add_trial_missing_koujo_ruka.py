from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_09_月永るか_COM.ERB")
START = ";=== RUKA MISSING COMMAND TRIAL START ==="
END = ";=== RUKA MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_9"


BLOCK = r''';=== RUKA MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ほ、ほかの子とキスするぼくを見たいなんて、先輩も倒錯してますね……。でも、あとでぼくの唇を取り返してくれるなら、いいです」
		ELSEIF A == 1
			PRINTFORMW 「ん、ちゅ……。（不思議。触れてるのはこの子なのに、頭のなかでは先輩に聞かせる言葉ばかり探してる）」
		ELSE
			PRINTFORMW 「これは裏切りの口づけじゃなくて、物語の途中にある寄り道です。ぼくが最後に帰る場所は……先輩ですから」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ええっ、キス!?　ぼくの個人的空間に、いきなり最接近イベントが発生してる～っ！」
		ELSEIF A == 1
			PRINTFORMW 「あ、相手の子も緊張してる……。じゃあ同盟を結ぼう？　せぇので目を閉じれば、たぶん怖くないよ」
		ELSE
			PRINTFORMW 「ん……。えへへ、思ってたより柔らかいんだね。こういう発見なら、未知との遭遇も悪くないかも♪」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 9, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%と同じリズムで先輩を挟むと、三人でひとつの曲みたい……。ぼく、この演奏なら舞台に立ってもいいです」
		ELSEIF A == 1
			PRINTFORMW 「先輩の吐息が強くなるところをサビにしよう。%LOCALS%、次はもう少し速く……あっ、ぼくまで擦れて、声が入っちゃった」
		ELSE
			PRINTFORMW 「元・敵同士のぼくたちが、こんな共同制作をするなんて運命は奇妙ですね。……先輩、ちゃんとぼくの脚も感じてくださいよ？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%、四拍ずつ交代しよう。ぼくはステージ苦手だけど、裏でリズムを支えるのは得意なんだよ♪」
		ELSEIF A == 1
			PRINTFORMW 「あっ、三人の動きがぴったり合った……！　先輩、今の顔もう一回見たい。%LOCALS%、同じところからいこう？」
		ELSE
			PRINTFORMW 「ぼくの脚、ちっちゃくてもちゃんと役に立ってる……えへへ♪　%LOCALS%、先輩をもっと喜ばせようよ」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：るかと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 9, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の震えが、なかからぼくの言葉を揺らしてる……っ。詩にするより先に、声で全部伝わっちゃうね……！」
		ELSEIF A == 1
			PRINTFORMW 「ふたりで同じ波に乗ってる……んあっ！　%LOCALS%、次はぼくから返すよ。ちゃんと受け取って……！」
		ELSE
			PRINTFORMW 「ぼくの内側が、%LOCALS%にだけ繋がってる……。ひゃぁっ、もっと奥まで、ぼくたちの秘密にして……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ、%LOCALS%が動くとこっちまで響く！　これが禁断の共鳴現象……ちょっと格好いいかも！」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%、ぼくの顔を見てタイミングを合わせて。せぇの……ひゃんっ！　あは、ふたりとも同時に跳ねた♪」
		ELSE
			PRINTFORMW 「声を我慢すると相手の音が聞こえないよ。ぼくも出すから、%LOCALS%もそのまま聞かせて……んっ！」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ぼくの身体がつくったものを先輩が飲んでくれる……。えへへ、言葉じゃない贈りものも、ちゃんと届くんですね」
		ELSEIF A == 1
			PRINTFORMW 「んっ、吸われるたび胸から力が抜けて、先輩のなかへ移っていくみたい。もっと元気になってください♪」
		ELSE
			PRINTFORMW 「これは月永るか特製の秘密の霊薬です。効能は……ぼくから離れたくなくなること、だったらいいなぁ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「こ、これを飲む勇気があるんですか？　ふふふ、何が起きても知りませんよ……たぶん栄養があるだけですけど♪」
		ELSEIF A == 1
			PRINTFORMW 「あっ、本当に飲んでる……。ぼくのちっちゃい胸にも、こんな役目があったんですね。ちょっと誇らしいかも」
		ELSE
			PRINTFORMW 「お味はどうですか？　感想を詩にしてくれたら、ぼくが曲名をつけてあげますよ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩の指が押すたび、白い言葉が一滴ずつ出てくるみたい……。全部集めたら、ぼくの気持ちまで読めますか？」
		ELSEIF A == 1
			PRINTFORMW 「あっ、そこ上手……♪　ぼくより先輩のほうが、ぼくの身体の扱いを知ってるみたいで少し悔しいです」
		ELSE
			PRINTFORMW 「急がなくていいですよ。こうして先輩に大事に触ってもらう時間、ぼくはけっこう好きですから」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「これは錬金術の採取工程……と考えれば恥ずかしくない！　先輩、笑ったら呪いますからね？」
		ELSEIF A == 1
			PRINTFORMW 「わっ、ちゃんと出た！　身体って、ぼくの知らない仕掛けがいっぱいあるんですね。もう一回やってみます？」
		ELSE
			PRINTFORMW 「力で握るより、指の腹でゆっくり……そう、それです。えへへ、ぼくたち共同研究者みたい♪」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩、そこ、ぼくの言葉が消え……ひゃぁっ！　詩も何もいらない、もっとぉ……！」
		ELSEIF A == 1
			PRINTFORMW 「絶対不可侵領域、完全陥落……っ。先輩になら、奥までぜんぶ、んあぁっ……！」
		ELSE
			PRINTFORMW 「すき、先輩……っ、指が来るたび身体で返事しちゃう……ひゃぅ、また答えさせてぇ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃぁっ!?　そ、そこだけ感覚が違う！　先輩、もう一回……あっ、心の準備はまだぁ！」
		ELSEIF A == 1
			PRINTFORMW 「頭では次の言葉があるのに、そこ押されると全部まっ白……んあっ！　これじゃ作詞できないよぉ！」
		ELSE
			PRINTFORMW 「逃げるつもりだったのに、腰が指を追ってる……っ。ぼ、ぼくの身体、いつから先輩の仲間になったの!?」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「封印は破れました。でも、先輩の前から逃げなかったぼくは少し格好いい……そういう詩にしてもいいですか？」
		ELSEIF A == 1
			PRINTFORMW 「身体が勝手に決めた結末でも、先輩の手を握るかはぼくが決めます。……だから、こっちは離さないで」
		ELSE
			PRINTFORMW 「こんな瞬間まで先輩と一緒なら、もう何を隠して格好つければいいんでしょうね。えへへ……無敵になった気分です」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ぼくの結界が水属性になって崩壊中～っ！　うう、せめて最後まで設定を守らせてください！」
		ELSEIF A == 1
			PRINTFORMW 「これは敗北じゃなくて、身体による突然の反乱です！　反乱軍の鎮圧は……む、無理なので見届けてくださいっ！」
		ELSE
			PRINTFORMW 「あとで今日のことを詩にします。恥ずかしい記憶も作品にできたら、ぼくの勝ちですからね！」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：るかと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 9, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%の胸から鼓動が伝わる……。ふたりの間だけで鳴ってる伴奏みたい。もう少し近くで聞かせて」
		ELSEIF A == 1
			PRINTFORMW 「んっ、先っぽが重なるたび同じ音が出るね……♪　%LOCALS%、次はもっとゆっくり響かせよう？」
		ELSE
			PRINTFORMW 「ひとりぶんの距離は欲しいはずなのに、%LOCALS%が入ってくるとあったかい。……今はもっと近くていいよ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ちっちゃい胸同士でも、ちゃんと合う場所はあるんだね。%LOCALS%、ぼくたち相性いいかも♪」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、そこが擦れると胸の奥まで響く……！　音がしないのに、すごく賑やかな感じ」
		ELSE
			PRINTFORMW 「%LOCALS%、顔を隠さなくていいよ。ぼくも同じくらい赤いし、ふたりなら恥ずかしさも半分だもん」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：るかはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 9, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%が先輩の顔を隠しても、ぼくはなかから繋がってる……んあっ！　先輩、そこで深く返事しないでぇ！」
		ELSEIF A == 1
			PRINTFORMW 「上では%LOCALS%、腰にはぼく……先輩を封印する陣の完成です。ひゃぁっ、下から術者を攻撃するのは反則ぅ！」
		ELSE
			PRINTFORMW 「顔が見えないぶん、先輩のがなかで動くたび全部伝わる……っ。ぼく、もっと上手に乗るから、ちゃんと感じて……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%が動くと先輩の腰まで揺れて、ぼくの奥に……ひゃんっ！　三人の共鳴、威力が高すぎるよぉ！」
		ELSEIF A == 1
			PRINTFORMW 「ぼくが上でリズムをつくります！　%LOCALS%はそのまま……あっ、先輩だけ勝手に裏拍を入れないでぇ！」
		ELSE
			PRINTFORMW 「ステージなら同時進行も支えられるのに、入ったままは無理ぃ……！　んあっ、奥が鳴るたび脚まで震える……！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：るかがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「ぼくの絶対不可侵領域へ、先輩だけ特別入場です。今日はここで、好きなだけ休んでください……なでなで♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩の髪を撫でてると、言葉にしなくても好きって伝えられる気がします。作詞家としては敗北ですけど……嬉しい敗北です」
		ELSE
			PRINTFORMW 「元・敵だったぼくに、こんな無防備な顔を見せるんですね。えへへ、もう裏切れませんよ……ずっと味方でいます」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あの転校生のひとが、ぼくの膝で静かにしてる……。ふふ、詩のモデルとしては今がいちばん扱いやすいです♪」
		ELSEIF A == 1
			PRINTFORMW 「歌詞が浮かぶまで、このまま撫でててもいいですか？　先輩の寝癖、何だか言葉になりそうなんです」
		ELSE
			PRINTFORMW 「ひとに触るの、前より怖くなくなりました。先輩が大人しく撫でられてくれるおかげかも……ありがとうございます♪」
		ENDIF
	ENDIF
ENDIF
;=== RUKA MISSING COMMAND TRIAL END ==='''


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
