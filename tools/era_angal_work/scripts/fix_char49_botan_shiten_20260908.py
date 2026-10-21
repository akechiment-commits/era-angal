"""CHAR49ぼたん側の女性相手COMに混入した観客メタ・行為解説を除去する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ERB/CHAR/CHAR_49_小松ぼたん_COM.ERB"


REPLACEMENTS = {
    'PRINTFORMW 「%LOCALS%を抱くと、やわらかさがそのまま返ってくる……。ふふ、女の子相手の採点は、転校生くんにも見せてあげる♪」':
        'PRINTFORMW 「%LOCALS%を抱くと、やわらかさがそのまま返ってくる……。ふふ、女の子相手の採点も、たまには新鮮だね♪」',
    'PRINTFORMW 「%LOCALS%の声を聞きながら、正面からゆっくり押すと……。ふふ、転校生くん、わたしの腕前も見ててね♪」':
        'PRINTFORMW 「%LOCALS%の声を聞きながら、正面からゆっくり押すと……。ふふ、わたしの腕前もなかなかでしょ♪」',
    'PRINTFORMW 「背中越しに震えが伝わると、%LOCALS%の気持ちが手に取るようにわかる……。ふふ、転校生くん、ちゃんと見てた？」':
        'PRINTFORMW 「背中越しに震えが伝わると、%LOCALS%の気持ちが手に取るようにわかる……。ふふ、その声、もっと聞かせて♪」',
    'PRINTFORMW 「%LOCALS%を味わいながら、転校生くんにも見せるなんて……。ふふ、二人分の反応を採点できるから、退屈しないね♪」':
        'PRINTFORMW 「%LOCALS%を味わいながら、ふふ、二人分の反応を採点できるから、退屈しないね♪」',
    'PRINTFORMW 「%LOCALS%と重ねるたび、身体の境目が曖昧になる……。ふふ、転校生くんに見せるには、なかなか贅沢な光景だね♪」':
        'PRINTFORMW 「%LOCALS%と重ねるたび、身体の境目が曖昧になる……。ふふ、なかなか贅沢な光景だね♪」',
    'PRINTFORMW 「%LOCALS%のを受け入れるなんて……女の子同士なのに、こんなに奥までちゃんと感じるんだね……♪」':
        'PRINTFORMW 「%LOCALS%のを受け入れるなんて……こんなに奥までちゃんと感じるんだね……♪」',
}


def main() -> None:
    data = PATH.read_text(encoding="cp932")
    for old, new in REPLACEMENTS.items():
        count = data.count(old)
        if count != 1:
            raise RuntimeError(f"expected one occurrence, found {count}: {old}")
        data = data.replace(old, new)
    PATH.write_bytes(data.replace("\n", "\r\n").encode("cp932"))
    print(f"fixed {len(REPLACEMENTS)} viewpoint/meta lines")


if __name__ == "__main__":
    main()
