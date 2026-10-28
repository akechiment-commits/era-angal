from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_06_藍乃あいか_COM.ERB")


BLOCK = """;--- COM316 髪を梳いて貰う ---
IF SELECTCOM == 316
	IF CFLAG:TARGET:217 == 0
		CFLAG:TARGET:217 = 1
		;初回：あいかが先輩の髪を梳く
		PRINTFORMW 「えっ、わたしが髪を梳くんですか? あ、あの、任せてください。ぼさぼさだったら恥ずかしいんですけど……」
	ELSE
		A = RAND:3
		IF TALENT:TARGET:153
			IF A == 0
				PRINTFORMW 「%CALLNAME:PLAYER%先輩の髪、さらさら……。わたしが梳くと、少しだけ眠そうになるの、かわいいです♪」
			ELSEIF A == 1
				PRINTFORMW 「動かないでくださいね。わたし、髪を傷めないように、丁寧にしますから……」
			ELSE
				PRINTFORMW 「先輩の髪を梳いてると、いつも頼ってばかりのわたしでも、役に立ててる気がします……」
			ENDIF
		ELSE
			IF A == 0
				PRINTFORMW 「あの、転校生の先輩。髪を梳いてもいいですか? わたし、チームメイトの髪なら結ったことがあるので……」
			ELSEIF A == 1
				PRINTFORMW 「うにゅ、絡まってますね……。痛くないようにほどくので、先輩、動かないでください」
			ELSE
				PRINTFORMW 「どうですか、これで整いました? わたし、自信はないですけど、最後までやりますから……」
			ENDIF
		ENDIF
	ENDIF
ENDIF
"""


def main() -> None:
    text = PATH.read_bytes().decode("cp932").replace("\r\n", "\n")
    start = text.find(";--- COM316 髪を梳いて貰う ---\n")
    if start < 0:
        raise RuntimeError("COM316 start not found")
    end = text.find("\n;--- COM", start + 1)
    if end < 0:
        raise RuntimeError("COM316 end not found")
    text = text[:start] + BLOCK.rstrip("\n") + text[end:]
    PATH.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print("CHAR06 COM316: active hair-combing viewpoint unified")


if __name__ == "__main__":
    main()
