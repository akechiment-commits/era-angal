"""CHAR68に残ったCHAR26/52との近似定型を、ふみの新聞部声へ戻す。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_68_深鳥ふみ_COM.ERB"

REPLACEMENTS = {
    "「ふふ、あんたの目を隠すわ。見えないぶん、あたしの声だけ追いなさい♪」":
        "「ふふ、目を閉じてなさい。見えないなら、あたしの声が手がかりよ……逃げちゃだめだからね♪」",
    "「そんなにされたら……っ。ふん、あたしも、もう……っ」":
        "「ふん、そんなところまで熱くするなんて……っ。これは大スクープよ……って、言えるわけないでしょ……っ」",
    "「ふん……っ。あんたの変態。……だ、誰にも言わないでよね……っ」":
        "「ふん……っ、こんな姿を記事にされたら廃刊ものよ。……あんた、笑ったら承知しないからね」",
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
