from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COM = ROOT / "ERB" / "CHAR" / "CHAR_27_夏野ゆり_COM.ERB"
YURI = ROOT / "ERB" / "CHAR" / "CHAR_27_夏野ゆり.ERB"
TSUYURI = ROOT / "ERB" / "CHAR" / "CHAR_25_八朔つゆり.ERB"
PREGNANCY = ROOT / "ERB" / "EVENT_N_妊娠イベント.ERB"

ORGASM_START = ";=== NATSUNO YURI TSUYURI ORGASM START ==="
ORGASM_END = ";=== NATSUNO YURI TSUYURI ORGASM END ==="
OLD_EJAC_START = ";=== NATSUNO YURI TSUYURI EJACULATION START ==="
OLD_EJAC_END = ";=== NATSUNO YURI TSUYURI EJACULATION END ==="

PLAYER_EJAC_MARKERS = [
    (
        ";=== NATSUNO YURI TSUYURI PLAYER EJAC GENERAL START ===",
        ";=== NATSUNO YURI TSUYURI PLAYER EJAC GENERAL END ===",
    ),
    (
        ";=== NATSUNO YURI TSUYURI PLAYER EJAC MOUTH START ===",
        ";=== NATSUNO YURI TSUYURI PLAYER EJAC MOUTH END ===",
    ),
    (
        ";=== NATSUNO YURI TSUYURI PLAYER EJAC IN START ===",
        ";=== NATSUNO YURI TSUYURI PLAYER EJAC IN END ===",
    ),
]
YURI_EJAC_MARKERS = (
    ";=== NATSUNO YURI TSUYURI YURI EJACULATION START ===",
    ";=== NATSUNO YURI TSUYURI YURI EJACULATION END ===",
)
YURI_MILK_MARKERS = (
    ";=== NATSUNO YURI TSUYURI MILK START ===",
    ";=== NATSUNO YURI TSUYURI MILK END ===",
)
YURI_PREG_MARKERS = (
    ";=== NATSUNO YURI TSUYURI PREGNANCY START ===",
    ";=== NATSUNO YURI TSUYURI PREGNANCY END ===",
)
TSUYURI_PREG_MARKERS = (
    ";=== NATSUNO YURI TSUYURI TSUYURI PREGNANCY START ===",
    ";=== NATSUNO YURI TSUYURI TSUYURI PREGNANCY END ===",
)


def crlf(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\r\n").rstrip("\r\n")


def remove_block(text: str, start: str, end: str) -> str:
    begin = text.find(start)
    if begin < 0:
        return text
    finish = text.find(end, begin)
    if finish < 0:
        raise SystemExit(f"end marker not found for {start}")
    finish += len(end)
    while text[finish : finish + 2] == "\r\n":
        finish += 2
    return text[:begin] + text[finish:]


def extract_block(text: str, start: str, end: str) -> str:
    begin = text.find(start)
    if begin < 0:
        raise SystemExit(f"start marker not found: {start}")
    finish = text.find(end, begin)
    if finish < 0:
        raise SystemExit(f"end marker not found for {start}")
    return text[begin : finish + len(end)]


def reset_after_label(text: str, label: str, block: str, start: str, end: str) -> str:
    text = remove_block(text, start, end)
    needle = "\r\n" + label + "\r\n"
    if needle not in text:
        raise SystemExit(f"label not found: {label}")
    rendered = crlf(block) + "\r\n"
    return text.replace(needle, needle + rendered, 1)


def render_four_stage(start: str, end: str, groups: tuple[tuple[str, str, str], ...]) -> str:
    lines = [start, "IF NO:PLAYER == 25", "    IF TFLAG:302 >= 2"]
    conditions = ["TFLAG:711 == 1", "", "TFLAG:711 == 1", ""]
    for index, group in enumerate(groups):
        if index == 0:
            lines.append("        IF TFLAG:711 == 1")
        elif index == 1:
            lines.append("        ELSE")
        elif index == 2:
            lines.extend(["    ELSE", "        IF TFLAG:711 == 1"])
        else:
            lines.append("        ELSE")
        lines.extend(
            [
                "            A = RAND:3",
                "            IF A == 0",
                f"                PRINTFORMW {group[0]}",
                "            ELSEIF A == 1",
                f"                PRINTFORMW {group[1]}",
                "            ELSE",
                f"                PRINTFORMW {group[2]}",
                "            ENDIF",
            ]
        )
        if index == 0:
            pass
        elif index == 1:
            lines.append("        ENDIF")
        elif index == 2:
            pass
        else:
            lines.append("        ENDIF")
    lines.extend(["    ENDIF", "    RETURN 0", "ENDIF", end])
    return "\n".join(lines)


def render_yuri_ejaculation() -> str:
    start, end = YURI_EJAC_MARKERS
    return "\n".join(
        [
            start,
            "IF NO:PLAYER == 25",
            "    IF TFLAG:715 >= 10",
            "        A = RAND:3",
            "        IF A == 0",
            "            PRINTFORMW 「……っ、出る……！　つゆりちゃん、見ないで、でも目を逸らさないで。わたしが、つゆりちゃんの前で……っ」",
            "        ELSEIF A == 1",
            "            PRINTFORMW 「……止まらない。つゆりちゃんに触られて、わたしの体が勝手に……っ。もっと、見て」",
            "        ELSE",
            "            PRINTFORMW 「……こんなに出た……。つゆりちゃんが受け止めてくれるなら、恥ずかしくない。たぶん」",
            "        ENDIF",
            "    ELSE",
            "        A = RAND:3",
            "        IF A == 0",
            "            PRINTFORMW 「……出た。つゆりちゃんの手で、わたしが……。ねえ、ちゃんと気持ちよさそうだった？」",
            "        ELSEIF A == 1",
            "            PRINTFORMW 「……っ、また震えた。つゆりちゃん、わたし、まだ止められない……もう少しだけ、触って」",
            "        ELSE",
            "            PRINTFORMW 「……つゆりちゃんに見られながら出すの、嫌じゃない。嫌じゃないから、そんな顔しないで」",
            "        ENDIF",
            "    ENDIF",
            "    RETURN 0",
            "ENDIF",
            end,
        ]
    )


def render_yuri_milk() -> str:
    start, end = YURI_MILK_MARKERS
    return "\n".join(
        [
            start,
            "IF NO:PLAYER == 25",
            "    IF TFLAG:716 >= 10",
            "        A = RAND:3",
            "        IF A == 0",
            "            PRINTFORMW 「……ひゃあっ、止まらない……！　つゆりちゃん、離れないで。わたしの全部が出てるの、ちゃんと見て、ぜんぶ受け取って……！」",
            "        ELSEIF A == 1",
            "            PRINTFORMW 「そんなに飲んでくれるの……？　ふふ、かわいい。まだ出るよ。つゆりちゃんが欲しがるなら、わたし、空っぽになるまであげる」",
            "        ELSE",
            "            PRINTFORMW 「……つゆりちゃんの口で、わたしがなくなっていく。もっと。もっと飲んで。わたしをつゆりちゃんだけのものにして」",
            "        ENDIF",
            "    ELSE",
            "        A = RAND:3",
            "        IF A == 0",
            "            PRINTFORMW 「……つゆりちゃん、飲んでる。わたしのものを、つゆりちゃんが。……ひゃあ、かわいい。もう少し、離れないで」",
            "        ELSEIF A == 1",
            "            PRINTFORMW 「出るたびに、つゆりちゃんの中に届いてるんだね。ねえ、ちゃんとわたしを味わって。わたし、つゆりちゃん専用だから」",
            "        ELSE",
            "            PRINTFORMW 「そんな顔で欲しがられたら、断れないよ。……もうちょっとだけ。つゆりちゃんが満足するまで、わたしがあげる」",
            "        ENDIF",
            "    ENDIF",
            "    RETURN 0",
            "ENDIF",
            end,
        ]
    )


def render_yuri_pregnancy() -> str:
    start, end = YURI_PREG_MARKERS
    return "\n".join(
        [
            start,
            "IF TFLAG:13 == 20 && CFLAG:TARGET:111 == 25",
            "    A = RAND:3",
            "    IF A == 0",
            "        PRINTFORMW 「……つゆりちゃんの子が、わたしの中にいる。……ひゃあ、まだ熱い。ねえ、もっと触って。つゆりちゃんがここに残したもの、わたしに分からせて」",
            "    ELSEIF A == 1",
            "        PRINTFORMW 「わたし、つゆりちゃんのものになったんだ。中までつゆりちゃんでいっぱいにされて、子どもまでくれて……ふふ、もうだめ。嬉しくて、顔が戻らない」",
            "    ELSE",
            "        PRINTFORMW 「できたよ、つゆりちゃん。わたしの中に、つゆりちゃんが残った。証拠だよ。今日、結婚しよう。だめって言われても、もう逃がさないから」",
            "    ENDIF",
            "    RETURN 0",
            "ELSEIF TFLAG:13 == 98 && ((CFLAG:MASTER:104 == 3 && CFLAG:MASTER:111 == 27) || (CFLAG:ASSI:104 == 3 && CFLAG:ASSI:111 == 27))",
            "    A = RAND:3",
            "    IF A == 0",
            "        PRINTFORMW 「……つゆりちゃんのお腹に、わたしの子？　ひゃああっ、やった……！　わたしがつゆりちゃんを孕ませたんだ。ねえ、もう一回言わせて。わたしが、つゆりちゃんを……！」",
            "    ELSEIF A == 1",
            "        PRINTFORMW 「ここ、触っていい？　……だめ、聞かなくていいよね。つゆりちゃんの中で、わたしの子が育つんだ。ひゃあ、わたし、もう離れられない」",
            "    ELSE",
            "        PRINTFORMW 「つゆりちゃんがわたしの子を産む。わたしが入れたものを、つゆりちゃんが育ててくれる。ねえ、これって結婚よりすごいよね？　もう誰にも返さないから」",
            "    ENDIF",
            "    RETURN 0",
            "ELSEIF TFLAG:13 == 25 && CFLAG:TARGET:111 == 25",
            "    A = RAND:3",
            "    IF A == 0",
            "        PRINTFORMW 「もうすぐ出てくるんだって。つゆりちゃん、ここ、触って。動いてるでしょ？　わたしの中で、つゆりちゃんの子がわたしを押してる……かわいい」",
            "    ELSEIF A == 1",
            "        PRINTFORMW 「痛い、痛いけど、つゆりちゃんが見てる。もっと見て、目をそらさないで。わたしがつゆりちゃんの子を産むところ、全部覚えて」",
            "    ELSE",
            "        PRINTFORMW 「手、もっと強く。わたしだけが痛いなんてずるい。つゆりちゃんも一緒に壊れてよ。……ねえ、離さないで」",
            "    ENDIF",
            "    RETURN 0",
            "ELSEIF TFLAG:13 == 21 && CFLAG:TARGET:111 == 25",
            "    A = RAND:3",
            "    IF A == 0",
            "        PRINTFORMW 「産まれた……！　つゆりちゃん、見て、わたしの中から出てきたよ。つゆりちゃんの子。ねえ、笑って、もっと近くに来て！」",
            "    ELSEIF A == 1",
            "        PRINTFORMW 「褒めて、褒めてよ。わたし、つゆりちゃんの子を産んだ。つゆりちゃんのために、ちゃんと壊れずに産んだんだから！」",
            "    ELSE",
            "        PRINTFORMW 「泣いてる、かわいい。つゆりちゃんの声を聞かせて。わたしだけの子じゃないって、ちゃんと分からせたい。つゆりちゃんも、わたしの家族だって！」",
            "    ENDIF",
            "    RETURN 0",
            "ELSEIF TFLAG:13 == 23 && CFLAG:TARGET:111 == 25",
            "    A = RAND:3",
            "    IF A == 0",
            "        PRINTFORMW 「つゆりちゃん、抱いて。わたしが産んだ子を、つゆりちゃんの腕で抱いて。……あ、だめ、嬉しくてまた泣く」",
            "    ELSEIF A == 1",
            "        PRINTFORMW 「眠れない。子どもがじゃなくて、わたしが。つゆりちゃんが来ないと息ができない。ねえ、ここにいて」",
            "    ELSE",
            "        PRINTFORMW 「ちゃんと食べて。つゆりちゃんが倒れたら、わたし、子どもを抱いたまま追いかけるから。……わたしの全部を残してくれた人なんだから」",
            "    ENDIF",
            "    RETURN 0",
            "ELSEIF TFLAG:13 == 22 && CFLAG:TARGET:111 == 25",
            "    A = RAND:3",
            "    IF A == 0",
            "        PRINTFORMW 「もう一人で歩くんだって。……じゃあ、つゆりちゃん、今度はわたしだけ見て。子どもに取られてた分、全部返して」",
            "    ELSEIF A == 1",
            "        PRINTFORMW 「寂しいのは、この子じゃなくてわたし。つゆりちゃんがまた隣に戻ってくれるなら、ちゃんと笑える。……絶対、戻ってきて」",
            "    ELSE",
            "        PRINTFORMW 「この子が離れても、わたしは離さない。つゆりちゃん、逃げないで。もう一度、つゆりちゃんをわたしの子でいっぱいにしたいくらい、好き」",
            "    ENDIF",
            "    RETURN 0",
            "ENDIF",
            end,
        ]
    )


def render_tsuyuri_pregnancy() -> str:
    start, end = TSUYURI_PREG_MARKERS
    return "\n".join(
        [
            start,
            "IF TFLAG:13 == 20 && CFLAG:TARGET:111 == 27 && NO:TARGET == 25",
            "    A = RAND:3",
            "    IF A == 0",
            "        PRINTFORMW 「コホ、コホ……ゆりちゃんの子が、わたしのお腹に……？　えへへ、ゆりちゃんがわたしをお母さんにしてくれるんだね」",
            "    ELSEIF A == 1",
            "        PRINTFORMW 「……びっくりした。ゆりちゃんの子、ちゃんとここにいる。怖いけど、嬉しいよ。わたし、最後まで大事にするから」",
            "    ELSE",
            "        PRINTFORMW 「コホ……ゆりちゃんが、わたしを孕ませたんだね。ふふ、今度はわたしがゆりちゃんを頼っても、いいのかな……？」",
            "    ENDIF",
            "    RETURN 0",
            "ELSEIF TFLAG:13 == 25 && CFLAG:TARGET:111 == 27 && NO:TARGET == 25",
            "    A = RAND:3",
            "    IF A == 0",
            "        PRINTFORMW 「コホ、コホ……もうすぐ生まれるんだね。ゆりちゃんの子を、ちゃんと抱けるように頑張らなきゃ」",
            "    ELSEIF A == 1",
            "        PRINTFORMW 「……お腹、重いよぉ。でも、ゆりちゃんの子が動くの。ねえ、ゆりちゃんにも触ってほしい」",
            "    ELSE",
            "        PRINTFORMW 「臨月だって。怖いけど、ゆりちゃんがくれた命だもん。最後まで、わたしが守るからね」",
            "    ENDIF",
            "    RETURN 0",
            "ELSEIF TFLAG:13 == 21 && CFLAG:TARGET:111 == 27 && NO:TARGET == 25",
            "    A = RAND:3",
            "    IF A == 0",
            "        PRINTFORMW 「……産まれたよ。ゆりちゃん、見て。わたしたちの子……ちゃんと、ここにいる」",
            "    ELSEIF A == 1",
            "        PRINTFORMW 「コホ、コホ……泣いてる。元気な声だね。ゆりちゃん、わたし、ちゃんとお母さんになれたかな」",
            "    ELSE",
            "        PRINTFORMW 「……ゆりちゃんがくれた子、抱けた。怖かったけど、ゆりちゃんの顔を思い出したら頑張れたよ」",
            "    ENDIF",
            "    RETURN 0",
            "ELSEIF TFLAG:13 == 23 && CFLAG:TARGET:111 == 27 && NO:TARGET == 25",
            "    A = RAND:3",
            "    IF A == 0",
            "        PRINTFORMW 「今は育児室から動けないの。ゆりちゃん、たまにでいいから顔を見せてね。……寂しいから」",
            "    ELSEIF A == 1",
            "        PRINTFORMW 「夜泣きで眠れないけど、ゆりちゃんの声を聞くと少し安心する。もう少しだけ、そばにいてくれる？」",
            "    ELSE",
            "        PRINTFORMW 「ゆりちゃん、この子を抱いてみる？　わたしの大事な子。ゆりちゃんにも、大事にしてほしいな」",
            "    ENDIF",
            "    RETURN 0",
            "ELSEIF TFLAG:13 == 22 && CFLAG:TARGET:111 == 27 && NO:TARGET == 25",
            "    A = RAND:3",
            "    IF A == 0",
            "        PRINTFORMW 「……あの子も親離れしたよ。ちょっと寂しいけど、これでまた、ゆりちゃんと一緒にいられるね」",
            "    ELSEIF A == 1",
            "        PRINTFORMW 「ゆりちゃん、わたし頑張ったよ。子供も大きくなったし、今度はわたしがゆりちゃんのところへ行ってもいい？」",
            "    ELSE",
            "        PRINTFORMW 「……家族が増えて、また少し落ち着いたね。ゆりちゃんがいてくれて、本当によかった」",
            "    ENDIF",
            "    RETURN 0",
            "ENDIF",
            end,
        ]
    )


PLAYER_EJAC_GENERAL = render_four_stage(
    PLAYER_EJAC_MARKERS[0][0],
    PLAYER_EJAC_MARKERS[0][1],
    (
        (
            "「……つゆりちゃん、出た……？　わたしの手の中で、こんなに震えてる。……見て、わたしがつゆりちゃんを気持ちよくした」",
            "「……熱い。つゆりちゃんの全部が、わたしの手に……っ。もっと欲しいって言ったら、困る？」",
            "「……まだ止まらないの？　大丈夫、こぼれても拭かない。つゆりちゃんがわたしにくれたものだから」",
        ),
        (
            "「……また出た。つゆりちゃん、わたしの手でこんなになって……。もう、わたしだけの仕事にして」",
            "「……何度でも出るんだ。ふふ、つゆりちゃんの体、わたしのことを覚えた？」",
            "「……手がべたべた。なのに離したくない。つゆりちゃんの熱、まだ残ってるから」",
        ),
        (
            "「……出た。つゆりちゃんの顔、見せて。わたし、ちゃんと気持ちよくできた？」",
            "「……つゆりちゃんの体が跳ねた。わたしの手で、そんな顔するんだ……覚えておく」",
            "「……あったかい。つゆりちゃん、今日はわたしのことだけ考えてて」",
        ),
        (
            "「……また出した。もう、つゆりちゃんの手はわたしのもの。違う、わたしの手がつゆりちゃんのもの」",
            "「……ふふ、何回目でも嬉しい。つゆりちゃんがわたしを選んでくれたみたいで」",
            "「……まだ欲しい？　なら、わたしが受け止める。つゆりちゃんの分、ぜんぶ」",
        ),
    ),
)

PLAYER_EJAC_MOUTH = render_four_stage(
    PLAYER_EJAC_MARKERS[1][0],
    PLAYER_EJAC_MARKERS[1][1],
    (
        (
            "「……んっ、ごく……。つゆりちゃんの味、口の中いっぱい。吐き出すなんてできない」",
            "「……苦いのに、つゆりちゃんのなら覚えたい。飲み込んだら、もっと近くなれる？」",
            "「……あふれちゃう。つゆりちゃん、わたしの口の中で、まだ震えてる……」",
        ),
        (
            "「……また口にくれるの？　ふふ、つゆりちゃんはわたしに甘いね。ちゃんと飲むから」",
            "「……何度も、ごく、ごく……。つゆりちゃんの熱が、喉の奥まで残ってる」",
            "「……もういっぱい。でも、つゆりちゃんが欲しいなら、まだ入る。たぶん」",
        ),
        (
            "「……ん、ごく。つゆりちゃん、今の顔かわいい。もっと近くで見せて」",
            "「……口に出した。わたしの中に、つゆりちゃんが入ってくるみたい」",
            "「……少し苦い。でも、つゆりちゃんの味なら、嫌いにならない」",
        ),
        (
            "「……また、ごくん。つゆりちゃんのもの、わたしが全部覚えていく」",
            "「……慣れたんじゃない。つゆりちゃんだから、受け止められるだけ」",
            "「……まだ出るの？　うん、いいよ。わたしの口、つゆりちゃん専用にする」",
        ),
    ),
)

PLAYER_EJAC_IN = render_four_stage(
    PLAYER_EJAC_MARKERS[2][0],
    PLAYER_EJAC_MARKERS[2][1],
    (
        (
            "「……奥に、熱いのが来た。つゆりちゃんがわたしの中に残ってる……」",
            "「……いっぱい。つゆりちゃんの熱で、わたしの中まで変になる。もっと、ぎゅってして」",
            "「……あふれてる。抜かないで、つゆりちゃん。わたしの中から逃げないで」",
        ),
        (
            "「……また中に。もう、つゆりちゃんでいっぱいなのに……ふふ、まだ入るんだ」",
            "「……何度も奥まで。つゆりちゃん、わたしの中を自分の場所にする気？」",
            "「……熱いのが残ってる。これ、洗わない。つゆりちゃんの証拠だから」",
        ),
        (
            "「……中で出した。つゆりちゃん、ちゃんとわたしを見て。わたし、逃げないから」",
            "「……奥があったかい。つゆりちゃんと繋がったまま、動けなくなりそう」",
            "「……ふふ、わたしの中に、つゆりちゃんがいる。もう少し、このままでいて」",
        ),
        (
            "「……また中。つゆりちゃんのもの、わたしが受け止める。何度でも」",
            "「……お腹の奥まで、つゆりちゃんでいっぱい。ねえ、これでわたしのこと忘れない？」",
            "「……まだ熱い。つゆりちゃんが抜けても、わたしの中では終わらないから」",
        ),
    ),
)


def main() -> None:
    com = COM.read_bytes().decode("cp932")
    yuri = YURI.read_bytes().decode("cp932")
    tsuyuri = TSUYURI.read_bytes().decode("cp932")
    pregnancy = PREGNANCY.read_bytes().decode("cp932")

    # 前回の誤った配置（関数ラベル前）を除去し、ラベル直後へ移す。
    orgasm_block = extract_block(com, ORGASM_START, ORGASM_END)
    com = remove_block(com, ORGASM_START, ORGASM_END)
    yuri = remove_block(yuri, OLD_EJAC_START, OLD_EJAC_END)

    com = reset_after_label(com, "@CHAR_EJAC_27", PLAYER_EJAC_GENERAL, *PLAYER_EJAC_MARKERS[0])
    com = reset_after_label(com, "@CHAR_EJAC_MOUTH_27", PLAYER_EJAC_MOUTH, *PLAYER_EJAC_MARKERS[1])
    com = reset_after_label(com, "@CHAR_EJAC_IN_27", PLAYER_EJAC_IN, *PLAYER_EJAC_MARKERS[2])
    com = reset_after_label(com, "@CHAR_ORGASM_27", orgasm_block, ORGASM_START, ORGASM_END)

    yuri = reset_after_label(yuri, "@CHAR_FUTA_EJAC_27", render_yuri_ejaculation(), *YURI_EJAC_MARKERS)
    yuri = reset_after_label(yuri, "@CHAR_MILK_27", render_yuri_milk(), *YURI_MILK_MARKERS)
    yuri = reset_after_label(yuri, "@KOJO_NINSIN_K27", render_yuri_pregnancy(), *YURI_PREG_MARKERS)
    tsuyuri = reset_after_label(tsuyuri, "@KOJO_NINSIN_K25", render_tsuyuri_pregnancy(), *TSUYURI_PREG_MARKERS)

    start = pregnancy.index("@GET_CHILD_T_TO_M")
    end = pregnancy.index("@PREGNANCY_FEEL", start)
    segment = pregnancy[start:end]
    old = "\t\tTFLAG:13 = 20\r\n\t\tCALL SELF_KOJO\r\n"
    new = (
        "\t\tZ = TARGET\r\n"
        "\t\tTARGET = MASTER\r\n"
        "\t\tTFLAG:13 = 20\r\n"
        "\t\tCALL SELF_KOJO\r\n"
        "\t\tTARGET = Z\r\n"
        "\t\tTFLAG:13 = 98\r\n"
        "\t\tCALL SELF_KOJO\r\n"
    )
    if "\t\tZ = TARGET\r\n" in segment:
        section_start = segment.index("\t\tZ = TARGET\r\n")
        section_end = segment.index("\tENDIF\r\nENDIF", section_start)
        segment = segment[:section_start] + new + segment[section_end:]
        pregnancy = pregnancy[:start] + segment + pregnancy[end:]
    elif segment.count(old) == 1:
        pregnancy = pregnancy[:start] + segment.replace(old, new, 1) + pregnancy[end:]
    else:
        raise SystemExit(f"GET_CHILD_T_TO_M target swap anchor count: {segment.count(old)}")

    COM.write_bytes(com.encode("cp932"))
    YURI.write_bytes(yuri.encode("cp932"))
    TSUYURI.write_bytes(tsuyuri.encode("cp932"))
    PREGNANCY.write_bytes(pregnancy.encode("cp932"))


if __name__ == "__main__":
    main()
