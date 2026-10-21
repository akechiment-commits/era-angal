"""CHAR23・鶯木こはるの既存多重絶頂と性交語彙を整える。"""

from __future__ import annotations

from redo_char20_rand3_20260902 import replace_block, section_spans


MULTI_ORGASM_BLOCK = r''' ;--- 五重絶頂（全部位同時） ---
IF TFLAG:710 >= 5
	;★全部位最強（特別）
	IF NOWEX:0 >= 9 && NOWEX:1 >= 9 && NOWEX:2 >= 9 && NOWEX:3 >= 9 && NOWEX:6 >= 9
		A = RAND:3
		IF TALENT:TARGET:153
			IF A == 0
				;恋人・五重絶頂・全部位最強★・1
				PRINTFORMW 「がう゛ぅ……っ!?　あ、あれ……っ、息、どこ……っ。お兄ちゃん先輩、そば、いて……っ♪」
			ELSEIF A == 1
				;恋人・五重絶頂・全部位最強★・2
				PRINTFORMW 「ひぐっ……あ゛っ……っ、もう、声にできない……っ。おいら、いま、どうなって……っ♪」
			ELSE
				;恋人・五重絶頂・全部位最強★・3
				PRINTFORMW 「きゅうう゛ん……っ、がう゛っ……お兄ちゃん先輩……っ、離れたら、だめ……っ♪」
			ENDIF
		ELSE
			IF A == 0
				;通常・五重絶頂・全部位最強★・1
				PRINTFORMW 「がう゛っ……!?　ひとつ来たら、また……っ。あ、あれ、止まらないぞ……っ」
			ELSEIF A == 1
				;通常・五重絶頂・全部位最強★・2
				PRINTFORMW 「ひあ゛っ……っ、息、できな……っ。おいら、もう、つかまってる……っ」
			ELSE
				;通常・五重絶頂・全部位最強★・3
				PRINTFORMW 「あ゛っ……が、がう゛……っ、足も声も、勝手に……っ。すごすぎるぞ……っ」
			ENDIF
		ENDIF
	;いずれかの部位が最強
	ELSEIF NOWEX:0 >= 9 || NOWEX:1 >= 9 || NOWEX:2 >= 9 || NOWEX:3 >= 9 || NOWEX:6 >= 9
		A = RAND:3
		IF TALENT:TARGET:153
			IF A == 0
				;恋人・五重絶頂・最強・1
				PRINTFORMW 「あ゛っ……っ、お兄ちゃん先輩……っ、好きって言う暇もない……っ♪」
			ELSEIF A == 1
				;恋人・五重絶頂・最強・2
				PRINTFORMW 「ひっ……あ゛、あ……っ、もう少し、やさしく……っ、でも、止めないで……っ♪」
			ELSE
				;恋人・五重絶頂・最強・3
				PRINTFORMW 「がう゛……っ、きゅうん……っ、おまえの熱で、ぜんぶほどける……っ♪」
			ENDIF
		ELSE
			IF A == 0
				;通常・五重絶頂・最強・1
				PRINTFORMW 「あ゛っ……!?　そこから来るの、ずるいぞ……っ」
			ELSEIF A == 1
				;通常・五重絶頂・最強・2
				PRINTFORMW 「ひぐっ……っ、ひとつじゃない……っ。おいら、追いつけない……っ」
			ELSE
				;通常・五重絶頂・最強・3
				PRINTFORMW 「んあ゛……っ、がう゛……っ、頭がぼんやりするぞ……っ」
			ENDIF
		ENDIF
	;いずれかの部位が強
	ELSEIF NOWEX:0 >= 2 || NOWEX:1 >= 2 || NOWEX:2 >= 2 || NOWEX:3 >= 2 || NOWEX:6 >= 2
		A = RAND:3
		IF TALENT:TARGET:153
			IF A == 0
				;恋人・五重絶頂・強・1
				PRINTFORMW 「あぁっ……っ、重なって、息が甘くなる……っ。お兄ちゃん先輩……♪」
			ELSEIF A == 1
				;恋人・五重絶頂・強・2
				PRINTFORMW 「がうう……っ、きゅん、きゅんって来るな……っ。おいら、笑っちゃう……っ♪」
			ELSE
				;恋人・五重絶頂・強・3
				PRINTFORMW 「はぁっ……っ、身体が波みたいだ……っ。おまえのそば、好きだぞ……♪」
			ENDIF
		ELSE
			IF A == 0
				;通常・五重絶頂・強・1
				PRINTFORMW 「んあっ……っ、ひとつずつじゃないんだな……っ。がう、変な感じだぞ……っ」
			ELSEIF A == 1
				;通常・五重絶頂・強・2
				PRINTFORMW 「ひゃうっ……っ、胸も脚も、同じにぞわっとする……っ」
			ELSE
				;通常・五重絶頂・強・3
				PRINTFORMW 「くぅっ……っ、おいら、どこから返事すればいいんだ……っ」
			ENDIF
		ENDIF
	ELSE
		A = RAND:3
		IF TALENT:TARGET:153
			IF A == 0
				;恋人・五重絶頂・通常・1
				PRINTFORMW 「がうがうっ♪　あ、また来た……っ。お兄ちゃん先輩といると、忙しいな♪」
			ELSEIF A == 1
				;恋人・五重絶頂・通常・2
				PRINTFORMW 「えへへ……っ、身体が勝手に跳ねるぞ。おまえ、見てるか……♪」
			ELSE
				;恋人・五重絶頂・通常・3
				PRINTFORMW 「はぁ……っ、きゅんってして、ふわってして……おいら、力が抜けたぞ♪」
			ENDIF
		ELSE
			IF A == 0
				;通常・五重絶頂・通常・1
				PRINTFORMW 「わぷっ……っ、いっぺんに来ると、びっくりするぞ……っ」
			ELSEIF A == 1
				;通常・五重絶頂・通常・2
				PRINTFORMW 「ぷはっ……っ、まだ揺れてるな。がう、おいら、変な顔してないか……？」
			ELSE
				;通常・五重絶頂・通常・3
				PRINTFORMW 「んん……っ、身体のあちこちが、まだ追いかけてくるぞ……っ」
			ENDIF
		ENDIF
	ENDIF

;--- 複絶頂（2～4箇所同時）---
ELSEIF TFLAG:710 >= 2
	;--- 膣を含む複絶頂 ---
	IF NOWEX:1 > 0
		IF NOWEX:0 >= 9 || NOWEX:1 >= 9 || NOWEX:2 >= 9 || NOWEX:3 >= 9 || NOWEX:6 >= 9
			A = RAND:3
			IF TALENT:TARGET:153
				IF A == 0
					;恋人・複絶頂・膣含む・最強・1
					PRINTFORMW 「あ゛っ……奥まで来た……っ。お兄ちゃん先輩の熱、逃げ場がないぞ……っ♪」
				ELSEIF A == 1
					;恋人・複絶頂・膣含む・最強・2
					PRINTFORMW 「ひぐっ……っ、そこだけじゃない……っ。胸まで、同じにほどける……っ♪」
				ELSE
					;恋人・複絶頂・膣含む・最強・3
					PRINTFORMW 「がう゛……っ、奥がきゅうって……っ。好き、好きだぞ……っ♪」
				ENDIF
			ELSE
				IF A == 0
					;通常・複絶頂・膣含む・最強・1
					PRINTFORMW 「んあ゛っ……!?　お、奥が跳ねたぞ……っ。まだ、ほかも……っ」
				ELSEIF A == 1
					;通常・複絶頂・膣含む・最強・2
					PRINTFORMW 「ひっ……あ゛っ、身体の中まで響く……っ。がう、怖いくらいだぞ……っ」
				ELSE
					;通常・複絶頂・膣含む・最強・3
					PRINTFORMW 「がうう゛……っ、脚が、もう立たない……っ。止まらないぞ……っ」
				ENDIF
			ENDIF
		ELSEIF NOWEX:0 >= 2 || NOWEX:1 >= 2 || NOWEX:2 >= 2 || NOWEX:3 >= 2 || NOWEX:6 >= 2
			A = RAND:3
			IF TALENT:TARGET:153
				IF A == 0
					;恋人・複絶頂・膣含む・強・1
					PRINTFORMW 「あぁっ……っ、奥も一緒にきゅんってする……っ。お兄ちゃん先輩、近い……っ♪」
				ELSEIF A == 1
					;恋人・複絶頂・膣含む・強・2
					PRINTFORMW 「がうう……っ、胸の奥まで熱いな……っ。おまえのせいだぞ……♪」
				ELSE
					;恋人・複絶頂・膣含む・強・3
					PRINTFORMW 「はぁ……っ、深いところが震えてる……っ。おいら、気持ちいい……っ♪」
				ENDIF
			ELSE
				IF A == 0
					;通常・複絶頂・膣含む・強・1
					PRINTFORMW 「んあっ……っ、奥まで、つられてる……っ。がう、ふしぎだぞ……」
				ELSEIF A == 1
					;通常・複絶頂・膣含む・強・2
					PRINTFORMW 「ひゃうっ……っ、そこがじんじんする……っ。おいら、慣れてないのに……っ」
				ELSE
					;通常・複絶頂・膣含む・強・3
					PRINTFORMW 「くぅっ……っ、内側からぞわぞわするな……っ。息がへんだぞ……」
				ENDIF
			ENDIF
		ELSE
			A = RAND:3
			IF TALENT:TARGET:153
				IF A == 0
					;恋人・複絶頂・膣含む・通常・1
					PRINTFORMW 「がうがう♪　奥もついてきたぞ。お兄ちゃん先輩、あったかいな♪」
				ELSEIF A == 1
					;恋人・複絶頂・膣含む・通常・2
					PRINTFORMW 「えへへ……っ、そこまで一緒に来るんだな。おいら、嬉しいぞ♪」
				ELSE
					;恋人・複絶頂・膣含む・通常・3
					PRINTFORMW 「ふぅ……っ、奥がふわふわするな。おまえとだと、もっと好きだぞ♪」
				ENDIF
			ELSE
				IF A == 0
					;通常・複絶頂・膣含む・通常・1
					PRINTFORMW 「わぷっ、奥まで来たな……っ。がう、身体って正直だぞっ」
				ELSEIF A == 1
					;通常・複絶頂・膣含む・通常・2
					PRINTFORMW 「ぷはっ……っ、内側がまだきゅんきゅんしてるな……♪」
				ELSE
					;通常・複絶頂・膣含む・通常・3
					PRINTFORMW 「んん……っ、変なところまであったかいぞ……。お兄ちゃん先輩、すごいな♪」
				ENDIF
			ENDIF
		ENDIF
	;--- 膣を含まない複絶頂 ---
	ELSE
		IF NOWEX:0 >= 9 || NOWEX:2 >= 9 || NOWEX:3 >= 9 || NOWEX:6 >= 9
			A = RAND:3
			IF TALENT:TARGET:153
				IF A == 0
					;恋人・複絶頂・膣なし・最強・1
					PRINTFORMW 「あ゛っ……っ、胸とそこが重なる……っ。お兄ちゃん先輩、見ないで……いや、見て……っ♪」
				ELSEIF A == 1
					;恋人・複絶頂・膣なし・最強・2
					PRINTFORMW 「ひぐっ……っ、手も口も、どっちも熱い……っ。おいら、逃げられない……っ♪」
				ELSE
					;恋人・複絶頂・膣なし・最強・3
					PRINTFORMW 「がう゛……っ、きゅううん……っ、身体の外まで溶けるみたいだ……っ♪」
				ENDIF
			ELSE
				IF A == 0
					;通常・複絶頂・膣なし・最強・1
					PRINTFORMW 「んあ゛っ……!?　こっちも、あっちも……っ。がう、声が変になるぞ……っ」
				ELSEIF A == 1
					;通常・複絶頂・膣なし・最強・2
					PRINTFORMW 「ひっ……あ゛っ、胸まで跳ねた……っ。おいら、もう、だめ……っ」
				ELSE
					;通常・複絶頂・膣なし・最強・3
					PRINTFORMW 「がうう゛……っ、息がうまくできない……っ。身体が勝手に揺れるぞ……っ」
				ENDIF
			ENDIF
		ELSEIF NOWEX:0 >= 2 || NOWEX:2 >= 2 || NOWEX:3 >= 2 || NOWEX:6 >= 2
			A = RAND:3
			IF TALENT:TARGET:153
				IF A == 0
					;恋人・複絶頂・膣なし・強・1
					PRINTFORMW 「あぁっ……っ、胸も一緒にきゅんってする……っ。お兄ちゃん先輩、まだ近くにいて……♪」
				ELSEIF A == 1
					;恋人・複絶頂・膣なし・強・2
					PRINTFORMW 「がうう……っ、そこから熱がひろがるな……っ。おいら、嬉しくて力が抜けるぞ……♪」
				ELSE
					;恋人・複絶頂・膣なし・強・3
					PRINTFORMW 「はぁ……っ、重なってくると、笑いそうになる……っ。好きだぞ、お兄ちゃん先輩……♪」
				ENDIF
			ELSE
				IF A == 0
					;通常・複絶頂・膣なし・強・1
					PRINTFORMW 「んあっ……っ、身体の外と中が、同時に跳ねる……っ」
				ELSEIF A == 1
					;通常・複絶頂・膣なし・強・2
					PRINTFORMW 「ひゃうっ……っ、胸が先に返事したぞ……っ。がう、すごいな……」
				ELSE
					;通常・複絶頂・膣なし・強・3
					PRINTFORMW 「くぅっ……っ、いろんな熱が残ってる……っ。おいら、まだ動けないぞ……」
				ENDIF
			ENDIF
		ELSE
			A = RAND:3
			IF TALENT:TARGET:153
				IF A == 0
					;恋人・複絶頂・膣なし・通常・1
					PRINTFORMW 「がうがう♪　胸も一緒に気持ちよくなったぞ。お兄ちゃん先輩、上手だな♪」
				ELSEIF A == 1
					;恋人・複絶頂・膣なし・通常・2
					PRINTFORMW 「えへへ……っ、あっちこっち跳ねて、楽しかったぞ♪」
				ELSE
					;恋人・複絶頂・膣なし・通常・3
					PRINTFORMW 「ふぅ……っ、まだ身体がぽかぽかだな。おまえとだと、また欲しくなるぞ♪」
				ENDIF
			ELSE
				IF A == 0
					;通常・複絶頂・膣なし・通常・1
					PRINTFORMW 「わぷっ、胸まで一緒にいったぞ！　がう、びっくりしたな♪」
				ELSEIF A == 1
					;通常・複絶頂・膣なし・通常・2
					PRINTFORMW 「ぷはっ……っ、まだぞわぞわするぞ。身体、忙しいな……♪」
				ELSE
					;通常・複絶頂・膣なし・通常・3
					PRINTFORMW 「んん……っ、いろんなところがふわふわだ……。がう、変なの♪」
				ENDIF
			ENDIF
		ENDIF
	ENDIF
'''


INTERCOURSE_REWRITES = {
    20: {
        "「はぁ、はぁ……っ、お兄ちゃん先輩、すきだ……っ。おいらの中、おまえでいっぱいにして……♪」":
        "「はぁ、はぁ……っ、お兄ちゃん先輩と交尾するの、楽しいな……っ。おいらの中、もっとおまえでいっぱいにして……♪」",
    },
    21: {
        "「んっ……後ろから、お兄ちゃん先輩に包まれて……っ。けものみたいで、おいららしいな……♪」":
        "「んっ……後ろから、お兄ちゃん先輩に包まれて……っ。交尾って、気持ちいいな……おいら、もっとしたい……♪」",
    },
    34: {
        "「はぁ……っ、おいらが、お兄ちゃん先輩を気持ちよくする番だ……っ。いっぱい、感じてくれ……♪」":
        "「はぁ……っ、お兄ちゃん先輩と交尾するの、楽しいぞ……っ。もっと、おいらを見ててくれ……♪」",
    },
    36: {
        "「んあっ……っ、お尻で、上に乗るのか……っ。が、がう、むずかしい格好だぞ……っ」":
        "「んあっ……っ、お尻で交尾するの、へんな感じだぞ……っ。でも、がう、気持ちいい……っ」",
    },
}


EJAC_REWRITES = {
    "「はぁ……っ、こんなにいっぱい注がれて……っ。お兄ちゃん先輩のぜんぶ、おいらが受け止めたぞ……えへへ♪」":
    "「はぁ……っ、こんなにいっぱい……っ。交尾って、気持ちいいな……お兄ちゃん先輩、もっと近くにいて……♪」",
    "「くぅ……っ、また奥に広がる……っ。ふしぎだけど、あったかくて、いい……っ」":
    "「くぅ……っ、また奥に広がる……っ。交尾、気持ちいいけど……まだ、力が抜けないぞ……っ」",
    "「んっ……奥に、お兄ちゃん先輩の……。あったかいな……。おいら、おまえと繋がってるって感じがする♪」":
    "「んっ……奥に、お兄ちゃん先輩の……。交尾、すごく気持ちいいな……おいら、まだ離れたくないぞ♪」",
    "「がう、また中だ。あったかいのがいっぱいで、おなかぽかぽかだぞ、えへへ♪」":
    "「がう、また中だ。交尾って、こんなに気持ちいいんだな……えへへ♪」",
}


def apply_existing_orgasm(text: str) -> str:
    marker_start = ";--- 五重絶頂（全部位同時） ---"
    marker_end = ";--- 単絶頂（1箇所） ---"
    start = text.index(marker_start)
    end = text.index(marker_end, start)
    text = text[:start] + MULTI_ORGASM_BLOCK.lstrip() + "\n" + text[end:]
    return text


def apply_intercourse_words(text: str) -> str:
    for command, rewrites in INTERCOURSE_REWRITES.items():
        start, end = section_spans(text)[command]
        block = text[start:end]
        for old, new in rewrites.items():
            if block.count(old) != 1:
                raise ValueError(f"CHAR23性交語彙の置換対象が一意でない: COM{command} {old}")
            block = block.replace(old, new)
        text = replace_block(text, command, block)
    for old, new in EJAC_REWRITES.items():
        count = text.count(old)
        if count != 1:
            raise ValueError(f"CHAR23中出し語彙の置換対象が一意でない: {old} ({count})")
        text = text.replace(old, new)
    return text


def apply_existing_rewrites(text: str) -> str:
    text = apply_existing_orgasm(text)
    return apply_intercourse_words(text)
