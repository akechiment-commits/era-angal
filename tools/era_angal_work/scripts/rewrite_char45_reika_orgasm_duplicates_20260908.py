"""CHAR45れいかの絶頂条件間に重複している6枝を分離する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ERB/CHAR/CHAR_45_円城寺れいか_COM.ERB"


REPLACEMENTS = {
    'PRINTFORMW 「やだ、やだぁ……っ、ぜんぶ、いっしょに……っ！　お兄さま、れいかを抱いて、置いていかないでぇ……っ！」':
        'PRINTFORMW 「ひぁっ……また来たのね……っ！　お兄さま、れいかのこと、ちゃんと抱いていて……っ！」',
    'PRINTFORMW 「あぁっ……！　むり、もうむり……っ！　ぎゅってして、もっと、もっと強く……っ！」':
        'PRINTFORMW 「あぁっ……っ、身体が勝手に跳ねる……！　ぎゅってして、わたくしを見失わせないで……っ！」',
    'PRINTFORMW 「ひぁぁ……っ、何も分からない……！　お兄さま、お願い、わたくしをひとりにしないでぇ……っ！」':
        'PRINTFORMW 「や……っ、まだ熱が残ってるのに……！　お兄さま、お願い、ここにいて……っ！」',
    'PRINTFORMW 「あ゛っ、あぁっ……！　ぜんぶ、同時に……っ、れいか、もう、保てない……っ！」':
        'PRINTFORMW 「ぁっ……！　もう、隠しきれない……っ。坊や、責任を取る覚悟はできていて……っ！」',
    'PRINTFORMW 「ひぃっ……！　な、何度も、いっぺんに……っ。頭が、真っ白よ……っ！」':
        'PRINTFORMW 「ひぃっ……！　繰り返されるたび、令嬢の顔が剥がれていくわ……っ！」',
    'PRINTFORMW 「あぁっ……とまらない……っ！　坊や、もう許して……っ、でも、離れたら駄目……っ！」':
        'PRINTFORMW 「あぁっ……！　まだ来るなんて聞いていなくてよ……！　坊や、離れることだけは許しません……っ！」',
}


def replace_second(data: str, old: str, new: str) -> str:
    first = data.find(old)
    if first < 0:
        raise RuntimeError(f"missing duplicate: {old}")
    second = data.find(old, first + len(old))
    if second < 0:
        raise RuntimeError(f"expected second occurrence: {old}")
    if data.find(old, second + len(old)) >= 0:
        raise RuntimeError(f"more than two occurrences: {old}")
    return data[:second] + new + data[second + len(old) :]


def main() -> None:
    data = PATH.read_text(encoding="cp932")
    for old, new in REPLACEMENTS.items():
        data = replace_second(data, old, new)
    PATH.write_bytes(data.replace("\n", "\r\n").encode("cp932"))
    print(f"rewrote {len(REPLACEMENTS)} duplicate orgasm branches")


if __name__ == "__main__":
    main()
