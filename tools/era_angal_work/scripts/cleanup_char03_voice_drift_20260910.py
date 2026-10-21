"""CHAR03ちよの原作外語彙と、過剰な「ですぅ」語尾を整理する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_03_小野ちよ_COM.ERB"
ENCODING = "cp932"


REWRITES = {
    "調合…ふふ、お菓子作りも実験みたいなものですよね。一緒にやってみましょう♪":
        "調合…ふふ、材料を混ぜるのって、お菓子作りに似てますよね。一緒にやってみましょう♪",
    "先輩と二人で調合、なんだか秘密の実験みたい。えへへ、わくわくしちゃう":
        "先輩と二人で調合、なんだか秘密のお菓子作りみたい。えへへ、わくわくしちゃう♪",
}


def main() -> None:
    text = TARGET.read_bytes().decode(ENCODING)
    for old, new in REWRITES.items():
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"置換対象の出現数が不正です: {count}件 / {old}")
        text = text.replace(old, new, 1)

    old_suffix_count = text.count("ですぅ")
    if old_suffix_count < 100:
        raise RuntimeError(f"ですぅの件数が想定より少ないため中止します: {old_suffix_count}件")
    text = text.replace("ですぅ", "です")
    TARGET.write_bytes(text.encode(ENCODING))
    print(f"CHAR03 voice cleanup: {len(REWRITES)} lines, ですぅ {old_suffix_count} occurrences -> です")


if __name__ == "__main__":
    main()
