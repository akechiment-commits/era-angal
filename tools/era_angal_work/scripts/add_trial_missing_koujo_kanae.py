from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_01_三善かなえ_COM.ERB")
START = ";=== KANAE MISSING COMMAND TRIAL START ==="
END = ";=== KANAE MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_1"


BLOCK = r''';=== KANAE MISSING COMMAND TRIAL START ===
; 試作：未実装10コマンド（ユーザー指定どおり、恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「……転校生さん。私が誰と口づけても平気な顔をなさるのですね。では後で、きっちり同じだけ返していただきます」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%、目を閉じてください。私も閉じます。……転校生さんの顔を見たままでは、たぶん最後までできませんから」
		ELSE
			PRINTFORMW 「一度だけ、の予定だったのですが……。転校生さんが止めないなら、これは命令の範囲内と解釈しても？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%、先に謝っておきます。嫌という意味ではなく、こういう距離に慣れていないだけです。……では、三秒で」
		ELSEIF A == 1
			PRINTFORMW 「ちょっ、待ってください。心の準備に必要な時間を見積もって――ああもう、近いですって！」
		ELSE
			PRINTFORMW 「……終わりましたね。お互い、今のことを妙に意識しない。よろしいですか、%LOCALS%？」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	; 三人コマンドなので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 1, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、動きを合わせてください。転校生さんがどちらを見ているかは……いえ、今はどうでもいいです」
		ELSEIF A == 1
			PRINTFORMW 「いち、に……いち、に……。だ、駄目です、転校生さんが声を出すたびに数が飛んで……っ」
		ELSE
			PRINTFORMW 「私のほうが、あなたを気持ちよくできます。……そんな顔で笑わないでください、張り合っているのではなく、責任感です」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「三人で動けば効率が上がる、という理屈は理解しました。理解しましたが……密着しすぎでは、%LOCALS%？」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%、もう少しゆっくり……っ。転校生さんまで急かさないでください、私の脚は二本しかありません！」
		ELSE
			PRINTFORMW 「今の反応、どちらのせいでしょう。……確認のためにもう一度、という顔をしないでください」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
	; 助手調教専用なので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 1, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、呼吸を合わせましょう。私が乱れたら手を握って――いえ、最初から握っていてください。たぶん、すぐ無理になります」
		ELSEIF A == 1
			PRINTFORMW 「あなたが震えるたび、こちらの奥まで同じ波が返ってきて……。顔を見れば次がわかるぶん、余計に逃げられませんね」
		ELSE
			PRINTFORMW 「ま、待って、そこで速くするのは反則です……っ。私にも同じだけ返ると知って、やっていますね？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「同じ速さで動けば安定するはずです。では四拍ずつ――ひゃっ、いきなり裏拍を入れないでください！」
		ELSEIF A == 1
			PRINTFORMW 「仕組みとしては単純なのに、相手の顔が目の前にあるだけで……。これは計算外の要素がおおすぎます」
		ELSE
			PRINTFORMW 「私が先に音を上げるとお思いですか？　いいでしょう、どちらがリズムを崩すか勝負です」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そんなに安心した顔をされると、止められないではありませんか。……もっと欲しいなら、ちゃんと私を見て頼んでください」
		ELSEIF A == 1
			PRINTFORMW 「飲みこむたびに喉が動いて……ふふ、ほんとうに子供みたいです。今日だけは、私が甘やかしてあげますね」
		ELSE
			PRINTFORMW 「私の身体から出たもので、転校生さんが満たされる……。おかしな話なのに、どうしてこんなに嬉しいのでしょう」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あの、味の感想は結構です。改善できる類のものではありませんし……真剣な顔で飲まれるほうが困ります」
		ELSEIF A == 1
			PRINTFORMW 「少しずつにしてください、むせたら大変です。……どうして私が、こんなときまで世話を焼いているのでしょうね」
		ELSE
			PRINTFORMW 「転校生さん、そこまで名残惜しそうにされると、こちらまで何か悪いことをした気分になります。もう終わりです」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「受け皿を用意したのですか。準備が良すぎます……。私より楽しみにしていたみたいで、少し癪ですね」
		ELSEIF A == 1
			PRINTFORMW 「こぼさないように、などと考えていたのに……っ。あなたの手で触れられると、それどころではありません」
		ELSE
			PRINTFORMW 「こんなものまで大切そうに扱って。……転校生さんは、私から出たものなら何でも嬉しいのですか？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「待ってください、せめて布と容器を。後始末まで含めて計画しないと、絶対に惨事になります」
		ELSEIF A == 1
			PRINTFORMW 「牛のような扱いは心外です。……いま笑いましたね？　終わったら覚えていてください」
		ELSE
			PRINTFORMW 「量を数えるのはやめてください。記録にも残さないで。これは実験でも部活動でもありませんから！」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「っ、そこ……！　先に見つけたからといって、得意そうな顔をしないでください。私の身体なのに……くやしい」
		ELSEIF A == 1
			PRINTFORMW 「もう少し上、いえ、今のは助言では――ひゃっ！　わざと正解だけ拾いましたね、転校生さん！」
		ELSE
			PRINTFORMW 「反応を観察しないでください。あなたに知られてしまうと、次から隠し通せなくなるではありませんか……っ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「その一点だけ特別だという話は、半信半疑だったのですが……。わ、私の身体で立証しないでくださいっ」
		ELSEIF A == 1
			PRINTFORMW 「今の声は忘れてください。反射です、私の意思や評価とは一切関係ありません」
		ELSE
			PRINTFORMW 「十秒なら耐えられます。いち、に、さん――だ、駄目です、数えるほど長く感じます……！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「予定も手順も、身体が従うことを前提に組んでいたんですね……。転校生さん、こんな私まで想定内みたいな顔をしないでください」
		ELSEIF A == 1
			PRINTFORMW 「これは事故ではありません。ここに残ると決めたのは私ですから……せめて、その選択まで奪われたようには扱わないで」
		ELSE
			PRINTFORMW 「転校生さん、私の名前を呼んで。きちんと返事ができるあいだは、まだ私は私でいられます……っ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「中止条件はとっくに満たしています！　なのに止まらないなんて……こんな事態への対処手順、準備表のどこにもありません！」
		ELSEIF A == 1
			PRINTFORMW 「格好よく失敗する方法くらい、いつもなら考えつくのに……っ。これはただ屈辱的です。ですから、勝手に同情しないでください！」
		ELSE
			PRINTFORMW 「逃げません。以前の私なら途中で逃げたでしょうけど……ここまでさせた責任として、最後まで私の目を見ていなさい、転校生さん」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
	; 助手調教専用なので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 1, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「近いのは胸だけのはずなのに、%LOCALS%の鼓動まで伝わって……。そんなに静かに見つめないでください」
		ELSEIF A == 1
			PRINTFORMW 「少しずれています。%LOCALS%、こちらへ――ひゃっ。合った途端にそんな顔をするなら、直さなければよかったです」
		ELSE
			PRINTFORMW 「どちらが先に震えたかは不問にしましょう。……私は、あなたのせいだと確信していますけどね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「位置を合わせるだけなのに、どうしてこんなに難しいのでしょう。%LOCALS%、笑わず協力してください」
		ELSEIF A == 1
			PRINTFORMW 「相手の反応が直接返ってくるのですね……。なるほど、これは想定以上に落ち着きません」
		ELSE
			PRINTFORMW 「比較実験のように見ないでください。胸の大きさも、反応の差も、検証項目には含まれません！」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
	; 三人コマンドなので、呼びかけ先を助手に切り替える
	CALL AITE_YOBI, 1, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生さん、私の下で%LOCALS%ばかり構うのは不公平です。……こちらにも、手を伸ばせるでしょう？」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%と目が合うたび、何をしているのだろうと思います。なのにあなたが動くと、考える余裕まで奪われて……っ」
		ELSE
			PRINTFORMW 「三人ぶんを受け止めるつもりですか。ほんとうにお人好しで、欲張りなひと……。なら私のことは、最後まで落とさないでください」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%、そこで身を乗り出すと均衡が――ひゃっ！　だから動く前に合図をしてください！」
		ELSEIF A == 1
			PRINTFORMW 「上と下で別々に動かれたら、調整役が必要です。……なぜ私を見るのです、そんな役まで引き受けませんよ」
		ELSE
			PRINTFORMW 「転校生さん、無事ですか？　返事ができないのは承知しています。せめて手を二回叩いて――あっ、そこは叩かなくて結構です！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：かなえがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「何があったか、言いたくなるまで聞きません。……その代わり、私の手から逃げないでくださいね、先輩」
		ELSEIF A == 1
			PRINTFORMW 「あの日、泣いていた私を見つけてくれたでしょう。今日は私の番です。肩車は無理ですが、これぐらいなら」
		ELSE
			PRINTFORMW 「頼られるのは、嫌いではありません。とくにあなたになら……。ですから、もうすこしだけこのままでいなさい」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「事情の説明は三十秒で――いえ、今は結構です。落ち着いてから、順番に聞かせてください」
		ELSEIF A == 1
			PRINTFORMW 「ぴこちゃんや妹にも、こうするとすこし大人しくなるんです。転校生さんにも効くとは思いませんでした」
		ELSE
			PRINTFORMW 「一度だけですよ。……もう一度？　仕方ありませんね、今日だけ特別です」
		ENDIF
	ENDIF
ENDIF
;=== KANAE MISSING COMMAND TRIAL END ==='''


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
