from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"

REPLACEMENTS = {
    "わたしの、わがまま": "わたしのわがまま",
    "わたしの、特別な秘密": "わたしの特別な秘密",
    "わたしの、んん、変な感じ": "わたしの中、んん、変な感じ",
    "わたしの、とっておきの一着": "わたしのとっておきの一着",
    "わたしの、はしたないとこ": "わたしのはしたないとこ",
    "わたしの、ちっちゃい胸": "わたしのちっちゃい胸",
    "わたしの、こんな姿": "わたしのこんな姿",
    "わたしの、はじめての人": "わたしのはじめての人",
    "わたしの、ぜんぶ": "わたしのぜんぶ",
    "わたしの、お役目": "わたしのお役目",
    "君の、熱いね": "君の熱、熱いね",
    "君の、わたしの脚": "君のこれ、わたしの脚",
    "君の、独り占め": "君のもの、独り占め",
    "君の、ぜんぶ飲んで": "君のぜんぶ、飲んで",
    "君が、いるから": "君がいるから",
    "君が、ほしくて": "君がほしくて",
    "君が、自分で": "君が自分で",
    "君に、めちゃくちゃに、されたい": "君にめちゃくちゃにされたい",
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    for old, new in REPLACEMENTS.items():
        if old not in text:
            raise SystemExit(f"grammar fragment not found: {old}")
        text = text.replace(old, new)
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
