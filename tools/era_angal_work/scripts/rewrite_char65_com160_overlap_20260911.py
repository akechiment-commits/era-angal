from pathlib import Path


TARGET = Path("ERB/CHAR/CHAR_65_時国そら_COM.ERB")
OLD = "れろ……ん。%LOCALS%のここ、こう……？　ん、わたしのも、そんなにされたら……っ"
NEW = "れろ……ん。%LOCALS%の息が耳のすぐそばで重なる……ゆん、ゆん……（わたしのも、こんなふうに聞こえているのかな……？）"


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    assert text.count(OLD) == 1, text.count(OLD)
    text = text.replace(OLD, NEW, 1)
    assert text.count(OLD) == 0
    assert text.count(NEW) == 1

    data = text.encode("cp932")
    with TARGET.open("wb") as f:
        f.write(data)

    print("CHAR65 COM160通常A=0の重複1行をそらの声へ修正")


if __name__ == "__main__":
    main()
