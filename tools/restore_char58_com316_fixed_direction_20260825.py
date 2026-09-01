from pathlib import Path


PATH = Path(r"C:\Users\guile\era-angal\ERB\CHAR\CHAR_58_天宮るり_COM.ERB")


OLD = ''';--- COM316 髪を梳いて貰う ---
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


NEW = ''';--- COM316 髪を梳いて貰う ---
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
				PRINTFORMW 「るるる……あなたの髪の感触が、指先に返ってきます。もう少し、梳かしてあげますね、転校生のひと☆」
			ENDIF
		ENDIF
	ENDIF
ENDIF
'''


def main() -> None:
    text = PATH.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    if text.count(OLD) != 1:
        raise RuntimeError(f"expected one mixed COM316 block, got {text.count(OLD)}")
    PATH.write_bytes(text.replace(OLD, NEW, 1).replace("\n", "\r\n").encode("cp932"))
    print("restored CHAR58 COM316 to fixed actor direction")


if __name__ == "__main__":
    main()
