# -*- coding: utf-8 -*-
"""
ERB/REVMODE_リバースモード.ERB の地の文を大幅に多パターン化・濃厚化・過熱分岐化するスクリプト。
"""

import os
import sys

def get_new_passivephase():
    return '''@TRAIN_MESSAGE_REVMODE_PASSIVEPHASE(ARG:0, ARG:1)
#DIM DYNAMIC HEAT, 1
HEAT = TFLAG:108

SELECTCASE ARG:1
;キス
CASE 0
	SELECTCASE ARG:0
	CASEELSE
		IF HEAT >= 2
			IF !RAND:2
				PRINTFORML %CALLNAME:TARGET%は熱い吐息を吹きかけながら%CALLNAME:PLAYER%の唇を激しく奪い、
				PRINTFORML 互いの舌が擦れ合い唾液が溢れるほど濃厚に口内を貪り尽くした…
			ELSE
				PRINTFORML %CALLNAME:TARGET%は恍惚とした瞳で%CALLNAME:PLAYER%を見つめ、絡みつくように唇を重ねると、
				PRINTFORML 口蓋をじっくりと舌先で撫で回し、息が詰まるほどの深い接吻を交わした…
			ENDIF
		ELSEIF HEAT == 1
			IF !RAND:2
				PRINTFORML %CALLNAME:TARGET%は愛おしそうに%CALLNAME:PLAYER%の頬を両手で包み、
				PRINTFORML 唇を奪いながら熱っぽい舌を侵入させて熱烈に求め合っている…
			ELSE
				PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の唇に何度も音を立てて吸い付き、
				PRINTFORML 蕩けるような甘い吐息を交わしながら口づけを繰り返した…
			ENDIF
		ELSE
			IF !RAND:2
				PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の口を自分の唇で塞ぎ、
				PRINTFORML 優しく舌先を触れ合わせながら穏やかに愛撫した…
			ELSE
				PRINTFORML %CALLNAME:TARGET%は少し照れくさそうに微笑みながら、
				PRINTFORML %CALLNAME:PLAYER%の唇にそっと重なり甘い感触を楽しんでいる…
			ENDIF
		ENDIF
	ENDSELECT

;手淫
CASE 1
	SELECTCASE ARG:0
	CASE 30
		IF HEAT >= 2
			IF !RAND:2
				PRINTFORML %CALLNAME:TARGET%は興奮に頬を染めながら、溢れ出る先走りを塗り広げ、
				PRINTFORML 陰茎全体を吸い付くような手のひらで激しく擦り上げ、翻弄している…
			ELSE
				PRINTFORML %CALLNAME:TARGET%は快感に喘ぐ%CALLNAME:PLAYER%の表情を愉悦に満ちた目で見下ろし、
				PRINTFORML 雁首を親指の腹で強く擦りながら、速いストロークで執拗に責め立てた…
			ENDIF
		ELSEIF HEAT == 1
			PRINTFORM %CALLNAME:TARGET%は
			SIF TALENT:TARGET:83
				PRINTFORM 悪戯っぽく微笑みながら
			PRINTFORML %CALLNAME:PLAYER%の男性器を手のひらで包み、緩急をつけてじっくりとしごき上げた…
		ELSE
			PRINTFORM %CALLNAME:TARGET%は
			IF !RAND:2 && TALENT:PLAYER:122
				PRINTFORM %CALLNAME:PLAYER%の陰嚢を優しく揉みながら、
			ELSE
				PRINTFORM 期待に満ちた表情で%CALLNAME:PLAYER%の目を見つめながら、
			ENDIF
			PRINTFORML 丁寧に男性器をしごきあげた…
		ENDIF
	CASEELSE
		IF HEAT >= 2
			PRINTFORML %CALLNAME:TARGET%は主導権を握る快感に瞳を潤ませ、
			PRINTFORML %CALLNAME:PLAYER%の男性器を熱のこもった手つきで激しく愛撫し始めた…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の男性器を手で愛撫し始めた…
		ENDIF
	ENDSELECT

;フェラチオ
CASE 2
	SELECTCASE ARG:0
	CASE 31, 69
		IF HEAT >= 2
			IF !RAND:2
				PRINTFORM %CALLNAME:TARGET%は
				SIF ARG:0 == 69
					PRINTFORM %CALLNAME:PLAYER%の顔面に跨りながら、
				PRINTFORML 一滴の蜜も逃さぬようにペニスに吸い付き、喉奥まで深々と咥え込んで激しく頭を前後に揺らした…
			ELSE
				PRINTFORM %CALLNAME:TARGET%は
				SIF ARG:0 == 69
					PRINTFORM 秘部を顔に押し付けたまま、
				PRINTFORML 充血した雁首を舌先で転がし、ズチュズチュと濃厚な水音を響かせながら一心不乱に奉仕している…
			ENDIF
		ELSEIF HEAT == 1
			PRINTFORM %CALLNAME:TARGET%は
			SIF ARG:0 == 69
				PRINTFORM %CALLNAME:PLAYER%の顔面に跨ったまま、
			PRINTFORML すぼめた唇で亀頭をしごきあげ、裏筋を丹念に舌で撫で上げて快感を煽り立てている…
		ELSE
			PRINTFORM %CALLNAME:TARGET%は
			SIF ARG:0 == 69
				PRINTFORM %CALLNAME:PLAYER%の顔面に跨ったまま
			PRINTFORML すぼめた唇で亀頭をしごきあげている…
		ENDIF
	CASEELSE
		IF HEAT >= 2
			PRINTFORML %CALLNAME:TARGET%は待ちきれない様子で%CALLNAME:PLAYER%の股間に吸い付き、
			PRINTFORML 口内全体で熱い男性器を包み込み、激しい吸引で責め立て始めた…
		ELSE
			PRINTFORM %CALLNAME:TARGET%は
			SIF ARG:0 == 1
				PRINTFORM 濡れた女性器を%CALLNAME:PLAYER%の顔面に擦りつけながら、
			PRINTFORML %CALLNAME:PLAYER%の股間に顔を埋めて男性器を口で愛撫し始めた…
		ENDIF
	ENDSELECT

;クンニする
CASE 3
	SELECTCASE ARG:0
	CASE 61, 69
		IF HEAT >= 2
			IF !RAND:2
				PRINTFORM %CALLNAME:TARGET%は
				SIF ARG:0 == 69
					PRINTFORM %CALLNAME:PLAYER%の顔面に跨りながら、
				PRINTFORML 敏感に尖った陰核を吸い上げ、舌先を小刻みに震わせて狂おしいほどの快楽を与えている…
			ELSE
				PRINTFORM %CALLNAME:TARGET%は愛液に塗れた秘唇を押し開き、
				PRINTFORML 膣口からクリトリスまでを激しく舐め上げ、逃げ場のない舌技で翻弄した…
			ENDIF
		ELSEIF HEAT == 1
			PRINTFORML %CALLNAME:TARGET%は溢れ出る愛液を美味しそうに舐め取りながら、
			PRINTFORML 柔らかな舌平で優しく、時に鋭く秘部を愛撫している…
		ELSE
			PRINTFORM %CALLNAME:TARGET%は
			SIF ARG:0 == 69
				PRINTFORM %CALLNAME:PLAYER%の顔面に跨ったまま
			PRINTFORML すぼめた唇で陰核に何度もキスをしている…
		ENDIF
	CASEELSE
		IF HEAT >= 2
			PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の太ももを大きく押し広げ、
			PRINTFORML 露出した秘唇に熱い唇を密着させて夢中で舐め貪り始めた…
		ELSE
			PRINTFORM %CALLNAME:TARGET%は
			SIF ARG:0 == 1
				PRINTFORM 濡れた女性器を%CALLNAME:PLAYER%の顔面に擦りつけながら
			PRINTFORML %CALLNAME:PLAYER%の股間に顔を埋めて秘唇を舐め始めた…
		ENDIF
	ENDSELECT

;パイズリ
CASE 4
	SELECTCASE ARG:0
	CASE 32
		IF HEAT >= 2
			IF !RAND:2
				PRINTFORML %CALLNAME:TARGET%は興奮で紅潮した胸元でペニスを強く挟み込み、
				PRINTFORML 溢れる汗と先走りを絡めながら、激しい上下運動で搾り取るように摩擦させた…
			ELSE
				PRINTFORML %CALLNAME:TARGET%は乳房の谷間に男性器を埋もれさせ、
				PRINTFORML 時折頭を下げて鈴口をチュウチュウと吸い上げながら、情熱的に胸を揺すぶっている…
			ENDIF
		ELSE
			PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%のペニスを胸で挟んだまま
			PRINTFORML 時折舌で先走りを舐めとっては激しく上半身を揺さぶっている…
		ENDIF
	CASEELSE
		IF HEAT >= 2
			PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の男性器を柔らかな胸でぎゅうぎゅうと圧迫し、
			PRINTFORML 熱狂的な吐息を漏らしながら擦り始めた…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の男性器を胸で挟んで擦り始めた…
		ENDIF
	ENDSELECT

;素股
CASE 5
	SELECTCASE ARG:0
	CASE 33
		IF HEAT >= 2
			PRINTFORML %CALLNAME:TARGET%は分泌した愛液で滑る性器を%CALLNAME:PLAYER%の男性器に強く押し当て、
			PRINTFORML 互いの熱が移るほどの密着感で、腰を激しく前後させて擦り合わせた…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は快感にあえぐ%CALLNAME:PLAYER%の上で性器が触れ合う感触を楽しんでいる…
		ENDIF
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の男性器を太ももで挟んで擦り始めた…
	ENDSELECT

;貝あわせ
CASE 6
	SELECTCASE ARG:0
	CASE 63
		IF HEAT >= 2
			PRINTFORML %CALLNAME:TARGET%は互いの陰核同士が直接擦れ合う位置で腰を密着させ、
			PRINTFORML 愛液を弾けさせながら狂おしいほどの速さで腰を激しく振り立てた…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は快感にあえぐ%CALLNAME:PLAYER%の上で性器が触れ合う感触を楽しんでいる…
		ENDIF
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は二人の女性器をぴったり重ねて擦りつけ始めた…
	ENDSELECT

;足扱き
CASE 7
	SELECTCASE ARG:0
	CASE 37
		IF HEAT >= 2
			PRINTFORML %CALLNAME:TARGET%は熱い瞳で%CALLNAME:PLAYER%を見下ろしながら、
			PRINTFORML 足指で亀頭を巧みに挟み上げ、足裏全体で強く踏みしごいて快感を叩き込んでいる…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は愉快そうに%CALLNAME:PLAYER%を見下ろしながら、
			PRINTFORML ペニスをぐりぐりと踏みつけている…
		ENDIF
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の男性器を踏みつけ擦り始めた…
	ENDSELECT

;正常位させる
CASE 8
	SELECTCASE ARG:0
	CASE 20, 120
		IF HEAT >= 2
			IF !RAND:2
				PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の首にしがみつき、腰を奥深くまで引き寄せると、
				PRINTFORML 膣内全体でペニスを強く締めつけながら、熱い嬌声を漏らして激しく腰を打ち付けさせた…
			ELSE
				PRINTFORML %CALLNAME:TARGET%は両脚を%CALLNAME:PLAYER%の腰に絡め、逃げられないように抱きしめたまま、
				PRINTFORML 最奥まで貫かれた快感に身悶え、貪るように腰を小刻みに震わせている…
			ENDIF
		ELSE
			PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の腰を引き寄せペニスを膣奥まで引きずりこんだ…
		ENDIF
	CASE 21, 24, 25, 34, 121, 122, 123, 124
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%に挿入させたまま倒れこみ体位を正常位に変えた…
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%のモノに軽く手を添え、股を開いてその先端を女陰へと誘導した…
	ENDSELECT

;後背位させる
CASE 9
	SELECTCASE ARG:0
	CASE 21, 121
		IF HEAT >= 2
			PRINTFORML %CALLNAME:TARGET%は四つん這いの姿勢でお尻を高く突き出し、
			PRINTFORML 膣奥を激しく抉られる快感に喘ぎながら、自ら腰を激しく突き出して結合を深めた…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は腰をくねらせ%CALLNAME:PLAYER%に更なる快感を与えた…
		ENDIF
	CASE 20, 24, 25, 34, 120, 121, 123, 124
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%に挿入させたまま四つん這いになった…
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%に背を向け、お尻を突き出して挿入を誘った…
	ENDSELECT

;対面座位させる
CASE 10
	SELECTCASE ARG:0
	CASE 24, 122
		IF HEAT >= 2
			PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%と肌を密着させて抱き合い、
			PRINTFORML 耳元で甘い吐息を漏らしながら、体重をかけて結合部を擦り上げるように腰を回した…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の首筋に顔を埋め、腰を深く押し当てた…
		ENDIF
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の膝の上に跨がり、ゆっくりと腰を降ろして結合させた…
	ENDSELECT

;背面座位させる
CASE 11
	SELECTCASE ARG:0
	CASE 25, 123
		IF HEAT >= 2
			PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の胸に背中を預け、
			PRINTFORML 最奥で擦れる快感に首を後ろに反らせながら、自ら腰を弾ませて激しく責め立てさせた…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は背後から抱きしめられた体勢で腰をくねらせた…
		ENDIF
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は背を向けた体勢で跨がり、ゆっくりとペニスを飲み込んだ…
	ENDSELECT

;騎乗位する
CASE 12
	SELECTCASE ARG:0
	CASE 34, 124
		IF HEAT >= 2
			IF !RAND:2
				PRINTFORML %CALLNAME:TARGET%は完全に主導権を握って自ら激しく腰を上下させ、
				PRINTFORML 溢れる愛液で滑る肉襞でペニスを絞り上げながら、恍惚とした表情で貪り続けている…
			ELSE
				PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の胸に手を突き、覆いかぶさるように腰をグラインドさせ、
				PRINTFORML 子宮口に先端がぶつかる刺激に狂おしい喘ぎ声をあげながら激しく乱れ踊った…
			ENDIF
		ELSEIF HEAT == 1
			PRINTFORML %CALLNAME:TARGET%は腰を浮き沈みさせながら、心地よい角度を探るように大きく腰を動かしている…
		ELSE
			PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の上で自分のペースで腰を揺すり始めた…
		ENDIF
	CASEELSE
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の上に跨がり、先端を秘裂にあてがうと一気に腰を沈めた…
	ENDSELECT

;顔面騎乗クンニ
CASE 13
	IF HEAT >= 2
		PRINTFORML %CALLNAME:TARGET%は熱く濡れそぼった秘部を%CALLNAME:PLAYER%の口元に容赦なく押し当て、
		PRINTFORML 息もできないほど強く顔面を圧迫しながら、激しく腰を擦りつけて快感を求めている…
	ELSE
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の顔の上に跨がり、秘唇を舌先へと押し当てた…
	ENDIF

;指挿入れ強制
CASE 14
	PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の手を掴み、びしょ濡れの膣口へと指先を導き、
	PRINTFORML 自らの身体を内側からかき乱すように指を動かせと命じた…

;顔面騎乗アナル
CASE 15
	PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の顔面の上に腰を降ろし、
	PRINTFORML 恥じらいと支配欲の入り混じった瞳で見下ろしながら、菊座を舐めるよう促した…

;胸を揉ませる
CASE 16
	IF HEAT >= 2
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の手を自らの豊かな胸に強く押し当て、
		PRINTFORML もっと激しく揉みしだいてほしいと甘えた声で促しながら、熱い吐息を漏らした…
	ELSE
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の手を胸元へ導き、愛撫を求めた…
	ENDIF

;フェラさせる
CASE 17
	PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の頭を押さえつけ、自らの男性器を口元へとあてがい、
	PRINTFORML 舌で包み込むように奉仕させ始めた…

;正常位する / 後背位する / 騎乗位させる (パートナー側が男性器持ち)
CASE 18 TO 20
	IF HEAT >= 2
		PRINTFORML %CALLNAME:TARGET%は昂った男性器を%CALLNAME:PLAYER%の奥深くまで強引に突き刺し、
		PRINTFORML 支配する歓喜に酔いしれながら、容赦ない腰使いで激しく貫き立てた…
	ELSE
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の膣内へ自らのペニスを沈め、腰を動かし始めた…
	ENDIF

;自慰見せつけ
CASE 21
	IF HEAT >= 2
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の目の前で大きく足を開き、
		PRINTFORML 指先で自らの秘部をぐちゅぐちゅとかき回しながら、蕩けた視線で見せつけている…
	ELSE
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%に見せつけるように自慰を始めた…
	ENDIF

;自慰強制
CASE 22
	PRINTFORML %CALLNAME:TARGET%は妖しく微笑みながら、
	PRINTFORML 自分の目の前で快楽に溺れる姿を見せるよう%CALLNAME:PLAYER%に自慰を命じた…

ENDSELECT
'''

def get_new_activephase():
    return '''@TRAIN_MESSAGE_REVMODE_ACTIVEPHASE(ARG:0, ARG:1)
#DIM DYNAMIC HEAT, 1
HEAT = TFLAG:108

SELECTCASE ARG:0
;キス
CASE 6, 120 TO 124
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
			PRINTFORML 喉奥を熱い精液で満たされながら、恍惚とした表情でゴクゴクと激しく吸い上げた！
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
	ENDSELECT

;正常位させる
CASE 20
	SELECTCASE ARG:1
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
	ENDSELECT

;後背位させる
CASE 21
	SELECTCASE ARG:1
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
	ENDSELECT

;対面座位させる
CASE 24
	SELECTCASE ARG:1
	;積極的にやる
	CASE 5
		PRINTFORML 互いに肌を密着させ、抱きしめ合いながら激しく腰を擦り合わせ、
		PRINTFORML 吐息と唾液を交わしながら情熱的な結合を楽しんだ…
	;快感を受け入れる
	CASE 7
		PRINTFORML %CALLNAME:TARGET%は%CALLNAME:PLAYER%の首筋に顔を埋め、体重をかけて結合部を押しつけ、
		PRINTFORML 膣奥でビクビクと脈打つペニスの熱を感じながら甘く喘いだ…
	ENDSELECT

;背面座位させる
CASE 25
	SELECTCASE ARG:1
	;積極的にやる
	CASE 5
		PRINTFORML %CALLNAME:PLAYER%が背後から抱きしめて腰を突き上げると、
		PRINTFORML %CALLNAME:TARGET%は胸を反らせて甘い声を響かせ、自らも激しく腰を動かした…
	;快感を受け入れる
	CASE 7
		PRINTFORML 敏感な乳首や首筋を愛撫されながら奥深くを貫かれ、
		PRINTFORML %CALLNAME:TARGET%は恍惚とした表情で腰を跳ね上げ、快楽に溺れ狂った…
	ENDSELECT

;騎乗位する
CASE 34
	SELECTCASE ARG:1
	;消極的にやる
	CASE 4
		PRINTFORML %CALLNAME:PLAYER%が圧倒されているのを見て、%CALLNAME:TARGET%は妖しく微笑み、
		PRINTFORML 「私のペースでいくね…」と囁いて自ら激しく腰を上下させ始めた…
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
	ENDSELECT

;自慰強制
CASE 205
	SELECTCASE ARG:1
	;積極的にやる
	CASE 5
		PRINTFORML %CALLNAME:PLAYER%が命じられるまま自らの体を弄び、喘ぎ声をあげると、
		PRINTFORML %CALLNAME:TARGET%は愉悦に満ちた瞳でその姿をじっくりと見つめ、優越感に浸っている…
	;快感を受け入れる
	CASE 7
		PRINTFORML %CALLNAME:PLAYER%が快楽に溺れて自ら悶える姿に、
		PRINTFORML %CALLNAME:TARGET%は興奮を隠せない様子で息を荒らげ、愛おしそうに見つめていた…
	ENDSELECT

ENDSELECT
'''

def main():
    target_path = 'ERB/REVMODE_リバースモード.ERB'
    with open(target_path, 'rb') as f:
        text = f.read().decode('cp932')
    text = text.replace('\r\n', '\n')

    # Replace PASSIVEPHASE
    idx1 = text.find('@TRAIN_MESSAGE_REVMODE_PASSIVEPHASE')
    idx2 = text.find('@REVMODE_ACTIVEPHASE')
    assert idx1 != -1 and idx2 != -1, "PASSIVEPHASE boundaries not found"

    new_passive = get_new_passivephase()
    text = text[:idx1] + new_passive + '\n' + text[idx2:]

    # Replace ACTIVEPHASE messages
    idx3 = text.find('@TRAIN_MESSAGE_REVMODE_ACTIVEPHASE')
    idx4 = text.find('@REVMODE_SOURCE_CHECK')
    assert idx3 != -1 and idx4 != -1, "ACTIVEPHASE boundaries not found"

    new_active = get_new_activephase()
    text = text[:idx3] + new_active + '\n' + text[idx4:]

    # Write back
    text_crlf = text.replace('\n', '\r\n')
    with open(target_path, 'wb') as f:
        f.write(text_crlf.encode('cp932'))

    print("Successfully expanded all train messages in ERB/REVMODE_リバースモード.ERB")

if __name__ == '__main__':
    main()
