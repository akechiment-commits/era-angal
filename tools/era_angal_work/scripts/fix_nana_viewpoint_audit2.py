from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_29_春風なな_COM.ERB")

# 注釈で、助手／他の女子が相手と明記されているCOM。
FEMALE_ASSISTANT_COMS = (
    23,
    56,
    61,
    63,
    65,
    66,
    160,
    188,
    189,
    192,
    193,
    194,
    195,
    196,
    200,
    203,
    381,
)

OLD_COM66 = """\t\t\tPRINTFORMW 「ちゅっ、ちゅぷっ……お口、ぱんぱんですけどっ、ぱりぱりがんばりますーっ☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ん、ちゅっ……ふたりで一緒に応援するんですねーっ☆　転校生くんが気持ちよさそうにしてくれると、あたしももっと頑張りたくなりますーっ♪」
\t\tELSE
\t\t\tPRINTFORMW 「隣の子に負けないように、あたしもファイトですーっ……。でも、息が重なると恥ずかしくて、応援の声がちょっと変になっちゃいますねーっ……」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\t;通常
\t\t\tPRINTFORMW 「ん、んむっ、に、二つってっ……交互にっ、かなっ……!?」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ふたりで口を使うんですかーっ……！　ん、ちゅっ……%LOCALS%さんも転校生くんも、ちゃんと元気になってくださいねーっ……！」
\t\tELSE
\t\t\tPRINTFORMW 「隣の子と一緒なんて恥ずかしいですーっ……。ん、ちゅ……あたしの番、ちゃんとできてますかーっ？　比べないでくださいねーっ……」"""

NEW_COM66 = """\t\t\tPRINTFORMW 「んっ、転校生くんも%LOCALS%さんも同時ですかーっ……！　あたし一人で二人分の応援、ちゃんと届いてますかーっ☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ちゅっ……二本いっぺんは息が難しいですよーっ……。でも、転校生くんと%LOCALS%さんが気持ちよさそうなら、あたし、口を離せないですーっ♪」
\t\tELSE
\t\t\tPRINTFORMW 「ふぁっ、右も左も熱くて、頭がぐるぐるですーっ……！　あたしの声、二人に届くように頑張りますから、急に動かさないでくださいねーっ……」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\t;通常
\t\t\tPRINTFORMW 「ん、んむっ……二本も同時なんですかーっ!?　あたし一人で、転校生くんと%LOCALS%さんの二人分を受け止めるんですかーっ……!?」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「転校生くんも%LOCALS%さんも、あたし一人でお口にするんですかーっ……!?　どっちから頑張ればいいか、まだ決められないですよーっ……！」
\t\tELSE
\t\t\tPRINTFORMW 「んっ、二本とも口で受け止めると、息が続かないですよーっ……！　転校生くんも%LOCALS%さんも、あたしの合図を見てくださいねーっ……」"""

# `%LOCALS%` already includes the complete character-specific address.
NEW_COM66 = NEW_COM66.replace("%LOCALS%さん", "%LOCALS%")


def main() -> None:
    text = PATH.read_bytes().decode("cp932").replace("\r\n", "\n")

    if text.count(OLD_COM66) == 1:
        text = text.replace(OLD_COM66, NEW_COM66)
    elif NEW_COM66 not in text:
        raise SystemExit(
            "COM66 target text is neither the pre-correction nor the corrected form"
        )

    inserted = 0
    for com in FEMALE_ASSISTANT_COMS:
        needle = f"IF SELECTCOM == {com}\n"
        replacement = (
            needle
            + "\tCALL AITE_YOBI, 29, ASSI\n"
            + '\tLOCALS \'= @"%RESULTS%"\n'
        )
        if replacement in text:
            continue
        if text.count(needle) != 1:
            raise SystemExit(f"COM{com} header count must be 1, got {text.count(needle)}")
        text = text.replace(needle, replacement, 1)
        inserted += 1

    PATH.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print(f"corrected COM66 and inserted assistant-name anchors: {inserted}")


if __name__ == "__main__":
    main()
