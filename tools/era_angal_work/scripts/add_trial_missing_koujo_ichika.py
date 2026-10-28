from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_12_神樹いちか_COM.ERB")
START = ";=== ICHIKA MISSING COMMAND TRIAL START ==="
END = ";=== ICHIKA MISSING COMMAND TRIAL END ==="
ANCHOR = ";==============================================================\r\n; 処女喪失時  @CHAR_VIRGIN_12"


BLOCK = r''';=== ICHIKA MISSING COMMAND TRIAL START ===
; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）

;--- COM60 助手にキスさせる ---
IF SELECTCOM == 60
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ、ちゅ……えへへ。先輩、あたしが誰にキスしても余裕そうですね？　あとで先輩のほうを真っ赤にしてやるんだから♪」
		ELSEIF A == 1
			PRINTFORMW 「女の子の唇、やわらか～い……♪　でもあたしが帰ってくる場所は先輩の隣ですから、心配しなくていいですよ」
		ELSE
			PRINTFORMW 「ちゅっ……ふふ、成功♪　次は先輩の番です。あたし、ちゃんと二人分かわいがってもらいますからね？」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「えっ、あたしから!?　う、うひゃあ……よぉし、腹を括った！　目ぇ閉じて、いきますよ～っ！」
		ELSEIF A == 1
			PRINTFORMW 「ちゅ……わっ、ふたりとも同時に離れちゃった。あはは、タイミングまでおんなじだったね♪」
		ELSE
			PRINTFORMW 「そんなに構えなくても大丈夫だって。あたしだって緊張してるし……一緒に恥ずかしがれば、半分こでしょ？」
		ENDIF
	ENDIF
ENDIF

;--- COM62 ダブル素股 ---
IF SELECTCOM == 62
	CALL AITE_YOBI, 12, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、今のリズムでもう一回！　先輩の弱点、ふたりで完全攻略しちゃおう♪」
		ELSEIF A == 1
			PRINTFORMW 「先輩のが、あたしたちの腿の間でびくびくしてる……。えへへ、どっちの脚が好きでも逃がしませんよ？」
		ELSE
			PRINTFORMW 「ふたりに挟まれて嬉しそうですね、先輩♪　%LOCALS%、もっとぴったりくっついて仕上げちゃおう」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%、そっちはそっちの速さでいいよ。あたしが合わせるから……よし、コンボ繋がった♪」
		ELSEIF A == 1
			PRINTFORMW 「おわっ、先輩の腰が勝手に動いた！　あはは、ちゃんと効いてるってわかりやすいですね～？」
		ELSE
			PRINTFORMW 「あたしの腿だけじゃ足りなくても、%LOCALS%となら隙間なし！　先輩、降参するなら今ですよ♪」
		ENDIF
	ENDIF
ENDIF

;--- COM76 双頭バイブ ---
; 助手調教専用：いちかと女性助手の二人だけ
IF SELECTCOM == 76
	CALL AITE_YOBI, 12, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ、%LOCALS%の動き、こっちの奥まで来てる……♪　あたしからも返すね、ちゃんと受け取ってよ？」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、急に揺らさないでよ～！　……あはは、でも今のすごかった。もう一回だけ、せぇのでやろ？」
		ELSE
			PRINTFORMW 「%LOCALS%、もっと近くに来て。顔を見てれば、どっちが先に限界かすぐわかるから……♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ、片方を動かしたらこっちまでっ!?　%LOCALS%、交代で操作したほうが面白そうじゃない？」
		ELSEIF A == 1
			PRINTFORMW 「んぅ……%LOCALS%の腰使い、意外とうまいね。あたしも負けないから、次はこっちの番っ♪」
		ELSE
			PRINTFORMW 「ふたり同時に変な声出た……あははっ！　こうなったら笑ったほうの負けね。続き、いくよ？」
		ENDIF
	ENDIF
ENDIF

;--- COM78 母乳飲み ---
IF SELECTCOM == 78
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「先輩、そんなに夢中で飲むんだ……。えへへ、あたしにしかあげられないものって、ちょっと嬉しいですね♪」
		ELSEIF A == 1
			PRINTFORMW 「んっ、吸われると胸の奥まできゅうって……。先輩、あたしのこと好きなら、残さず飲んでくださいね？」
		ELSE
			PRINTFORMW 「ほら、こっちもまだありますよ。あたしが抱いててあげるから、先輩は甘えるのに専念すること♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「ほ、本当に飲むんですか？　うぅ、見られるより吸われるほうが恥ずかしいんですけど……飲むなら堂々とどうぞっ！」
		ELSEIF A == 1
			PRINTFORMW 「ふぁっ、舌そこ……！　先輩、飲みかた上手すぎません？　あたしのほうが変になりそうなんですけどっ」
		ELSE
			PRINTFORMW 「おいしいですか？　ふふん、先輩のその顔なら高評価ってことでいいですよね♪」
		ENDIF
	ENDIF
ENDIF

;--- COM79 乳搾り ---
IF SELECTCOM == 79
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「んっ、そこ押されると一気に出る……。先輩、あたしの反応見て楽しんでません？」
		ELSEIF A == 1
			PRINTFORMW 「わっ、今の一押しで一気に増えた！　先輩、レア演出引いたみたいな顔してますよ♪」
		ELSE
			PRINTFORMW 「一滴ずつ増えるの見てると、ゲージ溜めてるみたい。先輩、満タンまで途中で手ぇ止めないで♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「押されるたび瓶の中身が増えてく……これ、進捗バーならもっとわかりやすいのになぁ」
		ELSEIF A == 1
			PRINTFORMW 「ひゃっ、強すぎ！　ボタン連打じゃないんだから、指一本ずつ優しくお願いしますっ」
		ELSE
			PRINTFORMW 「あはは、思ったより勢いあるなぁ。先輩、ぼんやりしてると次も顔に当たりますよ？」
		ENDIF
	ENDIF
ENDIF

;--- COM84 Gスポット刺激 ---
IF SELECTCOM == 84
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「そこっ、先輩そこぉ……！　だめ、あたし、すぐ負けちゃうっ……！」
		ELSEIF A == 1
			PRINTFORMW 「んぁっ、指だけで奥までっ……先輩、もう、止めないで……！」
		ELSE
			PRINTFORMW 「せんぱい、好きっ……そこ触られると、何も考えられないぃ……！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃあっ!?　な、何そこっ、身体が勝手に跳ねるんですけど！」
		ELSEIF A == 1
			PRINTFORMW 「待って、今の反則っ……んぁっ！　先輩、同じところばっかりぃ……！」
		ELSE
			PRINTFORMW 「ひぁっ、脚に力入らない……！　でも、あと一回だけっ……そこ！」
		ENDIF
	ENDIF
ENDIF

;--- COM86 強制放尿 ---
IF SELECTCOM == 86
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「あぁもう、止まんない……！　先輩には格好つけても無駄ですね。最後までちゃんと見ててくださいっ」
		ELSEIF A == 1
			PRINTFORMW 「こんなのまで受け止めて笑ってるんだもん……。先輩、あたしのこと好きすぎでしょ。えへへ♪」
		ELSE
			PRINTFORMW 「ふぁ……全部出たら、すっごくすっきりしました。先輩の前なら、もう開き直って満点ですっ♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うわっ、待って、ほんとに出たぁ!?　あぁもう、こうなったら止めようとするほうが負けですっ！」
		ELSEIF A == 1
			PRINTFORMW 「うひゃあ、音までしっかり聞こえる～っ！　先輩、今のはリプレイ禁止ですからね！」
		ELSE
			PRINTFORMW 「よ、よぉし……出ちゃったものはしょうがない！　あたし、最後まで胸張っていきますからねっ」
		ENDIF
	ENDIF
ENDIF

;--- COM202 乳首合わせ ---
; 助手調教専用：いちかと女性助手の二人だけ
IF SELECTCOM == 202
	CALL AITE_YOBI, 12, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、もう少し強く押して……んっ、先っぽ同士が擦れると、胸の奥までじんじんするね♪」
		ELSEIF A == 1
			PRINTFORMW 「あたしたち、同じところで一緒に声出してる……。ふふ、%LOCALS%の顔見てるともっと熱くなるよ」
		ELSE
			PRINTFORMW 「離れたらもったいないでしょ？　このまま胸をくっつけて、どっちが先に震えるか勝負ね♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「うひゃっ、そこ同士は刺激強いって！　%LOCALS%、今度はもっとゆっくり擦ろう？」
		ELSEIF A == 1
			PRINTFORMW 「胸の大きさが違っても、先っぽはちゃんと当たるんだね。んっ、ほら、もう一回♪」
		ELSE
			PRINTFORMW 「%LOCALS%も照れてる？　あはは、あたしも同じ。せっかくだから笑って続けよっか♪」
		ENDIF
	ENDIF
ENDIF

;--- COM258 助手顔面騎乗 ---
; 視点：いちかはPLAYERと騎乗位を続け、助手がPLAYERの顔へ跨る
IF SELECTCOM == 258
	CALL AITE_YOBI, 12, ASSI
	LOCALS '= @"%RESULTS%"
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「%LOCALS%、上は任せたっ……あたしは先輩のここで……んぁっ、奥、突かれてるぅ！」
		ELSEIF A == 1
			PRINTFORMW 「顔が見えなくても、先輩がなかで暴れてる……！　ひゃぁっ、もっと、下からっ……！」
		ELSE
			PRINTFORMW 「先輩、あたしを置いて%LOCALS%に夢中にならないで……んっ！　こっちも、もっと動いてぇ！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「%LOCALS%が腰を動かすたび、先輩まで揺れて……ひぁっ、奥に当たるっ！」
		ELSEIF A == 1
			PRINTFORMW 「あたしが上の操作担当……って、うひゃぁっ！　先輩、勝手に突きあげないでっ！」
		ELSE
			PRINTFORMW 「上も下も忙しそうですね、先輩……んぁっ！　なのに、あたしのなかでは全然鈍ってないっ！」
		ENDIF
	ENDIF
ENDIF

;--- COM318 頭を撫でてもらう ---
; 視点：いちかがプレイヤーの頭を撫でる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「よしよし♪　いつも頑張ってる先輩には、あたしから特別ボーナスです。眠るまで撫でてあげますね」
		ELSEIF A == 1
			PRINTFORMW 「先輩の髪、こうして触ると安心します。あたしが守ってあげられるもの、ちゃんとここにあるんだなって♪」
		ELSE
			PRINTFORMW 「えへへ、今日は先輩が甘える番。あたしのお膝、恋人限定のセーブポイントですからね♪」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「先輩、お疲れ顔してますよ。ほら、頭こっち。あたしだって人を休ませるくらいできますから」
		ELSEIF A == 1
			PRINTFORMW 「撫でられると大人しくなるんですね～？　ふふん、先輩の攻略法をひとつ見つけちゃった♪」
		ELSE
			PRINTFORMW 「よ～しよし。あはは、こんな先輩をみんなに見せたら驚くだろうなぁ。今だけ内緒にしときますね」
		ENDIF
	ENDIF
ENDIF
;=== ICHIKA MISSING COMMAND TRIAL END ==='''


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
