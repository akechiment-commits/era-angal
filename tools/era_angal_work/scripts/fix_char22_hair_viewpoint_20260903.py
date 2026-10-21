"""CHAR22いかりのCOM316を、いかりがPLAYERの髪を梳く側へ固定する。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_22_鯱いかり_COM.ERB"


COM316 = ''';--- COM316 髪を梳いて貰う ---
; 視点：TARGETがPLAYERの髪を梳く。PLAYERは梳かれる側
IF SELECTCOM == 316
	IF CFLAG:TARGET:217 == 0
		CFLAG:TARGET:217 = 1
		;初回
		PRINTFORMW 「髪、梳いてあげるし？　にししっ、あたし自分じゃ雑だけど、先輩の髪ならきれいにしてあげるしっ♪」
	ELSE
		A = RAND:3
		IF TALENT:TARGET:153
			IF A == 0
				PRINTFORMW 「ししょ～の髪、指を通すとさらさらで気持ちいいし～。にしし、もっと丁寧にしてあげるしっ♪」
			ELSEIF A == 1
				PRINTFORMW 「えへへ、ししょ～の後ろにいると近くて嬉しいし……髪の先まできれいにするし♪」
			ELSE
				PRINTFORMW 「んん、眠そうだし？　あたしが終わるまで、ししょ～はそのまま任せるし～♪」
			ENDIF
		ELSE
			IF A == 0
				PRINTFORMW 「先輩の髪、ここから梳くとさらさらになるし～。あたし、ちょっと得意になってきたし♪」
			ELSEIF A == 1
				PRINTFORMW 「にしし、髪の流れがきれいになったし～。先輩、あたしの腕前どうだし？♪」
			ELSE
				PRINTFORMW 「ふぃ～、毛先までできたし。先輩、振り向いて見せるし？　きれいにしたし～♪」
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
			PRINTFORMW 「ししょ～、頭を出すし♪　いつも頑張ってるから、今日はあたしがわしゃわしゃ褒めてあげますし～っ☆」
		ELSEIF A == 1
			PRINTFORMW 「にししっ、撫でるとししょ～があったかくなるし。あたしの膝で安心するまで、ここにいていいですし」
		ELSE
			PRINTFORMW 「よしよしですし♪　ししょ～を元気にする方法、ひとつ覚えたし。次に疲れたときもあたしを呼ぶし！」
		ENDIF
	ELSE
		IF A == 0
			PRINTFORMW 「先輩の髪に触れると、さらさらで気持ちいいし……そのまま楽にしてるし♪」
		ELSEIF A == 1
			PRINTFORMW 「泳いだあとの先輩の髪、あたしがわしゃわしゃにするし♪　にしし、今日はあたしの番だし！」
		ELSE
			PRINTFORMW 「にししっ、撫でると先輩の目が細くなるし♪　もう少しだけ、あたしの手ぇに預けるし？」
		ENDIF
	ENDIF
ENDIF
'''


def apply_hair_viewpoint(text: str) -> str:
    start = text.index(";--- COM316")
    end = text.index(";--- COM320", start)
    text = text[:start] + COM316.rstrip("\n") + "\n\n" + text[end:]
    start = text.index(";--- COM318")
    end = text.index(";=== IKARI MISSING COMMAND TRIAL END ===", start)
    return text[:start] + COM318.rstrip("\n") + "\n\n" + text[end:]


def main() -> int:
    text = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n")
    TARGET.write_bytes(apply_hair_viewpoint(text).replace("\n", "\r\n").encode("cp932"))
    print("CHAR22: COM316髪梳きとCOM318頭撫での行為者・追加口調を固定")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
