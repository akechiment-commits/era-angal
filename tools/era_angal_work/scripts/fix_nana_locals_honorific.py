from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_29_春風なな_COM.ERB")
OLD = "%LOCALS%さん"


def main() -> None:
    text = PATH.read_bytes().decode("cp932")
    count = text.count(OLD)
    if count:
        text = text.replace("\r\n", "\n").replace(OLD, "%LOCALS%")
        PATH.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print(f"removed duplicated honorifics: {count}")


if __name__ == "__main__":
    main()
