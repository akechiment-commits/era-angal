from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_29_春風なな_COM.ERB")

OLD = """\t\t\tPRINTFORMW 「んっ、足の指で挟まれてっ……えへっ、くすぐったいですーっ♪　腰、ふわってしますっ……」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「足で触るだけなのに、転校生くんの熱がどんどん伝わりますーっ……。あたしの足で元気になってくれるなら、もっとリズムよく動かしますねーっ☆」
\t\tELSE
\t\t\tPRINTFORMW 「ひゃっ、転校生くんの顔、そんなに気持ちよさそうなんですかーっ……。恥ずかしいですけど、あたし、応援する側として手を抜けませんよーっ♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\t;通常
\t\t\tPRINTFORMW 「やっ、足の裏でこすられてっ……んっ、変な声出ちゃうっ……こんなの聞いてないですーっ！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「あたしの足で、転校生くんがそんな顔するんですかーっ!?　恥ずかしいですけど、元気になってくれるなら、もう少し続けますーっ……！」
\t\tELSE
\t\t\tPRINTFORMW 「ひゃっ、腰が動いちゃってますーっ……！　足を離せばいいのか、続ければいいのか、あたし、わからないですよーっ……声で教えてくださいーっ……！」"""

NEW = """\t\t\tPRINTFORMW 「んっ、足でされるのっ……ふぁ、転校生くんの足、あったかいですーっ♪　力が抜けちゃいますーっ……」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「足の指が触れるたび、あたしの身体が勝手に跳ねますーっ……。転校生くん、そんなふうに応援されたら、声を抑えられないですよーっ☆」
\t\tELSE
\t\t\tPRINTFORMW 「ひゃっ、そこを擦られると、あたし、もう立っていられないですーっ……！　足だけでこんなに追い込まれるなんて、ずるいですよーっ……」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\t;通常
\t\t\tPRINTFORMW 「やっ、足でされるんですかーっ!?　うぅ、ふくらはぎまで震えて、あたし、どう受ければいいかわからないですよーっ……！」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「ひゃっ、足の裏が当たるたび、身体がびくってしますーっ……。転校生くん、強さ、教えてくださいーっ……！」
\t\tELSE
\t\t\tPRINTFORMW 「あぅ、もう足を離されたら足りないみたいになってますーっ……！　こんなの、あたしが応援する側じゃなくて、完全に元気をもらってる側ですよーっ……！」"""


def main() -> None:
    text = PATH.read_bytes().decode("cp932")
    normalized = text.replace("\r\n", "\n")
    if normalized.count(OLD) != 1:
        raise SystemExit(f"COM67 target text count must be 1, got {normalized.count(OLD)}")
    updated = normalized.replace(OLD, NEW)
    PATH.write_bytes(updated.replace("\n", "\r\n").encode("cp932"))
    print("corrected COM67 to the annotated receiving perspective")


if __name__ == "__main__":
    main()
