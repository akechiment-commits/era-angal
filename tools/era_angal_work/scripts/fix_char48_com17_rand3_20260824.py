from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_48_四方みつる_COM.ERB"


OLD = r'''IF SELECTCOM == 17
	IF TEQUIP:17
		;装着（トグル後なので TEQUIPオン＝今装着した）
		IF TALENT:TARGET:153
			PRINTFORMW 「ん、ふぁっ、ぼ、僕、ひとりでに反応して……。こんな乱れた姿、見せるのは君だけだよ……♪」
		ELSE
			PRINTFORMW 「おっと、なんだこれは……! 僕の腰が、勝手に動く……と、止めてくれっ、君っ!?」
		ENDIF
	ELSE
		;取り外し
		IF TALENT:TARGET:153
			PRINTFORMW 「ふぁ、まだ脈打って……。もう、君は、とことん甘やかすんだね……ふふ♪」
		ELSE
			PRINTFORMW 「ぬ、そろそろ限界だ! こんな玩具ひとつに、この僕が……うぅ、わ、わたし、もう、格好つけていられないよ……」
		ENDIF
	ENDIF
ENDIF'''

NEW = r'''IF SELECTCOM == 17
	IF TEQUIP:17
		;装着（トグル後なので TEQUIPオン＝今装着した）
		A = RAND:3
		IF TALENT:TARGET:153
			IF A == 0
				PRINTFORMW 「ん、ふぁっ、ぼ、僕、ひとりでに反応して……。こんな乱れた姿、見せるのは君だけだよ……♪」
			ELSEIF A == 1
				PRINTFORMW 「っ、また動いた……。君の前で、僕の身体だけが正直になるね……♪」
			ELSE
				PRINTFORMW 「あっ、だめ……っ。もう『僕』の顔を保てない。わたし、こんなに乱されて……」
			ENDIF
		ELSE
			IF A == 0
				PRINTFORMW 「おっと、なんだこれは……! 僕の腰が、勝手に動く……と、止めてくれっ、君っ!?」
			ELSEIF A == 1
				PRINTFORMW 「んっ……勝手に動くなぁ。転校生くん、こんなものを着けたまま平気でいられると思ったのかい？」
			ELSE
				PRINTFORMW 「ひゃっ、また来た……っ、止められないよ。僕の余裕が、どこかへ行っちゃう……！」
			ENDIF
		ENDIF
	ELSE
		;取り外し
		A = RAND:3
		IF TALENT:TARGET:153
			IF A == 0
				PRINTFORMW 「ふぁ、まだ脈打って……。もう、君は、とことん甘やかすんだね……ふふ♪」
			ELSEIF A == 1
				PRINTFORMW 「ん……外れたのに、まだ君の熱が残ってる。わたし、もう少しだけ甘えていたいな……♪」
			ELSE
				PRINTFORMW 「ふぅ……っ、やっと……。立てるかな、僕。君、肩を貸してくれるかい？」
			ENDIF
		ELSE
			IF A == 0
				PRINTFORMW 「ぬ、そろそろ限界だ! こんな玩具ひとつに、この僕が……うぅ、わ、わたし、もう、格好つけていられないよ……」
			ELSEIF A == 1
				PRINTFORMW 「はぁ……外れたぁ。ふふ、こんな玩具に夢中にされるなんて、僕も大概だね……」
			ELSE
				PRINTFORMW 「うぅ……もう十分だよ……。わたし、今は格好つけられないから、少し休ませて……」
			ENDIF
		ENDIF
	ENDIF
ENDIF'''


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    normalized = text.replace("\r\n", "\n")
    count = normalized.count(OLD)
    if count != 1:
        raise RuntimeError(f"expected one COM17 block, found {count}")
    result = normalized.replace(OLD, NEW, 1)
    TARGET.write_bytes(result.replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
