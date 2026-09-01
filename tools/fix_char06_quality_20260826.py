from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_06_藍乃あいか_COM.ERB")


def main() -> None:
    text = PATH.read_bytes().decode("cp932")
    replacements = {
        "PRINTFORMW 「先輩に見られながら受けるの、緊張します……。手を握っていてくれたら、もう少し頑張れます」":
            "PRINTFORMW 「%CALLNAME:PLAYER%先輩に見られながら受けるの、緊張します……。手を握っていてくれたら、もう少し頑張れます」",
        "PRINTFORMW 「んっ……こんな所で、奥まで……っ。%LOCALS%、びくびくして……こ、怖いけと、止まらない……っ」":
            "PRINTFORMW 「んっ……こんな所で、奥まで……っ。%LOCALS%、びくびくして……こ、怖いけど、止まらない……っ」",
    }
    for old, new in replacements.items():
        if text.count(old) != 1:
            raise RuntimeError(f"quality replacement match={text.count(old)}")
        text = text.replace(old, new, 1)
    PATH.write_bytes(text.encode("cp932"))
    print("CHAR06 quality: callname and COM381 typo fixed")


if __name__ == "__main__":
    main()
