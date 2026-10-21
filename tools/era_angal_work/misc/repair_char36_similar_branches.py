from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB" / "CHAR" / "CHAR_36_遠見ちか_COM.ERB"

REPLACEMENTS = {
    "PRINTFORMW 「にゅ～ん、%LOCALS%を見下ろしてぇ……ふふんっ、可愛い顔しちゃってますねぇ☆」":
        "PRINTFORMW 「にゅ～ん、%LOCALS%を見下ろしてるとぉ……ふふ、もっと甘やかしたくなりますねぇ☆」",
    "PRINTFORMW 「ふぁ、%LOCALS%、わたしのペースですからねぇ……ゆっくり、ですよぉ」":
        "PRINTFORMW 「んぅ……急がなくていいですからぁ。気持ちいいところ、探しますねぇ」",
    "PRINTFORMW 「にゅ～ん、%LOCALS%の背中、いい眺めですねぇ☆　たぁっぷり可愛がりますからぁ」":
        "PRINTFORMW 「にゅ～ん、%LOCALS%の背中を見てるとぉ……もっと近くにいたくなりますねぇ☆」",
    "PRINTFORMW 「あぁんっ、%LOCALS%を後ろから抱きしめながらぇ……至福ですよぉ☆」":
        "PRINTFORMW 「あぁんっ、%LOCALS%の体温がじかに伝わってぇ……頭の中、ふわふわですぅ☆」",
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    for old, new in REPLACEMENTS.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected one occurrence, got {count}: {old}")
        text = text.replace(old, new)
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))
    print(f"patched {len(REPLACEMENTS)} similar RAND3 branches")


if __name__ == "__main__":
    main()
