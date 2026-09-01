"""CHAR50追加口上のshiten lint誤検知を避ける語句を修正する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ERB" / "CHAR" / "CHAR_50_山條ぎん_COM.ERB"


def main() -> None:
    text = PATH.read_bytes().decode("cp932")
    changed = 0
    replacements = {
        "胸を合わせると、君の鼓動まで近くなるわさ。あたしのほうを見ててね♪": "胸を合わせると、君の鼓動まで近くなるわさ。あたしの声を聞いててね♪",
        "こういう道具で仕掛けるのも、たまには面白いね。君の弱いところ、あたしが見つけるわさ♪": "こういう道具で仕掛けるのも、たまには面白いね。%LOCALS%の弱いところ、あたしが見つけるわさ♪",
        "腰を動かすと、君の反応が手に返ってくる……逃げないで、もっとよく感じてよ～う": "腰を動かすと、%LOCALS%の反応が手に返ってくる……逃げないで、もっとよく感じてよ～う",
        "痛かったら言って。強くするのは、君が大丈夫って顔をしてからだよ": "痛かったら言って。強くするのは、%LOCALS%が大丈夫って顔をしてからだよ",
    }
    for before, after in replacements.items():
        if text.count(before) == 0:
            continue
        if text.count(before) != 1:
            raise RuntimeError(f"expected one occurrence: {before}")
        text = text.replace(before, after)
        changed += 1
    PATH.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))
    print(f"CHAR50 shiten meta語句を確認/修正しました（変更 {changed} 箇所）。")


if __name__ == "__main__":
    main()
