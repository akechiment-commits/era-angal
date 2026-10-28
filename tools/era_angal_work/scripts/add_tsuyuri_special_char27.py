from pathlib import Path

from revise_tsuyuri_special_char27 import BLOCK as CURRENT_BLOCK


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_27_夏野ゆり_COM.ERB"
START_MARKER = ";=== NATSUNO YURI TSUYURI TRAINER SPECIAL START ==="

BLOCK = r''';=== NATSUNO YURI TSUYURI TRAINER SPECIAL START ===
; つゆりが現在の調教者（PLAYER）の時だけ使う、ゆり専用の助手口上
; 原作準拠：保護欲・世話焼き・独占欲を前面に出しすぎず、つゆりの前だけ崩れる
IF NO:PLAYER == 25
    IF SELECTCOM == 60
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃん、顔を上げて。……キスくらいなら、わたしからする」
        ELSEIF A == 1
            PRINTFORMW 「……ん。……今の、忘れなくていい。わたしも、忘れないから」
        ELSE
            PRINTFORMW 「……そんなに見ないで。つゆりちゃんに触れたくなったのは、わたしのほうだから」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 62
        CALL AITE_YOBI, 27, PLAYER
        LOCALS '= @"%RESULTS%"
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……%LOCALS%、急がないで。……うん、そのまま。呼吸を合わせよう」
        ELSEIF A == 1
            PRINTFORMW 「……つゆりちゃんが近いと、隠せない。……こっちまで熱くなる」
        ELSE
            PRINTFORMW 「……あまり動かないで。……離れるほうが、嫌だから」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 76
        CALL AITE_YOBI, 27, PLAYER
        LOCALS '= @"%RESULTS%"
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……%LOCALS%、痛くない？　わたしに合わせて。……大丈夫、ここにいる」
        ELSEIF A == 1
            PRINTFORMW 「……声、聞こえる。つゆりちゃんが感じてるの、わかる……ふ、変じゃない」
        ELSE
            PRINTFORMW 「……もっと近くにいて。……離れると、わたしまで落ちつかない」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 78
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……急がなくていいよ、つゆりちゃん。むせたら、すぐ止めるから」
        ELSEIF A == 1
            PRINTFORMW 「……そんな顔して飲むんだ。……かわいい、って言ったら怒る？」
        ELSE
            PRINTFORMW 「……まだ欲しいなら、言って。……わたし、つゆりちゃんになら」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 79
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃんの手、あったかい。……だから、任せてもいい」
        ELSEIF A == 1
            PRINTFORMW 「……そんなに一生懸命にならなくていい。……でも、その顔は好き」
        ELSE
            PRINTFORMW 「……出てるの、見てる？　つゆりちゃんになら……もう少し見られても」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 84
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃん、そこ。……そこは、まだ言ってないのに」
        ELSEIF A == 1
            PRINTFORMW 「……待って、待ってって言ってるのに……つゆりちゃんの手、止めないで」
        ELSE
            PRINTFORMW 「……こんな声、つゆりちゃんに聞かれるなんて……ふ、でも、離れないで」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 86
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃん、見てた？　……忘れて。いや、忘れないで、でも言わないで」
        ELSEIF A == 1
            PRINTFORMW 「……笑わないで。つゆりちゃんにだけは、笑われたくない」
        ELSE
            PRINTFORMW 「……そばにいて。……つゆりちゃんがいるなら、片づけるから」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 202
        CALL AITE_YOBI, 27, PLAYER
        LOCALS '= @"%RESULTS%"
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……%LOCALS%、そんなに寄せないで。……息が合うと、困る」
        ELSEIF A == 1
            PRINTFORMW 「……乳首、当たってる。……つゆりちゃんのほうから来たんだから、責任とって」
        ELSE
            PRINTFORMW 「……胸だけなのに、つゆりちゃんの顔が近い。……もう少し、このまま」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 258
        CALL AITE_YOBI, 27, PLAYER
        LOCALS '= @"%RESULTS%"
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……%LOCALS%が動くたび、こっちまで揺れる。……わたしを置いていかないで」
        ELSEIF A == 1
            PRINTFORMW 「……そんな顔で見ないで、つゆりちゃん。……ちゃんと、わたしのことも見て」
        ELSE
            PRINTFORMW 「……つゆりちゃんとなら、どこまででも……って、今のは忘れて」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 318
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃん、よくがんばったね。……今日はわたしがそばにいる」
        ELSEIF A == 1
            PRINTFORMW 「……言わなくていい。つゆりちゃんが甘えたいなら、黙って撫でる」
        ELSE
            PRINTFORMW 「……手を離すな、とは言わない。……でも、もう少しだけ」
        ENDIF
        RETURN 0
    ENDIF
ENDIF
;=== NATSUNO YURI TSUYURI TRAINER SPECIAL END ===

'''


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    if START_MARKER in text:
        return

    anchor = 'LOCALS \'= @"%RESULTS%"\r\n'
    if anchor not in text:
        raise SystemExit("anchor not found")

    block = CURRENT_BLOCK.replace("\n", "\r\n")
    TARGET.write_bytes(text.replace(anchor, anchor + block, 1).encode("cp932"))


if __name__ == "__main__":
    main()
