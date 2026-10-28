"""CHAR52のCHAR68との共有文を、やこの演劇部長・裏方軸へ戻す。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_52_湖南やこ_COM.ERB"

REPLACEMENTS = {
    "「あぁ、%LOCALS%感じてる……あたしも、夢中になっちゃう……っ」":
        "「%LOCALS%、ちゃんと息をして……っ。そんなふうに鳴かれたら、あたしの演出まで狂うじゃない……っ」",
    "「奥まで突いたら……あたしも、もう……っ」":
        "「ふん、幕が下りるまで離さないわよ。%LOCALS%、そんなに震えて……あたしのほうまで、調子が狂うじゃない……っ」",
    "「谷間でこすれて……っ。べ、べつに、気持ちよくなんか……」":
        "「胸を合わせて……っ。ふん、こんな近さで平気な顔なんて無理よ。あたしのほうまで、熱くなるじゃない……」",
    "「そんなにされたら……っ。ふん、あたしも、もう……っ」":
        "「ちょっと、そんなに押しつけたら……っ。べ、べつに逃げないけど、あたしのペースを乱すんじゃないわよ……っ」",
}


def main() -> int:
    text = TARGET.read_bytes().decode("cp932")
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected exactly one occurrence: {old!r}, got {count}")
        text = text.replace(old, new, 1)
    TARGET.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print(f"rewrote {len(REPLACEMENTS)} lines in {TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
