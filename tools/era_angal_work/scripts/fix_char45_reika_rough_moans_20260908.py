"""CHAR45れいかの原作外の濁点付き喘ぎを、お嬢様らしい崩れへ直す。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ERB/CHAR/CHAR_45_円城寺れいか_COM.ERB"

REPLACEMENTS = {
    'PRINTFORMW 「あ゛っ、あぁっ……！　ぜんぶ、同時に……っ、れいか、もう、保てない……っ！」':
        'PRINTFORMW 「あっ、あぁっ……！　ぜんぶ、同時に……っ、れいか、もう、保てない……っ！」',
    'PRINTFORMW 「あ゛っ……！　お、お尻が……っ、こんな、令嬢のわたくしが……っ！」':
        'PRINTFORMW 「あっ……！　お、お尻が……っ、こんな、令嬢のわたくしが……っ！」',
    'PRINTFORMW 「あ゛っ……！　そこ、だめ、もう……っ！　お兄さま、れいか、壊れちゃう……っ！」':
        'PRINTFORMW 「あぁっ……！　そこ、だめ、もう……っ！　お兄さま、れいか、壊れちゃう……っ！」',
    'PRINTFORMW 「ぁ゛っ……！　そ、そこは……っ、円城寺の令嬢が、こんな……っ！」':
        'PRINTFORMW 「ぁっ……！　そ、そこは……っ、円城寺の令嬢が、こんな……っ！」',
    'PRINTFORMW 「く゛っ、あぁっ……！　止まらない……っ。わたくし、どうなってしまうの……っ！」':
        'PRINTFORMW 「くっ、あぁっ……！　止まらない……っ。わたくし、どうなってしまうの……っ！」',
    'PRINTFORMW 「あ゛っ……！　胸、むね、もう……っ！　お兄さま、れいかをぎゅってしてぇ……っ！」':
        'PRINTFORMW 「あっ……！　胸、むね、もう……っ！　お兄さま、れいかをぎゅってしてぇ……っ！」',
    'PRINTFORMW 「ぁ゛っ……！　む、胸が……っ、こんな、円城寺の令嬢が……っ！」':
        'PRINTFORMW 「ぁっ……！　む、胸が……っ、こんな、円城寺の令嬢が……っ！」',
    'PRINTFORMW 「く゛っ、あぁっ……！　胸が止まらない……っ。わたくし、もう余裕がなくてよ……っ！」':
        'PRINTFORMW 「くっ、あぁっ……！　胸が止まらない……っ。わたくし、もう余裕がなくてよ……っ！」',
    'PRINTFORMW 「く゛っ、はぁっ……！　唇が止まらない……っ。わたくし、もう、おかしくなる……っ！」':
        'PRINTFORMW 「くっ、はぁっ……！　唇が止まらない……っ。わたくし、もう、おかしくなる……っ！」',
}


def main() -> None:
    data = PATH.read_text(encoding="cp932")
    for old, new in REPLACEMENTS.items():
        count = data.count(old)
        if count != 1:
            raise RuntimeError(f"expected one occurrence, found {count}: {old}")
        data = data.replace(old, new)
    PATH.write_bytes(data.replace("\n", "\r\n").encode("cp932"))
    print(f"fixed {len(REPLACEMENTS)} rough moans")


if __name__ == "__main__":
    main()
