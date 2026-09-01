from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_27_夏野ゆり_COM.ERB"
START_MARKER = ";=== NATSUNO YURI TSUYURI TRAINER SPECIAL START ==="
END_MARKER = ";=== NATSUNO YURI TSUYURI TRAINER SPECIAL END ==="

BLOCK = r''';=== NATSUNO YURI TSUYURI TRAINER SPECIAL START ===
; つゆりが現在の調教者（PLAYER）の時だけ使う、ゆり専用の口上
; 原作準拠：つゆりへの献身・独占欲・神格化が一気に暴走し、直後に慌てて取り繕う
IF NO:PLAYER == 25
    IF SELECTCOM == 60
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃんマジ天使☆　いま、わたしにキスした？　直接？　ひゃああああっ、もう死んでもいい♪」
        ELSEIF A == 1
            PRINTFORMW 「……つゆりちゃん、もう一回。今度はわたしからする。え、嫌？　違う、今のは忘れて。忘れないで」
        ELSE
            PRINTFORMW 「……つゆりちゃんと結婚する。今日から一緒に住もう。お風呂もごはんも寝るのも全部わたしがする」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 62
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃんと動きが重なってる！　これが愛のシンフォニー！　もっと、もっと合わせて！」
        ELSEIF A == 1
            PRINTFORMW 「……つゆりちゃん、他の人なんか見なくていい。わたしだけ見て。わたしが一番近くにいるから」
        ELSE
            PRINTFORMW 「……ひっ、つゆりちゃんが近い。近いのに離れられない。いや、離れないで！　わたし、もう駄目！」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 76
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……うわあああっ、つゆりちゃんも感じてる！　わたしのせい？　わたしがつゆりちゃんを気持ちよくしてる!?」
        ELSEIF A == 1
            PRINTFORMW 「……つゆりちゃん、息を合わせて。わたしと一緒に、同じところで声を出して。愛の共同作業だから！」
        ELSE
            PRINTFORMW 「……だめ、つゆりちゃんの声が近すぎる。頭が真っ白になる。誰か来ても、もう知らない」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 78
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……急がなくていいよ、つゆりちゃん。あ、でも全部飲んで。わたしの中身を全部あげるから！」
        ELSEIF A == 1
            PRINTFORMW 「……つゆりちゃんが飲んでる。かわいい、天使。もっと甘えて。わたし、つゆりちゃんのためなら空っぽでも幸せ」
        ELSE
            PRINTFORMW 「……つゆりちゃんの口が離れた。まだ足りない？　すぐあげる。病気でも怪我でも、わたしが全部治すから」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 79
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃんがわたしのために絞ってる。手、あったかい。これ、もう家族だよね？」
        ELSEIF A == 1
            PRINTFORMW 「……出た。つゆりちゃんが見てる。そんな目で見られたら、もっと出る。止めないで」
        ELSE
            PRINTFORMW 「……全部あげる。足りないなら、内臓を売り払ってでも用意する。つゆりちゃんを満たすから」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 84
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃん、そこ！　そこそこ！　ひゃああああっ、上手すぎる！　好き、つゆりちゃん好きぃ！」
        ELSEIF A == 1
            PRINTFORMW 「……止めないで！　つゆりちゃんが手を止めたら、わたし死ぬ！　もう一度、今のをお願い！」
        ELSE
            PRINTFORMW 「……今の声は忘れて。嘘、忘れないで。つゆりちゃんにだけは、わたしが好きだって覚えていてほしい」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 86
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……ひっ、ひいいっ、つゆりちゃんの前でこんな。見ないで！　いや、逃げないで！　そばにいて！」
        ELSEIF A == 1
            PRINTFORMW 「……笑わないで。笑われたら死ぬ。でも、つゆりちゃんがそばにいるなら平気。たぶん」
        ELSE
            PRINTFORMW 「……つゆりちゃん、何も言わなくていい。手だけ握って。わたし、つゆりちゃんに嫌われるのが一番怖い」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 202
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃんの胸が、わたしに？　ひゃああっ、近い！　これ、結婚式の予行演習だよね♪」
        ELSEIF A == 1
            PRINTFORMW 「……もっと押して。つゆりちゃんの体温を、わたしに分けて。風邪をひかないように、ずっとくっついていて」
        ELSE
            PRINTFORMW 「……見ないで、つゆりちゃん。いや、見てて。わたしだけを見て。ほかの人には、この顔を見せないから」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 258 && ASSIPLAY == 0
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃんがわたしの上にいる。夫婦の共同作業だね♪　もっと動いて、わたしを置いていかないで！」
        ELSEIF A == 1
            PRINTFORMW 「……つゆりちゃん、足に力を入れて。わたしが支えるから。地球が滅んでも、つゆりちゃんだけは落とさない」
        ELSE
            PRINTFORMW 「……ひっ、つゆりちゃんが揺れるたび、わたしまで壊れる。待って、待ってじゃない、もっと！」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 318
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃん、よく頑張ったね。もう誰にも無理をさせない。わたしが一生、面倒を見るから」
        ELSEIF A == 1
            PRINTFORMW 「……いい子。そうして甘えて。つゆりちゃんがわたしを頼るの、好き。もっと頼って」
        ELSE
            PRINTFORMW 「……つゆりちゃんと結婚する。わたしが看護師の資格を取って、朝も夜もそばにいる。気持ち悪い？　ごめん、今のは忘れて」
        ENDIF
        RETURN 0
    ENDIF
ENDIF
;=== NATSUNO YURI TSUYURI TRAINER SPECIAL END ===

'''


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    start = text.find(START_MARKER)
    end = text.find(END_MARKER)
    if start < 0 or end < start:
        raise SystemExit("existing special block markers not found")
    end += len(END_MARKER)
    replacement = BLOCK.replace("\n", "\r\n").rstrip("\r\n")
    TARGET.write_bytes((text[:start] + replacement + text[end:]).encode("cp932"))


if __name__ == "__main__":
    main()
