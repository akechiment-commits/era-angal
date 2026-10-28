"""CHAR07 COM188に残る高類似の同時受け反応を、ちあきの原作軸で補正する。"""

from pathlib import Path


TARGET = Path(__file__).resolve().parents[1] / "ERB/CHAR/CHAR_07_高原ちあき_COM.ERB"

REWRITES = {
    "「ん、ぬぷっ……%LOCALS%の奥に挿れながら、あたしのなかにも、ぐって……♪ りょ、両方なんて、あたま真っ白……♪」": "「ん、ぬぷっ……%LOCALS%の奥と、あたしのなかが同時に押されて……っ。れ、連携が近すぎて、声かけする余裕もないですよ～っ♪」",
    "「%LOCALS%の奥に入れながら、あたしのなかにも……両方が近すぎて、頭が真っ白です♪」": "「%LOCALS%の奥へ進むのと、あたしのなかへ押されるのが重なって……っ。ふたり分を受け止めるなんて、身体が追いつかないですよ～♪」",
}


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    for old, new in REWRITES.items():
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"置換対象が一意でない: {count}件: {old}")
        text = text.replace(old, new, 1)
    data = text.encode("cp932")
    if data.count(b"\r\n") != data.count(b"\n"):
        raise SystemExit("CRLF検査失敗")
    TARGET.write_bytes(data)
    print(f"CHAR07 COM188: {len(REWRITES)}件を補正")


if __name__ == "__main__":
    main()
