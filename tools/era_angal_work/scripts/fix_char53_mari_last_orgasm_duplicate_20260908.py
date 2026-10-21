"""CHAR53まりの絶頂部に残った最後の完全重複を解消する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ERB/CHAR/CHAR_53_花丘まり_COM.ERB"
OLD = 'PRINTFORMW 「あっ……そんな顔で見ないでおくれよ。そこ、まだ震えてるんだから……ふふ、責任を取っておくれ♪」'
NEW = 'PRINTFORMW 「あっ……そこを急に責めると、身体が先に返事しちまうよ……。ふふ、まいったねぇ♪」'


def main() -> None:
    data = PATH.read_text(encoding="cp932")
    if data.count(OLD) != 2:
        raise RuntimeError(f"expected two occurrences, found {data.count(OLD)}")
    second = data.find(OLD, data.find(OLD) + len(OLD))
    data = data[:second] + NEW + data[second + len(OLD) :]
    PATH.write_bytes(data.replace("\n", "\r\n").encode("cp932"))
    print("fixed last orgasm duplicate")


if __name__ == "__main__":
    main()
