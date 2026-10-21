"""CHAR07 COM205通常の近似RAND枝を分離する。"""

from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_07_高原ちあき_COM.ERB"
OLD = "「あたしの目の前でそんなことするんですか!?　どこを見ればいいか分からないですよ～っ！」"
NEW = "「えっ、目の前で続けるんですか!?　あたし、応援席みたいに声をかければいいのか、見なかったことにすればいいのか……どっちですか～っ！」"


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    if text.count(OLD) != 1:
        raise SystemExit(f"置換対象が一意でない: {text.count(OLD)}件")
    text = text.replace(OLD, NEW, 1)
    data = text.encode("cp932")
    if data.count(b"\r\n") != data.count(b"\n"):
        raise SystemExit("CRLF検査失敗")
    TARGET.write_bytes(data)
    print("CHAR07 COM205: RAND枝の近似1件を分離")


if __name__ == "__main__":
    main()
