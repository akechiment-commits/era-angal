"""CHAR21すみれの髪梳き・頭撫での行為者と受け手を固定する。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_21_雉子すみれ_COM.ERB"


COM306 = ''';--- COM306 髪梳き ---
; 視点：PLAYERがTARGETの髪を手で梳く。TARGETは梳かれる側
IF SELECTCOM == 306
	IF CFLAG:TARGET:216 == 0
		CFLAG:TARGET:216 = 1
		;初回
		PRINTFORMW 「髪を梳いていただけるのですか？　ふむ……それでは、お願いいたします。眠ってしまいましたら、失礼♪」
	ELSE
		A = RAND:3
		IF TALENT:TARGET:153
			IF A == 0
				PRINTFORMW 「ふむ……あなたの指が髪を分けるたび、頭までゆるむようです。もう少し、このままで……♪」
			ELSEIF A == 1
				PRINTFORMW 「耳の近くを梳かれると、声がよく響きますね。……あなた、わたしが眠るまで続けてくださいますか♪」
			ELSE
				PRINTFORMW 「髪に触れられているだけなのに、あなたの気配まで近く……。おや、これは考えがまとまりません♪」
			ENDIF
		ELSE
			IF A == 0
				PRINTFORMW 「わたしの髪を……？　では、お願いいたします。絡まったところから、そっとお願いしますね」
			ELSEIF A == 1
				PRINTFORMW 「頭の重さが抜けるようです。先輩、これは居眠りではありませんから……たぶん」
			ELSE
				PRINTFORMW 「指が通るたび、乱れたところまで整っていきますね。……お礼は、あとで改めて」
			ENDIF
		ENDIF
	ENDIF
ENDIF
'''


COM307 = ''';--- COM307 櫛で梳かす ---
; 視点：PLAYERがTARGETの髪を櫛で梳く。TARGETは梳かれる側
IF SELECTCOM == 307
	IF CFLAG:TARGET:217 == 0
		CFLAG:TARGET:217 = 1
		;初回
		PRINTFORMW 「その櫛で、わたしの髪を……？　はい、お願いいたします。桔梗色の櫛は、少しだけ大切なものなのです♪」
	ELSE
		A = RAND:3
		IF TALENT:TARGET:153
			IF A == 0
				PRINTFORMW 「櫛の歯が頭皮をなぞるたび、思考まで静かになります。あなたのそばでは、理屈を休ませてもよいでしょうか♪」
			ELSEIF A == 1
				PRINTFORMW 「髪を整えてくださるあなたの手つき、絵筆よりも慎重ですね。……嬉しいです♪」
			ELSE
				PRINTFORMW 「あ、そこは……。櫛が通るたび、肩の力が抜けていきます。もう一度、お願いします♪」
			ENDIF
		ELSE
			IF A == 0
				PRINTFORMW 「櫛をお借りして、わたしの髪を……。ふむ、細いところは絡みやすいので、そっとお願いいたします」
			ELSEIF A == 1
				PRINTFORMW 「毛先まで通ると、見た目だけでなく気分も変わりますね。先輩、腕を上げましたね」
			ELSE
				PRINTFORMW 「……なるほど、櫛とは便利です。ですが、扱う人の手が丁寧でなければ意味がありませんね」
			ENDIF
		ENDIF
	ENDIF
ENDIF
'''


COM312 = ''';--- COM312 頭を撫でる ---
; 視点：PLAYERがTARGETの頭を撫でる。TARGETは撫でられる側
IF SELECTCOM == 312
	IF CFLAG:TARGET:217 == 0
		CFLAG:TARGET:217 = 1
		;初回
		PRINTFORMW 「頭を撫でてくださるのですか？　ふむ……では、少しだけ甘えさせていただきますね」
	ELSE
		A = RAND:3
		;--- 失敗時 ---
		IF TFLAG:18 == -1
			IF TALENT:TARGET:153
				;恋人・失敗
				PRINTFORMW 「すみません、今は……いえ、あなたの手なら、離れないでください。落ちつきますから」
			ELSE
				;失敗
				PRINTFORMW 「頭を撫でるのですか？　あの、わたしは小さな子どもでは……。……ですが、手はそのままで結構です」
			ENDIF
		;--- 成功時 ---
		ELSE
			;--- 恋人 ---
			IF TALENT:TARGET:153
				IF A == 0
					PRINTFORMW 「あなたの手が髪に触れると、言葉が少なくなります。……このまま、そばにいてください♪」
				ELSEIF A == 1
					PRINTFORMW 「撫でられていると、診察のあとのように力が抜けますね。ふふ、今日は患者役でよろしいでしょうか♪」
				ELSE
					PRINTFORMW 「もう少し、耳の近くを……。いえ、注文が多いですか？　でも、あなたなら安心です♪」
				ENDIF
			;--- 親密 ---
			ELSEIF ABL:TARGET:0 >= 6
				IF A == 0
					PRINTFORMW 「手の重さがちょうどよいですね。ふむ、眠気まで来るとは興味深いです」
				ELSEIF A == 1
					PRINTFORMW 「髪が乱れても構いません。今は整えるより、触れていただくほうが嬉しいので」
				ELSE
					PRINTFORMW 「撫でられると、返事を急がなくてよい気がします。……もう一度、お願いします」
				ENDIF
			;--- 通常 ---
			ELSE
				IF A == 0
					PRINTFORMW 「頭を撫でるのですか？　……では、お願いいたします。どの程度が適切でしょう」
				ELSEIF A == 1
					PRINTFORMW 「指が髪を通るたび、緊張がほどけますね。先輩、これは便利な慰労法です」
				ELSE
					PRINTFORMW 「おや、子ども扱いですか？　……抗議はしますが、手はそのままで結構です」
				ENDIF
			ENDIF
		ENDIF
	ENDIF
ENDIF
'''


COM316 = ''';--- COM316 髪を梳く ---
; 視点：TARGETがPLAYERの髪を梳く。PLAYERは梳かれる側
IF SELECTCOM == 316
	IF CFLAG:TARGET:217 == 0
		CFLAG:TARGET:217 = 1
		;初回
		PRINTFORMW 「あなたの髪を、わたしが梳いて差し上げますね。ふむ、絡まりはありません……丁寧に参ります♪」
	ELSE
		A = RAND:3
		IF TALENT:TARGET:153
			IF A == 0
				PRINTFORMW 「ふむ、あなたの髪は、指を通すと素直に整いますね。……わたしが触れているのに、あなたのほうが落ちついて見えます♪」
			ELSEIF A == 1
				PRINTFORMW 「耳の後ろまで梳きますね。ここは見えにくいぶん、わたしの手に任せてください」
			ELSE
				PRINTFORMW 「おや、眠ってしまいそうですか？　では、起こさないように、もう少しだけ続けます♪」
			ENDIF
		ELSE
			IF A == 0
				PRINTFORMW 「先輩の髪を梳くのは、思ったより慎重になります。……痛くないようにいたしますね」
			ELSEIF A == 1
				PRINTFORMW 「櫛を通す向きは、こちらでよろしいでしょうか。ふむ、整っていく様子は面白いです」
			ELSE
				PRINTFORMW 「はい、毛先まで終わりました。……振り向いていただけますか？　出来栄えを確認したいです」
			ENDIF
		ENDIF
	ENDIF
ENDIF
'''


COM318 = ''';--- COM318 頭を撫でてもらう ---
; 視点：TARGETがPLAYERの頭を撫でる。PLAYERは撫でられる側
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:85
		IF A == 0
			PRINTFORMW 「転校生さん、こちらへ頭を。今日はわたしが労う側ですので、安心して目を閉じてください」
		ELSEIF A == 1
			PRINTFORMW 「髪を撫でると、普段より幼いお顔になりますね。……この観察結果は、わたしだけの記録にしておきます」
		ELSE
			PRINTFORMW 「よく頑張りました。言葉だけでは足りないので、落ちつくまで何度でも撫でさせてくださいね」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「転校生さんの髪は、この方向へ撫でると整うのですね。ふむ、実用と慰労を兼ねた良い方法です」
		ELSEIF A == 1
			PRINTFORMW 「頭を撫でられるのは子どもだけ、という規則はありません。遠慮なさらず、もう少し低くしてください」
		ELSE
			PRINTFORMW 「お疲れの方には休息が必要です。まずは五分間、わたしの膝で何も考えずにいてください」
		ENDIF
	ENDIF
ENDIF
'''


def replace_section(text: str, start: str, end: str, replacement: str) -> str:
    first = text.index(start)
    last = text.index(end, first)
    return text[:first] + replacement.rstrip("\n") + "\n\n" + text[last:]


def apply_viewpoint_fixes(text: str) -> str:
    text = replace_section(text, ";--- COM306", ";--- COM307", COM306)
    text = replace_section(text, ";--- COM307", ";--- COM309", COM307)
    text = replace_section(text, ";--- COM312", ";--- COM313", COM312)
    text = replace_section(text, ";--- COM316", ";--- COM320", COM316)
    text = replace_section(text, ";--- COM318", ";=== SUMIRE MISSING COMMAND TRIAL END ===", COM318)
    return text


def main() -> int:
    text = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n")
    text = apply_viewpoint_fixes(text)
    TARGET.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print("CHAR21: COM306/307/312/316/318の髪梳き・頭撫で視点を固定")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
