from pathlib import Path


PATH = Path(r"ERB/CHAR/CHAR_06_藍乃あいか_COM.ERB")


def main() -> None:
    text = PATH.read_bytes().decode("cp932")
    before = (text.count("あたし"), text.count("～"))
    text = text.replace("あたし", "わたし").replace("～", "〜")
    PATH.write_bytes(text.encode("cp932"))
    after = (text.count("あたし"), text.count("～"), text.count("〜"))
    print(f"CHAR06 voice normalization: before={before}, after={after}")


if __name__ == "__main__":
    main()
