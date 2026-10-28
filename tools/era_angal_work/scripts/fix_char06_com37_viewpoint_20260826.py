from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_06_藍乃あいか_COM.ERB")


def main() -> None:
    text = PATH.read_bytes().decode("cp932")
    replacements = {
        "PRINTFORMW 「ふぁ、%CALLNAME:PLAYER%先輩。あ、足で、ですか……? えへへ、こうかな♪」":
            "PRINTFORMW 「ふぁ、%CALLNAME:PLAYER%先輩。わたしが足でしてあげるんですね……? えへへ、こうかな♪」",
        "PRINTFORMW 「あう、転校生の先輩。足で、なんて……。う、うまくできてますか?」":
            "PRINTFORMW 「あう、転校生の先輩。わたしの足でしてあげるなんて……う、うまくできてますか?」",
    }
    for old, new in replacements.items():
        if text.count(old) != 1:
            raise RuntimeError(f"COM37 match={text.count(old)}")
        text = text.replace(old, new, 1)
    PATH.write_bytes(text.encode("cp932"))
    print("CHAR06 COM37: active footjob wording made explicit")


if __name__ == "__main__":
    main()
