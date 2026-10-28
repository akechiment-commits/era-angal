"""CHAR07 COM9に残るCHAR09との高類似台詞を、ちあき原作準拠で補正する。"""

from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_07_高原ちあき_COM.ERB"
OLD = "「ひゃっ、そこまで舐めるんですか!?　あたし、心の準備が追いついてないですよ～っ！」"
NEW = "「ひゃっ、そこまで舐めるんですか!?　あたし、先にひと声かけてもらわないと、反射で足が跳ねちゃいますよ～っ！」"


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    if text.count(OLD) != 1:
        raise SystemExit(f"置換対象が一意でない: {text.count(OLD)}件")
    text = text.replace(OLD, NEW, 1)
    data = text.encode("cp932")
    if data.count(b"\r\n") != data.count(b"\n"):
        raise SystemExit("CRLF検査失敗")
    TARGET.write_bytes(data)
    print("CHAR07 COM9: 高類似1件を補正")


if __name__ == "__main__":
    main()
