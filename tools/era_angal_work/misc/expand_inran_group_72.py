# -*- coding: utf-8 -*-
"""
Expand @EVENT_NEWDAY_INRAN_GROUP to support 6 tiers across all 72 girls.
"""
import sys
import os

ERB_FILE = 'ERB/EVENT_MORNING_朝のイベント.ERB'

NEW_FUNC = '''@EVENT_NEWDAY_INRAN_GROUP
#DIM INRAN_COUNT
#DIM PARTICIPANTS, 100
#DIM TIER
#DIM SEED
#DIM EJAC_COUNT
#DIM CHARA_ID
#DIM R_NAME1
#DIM R_NAME2
#DIM R_NAME3
#DIM R_NAME4

; 参加可能な淫乱キャラを収集
INRAN_COUNT = 0
VARSET PARTICIPANTS, 0

FOR LOCAL, 0, CHARANUM
	SIF LOCAL == MASTER
		CONTINUE
	; 臨月・育児中・体力切れは除外
	SIF CFLAG:LOCAL:16 == 1	; 臨月休養
		CONTINUE
	SIF CFLAG:LOCAL:21 > 0	; 育児中
		CONTINUE
	SIF BASE:LOCAL:0 <= 0	; 体力切れ
		CONTINUE
	; 【淫乱】所持者をリストアップ
	IF TALENT:LOCAL:76
		PARTICIPANTS:INRAN_COUNT = LOCAL
		INRAN_COUNT += 1
		SIF INRAN_COUNT >= 90
			BREAK
	ENDIF
NEXT

; 最低3人以上いないと発生しない
SIF INRAN_COUNT < 3
	RETURN 0

; 発生確率チェック（淫乱人数に応じて上昇：3人で9%、12人で12%、24人で16%、36人で20%、51人以上で25〜30%）
LOCAL:1 = MIN(8 + INRAN_COUNT / 3, 30)
SIF RAND:100 >= LOCAL:1
	RETURN 0

; 段階（TIER）判定：72人全域をカバーする6段階制
; 第1段階: 3〜5人（少人数・寝室包囲）
; 第2段階: 6〜11人（中規模・複数人同時攻め）
; 第3段階: 12〜19人（大規模・寝所占領・行列搾取）
; 第4段階: 20〜35人（教室規模・狂乱の波状輪姦）
; 第5段階: 36〜50人（学園半数規模・感覚遮断・極限搾精）
; 第6段階: 51〜72人（学園制覇・全校淫蕩・神域大ハーレム）
IF INRAN_COUNT >= 51
	TIER = 6
ELSEIF INRAN_COUNT >= 36
	TIER = 5
ELSEIF INRAN_COUNT >= 20
	TIER = 4
ELSEIF INRAN_COUNT >= 12
	TIER = 3
ELSEIF INRAN_COUNT >= 6
	TIER = 2
ELSE
	TIER = 1
ENDIF

; 参加者を代表して名前を呼ぶキャラを抽出（最大4名）
LOCAL:2 = RAND:INRAN_COUNT
R_NAME1 = PARTICIPANTS:(LOCAL:2)

LOCAL:3 = RAND:INRAN_COUNT
WHILE LOCAL:3 == LOCAL:2 && INRAN_COUNT > 1
	LOCAL:3 = RAND:INRAN_COUNT
WEND
R_NAME2 = PARTICIPANTS:(LOCAL:3)

LOCAL:4 = RAND:INRAN_COUNT
WHILE (LOCAL:4 == LOCAL:2 || LOCAL:4 == LOCAL:3) && INRAN_COUNT > 2
	LOCAL:4 = RAND:INRAN_COUNT
WEND
R_NAME3 = PARTICIPANTS:(LOCAL:4)

LOCAL:5 = RAND:INRAN_COUNT
WHILE (LOCAL:5 == LOCAL:2 || LOCAL:5 == LOCAL:3 || LOCAL:5 == LOCAL:4) && INRAN_COUNT > 3
	LOCAL:5 = RAND:INRAN_COUNT
WEND
R_NAME4 = PARTICIPANTS:(LOCAL:5)

; 地の文のランダムバリエーション（0〜2）
SEED = RAND:3

DRAWLINE
DRAWLINE
SETCOLOR 255, 100, 180
IF TIER == 1
	PRINTFORML 集団朝襲撃・囲い込み搾精（淫乱人数：{INRAN_COUNT}人）
ELSEIF TIER == 2
	PRINTFORML 集団朝襲撃・群がり乱れ交わり（淫乱人数：{INRAN_COUNT}人）
ELSEIF TIER == 3
	PRINTFORML 集団朝襲撃・寝所占領・行列搾取（淫乱人数：{INRAN_COUNT}人）
ELSEIF TIER == 4
	PRINTFORML 集団朝襲撃・狂乱の波状輪姦（淫乱人数：{INRAN_COUNT}人）
ELSEIF TIER == 5
	PRINTFORML 集団朝襲撃・学園狂乱・限界搾精（淫乱人数：{INRAN_COUNT}人）
ELSE
	PRINTFORML 集団朝襲撃・全校淫蕩・神域大ハーレム（淫乱人数：{INRAN_COUNT}人）
ENDIF
RESETCOLOR
DRAWLINE

; --- 描写部 ---
IF TIER == 1
	; 【第1段階：3〜5人】
	IF SEED == 0
		PRINTFORML 朝の薄暗い寝室、微かな吐息の音で%CALLNAME:MASTER%が目を覚ますと、
		PRINTFORML すでにベッドの周囲を%CALLNAME:R_NAME1%や%CALLNAME:R_NAME2%たち少女に完全に囲まれていた。
		PRINTFORMW 「ふふ、まだ寝てる…可愛い」「抜け駆け、ずるいぞ…」
		PRINTFORML 寝ぼけ眼のまま、幾重にも重なる柔らかな身体の重みで押さえ込まれ、パジャマを脱がされていく。
		PRINTFORML 身動きの取れない無防備な肉体に、彼女たちの濡れた手が、舌が這い回り始める。
		PRINTFORMW 耳元に甘い吐息を吹きかけられ、豊満な胸に挟み込まれながら、密室の愛撫が激しさを増していく。
		PRINTFORML 止まらない快感の波状攻撃に、%CALLNAME:MASTER%は目覚めたばかりの身体を痙攣させ、ビクビクと跳ね上げた。
		PRINTFORMW 「あはっ、ピクピクしてる！ 出して、私たちの中にいっぱい出して…！」
		PRINTFORML 甘美な囁きを浴びせられながら激しく吸い上げられ、抗う間もなく濃厚な白濁を勢いよく吐き出させられた。
	ELSEIF SEED == 1
		PRINTFORML まだほの暗い静まり返る早朝、%CALLNAME:MASTER%の部屋の扉が静かに開け放たれ、忍び足で寝所が包囲された。
		PRINTFORML 目を覚ます瞬間、%CALLNAME:R_NAME1%の濡れそぼる肉体がペニスの上にズシリと落とされ、完全に咥え込まれた。
		PRINTFORMW 「おはよう%CALLNAME:MASTER%…今朝は、たっぷり愛してあげるね…」
		PRINTFORML %CALLNAME:R_NAME2%が上半身へ覆いかぶさり、息の詰まるようなディープキスで叫び声を封じ込めてくる。
		PRINTFORML 下半身では%CALLNAME:R_NAME1%が容赦なく腰を落とし、熱い蜜壷で根元まで一気に呑み込んで激しく揺すぶる。
		PRINTFORMW 左右からは別の少女たちの熱い手が伸び、乳首と太股を容赦なく擦り上げ、全身の性感帯を同時に弄び尽くす。
		PRINTFORML 呼吸すら奪われた密室の快楽地獄の中で、%CALLNAME:MASTER%は背筋を反らし、全身を震わせながら勢いよく絶頂を迎えた。
	ELSE
		PRINTFORML 目覚めると、全身がまとわりつくような熱気と甘い香りに満ちていた。
		PRINTFORML %CALLNAME:R_NAME1%と%CALLNAME:R_NAME2%がベッドの上に滑り込み、%CALLNAME:MASTER%の朝立ちを品定めするように見つめている。
		PRINTFORMW 「ほら、こんなに熱くて硬い…」「昨日のご奉仕のお礼、身体に教えてあげなくちゃね…」
		PRINTFORML 口に含む者、手で激しく擦り上げる者、太腿で挟み込む者――幾重もの奉仕が休む間もなく襲いかかる。
		PRINTFORML 彼女たちの淫らな笑みとともに跨がれ、容赦のない腰使いが%CALLNAME:MASTER%を貫く。
		PRINTFORMW 声にならない嬌声を漏らしながら、限界まで達した身体は幾度となく跳ね上げられ、濃密な精を貪り取られた。
	ENDIF
ELSEIF TIER == 2
	; 【第2段階：6〜11人】
	IF SEED == 0
		PRINTFORML 朝の光が差し込む寝室は、すでに濃厚な淫液の匂いと淫らな少女たちのフェロモンで充満していた。
		PRINTFORML ベッドの上どころか床にまで群がるのは、%CALLNAME:R_NAME1%、%CALLNAME:R_NAME2%、%CALLNAME:R_NAME3%をはじめとする少女たち。
		PRINTFORMW 「ちょっと、次は私の番よ！」「抜け駆けはずるい、私の中にも頂戴…！」
		PRINTFORML もはや順番待ちすらもどかしいとばかりに、欲望を剥き出しにした少女たちが雪崩のように%CALLNAME:MASTER%の上に殺到する。
		PRINTFORML 1人が腰を激しく振って絶頂を迎えると、引き抜く間もなく別の少女がペニスを奪い取り、自らの奥深くへねじり込む。
		PRINTFORMW 射精の余韻で過敏になり跳ね上がるペニスを休ませることなく、容赦のないピストンが叩きつけられる。
		PRINTFORML 次々に押し寄せる肉欲の濁流。%CALLNAME:MASTER%の身体は限界を超えてガクガクと震え、
		PRINTFORMW 嬌声と肉が打ち付け合う激しい音の渦の中で、何度も何度も濃密な精を注ぎ込まされた。
	ELSEIF SEED == 1
		PRINTFORML 目覚めた瞬間、視界も呼吸もすべて柔らかな少女たちの肉体に完全に飲み込まれていた。
		PRINTFORML 正面からは%CALLNAME:R_NAME1%が身体を擦り寄せ、両腕は%CALLNAME:R_NAME2%の豊満な胸に埋め込まれ、
		PRINTFORMW 下半身は%CALLNAME:R_NAME3%をはじめとする複数の少女たちによって、まるで肉の檻のように包み込まれている。
		PRINTFORML 蠢く肌が擦れ合うたびに甘い匂いが立ち上り、脳の奥まで痺れさせて思考力を奪っていく。
		PRINTFORML 「あはっ、ピクピク跳ねてる！ まだまだ出せるよね？ 全部、全部出し切って…！」
		PRINTFORMW 前後左右から押し寄せる快感の奔流に、%CALLNAME:MASTER%の神経は焼き切れる寸前まで追い詰められる。
		PRINTFORML 止まらぬ射精の連打に腰が浮き、白目を剥きながら、限界を超えた快楽の海へと沈められていった。
	ELSE
		PRINTFORML 「おはよう、私たちの愛しいご主人様…」
		PRINTFORML 妖艶な微笑みを浮かべる%CALLNAME:R_NAME1%に囲まれ、%CALLNAME:MASTER%はベッドの上で完全に身動きを奪われていた。
		PRINTFORMW 背後からは柔らかな胸が押し付けられ、正面からは滴る愛液の香りが鼻腔をくすぐる。
		PRINTFORML 6人を超える少女たちが、手、口、胸、秘所、指先、髪に至るまで、すべての性感帯を余すところなく貪り尽くす。
		PRINTFORML 同時に押し寄せる快楽の嵐に、%CALLNAME:MASTER%の喉からは呻き声しか上がらない。
		PRINTFORMW 「ほら、もっとビクビクして！ まだまだ奥に溜まってるんでしょ…！」
		PRINTFORML 絶頂とともに幾度となく大量の精液を噴き出させられ、魂の底まで吸い尽くされるような快楽の嵐に呑み込まれた。
	ENDIF
ELSEIF TIER == 3
	; 【第3段階：12〜19人】
	IF SEED == 0
		PRINTFORML 部屋を埋め尽くす熱気、充満する愛液の匂い、そして理性のタガが外れた十数人もの淫乱な少女たち。
		PRINTFORML %CALLNAME:R_NAME1%、%CALLNAME:R_NAME2%、%CALLNAME:R_NAME3%らは手を取り合って%CALLNAME:MASTER%を取り囲み、
		PRINTFORMW 廊下にまで並んだ少女たちが扉の隙間から熱い視線を注いでいる。
		PRINTFORML もはや朝の挨拶など誰一人として口にせず、ただひたすらに貪欲な肉欲の衝動だけが渦巻いていた。
		PRINTFORML 「出ないなんて言わせないよ…全部搾り取ってあげる」「順番に跨がれば、いくらでも出せるよね…！」
		PRINTFORMW 果てたばかりのペニスは休む間もなく次の少女の熱い肉壺へと飲み込まれ、容赦のない腰振りが再開される。
		PRINTFORML 幾重にも重なる絶頂の津波に、%CALLNAME:MASTER%は抗うことすら忘れ、快楽の波間に翻弄され続けた。
	ELSEIF SEED == 1
		PRINTFORML 寝室の扉が開け放たれ、廊下からベッドまで少女たちの行列が連なっていた。
		PRINTFORML ベッドの中央に仰向けに拘束された%CALLNAME:MASTER%の身体は、完全に少女たちの共有物と化している。
		PRINTFORMW 「はい、次！」「早く代わって、私だって我慢できない…！」
		PRINTFORML 1人が絶頂して引き抜くや否や、待ちきれない少女がすぐに覆いかぶさり、根元まで一気に呑み込んで腰を打ち付ける。
		PRINTFORML 手には別の少女の濡れそぼる秘唇が押し付けられ、口はディープキスで塞がれ、乳首は指先で激しく弄られる。
		PRINTFORMW 一切の隙間もない全方位の波状攻撃に、%CALLNAME:MASTER%の意識は朦朧とし、
		PRINTFORML 果てても果てても終わらないリレー搾精の中で、全身を激しく痙攣させながら白濁を噴き出し続けた。
	ELSE
		PRINTFORML 朝の光が窓から差し込む中、部屋中に響き渡るのは激しい水音と、少女たちの狂おしい嬌声の合唱だった。
		PRINTFORML %CALLNAME:R_NAME1%たちが代わる代わる%CALLNAME:MASTER%の上に腰を下ろし、容赦なく肉襞を締め上げていく。
		PRINTFORMW 十数人もの淫乱な少女たちに囲まれ、一人一人が主人公を限界まで搾り尽くそうと技巧を凝らす。
		PRINTFORML 「もっと熱いの頂戴！」「あはぁっ、奥まで届いてる…！」
		PRINTFORML もはや何回射精したかも数え切れず、身体の芯から快楽の熱病に侵されていく。
		PRINTFORMW 全身の力を抜き去られ、ただ快感に喘ぐだけの肉塊となりながら、朝の寝所は果てしない淫宴の場と化した。
	ENDIF
ELSEIF TIER == 4
	; 【第4段階：20〜35人】
	IF SEED == 0
		PRINTFORML 朝の寝室の扉は押し破られ、部屋から廊下まで20人を超える淫乱な少女たちで埋め尽くされていた。
		PRINTFORML 教室一つ分もの少女たちが一斉に発情し、充満する濃密なフェロモンで部屋全体の空気が白く霞むほどだ。
		PRINTFORMW 「ご主人様、朝ですよ…♪」「みんなで搾りに来ちゃいました…♪」
		PRINTFORML %CALLNAME:R_NAME1%、%CALLNAME:R_NAME2%、%CALLNAME:R_NAME3%、%CALLNAME:R_NAME4%らが狂おしい笑みを浮かべ、
		PRINTFORML 仰向けに倒れた%CALLNAME:MASTER%の手足をガッチリと押さえ込んで完全に身動きを奪う。
		PRINTFORMW 1人が跨がって激しく腰を振り、絶頂して腰を浮かせた刹那、次の少女が滑り込んできて根元まで一息に呑み込む。
		PRINTFORML 息をつく間もないベルトコンベアのような狂乱の輪姦リレーに、%CALLNAME:MASTER%は声を上げることすらできず、
		PRINTFORMW 限界を遥かに超越した連続射精のあまり、白目を剥いてガクガクと激しく全身を跳ねさせ続けた。
	ELSEIF SEED == 1
		PRINTFORML 「ふふっ、すごい…もう何回も出してるのに、ピクピク収まらない…♪」
		PRINTFORML ベッドを取り囲む少女たちの群れは、もはや理性のタガが完全に消し飛んでいた。
		PRINTFORMW %CALLNAME:R_NAME1%が激しく腰を打ち付けながら嬌声を上げ、周囲の少女たちは我先にと胸や手、口を差し出し、
		PRINTFORML %CALLNAME:MASTER%の全身のあらゆる性感帯に群がって休む間もなく吸い上げ、擦り立てる。
		PRINTFORML 射精が終わる瞬間すら待たずに新たな快感の刺激が叩き込まれ、オーガズムの波が途切れることなく連鎖する。
		PRINTFORMW 「まだまだ！ 全員分たっぷり注ぎ込んでもらうんだから…！」
		PRINTFORML 過負荷を起こした神経系が激痛と極上の快楽を混濁させ、%CALLNAME:MASTER%は涎を垂らしながら、
		PRINTFORMW 抗う術のない肉欲の渦の中で無我夢中に腰を震わせ続けた。
	ELSE
		PRINTFORML 早朝の静寂はどこへやら、部屋中が獣のような荒い息遣いと愛液の激しい飛沫音で満ちていた。
		PRINTFORML 20人以上の少女たちが順番を待ちきれず、%CALLNAME:MASTER%の身体の上で折り重なるように乱れ狂っている。
		PRINTFORMW 「出ない？ ううん、出なくてもいいの…空っぽになるまで搾り尽くすのが気持ちいいんだよ…♪」
		PRINTFORML %CALLNAME:R_NAME1%の囁きとともに、限界を越えて萎えかけたペニスが強引に熱い肉襞へと押し込まれる。
		PRINTFORML 精液が出尽くして透明な体液しか噴き出さなくなっても、少女たちの容赦のないピストンは止まらない。
		PRINTFORMW 過敏になりすぎた神経に直接触れられるような激痛混じりの極限快楽に、%CALLNAME:MASTER%は背筋を弓なりに反らせ、
		PRINTFORML 尽きることのない搾精の嵐の中で完全に思考を停止させられた。
	ENDIF
ELSEIF TIER == 5
	; 【第5段階：36〜50人】
	IF SEED == 0
		PRINTFORML 扉の向こう、廊下の果てまで少女たちの列が伸び、学園の半数以上を占める30〜40人以上の少女たちが押し寄せていた。
		PRINTFORML 部屋の中に立ち込める雌の甘い匂いと愛液の芳香は濃密を極め、呼吸するだけで脳が蕩けそうなほどだ。
		PRINTFORMW もはやベッドは崩壊寸前であり、%CALLNAME:MASTER%は神輿のように無数の柔らかな手で担ぎ上げられ、
		PRINTFORML %CALLNAME:R_NAME1%、%CALLNAME:R_NAME2%、%CALLNAME:R_NAME3%、%CALLNAME:R_NAME4%ら少女たちに次々と跨がれていく。
		PRINTFORML 「私たちの愛しい%CALLNAME:MASTER%…全部、全部みんなで美味しくいただきます♪」
		PRINTFORMW 一人が果てれば二人がかりで口と秘部を攻め立て、次から次へと休む暇なく少女たちが腰を落とす。
		PRINTFORML 数十人もの情熱的な腰振りと激しい締め付けに、%CALLNAME:MASTER%の身体は完全に限界を突き破り、
		PRINTFORMW 喉から音にならない絶叫を漏らしながら、全身の生気を全て注ぎ込むように幾度も幾度も跳ね上がった。
	ELSEIF SEED == 1
		PRINTFORML それはもはや朝の挨拶などではなく、学園を揺るがす狂乱の搾精儀式そのものだった。
		PRINTFORML 36人を超える淫乱の少女たちが寝所を完全に包囲・占領し、誰一人として逃げ場を与える気はない。
		PRINTFORMW 「あはぁっ、すごいビクビクしてる…！」「私の番、早く！ 奥まで出してぇ…！」
		PRINTFORML %CALLNAME:R_NAME1%が跨がり、%CALLNAME:R_NAME2%が顔の上に腰を下ろし、%CALLNAME:R_NAME3%が両腕を豊満な谷間で挟み込む。
		PRINTFORML あらゆる五感が柔らかな肌と甘い嬌声と愛液の味で塞がれ、外部の世界との繋がりを完全に断ち切られる。
		PRINTFORMW 射精しても射精しても終わらない。空撃ちの痙攣を繰り返すペニスは、それでも少女たちの熱い肉壁に貪られ続け、
		PRINTFORML %CALLNAME:MASTER%は白目を剥き、快楽の奈落の底へと引きずり込まれていった。
	ELSE
		PRINTFORML 早朝から昼近くまで続く、果てなき快楽の地獄絵図。
		PRINTFORML 部屋の中は床一面が愛液と白濁で汚れ、熱狂した少女たちの汗と香水が混ざり合って白く蒸せ返っている。
		PRINTFORMW %CALLNAME:MASTER%の身体は度重なる射精で完全に脱力し、指一本すら動かすことができない。
		PRINTFORML それでも、群がる少女たちの愛撫の手と腰の動きは止まらない。
		PRINTFORML 「ふふ、もうぐったり…でも、おちんちんはこんなに元気にビクビクしてるよ♪」
		PRINTFORMW 「みんなで愛してあげるからね…魂の最後の一滴まで、ぜーんぶちょうだい…♪」
		PRINTFORML 少女たちに崇拝されるように抱きしめられ、幾重にも重なる絶頂の雷撃を叩き込まれながら、
		PRINTFORMW %CALLNAME:MASTER%は自らの存在が蕩けていくような極限の忘我の境地へと沈んでいった。
	ENDIF
ELSE
	; 【第6段階：51〜72人】
	IF SEED == 0
		PRINTFORML 全校制覇・神域の大ハーレム――学園のほぼ全域、50人〜70人以上もの少女たちが朝の寝所を埋め尽くす前代未聞の光景。
		PRINTFORML 部屋はおろか廊下、階段にまで裸や半脱ぎの淫乱少女たちが溢れ返り、学園全体が濃密な情欲の熱気に包まれていた。
		PRINTFORMW %CALLNAME:R_NAME1%、%CALLNAME:R_NAME2%、%CALLNAME:R_NAME3%、%CALLNAME:R_NAME4%ら全員の瞳がハートに染まり、
		PRINTFORML 仰向けに倒れた%CALLNAME:MASTER%の周りに何重もの歓喜の輪が作られている。
		PRINTFORML 「ご主人様、おはようございます♪ 学園のみんなで、朝の搾精に来ましたよ…♪」
		PRINTFORMW 「もう逃げられません…今日という日は、全員の胎に命の雫を注ぎ込んでもらいます♪」
		PRINTFORML 言葉が終わるや否や、怒涛の勢いで少女たちが次々と腰を打ち付け、終わりのない輪姦リレーが幕を開ける。
		PRINTFORML 1人が絶頂を迎えると歓声が上がり、待機していた少女が即座に肉襞を滑り込ませて激しく腰を振る。
		PRINTFORMW 人間としての生理的限界など遥か昔に消し飛び、30回、40回を超える狂乱の連続射精。
		PRINTFORML 全身の筋肉が激しく硬直と弛緩を繰り返し、%CALLNAME:MASTER%は至高の快楽の光の中で完全に意識を融解させた。
	ELSEIF SEED == 1
		PRINTFORML 部屋の壁も床も、全てが少女たちの火照った素肌と甘い息遣いで埋め尽くされている。
		PRINTFORML 70人近くの淫乱なヒロインたちに囲まれた%CALLNAME:MASTER%は、もはや一個の人間ではなく、
		PRINTFORMW 学園中の欲望を一身に受け止めて満たすための「神聖なる搾精の生贄」と化していた。
		PRINTFORML 「見て、もう出ないのにこんなに脈打ってる…！」「次は私！ 私の奥に種付けしてぇっ！」
		PRINTFORML 熱狂した少女たちが競い合うように跨がり、全身の肌を擦り寄せ、口づけを降らせ、休む間もなく腰を打ち鳴らす。
		PRINTFORMW 果てるたびに全身を駆け抜ける激しい電撃。もはや精液ではなく透明な前立腺液と魂そのものを吸い出されるように、
		PRINTFORML ビクビクと跳ねるペニスは少女たちの熱い肉壷に次から次へと呑み込まれ、搾り尽くされていく。
		PRINTFORMW 「あはぁっ…！ ご主人様、大好き…！」「一生、私たちみんなのモノだからね…♪」
		PRINTFORML 果てなき愛と執着の言葉を浴びせられながら、%CALLNAME:MASTER%は幸福感に満ちた絶頂の果てに白目を剥いて倒れ伏した。
	ELSE
		PRINTFORML 昼を過ぎてもなお収まらない、学園史上最大の淫宴。
		PRINTFORML 50人以上の少女たちが満足げに頬を紅潮させ、息を弾ませながら、ベッドの周りで幸せそうに寄り添い合っている。
		PRINTFORMW その中心で、%CALLNAME:MASTER%は全身の力を完全に搾り取られ、ピクピクと痙攣しながら大の字に倒れていた。
		PRINTFORML 数十回に及ぶ極限の射精、空撃ちになっても止まらなかった激しいピストンの嵐。
		PRINTFORML 身体の奥底からあらゆる生気を吸い尽くされ、立っていることすら不可能な完全な脱力状態。
		PRINTFORMW しかし、周囲を取り囲む少女たちの顔には、かつてないほどの満ち足りた笑顔と、深い愛情が浮かんでいた。
		PRINTFORML 「ふふっ、本当に全部出し切っちゃったね…お疲れ様、私たちの愛しい人…♪」
		PRINTFORMW %CALLNAME:R_NAME1%たちが優しく頭を撫で、口づけを落としながら、力尽きた%CALLNAME:MASTER%を優しく抱きしめる。
		PRINTFORML 全身が痺れるような脱力感と甘やかな快感の余韻に包まれながら、%CALLNAME:MASTER%は心地よい眠りの中へと落ちていった。
	ENDIF
ENDIF

; --- 効果・数値計算 ---
; 射精回数決定
IF TIER == 1
	EJAC_COUNT = 3 + RAND:3
	LOSEBASE:MASTER:0 = 400
	BASE:MASTER:1 = MAX(0, BASE:MASTER:1 - 600)
ELSEIF TIER == 2
	EJAC_COUNT = 6 + RAND:5
	LOSEBASE:MASTER:0 = 800
	BASE:MASTER:1 = 0
ELSEIF TIER == 3
	EJAC_COUNT = 11 + RAND:6
	LOSEBASE:MASTER:0 = 1200
	BASE:MASTER:1 = 0
ELSEIF TIER == 4
	EJAC_COUNT = 18 + RAND:8
	LOSEBASE:MASTER:0 = 1700
	BASE:MASTER:1 = 0
ELSEIF TIER == 5
	EJAC_COUNT = 27 + RAND:10
	LOSEBASE:MASTER:0 = 2200
	BASE:MASTER:1 = 0
ELSE
	; 第6段階（51〜72人）：極限超越（38〜52回射精）
	EJAC_COUNT = 38 + RAND:15
	LOSEBASE:MASTER:0 = 2800
	BASE:MASTER:1 = 0
ENDIF

; 主人の体力減少（最低1残る）
BASE:MASTER:0 = MAX(1, BASE:MASTER:0 - LOSEBASE:MASTER:0)

; 主人の射精・絶頂経験加算
EXP:MASTER:3 += EJAC_COUNT
FLAG:5040 += EJAC_COUNT

; 主人が女児・女の場合のレズ・絶頂経験加算
IF TALENT:MASTER:122 == 0
	EXP:MASTER:40 += TIER * 6
	EXP:MASTER:2 += TIER * 4
ENDIF

; 参加者全員への経験・珠加算
FOR LOCAL, 0, INRAN_COUNT
	CHARA_ID = PARTICIPANTS:LOCAL
	; 精液経験
	EXP:CHARA_ID:20 += TIER * 2
	; 絶頂経験
	EXP:CHARA_ID:2 += TIER
	; 非処女ならV経験
	SIF TALENT:CHARA_ID:0 == 0
		EXP:CHARA_ID:0 += TIER
	; 珠加算
	JUEL:CHARA_ID:1 += TIER * 150	; 快Vの珠
	JUEL:CHARA_ID:4 += TIER * 100	; 恭順の珠
	JUEL:CHARA_ID:5 += TIER * 200	; 欲情の珠
	JUEL:CHARA_ID:17 += TIER * 100	; 恥情の珠
	; 好感度加算
	CFLAG:CHARA_ID:2 += TIER * 3
	; 膣内射精量（受胎チェック用）
	CFLAG:CHARA_ID:101 += TIER
	; 累積射精量
	FLAG:(5800 + NO:CHARA_ID) += TIER * 2
NEXT

DRAWLINE
SETCOLOR 255, 120, 180
PRINTFORML %CALLNAME:MASTER%は限界の快楽に達して【{EJAC_COUNT}回】の射精を強制された…
PRINTFORML 主人体力 -{LOSEBASE:MASTER:0} / 気力完全枯渇（残り 0）
PRINTFORML 参加した【{INRAN_COUNT}人】の全員の精液経験・絶頂経験・好感度・各種珠が大幅に上昇しました！
RESETCOLOR
DRAWLINE
WAIT
RETURN 1
'''

def apply():
    with open(ERB_FILE, 'r', encoding='cp932') as f:
        content = f.read()

    pos = content.find('@EVENT_NEWDAY_INRAN_GROUP')
    if pos == -1:
        print('Error: @EVENT_NEWDAY_INRAN_GROUP not found!')
        sys.exit(1)

    prefix = content[:pos]
    
    # Normalize CRLF
    new_full = prefix + NEW_FUNC.strip() + '\n'
    new_full = new_full.replace('\r\n', '\n').replace('\n', '\r\n')

    encoded_bytes = new_full.encode('cp932')
    with open(ERB_FILE, 'wb') as f:
        f.write(encoded_bytes)

    print('Successfully updated', ERB_FILE)

if __name__ == '__main__':
    apply()
