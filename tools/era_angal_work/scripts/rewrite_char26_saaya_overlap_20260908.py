"""CHAR26のCHAR52/68との共有文を、さあやの委員長・初心軸へ戻す。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_26_堀田さあや_COM.ERB"

REPLACEMENTS = {
    "「あぁ、%LOCALS%感じてる……あたしも、夢中になっちゃう……っ」":
        "「%LOCALS%、無理してないでしょうね……？　……って、そんな声を出されたら、あたしまで止まれなくなるじゃない……っ」",
    "「奥まで突いたら……あたしも、もう……っ」":
        "「ふん、最後まで面倒みてあげる。%LOCALS%、そんなに震えて……あたしのほうまで、変になるじゃない……っ」",
}


def main() -> int:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
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
