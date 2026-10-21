"""CHAR45 COM131の行為者視点を監査契約に合わせて明示する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ERB/CHAR/CHAR_45_円城寺れいか_COM.ERB"

REPLACEMENTS = {
    "PRINTFORMW あ……っ、縛られたあなたを見ていると、胸が高鳴るわ。怖くないよう、そばにいるから……♪":
        "PRINTFORMW あ……っ、わたくしの縄で動けなくなったあなたを見ていると、胸が高鳴るわ。怖くないよう、そばにいるから……♪",
    "PRINTFORMW 拘束されるのが怖い？　なら、わたくしを退屈させないことね。解いてほしければ、上手に頼みなさい♪":
        "PRINTFORMW 拘束が怖い？　なら、わたくしを退屈させないことね。解いてほしければ、上手に頼みなさい♪",
}


def main() -> None:
    data = PATH.read_text(encoding="cp932")
    for old, new in REPLACEMENTS.items():
        count = data.count(old)
        if count != 1:
            raise RuntimeError(f"expected one occurrence, found {count}: {old}")
        data = data.replace(old, new)
    PATH.write_bytes(data.replace("\n", "\r\n").encode("cp932"))
    print(f"fixed {len(REPLACEMENTS)} COM131 viewpoint lines")


if __name__ == "__main__":
    main()
