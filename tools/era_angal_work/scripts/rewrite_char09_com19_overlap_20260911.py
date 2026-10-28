from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_09_月永るか_COM.ERB")
OLD = "ひとつ増えるたび、先輩の手が奥へ近づく感じがします……最後まで任せますね♪"
NEW = "ひゃぅ……せんぱぁい、増えるたびに、奥がきゅうって……っ。ぼ、ぼく、もう逃げられないみたいです……♪"


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    assert text.count(OLD) == 1, text.count(OLD)
    text = text.replace(OLD, NEW, 1)
    assert text.count(OLD) == 0
    assert text.count(NEW) == 1

    data = text.encode("cp932")
    with TARGET.open("wb") as f:
        f.write(data)

    print("CHAR09 COM19恋人A=1の重複1行をるかの声へ修正")


if __name__ == "__main__":
    main()
