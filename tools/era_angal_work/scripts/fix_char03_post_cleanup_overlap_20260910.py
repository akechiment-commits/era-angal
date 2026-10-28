"""CHAR03の語尾整理後に顕在化した他CHARとの再重複を分離する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_03_小野ちよ_COM.ERB"
ENCODING = "cp932"


REWRITES = {
    "ひっ……いやです、こんなの……。口に入れないでください……っ":
        "ひっ……いやですぅ、こんなの……。お兄ちゃん先輩、もうやめてください～っ",
    "やっ……抜いてください……っ。女の子にされるなんて、恥ずかしいです……":
        "やっ……抜いてください……っ。女の子にされるなんて、ふぇ、恥ずかしくてどうしたらいいか……",
    "は……っ、%LOCALS%の中に入れながら、わたしも入れられて……。頭が追いつかないです……":
        "は……っ、%LOCALS%の中に入れながら、わたしも入れられて……。ふぇ、頭がぐるぐるしちゃいます……っ",
    "ぷはっ……息が続かないです。お互いに口を使うなんて、聞いてません……っ":
        "ぷはっ……っ、もう息が足りません……。お互いに口を使うなんて、聞いてないですぅ……っ",
    "んっ……指先が熱いです。見られながらするものじゃないです……っ":
        "んっ……指先が熱いです……。お兄ちゃん先輩、見られながらするの、こんなに恥ずかしいんですね……っ",
}


def main() -> None:
    text = TARGET.read_bytes().decode(ENCODING)
    for old, new in REWRITES.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"置換対象の出現数が不正です: {count}件 / {old}")
        text = text.replace(old, new, 1)
    TARGET.write_bytes(text.encode(ENCODING))
    print(f"CHAR03 post-cleanup overlap fix: {len(REWRITES)} lines")


if __name__ == "__main__":
    main()
