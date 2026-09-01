from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_27_夏野ゆり_COM.ERB"
START = ";=== NATSUNO YURI TSUYURI ASSISTANT NON-EROTIC START ==="
END = ";=== NATSUNO YURI TSUYURI ASSISTANT NON-EROTIC END ==="
TRAINER_START = ";=== NATSUNO YURI TSUYURI TRAINER SPECIAL START ==="

BLOCK = r''';=== NATSUNO YURI TSUYURI ASSISTANT NON-EROTIC START ===
; 助手調教で、つゆりがPLAYERの時だけ使う非性愛コマンド口上
IF ASSIPLAY && NO:PLAYER == 25
    IF SELECTCOM == 300
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃんと勉強できるの、ずっと待ってた。教科書より、隣のつゆりちゃんのほうが気になって、ページが進まない」
        ELSEIF A == 1
            PRINTFORMW 「ここ、わからない？　じゃあわたしが教える。つゆりちゃんに頼られるの、好き。もっとこっちに寄って」
        ELSE
            PRINTFORMW 「朝まで勉強する。つゆりちゃんが眠るまで見てるし、眠ったら寝顔を見てる。……だめ？」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 301
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃんの話、全部聞く。誰にも言わない。わたしだけにして」
        ELSEIF A == 1
            PRINTFORMW 「今の顔、もう一度して。笑ったつゆりちゃん、わたしの記憶にずっと残したい」
        ELSE
            PRINTFORMW 「話が終わっても帰らないで。つゆりちゃんが黙ってる時間も、わたしには必要だから」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 302
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃんが選んでくれた？　これ、もう一生捨てられない。ずっと肌身離さないから」
        ELSEIF A == 1
            PRINTFORMW 「ありがとう。つゆりちゃんからもらったものなら、何でも宝物。つゆりちゃんごと、大事にする」
        ELSE
            PRINTFORMW 「つゆりちゃんが欲しいもの、今度はわたしが探す。足りなければ、わたしの全部で払う」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 303
        A = RAND:3
        IF A == 0
            PRINTFORMW 「……つゆりちゃん、手、出して。触れたい。触っていい理由なんて、もういらないよね？」
        ELSEIF A == 1
            PRINTFORMW 「肩が触れてる……近い。嬉しい。誰か来ても、この手だけは離さない」
        ELSE
            PRINTFORMW 「つゆりちゃんの手、あったかい。もう少しだけ。……もう少しが終わらなくてもいい？」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 304
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃんと何もしないでいられるのが、一番好き。動かなくていい、ここにいて」
        ELSEIF A == 1
            PRINTFORMW 「眠いなら寝て。わたしが見張ってる。つゆりちゃんが目を開けるまで、誰も近づけない」
        ELSE
            PRINTFORMW 「この隣、わたしの場所にして。今日だけじゃなくて、ずっと」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 305
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃんは座ってて。ここは全部わたしがやる。つゆりちゃんの手を汚すくらいなら、わたしが壊れる」
        ELSEIF A == 1
            PRINTFORMW 「つゆりちゃんの部屋、わたしがきれいにする。匂いも、触ったものも、全部覚えておきたい」
        ELSE
            PRINTFORMW 「終わったら褒めて。つゆりちゃんの役に立てたって、ちゃんと聞かせて」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 306
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃんの髪、触らせて。一本も痛くしない。わたし、つゆりちゃんを傷つけるものが嫌い」
        ELSEIF A == 1
            PRINTFORMW 「きれい……ずっと梳かしていたい。つゆりちゃんが眠るまで、わたしの手を置いてて」
        ELSE
            PRINTFORMW 「髪に触れていいなら、もっと近くにいてもいい？　結婚の許可まで、もらった気がする」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 307
        A = RAND:3
        IF A == 0
            PRINTFORMW 「櫛が通るたび、つゆりちゃんがわたしに預けてくれてるみたい。動かないで、全部大事にする」
        ELSEIF A == 1
            PRINTFORMW 「絡まってる。わたしがほどく。つゆりちゃんを困らせるものは、ひとつずつ消すから」
        ELSE
            PRINTFORMW 「終わっても手を離したくない。髪じゃなくて、つゆりちゃんごと抱いててもいい？」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 309
        A = RAND:3
        IF A == 0
            PRINTFORMW 「危ないものはわたしが持つ。つゆりちゃんは後ろ。絶対にわたしから離れないで」
        ELSEIF A == 1
            PRINTFORMW 「つゆりちゃんが欲しいものなら、どこまでも探す。見つかるまで帰らない」
        ELSE
            PRINTFORMW 「見つけた……つゆりちゃんの役に立てた。これだけで、今日来た意味がある」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 310
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃんのために作る。失敗したらわたしが飲む。だから、怖がらなくていい」
        ELSEIF A == 1
            PRINTFORMW 「できた。体調は？　痛いところは？　すぐ治すから、全部言って」
        ELSE
            PRINTFORMW 「つゆりちゃんを助けるためなら、時間も体も好きに使って。わたし、これしかできないから」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 312
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃん、こっち。今日はわたしが撫でる。頑張ったぶん、全部甘えて」
        ELSEIF A == 1
            PRINTFORMW 「いい子。つゆりちゃんがわたしを頼ってくれるの、好き。もっと困らせて」
        ELSE
            PRINTFORMW 「手を止めたら、また無理するでしょ。眠るまで、わたしが離さない」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 313
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃんの願いなら、何度でも祈る。神様に断られても、わたしが叶える」
        ELSEIF A == 1
            PRINTFORMW 「つゆりちゃんが幸せになりますように。わたしの幸せは、その隣でいい」
        ELSE
            PRINTFORMW 「お願いごとなんていらない。わたしがずっと守るから、つゆりちゃんは笑って」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 314
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃんと炬燵。足が触れた……もう出られないね、ずっとここにいよう」
        ELSEIF A == 1
            PRINTFORMW 「眠そう。わたしの肩を使って。朝まで動かないし、誰にも起こさせない」
        ELSE
            PRINTFORMW 「見えないところで手をつなぐの、好き。つゆりちゃんを独り占めしてるみたい」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 315
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃんと歩く。歩幅も、帰る場所も、これから全部合わせたい」
        ELSEIF A == 1
            PRINTFORMW 「急がなくていいよ。今日が終わるのが惜しいから、もっと遠回りしよう」
        ELSE
            PRINTFORMW 「どこまででも行く。つゆりちゃんが手を離さないなら、世界の外まで」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 316
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃんに梳かしてもらうの、好き。手が触れるたび、頭の中がつゆりちゃんだけになる」
        ELSEIF A == 1
            PRINTFORMW 「そこ、もう少し。……気持ちいいって言うの、つゆりちゃん相手なら恥ずかしくない」
        ELSE
            PRINTFORMW 「終わっても手を置いてて。つゆりちゃんの手が離れると、急に寒くなる」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 318
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃん、今度はわたしが撫でる。頑張ったねって、何度でも言うから」
        ELSEIF A == 1
            PRINTFORMW 「眠るまでここにいて。つゆりちゃんが安心できるなら、わたしは朝まで動かない」
        ELSE
            PRINTFORMW 「つゆりちゃんが甘えてくれるの、嬉しい。もっとわたしだけを頼って」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 320
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃんと食べると、何でも特別。熱いなら冷ますから、わたしに任せて」
        ELSEIF A == 1
            PRINTFORMW 「半分こ？　つゆりちゃんとなら平気。つゆりちゃんが口をつけたところも、わたしがもらう」
        ELSE
            PRINTFORMW 「何食べたい？　今日はつゆりちゃんの好きなものだけにする。わたしは見てるから」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 321
        A = RAND:3
        IF A == 0
            PRINTFORMW 「今日はつゆりちゃんだけ見てる。他のものは後でいい」
        ELSEIF A == 1
            PRINTFORMW 「楽しい？　じゃあまた来る。つゆりちゃんが飽きるまで、わたしが全部付き合う」
        ELSE
            PRINTFORMW 「笑ってる……もっと笑わせる。わたしの命、使えるものは全部使う」
        ENDIF
        RETURN 0
    ELSEIF SELECTCOM == 323
        A = RAND:3
        IF A == 0
            PRINTFORMW 「つゆりちゃんと出かける日、ずっと待ってた。手、つないで。迷子になりたい」
        ELSEIF A == 1
            PRINTFORMW 「どこへ行く？　つゆりちゃんが望む場所なら、帰り道をなくしてもいい」
        ELSE
            PRINTFORMW 「並んで歩いてるだけなのに、もう家族みたい。……今日だけじゃ足りない」
        ENDIF
        RETURN 0
    ENDIF
ENDIF
;=== NATSUNO YURI TSUYURI ASSISTANT NON-EROTIC END ===

'''


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    if START in text:
        begin = text.index(START)
        finish = text.index(END, begin) + len(END)
        while text[finish : finish + 2] == "\r\n":
            finish += 2
        text = text[:begin] + text[finish:]
    anchor = text.index(TRAINER_START)
    rendered = BLOCK.replace("\n", "\r\n")
    text = text[:anchor] + rendered + text[anchor:]
    TARGET.write_bytes(text.encode("cp932"))


if __name__ == "__main__":
    main()
