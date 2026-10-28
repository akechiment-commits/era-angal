"""CHAR53 COM203の女性相手視点から観客メタを除去する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ERB/CHAR/CHAR_53_花丘まり_COM.ERB"
OLD = 'PRINTFORMW 「おやまぁ、%LOCALS%の後ろを診るとはねぇ。あたしの反応を見て楽しんでるんだろう？……んっ♪」'
NEW = 'PRINTFORMW 「おやまぁ、%LOCALS%の後ろを診るとはねぇ。ふふ、こんなところまで確かめるとは、ずいぶん熱心だねぇ……んっ♪」'


def main() -> None:
    data = PATH.read_text(encoding="cp932")
    if data.count(OLD) != 1:
        raise RuntimeError(f"expected one occurrence, found {data.count(OLD)}")
    PATH.write_bytes(data.replace(OLD, NEW).replace("\n", "\r\n").encode("cp932"))
    print("fixed COM203 viewpoint")


if __name__ == "__main__":
    main()
