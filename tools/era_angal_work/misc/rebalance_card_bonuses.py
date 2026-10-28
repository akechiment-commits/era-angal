from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVENT_BOARD = ROOT / "ERB" / "EVENT_BOARD_イベントボード周回.ERB"
GACHA = ROOT / "ERB" / "GACHA_ガチャシステム.ERB"


def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932").replace("\r\n", "\n").replace("\n", "\r\n")


def write_cp932(path: Path, text: str) -> None:
    path.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


def crlf(text: str) -> str:
    return text.replace("\n", "\r\n")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old in text:
        return text.replace(old, new, 1)
    if new not in text:
        raise SystemExit(f"{label} anchor not found")
    return text


def update_event_board() -> None:
    board = read_cp932(EVENT_BOARD)
    old = crlf(
        """	;カードボーナス（定期戦と同じ、×2）
	LOCAL:1 += CFLAG:Z:303 * 2
	LOCAL:1 += CFLAG:Z:304 * 2
	LOCAL:1 += CFLAG:Z:305 * 2
	LOCAL:1 += CFLAG:Z:306 * 2
"""
    )
    new = crlf(
        """	;カード収集ボーナス。イベント発揮値では所持カードの成長を強く反映する。
	LOCAL:1 += CFLAG:Z:303 * 5
	LOCAL:1 += CFLAG:Z:304 * 5
	LOCAL:1 += CFLAG:Z:305 * 5
	LOCAL:1 += CFLAG:Z:306 * 5
"""
    )
    board = replace_once(board, old, new, "event board card multiplier")
    old_breakdown = (
        "\tLOCAL:3 = CFLAG:Z:303 + CFLAG:Z:304 + CFLAG:Z:305 + CFLAG:Z:306\r\n"
    )
    new_breakdown = (
        "\tLOCAL:3 = (CFLAG:Z:303 + CFLAG:Z:304 + CFLAG:Z:305 + CFLAG:Z:306) * 5\r\n"
    )
    board = replace_once(
        board,
        old_breakdown,
        new_breakdown,
        "event board card contribution display",
    )
    write_cp932(EVENT_BOARD, board)


def update_gacha() -> None:
    gacha = read_cp932(GACHA)
    old_distribution = crlf(
        """		LOCAL:91 = RESULT:2	;レア度
		LOCAL:92 = RESULT:4	;基本ボーナス値
		IF LOCAL:90 > 0 && LOCAL:92 > 0
			LOCAL:89 = GETCHARA(LOCAL:90)
			IF LOCAL:89 >= 0
				;K枚所持時の合計ボーナス = base + (K-1)*base/rate + (K>=12 ? base*3 : 0)
				SELECTCASE LOCAL:91
				CASE 6	;MR rate=2
					LOCAL:93 = LOCAL:92 + (LOCAL:96 - 1) * LOCAL:92 / 2
				CASE 5	;UR rate=4
					LOCAL:93 = LOCAL:92 + (LOCAL:96 - 1) * LOCAL:92 / 4
				CASE 4	;SR rate=5
					LOCAL:93 = LOCAL:92 + (LOCAL:96 - 1) * LOCAL:92 / 5
				CASE 1	;N rate=20
					LOCAL:93 = LOCAL:92 + (LOCAL:96 - 1) * LOCAL:92 / 20
				CASEELSE	;R,HR rate=10
					LOCAL:93 = LOCAL:92 + (LOCAL:96 - 1) * LOCAL:92 / 10
				ENDSELECT
				SIF LOCAL:96 >= 12
					LOCAL:93 += LOCAL:92 * 3
				;レア度別振り分け
				SELECTCASE LOCAL:91
				CASE 1, 2	;N/R → 好感度
					CFLAG:(LOCAL:89):306 += LOCAL:93
				CASEELSE	;HR以上 → 全能力1/4
					CFLAG:(LOCAL:89):303 += LOCAL:93 / 4
					CFLAG:(LOCAL:89):304 += LOCAL:93 / 4
					CFLAG:(LOCAL:89):305 += LOCAL:93 / 4
					CFLAG:(LOCAL:89):306 += LOCAL:93 / 4
				ENDSELECT
			ENDIF
		ENDIF
"""
    )
    new_distribution = crlf(
        """		LOCAL:91 = RESULT:2	;レア度
		LOCAL:92 = RESULT:4	;基本ボーナス値
		LOCAL:94 = RESULT:3	;主補正タイプ（0=表現/1=運動/2=学力/3=デッキ戦力）
		IF LOCAL:90 > 0 && LOCAL:92 > 0
			LOCAL:89 = GETCHARA(LOCAL:90)
			IF LOCAL:89 >= 0
				;K枚所持時の合計ボーナス = base + (K-1)*base/rate + (K>=12 ? base*3 : 0)
				SELECTCASE LOCAL:91
				CASE 6	;MR rate=2
					LOCAL:93 = LOCAL:92 + (LOCAL:96 - 1) * LOCAL:92 / 2
				CASE 5	;UR rate=4
					LOCAL:93 = LOCAL:92 + (LOCAL:96 - 1) * LOCAL:92 / 4
				CASE 4	;SR rate=5
					LOCAL:93 = LOCAL:92 + (LOCAL:96 - 1) * LOCAL:92 / 5
				CASE 1	;N rate=20
					LOCAL:93 = LOCAL:92 + (LOCAL:96 - 1) * LOCAL:92 / 20
				CASEELSE	;R,HR rate=10
					LOCAL:93 = LOCAL:92 + (LOCAL:96 - 1) * LOCAL:92 / 10
				ENDSELECT
				SIF LOCAL:96 >= 12
					LOCAL:93 += LOCAL:92 * 3

				;レア度が上がるほど、主能力特化から複数能力型へ広がる。
				;主/第2/第3/第4: N=100/0/0/0, R=70/10/10/10,
				;HR=60/20/10/10, SR=50/20/20/10, UR=40/25/20/15, MR=35/25/20/20
				SELECTCASE LOCAL:91
				CASE 1
					LOCAL:80 = 0
					LOCAL:81 = 0
					LOCAL:82 = 0
				CASE 2
					LOCAL:80 = 10
					LOCAL:81 = 10
					LOCAL:82 = 10
				CASE 3
					LOCAL:80 = 20
					LOCAL:81 = 10
					LOCAL:82 = 10
				CASE 4
					LOCAL:80 = 20
					LOCAL:81 = 20
					LOCAL:82 = 10
				CASE 5
					LOCAL:80 = 25
					LOCAL:81 = 20
					LOCAL:82 = 15
				CASEELSE
					LOCAL:80 = 25
					LOCAL:81 = 20
					LOCAL:82 = 20
				ENDSELECT
				LOCAL:83 = LOCAL:93 * LOCAL:80 / 100
				LOCAL:84 = LOCAL:93 * LOCAL:81 / 100
				LOCAL:85 = LOCAL:93 * LOCAL:82 / 100
				LOCAL:86 = LOCAL:93 - LOCAL:83 - LOCAL:84 - LOCAL:85
				CFLAG:(LOCAL:89):(303 + LOCAL:94) += LOCAL:86
				CFLAG:(LOCAL:89):(303 + (LOCAL:94 + 1) % 4) += LOCAL:83
				CFLAG:(LOCAL:89):(303 + (LOCAL:94 + 2) % 4) += LOCAL:84
				CFLAG:(LOCAL:89):(303 + (LOCAL:94 + 3) % 4) += LOCAL:85
			ENDIF
		ENDIF
"""
    )
    gacha = replace_once(
        gacha,
        old_distribution,
        new_distribution,
        "rarity-specific card distribution",
    )
    old_deck_scale = crlf(
        """				CFLAG:(LOCAL:89):(303 + LOCAL:94) += LOCAL:86
				CFLAG:(LOCAL:89):(303 + (LOCAL:94 + 1) % 4) += LOCAL:83
				CFLAG:(LOCAL:89):(303 + (LOCAL:94 + 2) % 4) += LOCAL:84
				CFLAG:(LOCAL:89):(303 + (LOCAL:94 + 3) % 4) += LOCAL:85
			ENDIF
		ENDIF
	ENDIF
NEXT
RETURN
"""
    )
    new_deck_scale = crlf(
        """				CFLAG:(LOCAL:89):(303 + LOCAL:94) += LOCAL:86
				CFLAG:(LOCAL:89):(303 + (LOCAL:94 + 1) % 4) += LOCAL:83
				CFLAG:(LOCAL:89):(303 + (LOCAL:94 + 2) % 4) += LOCAL:84
				CFLAG:(LOCAL:89):(303 + (LOCAL:94 + 3) % 4) += LOCAL:85
			ENDIF
		ENDIF
	ENDIF
NEXT
;デッキ戦力はカード収集の効果を実感しやすくするため、最終値を2倍にする。
REPEAT CHARANUM
	CFLAG:COUNT:306 *= 2
REND
RETURN
"""
    )
    gacha = replace_once(
        gacha,
        old_deck_scale,
        new_deck_scale,
        "card deck-strength multiplier",
    )

    old_acquire_message = crlf(
        """IF LOCAL:0 > 0
	SELECTCASE LOCAL:1
	CASE 1, 2
		;N/R → 好感度
		PRINTFORML %CALLNAME:TARGET%のデッキ戦力ボーナス +{LOCAL:4}！
	CASEELSE
		;HR以上 → 全能力1/4ずつ
		PRINTFORML %CALLNAME:TARGET%の全能力ボーナス +{LOCAL:4/4}ずつ！
	ENDSELECT
	CFLAG:TARGET:307 += 1
ENDIF
"""
    )
    new_acquire_message = crlf(
        """IF LOCAL:0 > 0
	;今回増えた総ボーナスを、再計算処理と同じレア度別割合で表示する。
	SELECTCASE LOCAL:1
	CASE 1
		LOCAL:14 = 0
		LOCAL:15 = 0
		LOCAL:16 = 0
	CASE 2
		LOCAL:14 = 10
		LOCAL:15 = 10
		LOCAL:16 = 10
	CASE 3
		LOCAL:14 = 20
		LOCAL:15 = 10
		LOCAL:16 = 10
	CASE 4
		LOCAL:14 = 20
		LOCAL:15 = 20
		LOCAL:16 = 10
	CASE 5
		LOCAL:14 = 25
		LOCAL:15 = 20
		LOCAL:16 = 15
	CASEELSE
		LOCAL:14 = 25
		LOCAL:15 = 20
		LOCAL:16 = 20
	ENDSELECT
	LOCAL:17 = LOCAL:4 * LOCAL:14 / 100
	LOCAL:18 = LOCAL:4 * LOCAL:15 / 100
	LOCAL:19 = LOCAL:4 * LOCAL:16 / 100
	LOCAL:20 = LOCAL:4 - LOCAL:17 - LOCAL:18 - LOCAL:19
	LOCAL:21 = 0
	LOCAL:22 = 0
	LOCAL:23 = 0
	LOCAL:24 = 0
	LOCAL:(21 + LOCAL:2) = LOCAL:20
	LOCAL:(21 + (LOCAL:2 + 1) % 4) = LOCAL:17
	LOCAL:(21 + (LOCAL:2 + 2) % 4) = LOCAL:18
	LOCAL:(21 + (LOCAL:2 + 3) % 4) = LOCAL:19
	;再計算処理ではデッキ戦力だけ最終2倍になる。
	LOCAL:24 *= 2
	PRINTFORML %CALLNAME:TARGET%のカード補正　表現力+{LOCAL:21}　運動力+{LOCAL:22}　学力+{LOCAL:23}　デッキ戦力+{LOCAL:24}！
	CFLAG:TARGET:307 += 1
ENDIF
"""
    )
    legacy_acquire_message = new_acquire_message.replace(
        "\t;再計算処理ではデッキ戦力だけ最終2倍になる。\r\n\tLOCAL:24 *= 2\r\n",
        "",
    )
    if legacy_acquire_message in gacha:
        gacha = gacha.replace(legacy_acquire_message, new_acquire_message, 1)
    else:
        gacha = replace_once(
            gacha,
            old_acquire_message,
            new_acquire_message,
            "card acquisition bonus display",
        )

    # FLAG:120 is the monthly reward-claim slot for event 0. Passing the
    # ten-pull state as an argument prevents gacha from destroying that slot.
    gacha = replace_once(
        gacha,
        "@GACHA_PULL(ARG)\r\n",
        "@GACHA_PULL(ARG, ARG:1)\r\n",
        "gacha pull optional skip argument",
    )
    gacha = replace_once(
        gacha,
        "ELSEIF FLAG:120 == 0\r\n",
        "ELSEIF ARG:1 == 0\r\n",
        "gacha result wait argument",
    )
    old_ten_pull = crlf(
        """; 10連ガチャ ARG:0=ガチャ種別(1-5)
; FLAG:120=1 で各結果のWAITを省略
;--------------------------------------------------
@GACHA_PULL_10(ARG)
FLAG:120 = 1
DRAWLINE
PRINTL 【10連ガチャ 開始！】
REPEAT 10
	CALL GACHA_PULL, ARG:0
REND
FLAG:120 = 0
"""
    )
    new_ten_pull = crlf(
        """; 10連ガチャ ARG:0=ガチャ種別(1-5)
; GACHA_PULL の第2引数=1で各結果のWAITを省略
;--------------------------------------------------
@GACHA_PULL_10(ARG)
DRAWLINE
PRINTL 【10連ガチャ 開始！】
REPEAT 10
	CALL GACHA_PULL, ARG:0, 1
REND
"""
    )
    gacha = replace_once(gacha, old_ten_pull, new_ten_pull, "ten-pull state")

    # MR枠は英字のMIRACLE演出がすでにあるため、重複するカタカナ行を出さない。
    miracle_katakana = "\tPRINTL 　　　　　ミラクルレア！\r\n"
    if gacha.count(miracle_katakana) > 1:
        raise SystemExit("duplicate miracle katakana lines found")
    gacha = gacha.replace(miracle_katakana, "", 1)
    write_cp932(GACHA, gacha)


def main() -> None:
    update_event_board()
    update_gacha()
    print(f"updated {EVENT_BOARD}")
    print(f"updated {GACHA}")


if __name__ == "__main__":
    main()
