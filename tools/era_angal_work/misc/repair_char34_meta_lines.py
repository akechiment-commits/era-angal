from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_34_桐島かいり_COM.ERB"


REPAIRS = {
    "%LOCALS%を、かいりが動かすんですのね……。転校生くんがそばで見守ってくれるなら、頑張れそうですの♪":
        "%LOCALS%を、かいりが動かすんですのね……。かいり、ちゃんと上手にできるようにしますの♪",
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    for old, new in REPAIRS.items():
        count = text.count(old)
        if count != 1:
            raise ValueError(f"想定外の置換回数: {count}: {old}")
        text = text.replace(old, new)
    encoded = text.replace("\r\n", "\n").replace("\r", "\n").encode("cp932")
    TARGET.write_bytes(encoded.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    print("CHAR_34のメタ表現2行を自然な言い回しへ修正しました。")


if __name__ == "__main__":
    main()
