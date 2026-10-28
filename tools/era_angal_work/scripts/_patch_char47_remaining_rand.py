from pathlib import Path
import re


path = Path(r"ERB\CHAR\CHAR_47_双葉みなづき_COM.ERB")
text = path.read_bytes().decode("cp932")


def span(command: int):
    start = re.search(rf"(?m)^;--- COM{command}(?![0-9])[^\r\n]*\r?\n", text)
    if not start:
        raise SystemExit(f"missing COM{command}")
    following = re.search(r"(?m)^;--- COM[^\r\n]*\r?\n", text[start.end():])
    end = start.end() + following.start() if following else len(text)
    return start.start(), end


def standard(command, love, normal):
    return "\r\n".join([
        f"IF SELECTCOM == {command}",
        "\tA = RAND:3",
        "\tIF TALENT:TARGET:153",
        "\t\t;恋人",
        "\t\tIF A == 0",
        f"\t\t\tPRINTFORMW {love[0]}",
        "\t\tELSEIF A == 1",
        f"\t\t\tPRINTFORMW {love[1]}",
        "\t\tELSE",
        f"\t\t\tPRINTFORMW {love[2]}",
        "\t\tENDIF",
        "\tELSE",
        "\t\t;通常",
        "\t\tIF A == 0",
        f"\t\t\tPRINTFORMW {normal[0]}",
        "\t\tELSEIF A == 1",
        f"\t\t\tPRINTFORMW {normal[1]}",
        "\t\tELSE",
        f"\t\t\tPRINTFORMW {normal[2]}",
        "\t\tENDIF",
        "\tENDIF",
        "ENDIF",
    ])


start, end = span(110)
block = text[start:end]
prefix = block[:block.index("IF SELECTCOM == 110")]
text = text[:start] + prefix + standard(
    110,
    [
        "「ひゃう……っ。広げられると、奥まで見られてるみたいだね……。ふふ、君になら、もう少し近くで見られてもいいよ……♪」",
        "「んっ……器具が触れるたび、身体の中まで意識しちゃうよ。お姉さんの秘密、君には隠せないね……」",
        "「あっ……っ、そんなところまで開くんだ……。恥ずかしいのに、君が丁寧にしてくれるから、目をそらせないよ……♪」",
    ],
    [
        "「やっ……だめ、そんな器具で……っ。お姉さんの中、覗かないでよぉ……。恥ずかしすぎる……っ」",
        "「ひゃっ……っ、急に広げないでよぉ。見えちゃうの、怖いし、恥ずかしいんだから……ゆっくりね」",
        "「んぅ……っ、冷たいよぉ。こんなふうにされると、どこに隠れたらいいか分からなくなっちゃう……」",
    ],
) + "\r\n\r\n" + text[end:]


start, end = span(17)
block = text[start:end]
prefix = block[:block.index("IF SELECTCOM == 17")]
return_at = block.index("RETURN 0")
body = "\r\n".join([
    "IF SELECTCOM == 17",
    "\tA = RAND:3",
    "\tIF TEQUIP:17",
    "\t\tIF TALENT:TARGET:153",
    "\t\t\t;装着・恋人",
    "\t\t\tIF A == 0",
    "\t\t\t\tPRINTFORMW 「ん、ぁっ……わたし、ぴくんと跳ねちゃう。こんなとこ見せるの、転校生くんだけだよ……♪」",
    "\t\t\tELSEIF A == 1",
    "\t\t\t\tPRINTFORMW 「ひゃっ……っ、急に動き出すと、身体が勝手に反応するね。ふふ、君の前だと隠せないや……」",
    "\t\t\tELSE",
    "\t\t\t\tPRINTFORMW 「んっ……お姉さんの中で、ずっと震えてる。君が見ててくれるなら、もう少し頑張れるよ……♪」",
    "\t\t\tENDIF",
    "\t\tELSE",
    "\t\t\t;装着・通常",
    "\t\t\tIF A == 0",
    "\t\t\t\tPRINTFORMW 「ふにゃっ、なにこれっ……！　下半身が、ふるふる震えちゃう……や、止めてっ、転校生くんっ!?」",
    "\t\t\tELSEIF A == 1",
    "\t\t\t\tPRINTFORMW 「ひゃわっ……っ、勝手に動くよぉ。お姉さん、こんなの聞いてないってばぁ……！」",
    "\t\t\tELSE",
    "\t\t\t\tPRINTFORMW 「んぅ……っ、そこにあるの、ずっと気になっちゃうよぉ。お願い、あんまり見ないで……」",
    "\t\t\tENDIF",
    "\t\tENDIF",
    "\tELSE",
    "\t\tIF TALENT:TARGET:153",
    "\t\t\t;取り外し・恋人",
    "\t\t\tIF A == 0",
    "\t\t\t\tPRINTFORMW 「ふぁ……まだ熱いよぉ。転校生くんは、お姉さんを甘やかしすぎだよぉ……えへへ♪」",
    "\t\t\tELSEIF A == 1",
    "\t\t\t\tPRINTFORMW 「んっ……外れたのに、身体がまだ覚えてるね。ふふ、君のせいで、しばらくふにゃふにゃだよ……」",
    "\t\t\tELSE",
    "\t\t\t\tPRINTFORMW 「はぁ……っ、やっと楽になった。君にこんな顔を見せたままなの、ちょっと悔しいけど……好き♪」",
    "\t\t\tENDIF",
    "\t\tELSE",
    "\t\t\t;取り外し・通常",
    "\t\t\tIF A == 0",
    "\t\t\t\tPRINTFORMW 「ぬ、もうげんかいっ！　こんなおもちゃに、お姉さんが、めろめろにされちゃうなんて……うにゃあ、もう、立てないよぉ……」",
    "\t\t\tELSEIF A == 1",
    "\t\t\t\tPRINTFORMW 「はぁ……っ、外れたぁ……。でも、まだ身体が変な感じだよぉ。お姉さん、少し休ませて……」",
    "\t\t\tELSE",
    "\t\t\t\tPRINTFORMW 「んぅ……っ、やっと終わったよぉ。こんなのに負けたって思うと、恥ずかしくて顔を上げられない……」",
    "\t\t\tENDIF",
    "\t\tENDIF",
    "\tENDIF",
    "ENDIF",
]) + "\r\n\r\n"
text = text[:start] + prefix + body + block[return_at:] + text[end:]

path.write_bytes(text.encode("cp932"))
