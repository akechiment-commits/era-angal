# -*- coding: utf-8 -*-
import sys, os, re

filepath = 'ERB/EVENT_MORNING_朝のイベント.ERB'
with open(filepath, 'rb') as f:
    text = f.read().decode('cp932')

# 1. Update EVENT_NEWDAY to call EVENT_NEWDAY_INRAN_GROUP
old_event_newday_block = (
    '\tELSEIF MARK:3 >= 3\t; 【反発感情】Lv>=3\r\n'
    '\t\t;朝寝起き襲い\r\n'
    '\t\tCALL EVENT_NEWDAY_OTO\r\n'
    '\tELSEIF TALENT:85 == 0 && TALENT:76 == 0\t; 【恋慕】なし / 【淫乱】なし\r\n'
    '\t\t;イベントは起きない\r\n'
    '\tELSE\r\n'
    '\t\t;朝起きイベント起きるかチェック\r\n'
    '\t\tCALL EVENT_NEWDAY_CHECK\r\n'
    '\tENDIF'
)

new_event_newday_block = (
    '\tELSE\r\n'
    '\t\t; 淫乱集団朝搾取イベントチェック（淫乱3人以上で稀に発生）\r\n'
    '\t\tCALL EVENT_NEWDAY_INRAN_GROUP\r\n'
    '\t\tIF RESULT == 0\r\n'
    '\t\t\tIF BASE:TARGET:0 <= 0\t; TARGET:【体力】<=0\r\n'
    '\t\t\t\tSETCOLOR 150, 150, 150\r\n'
    '\t\t\t\tPRINTFORML （%CALLNAME:TARGET%は精力減退（お休み）のため、朝のイベントは発生しません）\r\n'
    '\t\t\t\tRESETCOLOR\r\n'
    '\t\t\t\t;イベントスキップ\r\n'
    '\t\t\tELSEIF MARK:3 >= 3\t; 【反発感情】Lv>=3\r\n'
    '\t\t\t\t;朝寝起き襲い\r\n'
    '\t\t\t\tCALL EVENT_NEWDAY_OTO\r\n'
    '\t\t\tELSEIF TALENT:85 == 0 && TALENT:76 == 0\t; 【恋慕】なし / 【淫乱】なし\r\n'
    '\t\t\t\t;イベントは起きない\r\n'
    '\t\t\tELSE\r\n'
    '\t\t\t\t;朝起きイベント起きるかチェック\r\n'
    '\t\t\t\tCALL EVENT_NEWDAY_CHECK\r\n'
    '\t\t\tENDIF\r\n'
    '\t\tENDIF\r\n'
    '\tENDIF'
)

# Let's inspect EVENT_NEWDAY in text
m_target = re.search(r'IF TARGET > -1[\s\S]*?(?=;出産関係チェック|\r?\nCALL NINSSINXTU)', text)
if not m_target:
    raise Exception('EVENT_NEWDAY target block not found!')

old_full_block = m_target.group(0)

new_full_block = (
    'IF TARGET > -1\r\n'
    '\tIF TFLAG:121\t; 【イベントスキップフラグ】\r\n'
    '\t\t;イベントスキップ\r\n'
    '\tELSE\r\n'
    '\t\t; 淫乱集団朝搾取イベントチェック（淫乱3人以上で稀に発生）\r\n'
    '\t\tCALL EVENT_NEWDAY_INRAN_GROUP\r\n'
    '\t\tIF RESULT == 0\r\n'
    '\t\t\tIF BASE:TARGET:0 <= 0\t; TARGET:【体力】<=0\r\n'
    '\t\t\t\tSETCOLOR 150, 150, 150\r\n'
    '\t\t\t\tPRINTFORML （%CALLNAME:TARGET%は精力減退（お休み）のため、朝のイベントは発生しません）\r\n'
    '\t\t\t\tRESETCOLOR\r\n'
    '\t\t\t\t;イベントスキップ\r\n'
    '\t\t\tELSEIF MARK:3 >= 3\t; 【反発感情】Lv>=3\r\n'
    '\t\t\t\t;朝寝起き襲い\r\n'
    '\t\t\t\tCALL EVENT_NEWDAY_OTO\r\n'
    '\t\t\tELSEIF TALENT:85 == 0 && TALENT:76 == 0\t; 【恋慕】なし / 【淫乱】なし\r\n'
    '\t\t\t\t;イベントは起きない\r\n'
    '\t\t\tELSE\r\n'
    '\t\t\t\t;朝起きイベント起きるかチェック\r\n'
    '\t\t\t\tCALL EVENT_NEWDAY_CHECK\r\n'
    '\t\t\tENDIF\r\n'
    '\t\tENDIF\r\n'
    '\tENDIF\r\n'
    'ENDIF\r\n'
)

text = text[:m_target.start()] + new_full_block + text[m_target.end():]

# 2. Append @EVENT_NEWDAY_INRAN_GROUP function
inran_group_func = '''
;-------------------------------------------------
; 淫乱集団朝搾取イベント
; 淫乱の人数が3人以上いる場合、稀に発生（人数に応じて確率上昇）。
; 人数に応じて3段階に激化（3〜4人: 段階1 / 5〜7人: 段階2 / 8人以上: 段階3）
; 各段階ごとにランダム3パターンの猛烈な地の文を完備。
; 主人公の体力の限界を超えた搾取と、参加者全員への経験・珠の加算を行う。
;-------------------------------------------------
@EVENT_NEWDAY_INRAN_GROUP
#DIM INRAN_COUNT
#DIM PARTICIPANTS, 100
#DIM TIER
#DIM SEED
#DIM EJAC_COUNT
#DIM CHARA_ID
#DIM R_NAME1
#DIM R_NAME2
#DIM R_NAME3

; 参加可能な淫乱キャラを収集
INRAN_COUNT = 0
VARSET PARTICIPANTS, 0

FOR LOCAL, 0, CHARANUM
	SIF LOCAL == MASTER
		CONTINUE
	; 臨月・育児・体力切れは除外
	SIF CFLAG:LOCAL:16 == 1	; 臨月お休み
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

; 淫乱が3人未満なら発生しない
SIF INRAN_COUNT < 3
	RETURN 0

; 発生確率チェック（稀に発生：3人なら10%、5人なら14%、8人以上なら20%、上限25%）
LOCAL:1 = MIN(INRAN_COUNT * 2 + 4, 25)
SIF RAND:100 >= LOCAL:1
	RETURN 0

; 段階（TIER）判定
; 段階1: 3〜4人
; 段階2: 5〜7人
; 段階3: 8人以上
IF INRAN_COUNT >= 8
	TIER = 3
ELSEIF INRAN_COUNT >= 5
	TIER = 2
ELSE
	TIER = 1
ENDIF

; 参加者から代表して名前を呼ぶキャラをランダム選出
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

; 地の文のランダムバリエーション決定（0〜2）
SEED = RAND:3

DRAWLINE
DRAWLINE
SETCOLOR 255, 100, 180
IF TIER == 1
	PRINTFORML ≪淫乱集団の朝襲来・包囲搾精（参加淫乱：{INRAN_COUNT}人）≫
ELSEIF TIER == 2
	PRINTFORML ≪淫乱集団の朝襲来・肉欲波状逆夜這い（参加淫乱：{INRAN_COUNT}人）≫
ELSE
	PRINTFORML ≪淫乱集団の朝襲来・極限ハーレム搾取地獄（参加淫乱：{INRAN_COUNT}人）≫
ENDIF
RESETCOLOR
DRAWLINE

; --- 描写部分 ---
IF TIER == 1
	; 【第1段階：3〜4人】
	IF SEED == 0
		PRINTFORML 夜明けの薄暗い寝室、微かな衣擦れの音に%CALLNAME:MASTER%が薄目を開けると、
		PRINTFORML すでにベッドの周囲は%CALLNAME:R_NAME1%や%CALLNAME:R_NAME2%たち数人の少女たちに完全に取り囲まれていた。
		PRINTFORMW 「うふふ、まだ寝てる…可愛い」「早い者勝ちだよ、朝一番の美味しい蜜…」
		PRINTFORML 警戒する間もなく、四肢をふわりと柔らかい少女たちの体重で押さえつけられ、パジャマが手際よく剥ぎ取られる。
		PRINTFORML 朝立ちして反り返る肉棒を前に、少女たちの濡れた瞳孔が妖しく開き、我先にと群がり始めた。
		PRINTFORMW 首筋に熱い吐息を吹きかけられ、左右から豊満な胸で腕を挟み込まれながら、先端を幾重もの温かい舌先が奪い合うように貪る。
		PRINTFORML 逃げ場のない快楽の波状攻撃に、%CALLNAME:MASTER%は目覚めたばかりの頭が真っ白に痺れ、腰をビクビクと跳ね上げる。
		PRINTFORMW 「あはっ、もうピクピクしてる！ 出して、私たちの中にいっぱい出して…！」
		PRINTFORML 耳元で甘い喘ぎを囁かれながら激しく吸い上げられ、抵抗する間もなく濃厚な白濁が勢いよく迸り出た。
	ELSEIF SEED == 1
		PRINTFORML まだ館が静まり返る早朝、%CALLNAME:MASTER%の部屋の扉が音もなく開き、抜き足差し足で寝込みが襲われた。
		PRINTFORML 目を開けた瞬間、%CALLNAME:R_NAME1%の濡れそぼる秘肉が腰の上にズシリと跨がり、逃げ道を完全に塞ぐ。
		PRINTFORMW 「おはよう%CALLNAME:MASTER%…朝の挨拶、たっぷりしようね…」
		PRINTFORML %CALLNAME:R_NAME2%が上半身へ覆い被さり、窒息するようなディープキスで叫び声を封じ込めてくる。
		PRINTFORML 下腹部では%CALLNAME:R_NAME1%が容赦なく腰を落とし、熱い最奥まで朝立ちした剛直を一気に呑み込んで激しく揺さぶる。
		PRINTFORMW 左右からは別の少女たちの熱い手が伸び、乳首と玉袋を容赦なく擦り上げ、全身の性感帯を同時に灼き尽くす。
		PRINTFORML 呼吸すら奪われた極上の快楽檻の中で、%CALLNAME:MASTER%は背筋を弓なりに反らせ、全身を痙攣させながら勢いよく達した。
	ELSE
		PRINTFORML 目覚めると、全身が甘い牝の匂いと温かい肌の感触に埋め尽くされていた。
		PRINTFORML %CALLNAME:R_NAME1%と%CALLNAME:R_NAME2%たちがベッドの上に雪崩れ込み、%CALLNAME:MASTER%を貪るように擦り寄っている。
		PRINTFORMW 「朝からこんなに熱くて硬いよ…」「誰の奉仕が一番気持ちいいか、身体に教えてもらわなきゃね…」
		PRINTFORML 先端を口元に含む者、根本を胸の谷間で扱く者、指先で敏感な筋を弾く者――多重の奉仕が休む間もなく襲いかかる。
		PRINTFORML 少女たちの淫靡な笑みと蕩けた視線に包まれ、逃げ場のない快感の濁流に%CALLNAME:MASTER%の理性が吹き飛ぶ。
		PRINTFORMW 声にならない喘ぎ声を漏らしながら、朝一番から限界まで絞り尽くされるように何度も腰を跳ねさせられた。
	ENDIF
ELSEIF TIER == 2
	; 【第2段階：5〜7人】
	IF SEED == 0
		PRINTFORML 朝の陽光が差し込む寝室は、すでに濃密な愛液の匂いと淫靡な牝のフェロモンでムッとするほど淀んでいた。
		PRINTFORML ベッドの上どころか床にまで犇めき合うのは、%CALLNAME:R_NAME1%、%CALLNAME:R_NAME2%、%CALLNAME:R_NAME3%ら淫乱に染まりきった大勢の少女たち。
		PRINTFORMW 「ちょっと、次は私の番だよ！」「抜け駆けはずるい、早く私の中にも種頂戴…！」
		PRINTFORML もはや順番待ちすら守られず、欲望を剥き出しにした少女たちが飢えた牝豹のように%CALLNAME:MASTER%の上に殺到する。
		PRINTFORML 1人が口内で激しく吸い上げ、達した瞬間すら待たずに別の少女が肉棒を力任せに奪い取り、自らの奥深くへねじ込む。
		PRINTFORMW 射精の余韻で過敏になり跳ねるペニスを休ませることなく、容赦のないピストンが激しく打ち付けられる。
		PRINTFORML 息をつく暇すら与えられぬ怒涛の連続種付け。%CALLNAME:MASTER%の身体は限界を超えてガクガクと軋み、
		PRINTFORMW 歓喜に狂う少女たちの嬌声の中で、乾いた喘ぎを上げながら幾度も連続で射精させられた。
	ELSEIF SEED == 1
		PRINTFORML 目覚めた瞬間、視界も呼吸もすべて柔らかな女性の肉体に完全に圧殺されていた。
		PRINTFORML 顔面には%CALLNAME:R_NAME1%の愛液滴る秘肉が跨がり、両腕は%CALLNAME:R_NAME2%たちの豊かな胸に埋め込まれ、
		PRINTFORMW 下半身は%CALLNAME:R_NAME3%をはじめとする複数の少女たちによって、まるで肉の玩具のように貪り食われている。
		PRINTFORML 息を吸おうとするたびに甘酸っぱい牝の芳香が肺腑を侵し、脳の奥深くまで痺れさせて思考力を奪っていく。
		PRINTFORML 「あはっ、ビクビク跳ねてる！ まだまだ出せるよね？ 私たち全員分、全部出し切って…！」
		PRINTFORMW 前後左右から押し寄せる肉の波状攻撃に、%CALLNAME:MASTER%の神経は焼き切れる寸前まで追い詰められる。
		PRINTFORML 止まらぬ射精の連鎖に腰が浮き上がり、白目を剥きかけながら、限界を超えた白濁を次々と少女たちの胎内へ注ぎ込まされた。
	ELSE
		PRINTFORML 「おはよう、私たちの愛しい種付けおもちゃ様…♪」
		PRINTFORML 妖艶な微笑みを浮かべる%CALLNAME:R_NAME1%たちに囲まれ、%CALLNAME:MASTER%はベッドの上で完全に磔にされていた。
		PRINTFORMW 背後からは敏感な前立腺を執拗に弄り倒され、正面からは幾重もの熱い秘唇が入れ代わり立ち代わり深く突き刺さる。
		PRINTFORML 5人以上の少女たちが連携し、乳首、喉奥、睾丸、会陰部、先端に至るまで、すべての性感帯を余すところなく苛み抜く。
		PRINTFORML 激痛に似た強烈すぎる快感の奔流が全身を駆け巡り、%CALLNAME:MASTER%の口からは涎が垂れ流され、叫び声すら上がらない。
		PRINTFORMW 「ほら、もっとビクビクして！ まだまだ奥に溜まってるでしょ…！」
		PRINTFORML 激しい痙攣とともに何度も何度も大量の精液を噴き出させられ、魂の髄まで吸い尽くされるような地獄の快楽に沈められた。
	ENDIF
ELSE
	; 【第3段階：8人以上】
	IF SEED == 0
		PRINTFORML 部屋を埋め尽くす熱気、充満する愛液の匂い、そして理性のタガが完全に消し飛んだ8人以上の淫乱な少女たち。
		PRINTFORML %CALLNAME:R_NAME1%、%CALLNAME:R_NAME2%、%CALLNAME:R_NAME3%をはじめとする群れを前に、
		PRINTFORMW %CALLNAME:MASTER%は逃げることすら許されない「共同の搾精生贄」として完全に組み敷かれていた。
		PRINTFORML すでに数え切れないほどの射精を強いられ、精嚢はとっくに枯れ果てているにもかかわらず、少女たちの狂乱は止まらない。
		PRINTFORML 「出ない？ ううん、出なくなるまで搾るんじゃないよ、出なくなってからが本当の搾り取りなんだから…！」
		PRINTFORMW 空っぽになった玉袋を力任せに揉みしだかれ、敏感すぎる先端を強引に吸い上げられ、奥深くを激しく掻き毟られる。
		PRINTFORML 出るはずのない精液を無理やり絞り出される激痛混じりのドライオーガズムに、%CALLNAME:MASTER%は白目を剥いて激しく跳ね上がる。
		PRINTFORMW ビクビクと痙攣するペニスから僅かに滲み出る透明な前立腺液すら、少女たちは歓喜の声を上げて飲み干していく。
		PRINTFORML 意識が朦朧として快楽の深淵へと沈みゆく中、%CALLNAME:MASTER%は完全に生き地獄のような極楽の中で果て続けた。
	ELSEIF SEED == 1
		PRINTFORML 朝の寝室はもはや人の住まう場所ではなく、肉と肉が激しくぶつかり合い、狂乱の嬌声が木霊する肉欲の坩堝だった。
		PRINTFORML 誰の腕が首に巻き付き、誰の胸が顔を覆い、誰の熱い秘所が自らを貪っているのかすら判別できない。
		PRINTFORMW 8人を超える淫魔の群れが、ベルトコンベアのように代わる代わる%CALLNAME:MASTER%の身体に跨がり、貪り尽くす。
		PRINTFORML 限界をとっくに超え、失神しかける%CALLNAME:MASTER%の顔に愛液を浴びせ、無理やり目を覚まさせては再び奥深くまで貫かせる。
		PRINTFORML 「あははっ、目がいっちゃってる！ でも腰は止まってないよ…もっと、もっと搾らせて…！」
		PRINTFORMW 手足は意志と無関係にピクピクと痙攣し、口からは泡混じりの涎がこぼれ、身体中の水分がすべて枯れ果てるまで貪り尽くされた。
	ELSE
		PRINTFORML 「ふふ、これだけ人数がいるんだもん、朝から誰一人満足させずに逃げられるわけないじゃない…」
		PRINTFORML %CALLNAME:R_NAME1%が顎を掴んで強制的に見つめ合わせる中、下半身では次から次へと少女たちが覆い被さり、貪欲に腰を打ち付ける。
		PRINTFORMW もはや%CALLNAME:MASTER%の自我など存在せず、ただ快感に反応してびくびくと反射的に汁を滴らせるだけの「生きた搾精機械」。
		PRINTFORML 身体の奥底から絞り出される激痛とオーガズムの波に、%CALLNAME:MASTER%の瞳からは光が消え、完全に意識を飛ばしながら果て続ける。
		PRINTFORML 少女たちは汗と愛液にまみれながら、主人公の限界を超えた姿にさらに興奮を募らせ、代わる代わる腰を狂ったように打ち付け続けた。
		PRINTFORMW やがて朝食の鐘が館に鳴り響く頃、少女たちは満足げに上気した顔で去っていき、ベッドの上には痙攣したまま身動き一つ取れない主人公の抜け殻だけが残された……。
	ENDIF
ENDIF

; --- 効果・数値計算 ---
; 射精回数決定
IF TIER == 1
	EJAC_COUNT = 3 + RAND:3
	LOSEBASE:MASTER:0 = 400
	BASE:MASTER:1 = MAX(0, BASE:MASTER:1 - 600)
ELSEIF TIER == 2
	EJAC_COUNT = 6 + RAND:4
	LOSEBASE:MASTER:0 = 800
	BASE:MASTER:1 = 0
ELSE
	EJAC_COUNT = 12 + RAND:5
	LOSEBASE:MASTER:0 = 1400
	BASE:MASTER:1 = 0
ENDIF

; 主人公の体力減少
BASE:MASTER:0 = MAX(1, BASE:MASTER:0 - LOSEBASE:MASTER:0)

; 主人公の射精・絶頂経験加算
EXP:MASTER:3 += EJAC_COUNT
FLAG:5040 += EJAC_COUNT

; 主人公が女性の場合はレズ・絶頂経験も加算
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
	; 珠の加算
	JUEL:CHARA_ID:1 += TIER * 150	; 快Vの珠
	JUEL:CHARA_ID:4 += TIER * 100	; 恭順の珠
	JUEL:CHARA_ID:5 += TIER * 200	; 欲情の珠
	JUEL:CHARA_ID:17 += TIER * 100	; 恥情の珠
	; 好感度加算
	CFLAG:CHARA_ID:2 += TIER * 3
	; 膣射精液量（妊娠チェック用）
	CFLAG:CHARA_ID:101 += TIER
	; 累積射精量
	FLAG:(5800 + NO:CHARA_ID) += TIER * 2
NEXT

DRAWLINE
SETCOLOR 255, 120, 180
PRINTFORML %CALLNAME:MASTER%は限界を遥かに超えて【{EJAC_COUNT}回】もの射精を強制された…
PRINTFORML 主人公体力 -{LOSEBASE:MASTER:0} / 気力完全枯渇（残り 0）
PRINTFORML 参加した{INRAN_COUNT}人の淫乱少女全員の精液経験・絶頂経験・好感度・各珠が大幅に上昇しました。
RESETCOLOR
DRAWLINE
WAIT
RETURN 1
'''

text += inran_group_func

with open(filepath, 'wb') as f:
    f.write(text.encode('cp932'))

print('Successfully added EVENT_NEWDAY_INRAN_GROUP and updated EVENT_NEWDAY!')
