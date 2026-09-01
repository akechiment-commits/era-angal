from pathlib import Path


PATH = Path(r"C:\Users\guile\era-angal\ERB\CHAR\CHAR_58_天宮るり_COM.ERB")


OLD_316 = ''';--- COM316 髪を梳いて貰う ---
IF SELECTCOM == 316
	IF CFLAG:TARGET:217 == 0
		CFLAG:TARGET:217 = 1
		;初回
		PRINTFORMW 「るるる、あなたの髪を梳いてあげるんですか……？　めずらしい。じゃあ、やってみます……☆」
	ELSE
		A = RAND:3
		IF TALENT:TARGET:153
			IF A == 0
				PRINTFORMW 「ん……あなたの髪を梳いていると、気持ちいい……すぅ……すぅ……。あ、寝そうになった、るるる♪」
			ELSEIF A == 1
				PRINTFORMW 「るるる、優しい手つき……。あなたの髪を梳いていると安心しちゃう。もっと、続けて♪」
			ELSE
				PRINTFORMW 「あなたの髪を梳くの、特別な感じ……。るり、あなたにだけは、こうしてあげるみたい☆」
			ENDIF
		ELSE
			IF A == 0
				PRINTFORMW 「るるる、人の髪を梳くのは、不思議な感覚……。任せてもらうって、こういうことですか☆」
			ELSEIF A == 1
				PRINTFORMW 「ふぅむ、わたしの手つき、丁寧でしょう。観測データに追加します……心地よい、です♪」
			ELSE
				PRINTFORMW 「くすぐったい……。でも、嫌じゃありません。続けていいですよ、転校生のひと、るるる☆」
			ENDIF
		ENDIF
	ENDIF
ENDIF
'''


NEW_316 = ''';--- COM316 髪を梳いて貰う ---
IF SELECTCOM == 316
	IF CFLAG:TARGET:217 == 0
		CFLAG:TARGET:217 = 1
		;初回
		IF TFLAG:45
			PRINTFORMW 「るるる、あなたの髪を梳いてあげるんですか……？　めずらしい。じゃあ、やってみます……☆」
		ELSE
			PRINTFORMW 「髪を、梳いてもらう……？　るるる、いいですよ。じっとしていますね、転校生のひと☆」
		ENDIF
	ELSE
		IF TFLAG:45
			A = RAND:3
			IF TALENT:TARGET:153
				IF A == 0
					PRINTFORMW 「ん……あなたの髪を梳いていると、気持ちいい……すぅ……すぅ……。あ、寝そうになった、るるる♪」
				ELSEIF A == 1
					PRINTFORMW 「るるる、優しい手つき……。あなたの髪を梳いていると安心しちゃう。もっと、続けて♪」
				ELSE
					PRINTFORMW 「あなたの髪を梳くの、特別な感じ……。るり、あなたにだけは、こうしてあげるみたい☆」
				ENDIF
			ELSE
				IF A == 0
					PRINTFORMW 「るるる、人の髪を梳くのは、不思議な感覚……。任せてもらうって、こういうことですか☆」
				ELSEIF A == 1
					PRINTFORMW 「ふぅむ、わたしの手つき、丁寧でしょう。観測データに追加します……心地よい、です♪」
				ELSE
					PRINTFORMW 「くすぐったい……。でも、嫌じゃありません。もう少し、梳かしてあげますね、転校生のひと、るるる☆」
				ENDIF
			ENDIF
		ELSE
			A = RAND:3
			IF TALENT:TARGET:153
				IF A == 0
					PRINTFORMW 「あたしの髪、梳いてもらうと……なんだか落ちつくね♪　ん、もう少しだけ☆」
				ELSEIF A == 1
					PRINTFORMW 「あなたの手で梳いてもらうの、好き……。星座を結ぶみたいで、静かになります☆」
				ELSE
					PRINTFORMW 「……ふぅん。恋人に髪を預けるって、こういうことですか。るるる、悪くありません♪」
				ENDIF
			ELSE
				IF A == 0
					PRINTFORMW 「髪を梳いてもらうのは、嫌いではありません。……でも、乱暴にしたら、すぐに言いますよ☆」
				ELSEIF A == 1
					PRINTFORMW 「人に髪を梳いてもらうの、めずらしいですね。観測対象としては……いえ、なんでもありません♪」
				ELSE
					PRINTFORMW 「くすぐったい……。でも、手を止めなくてもいいです。もう少しだけ、お願いします☆」
				ENDIF
			ENDIF
		ENDIF
	ENDIF
ENDIF
'''


OLD_318 = ''';--- COM318 頭を撫でてもらう ---
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「ん…あなたの頭を撫でてると、落ち着く、もう少しだけ、続けて♪」
		ELSEIF A == 1
			PRINTFORMW 「あなたの髪を梳く手が優しい、あたしまで、静かになるみたい♪」
		ELSE
			PRINTFORMW 「るるる、頭から入る重力は、心まで静かにするね☆」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あなたの頭を撫でて、ん、接触が、緊張を下げています」
		ELSEIF A == 1
			PRINTFORMW 「髪を梳く手の速度と呼吸が同期、安心の反応でしょうか☆」
		ELSE
			PRINTFORMW 「るるる、観測者にも、こうして休む時間が必要なのですね」
		ENDIF
	ENDIF
ENDIF
'''


NEW_318 = ''';--- COM318 頭を撫でてもらう ---
IF SELECTCOM == 318
	A = RAND:3
	IF TALENT:TARGET:153
		IF A == 0
			PRINTFORMW 「ん……じっとしてて。こうしてると、あなたの緊張がほどけていくの、わかります♪」
		ELSEIF A == 1
			PRINTFORMW 「髪にも触れておきますね。……ふふ、さっきより呼吸が静かになりました☆」
		ELSE
			PRINTFORMW 「るるる……。あなたが静かになるまで、るりはここにいます」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「あなた、少し肩に力が入っています。……ほら、息を吐いて。あたしが撫でていますから」
		ELSEIF A == 1
			PRINTFORMW 「髪に触れると、すこし安心しますか？　……そうですか。では、もう少しだけ」
		ELSE
			PRINTFORMW 「るるる……。目を閉じてもいいですよ。起きるまで、逃げませんから☆」
		ENDIF
	ENDIF
ENDIF
'''


def replace_once(text: str, old: str, new: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected one block, got {count}")
    return text.replace(old, new, 1)


def main() -> None:
    text = PATH.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    text = replace_once(text, OLD_316, NEW_316)
    text = replace_once(text, OLD_318, NEW_318)
    PATH.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print("rewrote CHAR58 COM316 role split and COM318")


if __name__ == "__main__":
    main()
