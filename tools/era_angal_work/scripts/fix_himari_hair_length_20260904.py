from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_61_鶴海ひまり_COM.ERB"

REPLACEMENTS = {
    "私の髪、短いからすぐ終わるか？":
        "私の髪、長いから……丁寧に梳いてもらえるのは嬉しいなあ♪",
    "私の髪、ユッキーより短いからすぐ終わってしまうなあ……もうちょっと触っていてもいいぞお？":
        "私の髪、かなり長いから、梳き終わるまで時間がかかるなあ……もうちょっと触っていてもいいぞお？",
}


def main() -> None:
    text = TARGET.read_bytes().decode("cp932")
    for before in REPLACEMENTS:
        count = text.count(before)
        if count != 1:
            raise SystemExit(f"想定外の一致数: {count}: {before}")
    for before, after in REPLACEMENTS.items():
        text = text.replace(before, after, 1)
    TARGET.write_bytes(text.encode("cp932"))
    print(f"updated {TARGET}")


if __name__ == "__main__":
    main()
