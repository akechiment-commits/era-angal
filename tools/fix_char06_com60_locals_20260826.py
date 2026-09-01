from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_06_藍乃あいか_COM.ERB")


def main() -> None:
    text = PATH.read_bytes().decode("cp932")
    old = (
        "IF SELECTCOM == 60\r\n"
        "\tA = RAND:3\r\n"
    )
    new = (
        "IF SELECTCOM == 60\r\n"
        "\tCALL AITE_YOBI, 6, ASSI\r\n"
        "\tLOCALS '= @\"%RESULTS%\"\r\n"
        "\tA = RAND:3\r\n"
    )
    if text.count(old) == 1:
        text = text.replace(old, new, 1)
    elif text.count(new) != 1:
        raise RuntimeError(f"COM60 header matches old={text.count(old)} new={text.count(new)}")

    replacements = {
        "PRINTFORMW 「相手の子のほうが震えてる……。安心させなきゃって思ったら、先輩に見られてることまで忘れられました。少しだけですけど」":
            "PRINTFORMW 「%LOCALS%のほうが震えてる……。安心させなきゃって思ったら、先輩に見られてることまで忘れられました。少しだけですけど」",
        "PRINTFORMW 「ん、ちゅ……。キスしてる間は何も言えないんですね。先輩に聞きたいことばかり浮かぶのに、唇が塞がってる……」":
            "PRINTFORMW 「ん、ちゅ……。%LOCALS%とキスしてる間は何も言えないんですね。先輩に聞きたいことばかり浮かぶのに、唇が塞がってる……」",
        "PRINTFORMW 「嫉妬を試して恋が深まる、なんて本にはありますけど……わたしは試したくないです。先輩の気持ち、本物だから怖いんです」":
            "PRINTFORMW 「%LOCALS%とのキスを見せて嫉妬を試して恋が深まる、なんて本にはありますけど……わたしは試したくないです。先輩の気持ち、本物だから怖いんです」",
        "PRINTFORMW 「ふぁっ、わたしが相手でいいんですか？　あの、嫌という意味じゃなくて……まず、そっちも困ってないか知りたくて」":
            "PRINTFORMW 「ふぁっ、%LOCALS%が相手でいいんですか？　あの、嫌という意味じゃなくて……まず、そっちも困ってないか知りたくて」",
        "PRINTFORMW 「んむ……ひゃっ。いま謝りそうになったけど、キスされて謝るのも変ですよね。……もう一度なら、今度は黙ってできます」":
            "PRINTFORMW 「んむ……ひゃっ。いま謝りそうになったけど、%LOCALS%にキスされて謝るのも変ですよね。……もう一度なら、今度は黙ってできます」",
        "PRINTFORMW 「ふたりとも目を閉じるタイミングを逃しちゃった……。ふふ、変な顔。笑えたから、さっきより怖くないです」":
            "PRINTFORMW 「%LOCALS%もわたしも目を閉じるタイミングを逃しちゃった……。ふふ、変な顔。笑えたから、さっきより怖くないです」",
    }
    for old_line, new_line in replacements.items():
        if text.count(old_line) != 1:
            raise RuntimeError(f"COM60 dialogue match={text.count(old_line)}: {old_line[:30]}")
        text = text.replace(old_line, new_line, 1)
    PATH.write_bytes(text.encode("cp932"))
    print("CHAR06 COM60: assistant name binding restored")


if __name__ == "__main__":
    main()
