"""CHAR21すみれの甘い言葉を、言われた側の反応へ固定する。"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_21_雉子すみれ_COM.ERB"


COM311 = ''';--- COM311 甘い言葉 ---
; 視点：PLAYERがTARGETへ甘い言葉を言う。TARGETは言われて反応する側
IF SELECTCOM == 311
	IF CFLAG:TARGET:216 == 0
		CFLAG:TARGET:216 = 1
		;初回
		PRINTFORMW 「あ、甘い言葉、ですか……？　わたしに言ってくださるのですか。……ふむ、少しだけ、聞かせてください」
	ELSE
		A = RAND:3
		;--- 失敗時 ---
		IF TFLAG:18 == -1
			IF TALENT:TARGET:153
				;恋人・失敗
				PRINTFORMW 「もう……。そんなに真っ直ぐ見つめられると、返事の前に顔が熱くなります。……聞こえていますから」
			ELSE
				;失敗
				PRINTFORMW 「ふむ、甘い言葉への返答を求めているのですね。……いえ、聞いてはおります。少々、返事を考えさせてください」
			ENDIF
		;--- 成功時 ---
		ELSE
			;--- 恋人 ---
			IF TALENT:TARGET:153
				IF A == 0
					PRINTFORMW 「あ……。そんなことを言われては、わたし、どんな顔をすれば……。嬉しい、ですけれど……♪」
				ELSEIF A == 1
					PRINTFORMW 「あなたの声で聞くと、ありふれた言葉も特別に響くのですね。……ふむ、これは困りました♪」
				ELSE
					PRINTFORMW 「好きと言ってもらえるのは、嬉しいものですね。……どんな賞よりも、今は幸せです♪」
				ENDIF
			;--- 親密 ---
			ELSEIF ABL:TARGET:0 >= 6
				IF A == 0
					PRINTFORMW 「そ、そういう言い方は……。胸の奥が落ちつきません。ですが、嫌ではありません」
				ELSEIF A == 1
					PRINTFORMW 「ふむ……。言葉だけでこんなに動揺するとは、興味深い現象です。……観察は、後にします」
				ELSE
					PRINTFORMW 「わたしへの言葉として受け取ってよいのですね。……では、忘れないようにしておきます」
				ENDIF
			;--- 通常 ---
			ELSE
				IF A == 0
					PRINTFORMW 「え、わたしに……？　あの、驚いております。聞き間違いではありませんよね」
				ELSEIF A == 1
					PRINTFORMW 「おや、ずいぶん真剣な表情です。……ふむ、まずはお礼を申し上げます」
				ELSE
					PRINTFORMW 「甘い言葉は、聞く側も困るものですね。……ですが、不快ではありません」
				ENDIF
			ENDIF
		ENDIF
	ENDIF
ENDIF
'''


def replace_section(text: str, start: str, end: str, replacement: str) -> str:
    first = text.index(start)
    last = text.index(end, first)
    return text[:first] + replacement.rstrip("\n") + "\n\n" + text[last:]


def apply_sweet_words_fix(text: str) -> str:
    return replace_section(text, ";--- COM311", ";--- COM312", COM311)


def main() -> int:
    text = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n")
    text = apply_sweet_words_fix(text)
    TARGET.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print("CHAR21: COM311甘い言葉を言われる側の反応へ固定")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
