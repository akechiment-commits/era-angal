from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_05_桃智あすか_COM.ERB")
START = ";=== ASUKA MISSING COMMAND TRIAL START ==="
END = ";=== ASUKA MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_5"


BLOCK = r''';=== ASUKA MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩、開始の合図はまだっすか？　……って、キスに笛なんか要らないっすね。あたしから行ってくるんで、ちゃんと見ててください♪」
		ELSEIF A == 1
			PRINTFORMW 「ん、ちゅ……。相手の子、肩に力入りすぎっすね。ほら、あたしに掴まっていいっすよ。先輩はちょっと待っててください」
		ELSE
			PRINTFORMW 「ヤキモチ妬いたなら、黙ってないで取り返しに来てくださいよ。あたし、先輩に追いかけてもらうのも好きっすから♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃ、いきなり本番っすか!?　よし、相手の子が怖がる前にあたしから行くっす。歯だけはぶつけないように……！」
		ELSEIF A == 1
			PRINTFORMW 「んむっ……おわっ、鼻が当たった！　あはは、ふたりして勢いよすぎっすね。今度はゆっくり近づくっすよ」
		ELSE
			PRINTFORMW 「キスに勝ち負けはないっすけど、先に照れて逃げたほうが負けっす。うにに、その顔ならいい勝負になりそうっすね♪」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 5, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、左右から挟んで速攻っすよ！　……うひゃっ、先輩まで急に腰を出したら、作戦が崩れるっす～！」
		ELSEIF A == 1
			PRINTFORMW 「先輩、ふたりの脚に挟まれて嬉しそうっすね？　うにに、あたしのほうを見てないと、その顔こっちに向けるっすよ♪」
		ELSE
			PRINTFORMW 「あっ、太ももの間で先輩のが跳ねて……%LOCALS%の脚まで擦れるっす。これ、あたしもけっこう響くんすけど……っ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ダブルチームなら得意っす！　%LOCALS%、せぇので……って、先輩がフェイント入れるのは反則っすよ～!?」
		ELSEIF A == 1
			PRINTFORMW 「うにに、もっとテンポ上げるっすよ！　……おわっ、脚が絡まった！　ちょ、ちょっとタイムっす～！」
		ELSE
			PRINTFORMW 「%LOCALS%、そっち力入りすぎっす！　あたしも押し返すと先輩が潰れそうだし……三人競技って難しいっすね!?」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
IF SELECTCOM == 76
	CALL AITE_YOBI, 5, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、先に動いたほうが先制点っすよ……ひゃぁっ!?　そっちの動き、あたしのなかまで一気に来るっす……！」
		ELSEIF A == 1
			PRINTFORMW 「あっ、待って、そんな速くされたら……っ！　あたし、全力勝負は好きだけど、これ、身体が追いつかな……ひゃぁっ！」
		ELSE
			PRINTFORMW 「%LOCALS%、手ぇ貸して……。一緒に揺れてるの、嬉しいのに……なか、また締まって、あたし立てないっす……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃぁっ、%LOCALS%が動いたぶん、全部こっちにも返ってくるっす！　聞いてないっすよ、こんなの～！」
		ELSEIF A == 1
			PRINTFORMW 「ちょ、いったんタイムっす！　呼吸を整えて……あっ、そこで動かしたらタイムの意味ないっすぅ！」
		ELSE
			PRINTFORMW 「ご、ごめん%LOCALS%、あたしが力んだらそっちまで引っぱられるっすね……！　でも抜いたら負けな気がするっす～！」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩、そんな夢中で飲むんすね……。あたしの身体で先輩を元気にできるなら、何だかすっごく嬉しいっす♪」
		ELSEIF A == 1
			PRINTFORMW 「吸われるたび、胸の奥がきゅってするっす。いつもの元気、先輩にぜんぶ持ってかれそうっすね……えへへ」
		ELSE
			PRINTFORMW 「練習のあとの水分補給みたいに一気飲みは駄目っすよ？　今日はあたしが、先輩のペースを見てあげるっす♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「え、直接飲むんすか!?　うひゃあ、あたしは逃げないっすけど……先輩のほうが思い切りよすぎっす！」
		ELSEIF A == 1
			PRINTFORMW 「んっ、そこ吸われると、思ったより力が抜けるっす……。これ、立ったままじゃ膝が危ないやつっすね」
		ELSE
			PRINTFORMW 「味、変じゃないっすか？　まずくても一気に飲んで誤魔化さないで、ちゃんと言ってほしいっすよ～？」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩の手、意外と丁寧っすね。もっと乱暴に来ると思って、あたしも受けて立つ気だったんすけど……♪」
		ELSEIF A == 1
			PRINTFORMW 「うひゃ、搾るたびに出るっす……！　そんな真剣に集められると、あたしのほうが先に照れるっすよぉ」
		ELSE
			PRINTFORMW 「先輩が欲しいなら、最後までちゃんと搾っていいっす。途中で投げだすの、あたし嫌いっすからね？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにに……あたしの胸を搾るのに、そんな集中力を発揮しないでほしいっす。見てるほうが恥ずかしいっすよ！」
		ELSEIF A == 1
			PRINTFORMW 「痛っ、そこは力任せじゃ駄目っす！　ボールと同じで、握ればいいってもんじゃないっすよ～！」
		ELSE
			PRINTFORMW 「おわっ、容器いっぱいになりそうっす！　あたしが持つと絶対こぼすんで、先輩は手を離さないでほしいっす！」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「笑って耐えるつもりだったのに……ひゃぁっ、そこ来ると、あたしの声ぜんぶ裏返るっす……！」
		ELSEIF A == 1
			PRINTFORMW 「先輩の指一本に負けるとか悔しい……っ。でも、もっとって言うのも悔し……あぁっ、もう、もっとぉ！」
		ELSE
			PRINTFORMW 「好きなひとに、こんな声出させられるの……ずるいっす。あたしも先輩を、同じくらい滅茶苦茶にしたいのにぃ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「のわぁっ!?　脚に力入れてたのに、腰だけ勝手に跳ねたっす！　あたしの身体、誰のチームなんすかぁ！」
		ELSEIF A == 1
			PRINTFORMW 「次どこに来るか目で追えても、避けられないっす……！　ひゃぁっ、フェイントなしでも無理ぃ……！」
		ELSE
			PRINTFORMW 「うひゃぁっ、ちょっと待って、笑えないくらい気持ちいいっす……！　あたし、こんな顔するんすね……っ」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「試合なら汗だくでも平気なのに、これは駄目っす……。先輩の前で、自分の身体に負けるのがこんな悔しいなんて……っ」
		ELSEIF A == 1
			PRINTFORMW 「先輩、『あと少し』って言ってください。止められなくても、先輩の声があれば最後まで踏んばれる気がするっす……！」
		ELSE
			PRINTFORMW 「身体は勝手に降参してるけど、あたしはまだ負けてないっす。先輩から逃げないでいられたら、それはあたしの勝ちっすよね……？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ、全力で締めても止まらないっす！　根性でどうにもならない勝負を持ちこむなんて、反則っすよぉ！」
		ELSEIF A == 1
			PRINTFORMW 「こんなの勝ち負けじゃないってわかってるのに……あたし、自分に負けたみたいで腹立つっす。笑うなら盛大に笑ってください！」
		ELSE
			PRINTFORMW 「黙って気まずそうにされるのが一番きついっす！　先輩、何でもいいからいつもの調子でツッコんでくださいよぉ！」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
IF SELECTCOM == 202
	CALL AITE_YOBI, 5, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、胸のサイズで勝負する気っすか？　うにに、負けてもこうして抱きつけるなら、あたしは嬉しいっすよ♪」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、先っぽ同士で擦れると、思ったより来るっすね……。%LOCALS%の顔も近くて、そっちのほうがドキドキするっす」
		ELSE
			PRINTFORMW 「あたし、立派な胸には憧れるっすけど……今は%LOCALS%のが好きっす。比べるより、もっとくっついてたいっすよ」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「胸と胸で1on1っすね！　……って、顔までこんな近いとは聞いてないっす。ちょっと照れるっすよ～！」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%、そこ擦れるとぞくっとするっすね。強く押すより、ゆっくりのほうが効くみたいっす……」
		ELSE
			PRINTFORMW 「おわっ、張り切って押したらずれたっす！　ごめん%LOCALS%、痛くなかったっすか？　次は合わせるっすよ」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
IF SELECTCOM == 258
	CALL AITE_YOBI, 5, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩、顔が見えなくてもあたしのリズムはわかるっすよね……！　%LOCALS%に気を取られたら、もっと深く乗るっす……ひゃぁっ！」
		ELSEIF A == 1
			PRINTFORMW 「%LOCALS%に上を取られても、先輩の腰はあたしが独占っす……っ。あぁっ、だから下から主導権を取り返さないでぇ！」
		ELSE
			PRINTFORMW 「あたしが先に音を上げると思ってるっすか……？　んあぁっ、思ってて正解っす、もう腰が勝手にぃ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「のわっ、%LOCALS%が乗った衝撃まで先輩の腰から来るっす！　三人ぶんの勢い、全部あたしで受けろってことっすか!?」
		ELSEIF A == 1
			PRINTFORMW 「顔を塞がれた先輩と、声だけで連携するっす！　あたしが三回動いたら……うひゃっ、勝手に突いたら作戦中止っすぅ！」
		ELSE
			PRINTFORMW 「バランスは崩しても先輩からは降りないっすよ……！　あっ、奥そこ、今のは反則、ほんとに落ちるっすぅ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：あすかがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「今日は時間制限なしっす。先輩の肩から力が抜けるまで、あたしの手はどけないっすよ……よしよし♪」
		ELSEIF A == 1
			PRINTFORMW 「いつもはあたしが先輩の胸に飛びこむ側っすけど、逆も大歓迎っす。頭くらい、いくらでも預けてください」
		ELSE
			PRINTFORMW 「お返しだから撫でるんじゃないっす。あたしが先輩に触ってたいから撫でてるんすよ。そこ、間違えないでくださいね？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うにに、先輩のつむじ発見っす。普段は上から見る機会ないんで新鮮っすね。もうちょっとだけ観察させてください♪」
		ELSEIF A == 1
			PRINTFORMW 「いつもあたしを受け止めてくれるお礼っす。今日は先輩が倒れても、あたしがちゃんと支えるっすからね？」
		ELSE
			PRINTFORMW 「動かないでください、髪が跳ねてるっす。……うにに、こうして静かにしてる先輩も、何だかかわいいっすね」
		ENDIF
	ENDIF
ENDIF
;=== ASUKA MISSING COMMAND TRIAL END ==='''


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
