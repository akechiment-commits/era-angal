# -*- coding: utf-8 -*-
"""
TRAIN_MESSAGE_REVMODE_ACTIVEPHASE 内の全体位における
- CASE 0 (キス)
- CASE 3 (胸愛撫)
- CASE 4, 5, 6, 7, 8 (全リアクション)
を完全に網羅し、地の文が絶対に出ない状態を解消する。
また、地の文内のキャラクターセリフ（「」）を完全に排除する。
"""

def get_complete_activephase():
    return '''@TRAIN_MESSAGE_REVMODE_ACTIVEPHASE(ARG:0, ARG:1)
#DIM DYNAMIC HEAT, 1
HEAT = TFLAG:108

SELECTCASE ARG:0
;キス
CASE 6
	SELECTCASE ARG:1
	;消極的にやる
	CASE 4
		PRINTFORML %CALLNAME:PLAYER%が戸惑いを見せる隙を逃さず、%CALLNAME:TARGET%は強引に唇を奪い、
		PRINTFORML 逃がさないように後頭部を押さえて濃厚に舌を絡め取った…
	;積極的にやる
	CASE 5
		IF HEAT >= 2
			PRINTFORML %CALLNAME:PLAYER%も自ら激しく舌を絡め返し、互いの唾液を飲み干し合うほど
			PRINTFORML 狂おしく熱烈なディープキスで求め合った…
		ELSE
			PRINTFORML %CALLNAME:PLAYER%は自らも%CALLNAME:TARGET%の口内に舌を侵入させ互いに舌を絡め合った…
		ENDIF
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%がもっと求めて唇を寄せると、%CALLNAME:TARGET%は愛おしそうに目を細め、
		PRINTFORML 息も継がせぬほど熱く情熱的なキスで応えてくれた…
	CASEELSE
		PRINTFORML 二人は熱い吐息を交わしながら、情熱的に唇を重ね合った…
	ENDSELECT

;手淫
CASE 30
	SELECTCASE ARG:1
	;快感に耐える
	CASE 6
		IF HEAT >= 2
			PRINTFORML %CALLNAME:PLAYER%が声を殺して快感に耐えようとするのを見て、%CALLNAME:TARGET%は嗜虐的な笑みを浮かべ、
			PRINTFORML 最も敏感な雁首のくびれを親指で執拗にグリグリと擦り上げて責め立てた…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は目を閉じて耐えようとする%CALLNAME:PLAYER%の下半身を押さえつけ、
			PRINTFORML 繰り返し弄ぶように陰茎のくびれを擦り上げた…
		ENDIF
	;快感を受け入れる
	CASE 7
		IF TFLAG:302
			PRINTFORML %CALLNAME:TARGET%は限界を迎えて腰を跳ね上げる%CALLNAME:PLAYER%を見つめ、
			PRINTFORML 激しいストロークで最後の一滴まで搾り取るように一気に絶頂へと導いた！
		ELSE
			IF HEAT >= 2
				PRINTFORML 快楽に身を委ねて喘ぐ%CALLNAME:PLAYER%の姿に、%CALLNAME:TARGET%は歓喜の表情を浮かべ、
				PRINTFORML 濡れた手のひらでビクビクと脈打つペニスを滑らせ、更なる高みへと誘っている…
			ELSE
				PRINTFORML %CALLNAME:TARGET%は腰を浮かせて快感をせがむ%CALLNAME:PLAYER%を上目遣いに見ながら
				PRINTFORML びくびくと痙攣する陰茎を手で弄んでいる…
			ENDIF
		ENDIF
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%がもっと気持ちよくしてほしいと哀願すると、
		PRINTFORML %CALLNAME:TARGET%はご褒美を与えるように微笑み、先走りを塗り広げながら極上の手つきで愛撫した…
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は手のひらの熱気と先走りを絡めながら、ペニスを丹念に擦り上げた…
	ENDSELECT

;フェラチオ
CASE 31
	SELECTCASE ARG:1
	;快感に耐える
	CASE 6
		IF HEAT >= 2
			PRINTFORML %CALLNAME:PLAYER%が歯を食いしばって堪えようとする姿に唆された%CALLNAME:TARGET%は、
			PRINTFORML 鈴口に舌先をねじ込み、喉奥の吸圧を高めて強引に快感を搾り取ろうとしている…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は息を止めて顔を背ける%CALLNAME:PLAYER%の下半身を抱え込み、
			PRINTFORML 雁首を唇で包み、声が漏れるまで執拗に裏筋を舐め上げた…
		ENDIF
	;快感を受け入れる
	CASE 7
		IF TFLAG:302
			PRINTFORML %CALLNAME:TARGET%は射精の予兆を感じ取るやいなやペニスを根元まで一気に飲み込み、
			PRINTFORML 喉奥を熱い精液で満たされながら、恍惚とした表情で激しく吸い上げた！
		ELSE
			IF HEAT >= 2
				PRINTFORML %CALLNAME:PLAYER%が快楽に声を漏らすたび、%CALLNAME:TARGET%は嬉しそうに目を細め、
				PRINTFORML 睾丸を優しく揉みながら、舌全体で陰茎を絡め取り、熱狂的にしゃぶり続けた…
			ELSE
				PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の睾丸を優しくもみほぐしながら、
				PRINTFORML 亀頭をチロチロと舌で刺激し間欠的に噴き上がる先走りを舐めとっている…
			ENDIF
		ENDIF
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%が頭を撫でて懇願すると、%CALLNAME:TARGET%は愛おしそうに上目遣いで見つめ、
		PRINTFORML 音を立てて亀頭を甘噛みし、じっくりと丹念に舐め清めるように奉仕した…
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は熱い口内でペニスを包み込み、激しく頭を前後に揺らして奉仕を続けた…
	ENDSELECT

;クンニする
CASE 61
	SELECTCASE ARG:1
	;快感に耐える
	CASE 6
		IF HEAT >= 2
			PRINTFORML %CALLNAME:PLAYER%がシーツを握りしめて耐えようとすると、%CALLNAME:TARGET%は執拗に陰核を舌先で弾き、
			PRINTFORML 声を漏らさずにはいられないほど激しく吸い付いて責め立てた…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は息を止めて顔を背ける%CALLNAME:PLAYER%の下半身を抱え込み、
			PRINTFORML 陰核を唇で包み、声が漏れるまで執拗に裏筋を舐め上げた…
		ENDIF
	;快感を受け入れる
	CASE 7
		IF HEAT >= 2
			PRINTFORML 快楽に腰を浮かせる%CALLNAME:PLAYER%を抑え込み、%CALLNAME:TARGET%は蜜に濡れた秘裂を押し開き、
			PRINTFORML 溢れる愛液を啜りながら、激しい舌使いで何度も絶頂へと追い詰めた…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の脚の付け根を大きく左右に開かせると、
			PRINTFORML 同時に陰核に吸い付いて舌で潰すように舐め始めた…
		ENDIF
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%が恥じらいながらももっと舐めてほしいとおねだりすると、
		PRINTFORML %CALLNAME:TARGET%は満足そうに微笑み、一番感じる部分に舌を集中させて貪り尽くした…
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は愛液に濡れた秘唇を舌先で丁寧に愛撫した…
	ENDSELECT

;シックスナイン
CASE 69
	SELECTCASE ARG:1
	;クンニ OR フェラする
	CASE 1, 2
		PRINTFORML %CALLNAME:PLAYER%も目の前の秘部に夢中で舌を伸ばし、
		PRINTFORML 互いに相手の性器を貪り合いながら、熱狂的な快楽を分かち合った…
	;快感に耐える
	CASE 6
		PRINTFORML %CALLNAME:TARGET%は耐えようとする%CALLNAME:PLAYER%の顔面に腰をぐりぐりと押しつけ、
		PRINTFORML 息苦しいほどの密着の中で、容赦なく口内の舌を激しく動かした…
	;快感を受け入れる
	CASE 7
		PRINTFORML 互いに快楽に身を委ね、甘い吐息と水音を響かせながら、
		PRINTFORML 狂おしいほどの興奮の中で相手の急所を吸い上げ続けた…
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%がおねだりするように腰を動かすと、%CALLNAME:TARGET%は嬉しそうに腰を揺らし、
		PRINTFORML さらに激しい奉仕で互いの快感を高め合った…
	CASEELSE
		PRINTFORML 二人は互いの性器を夢中で舐め合い、熱い結合を楽しんだ…
	ENDSELECT

;パイズリ
CASE 32
	SELECTCASE ARG:1
	;快感に耐える
	CASE 6
		PRINTFORML %CALLNAME:PLAYER%が快感を堪えようと身を固くするが、
		PRINTFORML %CALLNAME:TARGET%は豊満な胸でペニスを強く圧迫し、逃がさないように激しく揺さぶった…
	;快感を受け入れる
	CASE 7
		IF TFLAG:302
			PRINTFORML %CALLNAME:TARGET%は胸の谷間から顔を出すペニスを激しく擦り上げ、
			PRINTFORML 限界を迎えた%CALLNAME:PLAYER%の精液を胸元一面に受け止めて恍惚となった！
		ELSE
			PRINTFORML %CALLNAME:TARGET%は愛液と汗でぬめる胸元にペニスを沈め、
			PRINTFORML 柔らかな感触で優しく包み込みながら、熱っぽい眼差しで見つめてきた…
		ENDIF
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%のおねだりに%CALLNAME:TARGET%は胸をぎゅっと寄せ、
		PRINTFORML 先端を舌先で転がしながら、極上の挟み心地で責め立てた…
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は豊かな胸でペニスを挟み込み、情熱的に擦り上げた…
	ENDSELECT

;素股
CASE 33
	SELECTCASE ARG:1
	;快感に耐える
	CASE 6
		PRINTFORML %CALLNAME:TARGET%は堪えようとする%CALLNAME:PLAYER%の腰を抱え込み、
		PRINTFORML 太ももの内側でペニスを強く挟んでリズミカルに擦り上げた…
	;快感を受け入れる
	CASE 7
		PRINTFORML 互いのぬくもりと熱い分泌液が混ざり合い、
		PRINTFORML %CALLNAME:TARGET%は激しく腰を密着させて快感を貪り尽くしている…
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:TARGET%は懇願する%CALLNAME:PLAYER%に身を重ね、
		PRINTFORML 愛液を塗りたくるように激しく腰を動かして快楽を注ぎ込んだ…
	CASEELSE
		PRINTFORML 互いの性器を太もも越しに擦り合わせ、熱い摩擦を楽しんだ…
	ENDSELECT

;貝あわせ
CASE 63
	SELECTCASE ARG:1
	;快感に耐える
	CASE 6
		PRINTFORML %CALLNAME:TARGET%は耐えようとする%CALLNAME:PLAYER%の腰を掴み、
		PRINTFORML 互いの秘所が逃げないように強く押し当てて激しく擦り合わせた…
	;快感を受け入れる
	CASE 7
		PRINTFORML 互いに腰を浮かせ合い、ジュチュジュチュと音を立てながら、
		PRINTFORML 二つの秘部を擦り合わせて激しい快楽の波に溺れ合っている…
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%が身悶えながら求めると、%CALLNAME:TARGET%はさらに体重を乗せて
		PRINTFORML 敏感な突起同士を擦り合わせ、狂ったように腰を振り乱した…
	CASEELSE
		PRINTFORML 二人は互いの秘唇を密着させて腰を揺すり合った…
	ENDSELECT

;足扱き
CASE 37
	SELECTCASE ARG:1
	;快感に耐える
	CASE 6
		PRINTFORML %CALLNAME:TARGET%は耐えようとする%CALLNAME:PLAYER%の顔を見て意地悪く微笑み、
		PRINTFORML 足裏で陰茎をぐりぐりと押し潰すように激しく踏みしごいた…
	;快感を受け入れる
	CASE 7
		PRINTFORML 屈服したように快感に身を委ねる%CALLNAME:PLAYER%を見下ろし、
		PRINTFORML %CALLNAME:TARGET%は柔らかくしっとりした足指で敏感な箇所を撫で回した…
	;おねだり
	CASE 8
		PRINTFORML 懇願する%CALLNAME:PLAYER%に、%CALLNAME:TARGET%は満足げに足指を絡め、
		PRINTFORML 先走りを足裏全体で塗り広げながら濃厚に擦り上げた…
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は足先で巧みにペニスを擦り上げた…
	ENDSELECT

;正常位させる
CASE 20, 120
	SELECTCASE ARG:1
	;キス
	CASE 0
		PRINTFORML %CALLNAME:PLAYER%が腰を深く結合させたまま身を寄せて唇を奪うと、
		PRINTFORML %CALLNAME:TARGET%は熱い吐息を漏らして応じ、結合部を強く締めつけながら熱烈に舌を絡め合わせた…
	;胸愛撫
	CASE 3
		PRINTFORML %CALLNAME:PLAYER%が結合したまま%CALLNAME:TARGET%の柔らかな胸を両手で揉みしだくと、
		PRINTFORML 先端を指先で弾かれる快感に%CALLNAME:TARGET%は身悶え、膣奥を激しく締め上げてきた…
	;消極的にやる
	CASE 4
		PRINTFORML %CALLNAME:PLAYER%が動きを緩めようとすると、%CALLNAME:TARGET%は自ら腰を強く引き寄せ、
		PRINTFORML 最奥まで貫かせたまま離さないように深く抱きしめてきた…
	;積極的にやる
	CASE 5
		IF HEAT >= 2
			PRINTFORML %CALLNAME:PLAYER%が夢中で腰を打ち付けると、%CALLNAME:TARGET%も歓喜の声をあげて腰を跳ね上げ、
			PRINTFORML 激しい肉のぶつかり合う音を部屋中に響かせながら狂おしく結合し合った！
		ELSE
			PRINTFORML 互いに腰を求め合い、深い結合感の中で激しく腰を揺らし合った…
		ENDIF
	;快感に耐える
	CASE 6
		PRINTFORML %CALLNAME:PLAYER%が息を詰まらせて耐えようとすると、%CALLNAME:TARGET%は膣壁をギュウギュウと締め上げ、
		PRINTFORML 逃れられない快楽の波で強引に快感を搾り取ろうとしてきた…
	;快感を受け入れる
	CASE 7
		IF TFLAG:302
			PRINTFORML %CALLNAME:TARGET%は射精を間近にしたペニスを膣奥深くへしっかりと抱き込み、
			PRINTFORML 激しいピストンで奥の子宮口に先端を導いて一気に解き放たせた！
		ELSE
			PRINTFORML %CALLNAME:PLAYER%が快楽に喘ぐ姿に興奮した%CALLNAME:TARGET%は、
			PRINTFORML 膣内全体でペニスを撫で回すようにうねらせ、更なる悦楽へと導いている…
		ENDIF
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%が腰をすがりつかせて懇願すると、%CALLNAME:TARGET%は愛おしそうに微笑み、
		PRINTFORML 膣奥の一番敏感な箇所へ先端を押し当て、腰をゆっくりと回して蕩けるような快楽を与えた…
	CASEELSE
		PRINTFORML 二人は深い結合を確かめ合いながら、熱狂的に腰を打ち付け合った…
	ENDSELECT

;後背位させる
CASE 21, 121
	SELECTCASE ARG:1
	;キス
	CASE 0
		PRINTFORML %CALLNAME:PLAYER%が背後から抱き寄せ、振り返らせた%CALLNAME:TARGET%の唇を激しく奪うと、
		PRINTFORML 体勢の苦しさも忘れたように甘い声を漏らし、腰を奥深くまで引き入れた…
	;胸愛撫
	CASE 3
		PRINTFORML %CALLNAME:PLAYER%が背後から手を回して豊満な乳房を鷲掴みにし、先端を強く擦り上げると、
		PRINTFORML %CALLNAME:TARGET%はお尻を突き出して身震いし、狭い膣内で激しくペニスを締め付けた…
	;消極的にやる
	CASE 4
		PRINTFORML %CALLNAME:TARGET%は背後から突き入れられた感触を味わいながら、自ら腰をくねらせて快感を貪った…
	;積極的にやる
	CASE 5
		PRINTFORML %CALLNAME:PLAYER%が後ろから激しく腰を叩きつけると、
		PRINTFORML %CALLNAME:TARGET%はお尻を突き出し、歓喜の嬌声を上げながら腰を揺すり乱れた…
	;快感に耐える
	CASE 6
		PRINTFORML %CALLNAME:TARGET%は耐えようとする%CALLNAME:PLAYER%の腰を後ろ向きに引き寄せ、
		PRINTFORML 狭い膣内をグリグリと抉るように腰を回転させて快感を煽った…
	;快感を受け入れる
	CASE 7
		PRINTFORML 最奥まで貫かれる衝撃に、二人は息を乱して腰を打ちつけ合い、
		PRINTFORML 獣のように激しく交わり合って絶頂へと突き進んだ…
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%が激しい突きを求めて腰を揺らすと、%CALLNAME:TARGET%はお尻を高く突き出し、
		PRINTFORML 膣奥深くまでペニスを咥え込んだまま、激しく腰を打ち付けさせた…
	CASEELSE
		PRINTFORML 背後から奥深くまで貫かれた体勢で、二人は激しく腰を揺らし合った…
	ENDSELECT

;対面座位させる
CASE 24, 122
	SELECTCASE ARG:1
	;キス
	CASE 0
		PRINTFORML 密着したまま互いの唇を貪り合い、熱い吐息と唾液を交わしながら、
		PRINTFORML %CALLNAME:TARGET%は腰を沈めて最奥までペニスを擦り上げた…
	;胸愛撫
	CASE 3
		PRINTFORML %CALLNAME:PLAYER%が密着した胸元に手を滑り込ませ、押し合うように乳房を揉みほぐすと、
		PRINTFORML %CALLNAME:TARGET%は首筋にしがみついて喘ぎ、結合部を激しく擦り合わせた…
	;消極的にやる
	CASE 4
		PRINTFORML 抱き合った体勢のまま、%CALLNAME:TARGET%はゆっくりと腰を回して奥深くを刺激した…
	;積極的にやる
	CASE 5
		PRINTFORML 互いに肌を密着させ、抱きしめ合いながら激しく腰を擦り合わせ、
		PRINTFORML 吐息と唾液を交わしながら情熱的な結合を楽しんだ…
	;快感に耐える
	CASE 6
		PRINTFORML 抱きしめられたまま腰を押し当てられ、逃げ場のない密着快楽に%CALLNAME:PLAYER%は息を詰まらせた…
	;快感を受け入れる
	CASE 7
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の首筋に顔を埋め、体重をかけて結合部を押しつけ、
		PRINTFORML 膣奥でビクビクと脈打つペニスの熱を感じながら甘く喘いだ…
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%が抱きしめる腕に力を込めてねだると、%CALLNAME:TARGET%は愛おしそうに微笑み、
		PRINTFORML 結合部を押しつぶすように体重をかけて極上の快感を注ぎ込んだ…
	CASEELSE
		PRINTFORML 二人は正面から抱き合い、熱い体温を感じながら腰を揺すり合った…
	ENDSELECT

;背面座位させる
CASE 25, 123
	SELECTCASE ARG:1
	;キス
	CASE 0
		PRINTFORML %CALLNAME:PLAYER%が後ろから首筋を抱き寄せ、頬を寄せて唇を重ねると、
		PRINTFORML %CALLNAME:TARGET%は熱い吐息を漏らしながら腰を弾ませ、最奥で擦れる快感に身を震わせた…
	;胸愛撫
	CASE 3
		PRINTFORML %CALLNAME:PLAYER%が後ろから両手を回して乳房を優しく、時に激しく揉みしだくと、
		PRINTFORML 先端をつまみ上げられる刺激に%CALLNAME:TARGET%は首を反らせて甘い声をあげ、膣壁を波打たせて締めつけてきた…
	;消極的にやる
	CASE 4
		PRINTFORML 背中を預けられた体勢で、%CALLNAME:TARGET%は時折腰を跳ね上げて奥の感触を楽しんでいる…
	;積極的にやる
	CASE 5
		PRINTFORML %CALLNAME:PLAYER%が背後から抱きしめて腰を突き上げると、
		PRINTFORML %CALLNAME:TARGET%は胸を反らせて甘い声を響かせ、自らも激しく腰を動かした…
	;快感に耐える
	CASE 6
		PRINTFORML 背後から抱きしめられ奥深くまで貫かれたまま、執拗に腰をうねらされて快感を責め立てられた…
	;快感を受け入れる
	CASE 7
		PRINTFORML 敏感な乳首や首筋を愛撫されながら奥深くを貫かれ、
		PRINTFORML %CALLNAME:TARGET%は恍惚とした表情で腰を跳ね上げ、快楽に溺れ狂った…
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%が背中越しに抱きしめて腰を突き上げると、%CALLNAME:TARGET%は身を震わせて応え、
		PRINTFORML 自ら腰を激しく上下させて奥深くにペニスを貪り入れた…
	CASEELSE
		PRINTFORML 背後から抱きしめられた体勢で、二人は奥深くの結合を激しく味わい合った…
	ENDSELECT

;騎乗位する
CASE 34, 124
	SELECTCASE ARG:1
	;キス
	CASE 0
		PRINTFORML %CALLNAME:PLAYER%が下から腕を伸ばして%CALLNAME:TARGET%を引き寄せ唇を塞ぐと、
		PRINTFORML 激しい腰の動きをそのままに、貪るようなディープキスで求め合ってきた…
	;胸愛撫
	CASE 3
		PRINTFORML %CALLNAME:PLAYER%が上下に激しく揺れる胸元を両手で受け止め、下から強く揉み上げると、
		PRINTFORML %CALLNAME:TARGET%は恍惚とした表情で腰の回転を激化させ、狂おしい刺激に身を乱した…
	;消極的にやる
	CASE 4
		PRINTFORML %CALLNAME:PLAYER%が圧倒されているのを見て、%CALLNAME:TARGET%は妖しく微笑み、
		PRINTFORML 自らのペースで激しく腰を上下させ、快感の波を押し寄せてきた…
	;積極的にやる
	CASE 5
		IF HEAT >= 2
			PRINTFORML %CALLNAME:PLAYER%が下から腰を突き上げると、%CALLNAME:TARGET%は狂おしい嬌声をあげ、
			PRINTFORML 自らも激しく腰を叩きつけて、貪るような激しいピストンで結合を乱舞させた！
		ELSE
			PRINTFORML 互いに腰を突き出し合い、激しい水音を響かせて求め合った…
		ENDIF
	;快感に耐える
	CASE 6
		PRINTFORML %CALLNAME:PLAYER%が耐えようとするのを見透かしたように、%CALLNAME:TARGET%は腰を回転させ、
		PRINTFORML 膣奥で一番感じるところを執拗にグリグリと擦り上げて身悶えさせた…
	;快感を受け入れる
	CASE 7
		IF TFLAG:302
			PRINTFORML %CALLNAME:TARGET%は限界を察して一気に腰のストロークを激化させ、
			PRINTFORML 膣奥深くまでペニスを咥え込んだまま、大量の精液を一滴残らず吸い取った！
		ELSE
			PRINTFORML 快楽に身を任せて腰を揺らす%CALLNAME:TARGET%の姿は神々しいほど美しく、
			PRINTFORML 二人は互いの視線を絡め合いながら熱い交わりを続けた…
		ENDIF
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%が下から腰を浮かせて哀願すると、%CALLNAME:TARGET%は妖艶に微笑み、
		PRINTFORML 一番気持ちいい角度で腰を激しくグラインドさせ、蕩けるような快楽を与えてくれた…
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は完全に主導権を握って腰を激しく上下させ、結合を深め続けた…
	ENDSELECT

;顔面騎乗クンニ
CASE 1
	SELECTCASE ARG:1
	;積極的にやる
	CASE 5
		PRINTFORML %CALLNAME:PLAYER%は夢中で舌を伸ばし、顔の上に押し付けられた秘部を激しく舐めしゃぶり、
		PRINTFORML %CALLNAME:TARGET%は息を乱して腰をガクガクと震わせた…
	;快感を受け入れる
	CASE 7
		PRINTFORML 押し付けられた肉のぬくもりと溢れ出る蜜を存分に味わい、
		PRINTFORML %CALLNAME:TARGET%は絶頂の波に身を震わせて腰を押し当て続けた…
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は顔面に秘唇を押し当て、熱い吐息を漏らしながら腰を揺すった…
	ENDSELECT

;指挿入れ強制
CASE 8
	SELECTCASE ARG:1
	;積極的にやる
	CASE 5
		PRINTFORML %CALLNAME:PLAYER%が指を奥深くまで差し込み、膣壁を曲げるように擦り上げると、
		PRINTFORML %CALLNAME:TARGET%は激しく腰を浮かせて嬌声をあげ、指に強く吸い付いてきた…
	;快感を受け入れる
	CASE 7
		PRINTFORML 溢れる愛液でぬめった膣内に指先を沈め、
		PRINTFORML %CALLNAME:TARGET%の昂った体温と締め付けをじっくりと味わった…
	CASEELSE
		PRINTFORML 膣内で指を小刻みに動かし、%CALLNAME:TARGET%の熱い感触を楽しんだ…
	ENDSELECT

;胸を揉ませる
CASE 5
	SELECTCASE ARG:1
	;積極的にやる
	CASE 5
		PRINTFORML %CALLNAME:PLAYER%が柔らかな胸を両手で激しく揉みしだき、先端を指で転がすと、
		PRINTFORML %CALLNAME:TARGET%は熱い吐息を漏らし、もっと強く揉んでほしいと身体を預けてきた…
	;快感を受け入れる
	CASE 7
		PRINTFORML 手のひらから伝わる豊かな感触と熱い鼓動を味わいながら、
		PRINTFORML %CALLNAME:TARGET%はうっとりと瞳を閉じて愛撫に身を委ねている…
	CASEELSE
		PRINTFORML 手のひら全体で柔らかな胸を包み込み、優しく揉みほぐした…
	ENDSELECT

;自慰見せつけ
CASE 3
	SELECTCASE ARG:1
	;快感を受け入れる
	CASE 7
		PRINTFORML 目の前で繰り広げられる淫らな光景に息を呑み、
		PRINTFORML %CALLNAME:TARGET%の指先が秘部をかき乱す音を聞きながら熱狂的な興奮を分かち合った…
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%が興奮した視線で熱心に見つめると、
		PRINTFORML %CALLNAME:TARGET%は嬉しそうに微笑み、より露わに秘裂を広げて指を激しく出し入れしてみせた…
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%が目の前で指を動かす姿をじっと見つめた…
	ENDSELECT

;自慰強制
CASE 205
	SELECTCASE ARG:1
	;積極的にやる
	CASE 5
		PRINTFORML %CALLNAME:PLAYER%が自らの体を弄び喘ぎ声をあげると、
		PRINTFORML %CALLNAME:TARGET%は愉悦に満ちた瞳でその姿をじっくりと見つめ、優越感に浸っている…
	;快感を受け入れる
	CASE 7
		PRINTFORML %CALLNAME:PLAYER%が快楽に溺れて自ら悶える姿に、
		PRINTFORML %CALLNAME:TARGET%は興奮を隠せない様子で息を荒らげ、愛おしそうに見つめていた…
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%の視線を受けながら、自らの身体に触れて快感を高めた…
	ENDSELECT

;パートナー側挿入 (正常位193, 後背位194, 騎乗位195)
CASE 193 TO 195
	SELECTCASE ARG:1
	;キス
	CASE 0
		PRINTFORML 結合したまま唇を重ね合わせ、熱狂的な舌の絡み合いの中で激しく腰を打ち付けられた…
	;胸愛撫
	CASE 3
		PRINTFORML 貫かれた体勢のまま胸を揉みしだくと、%CALLNAME:TARGET%は熱い吐息を漏らし、腰の突き出しを激化させた…
	;積極的にやる
	CASE 5
		PRINTFORML 互いに腰を求め合い、激しい結合音を響かせながら熱狂的な交わりを続けた…
	;快感に耐える
	CASE 6
		PRINTFORML 突き上げられる激しい快感に耐えようと身を固くするが、容赦ないピストンに翻弄された…
	;快感を受け入れる
	CASE 7
		PRINTFORML 全身で快楽を受け止め、最奥を貫かれる歓喜に身悶えて絶頂へと誘われた…
	CASEELSE
		PRINTFORML 激しい結合感の中で、二人は熱く腰を揺らし合った…
	ENDSELECT

;包括フォールバック（どのCASEにも該当しなかった場合の安全装置）
CASEELSE
	SELECTCASE ARG:1
	;キス
	CASE 0
		PRINTFORML %CALLNAME:PLAYER%が身を寄せて唇を奪うと、%CALLNAME:TARGET%は吐息を漏らして応じ、熱烈に舌を絡め合わせた…
	;胸愛撫
	CASE 3
		PRINTFORML %CALLNAME:PLAYER%が%CALLNAME:TARGET%の胸を愛撫すると、敏感な突起を指で弄ばれる刺激に身を震わせて甘く喘いだ…
	;積極的にやる
	CASE 5
		PRINTFORML %CALLNAME:PLAYER%も積極的に求め返し、二人は激しく肌を重ね合わせて快楽を高め合った…
	;快感に耐える
	CASE 6
		PRINTFORML %CALLNAME:PLAYER%が息を詰めて耐えようとするのを見て、%CALLNAME:TARGET%は更に激しく責め立ててきた…
	;快感を受け入れる
	CASE 7
		PRINTFORML %CALLNAME:PLAYER%が快感に身を委ねると、%CALLNAME:TARGET%は満足そうに微笑み、更なる悦楽へと導いた…
	;おねだり
	CASE 8
		PRINTFORML %CALLNAME:PLAYER%が熱い視線でねだると、%CALLNAME:TARGET%は愛おしそうに応じ、濃厚な愛撫を与えてくれた…
	CASEELSE
		PRINTFORML 二人は熱い体温を感じ合いながら、情熱的な愛撫を交わし続けた…
	ENDSELECT

ENDSELECT
'''

def main():
    target_path = 'ERB/REVMODE_リバースモード.ERB'
    with open(target_path, 'rb') as f:
        text = f.read().decode('cp932')
    text = text.replace('\r\n', '\n')

    idx3 = text.find('@TRAIN_MESSAGE_REVMODE_ACTIVEPHASE')
    idx4 = text.find('@REVMODE_SOURCE_CHECK')
    assert idx3 != -1 and idx4 != -1, "ACTIVEPHASE boundaries not found"

    new_active = get_complete_activephase()
    text = text[:idx3] + new_active + '\n' + text[idx4:]

    # Remove any dialogue quotes from the entire file
    quotes = ['「', '」', '『', '』']
    # Check if Line 931 quote is present
    old_q = 'PRINTFORML 「私のペースでいくね…」と囁いて自ら激しく腰を上下させ始めた…'
    new_q = 'PRINTFORML %CALLNAME:TARGET%は妖しく微笑み、自らのペースで激しく腰を上下させ始めた…'
    if old_q in text:
        text = text.replace(old_q, new_q)
        print("Removed dialogue quote.")

    # Write back
    text_crlf = text.replace('\n', '\r\n')
    with open(target_path, 'wb') as f:
        f.write(text_crlf.encode('cp932'))

    print("Successfully replaced TRAIN_MESSAGE_REVMODE_ACTIVEPHASE with complete reaction coverage.")

if __name__ == '__main__':
    main()
