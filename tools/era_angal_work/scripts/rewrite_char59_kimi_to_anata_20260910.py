"""CHAR59うしおの原作外呼称「きみ」を、原作にある「あなた」へ戻す。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_59_水嶌うしお_COM.ERB"
ENCODING = "cp932"


def main() -> None:
    text = TARGET.read_bytes().decode(ENCODING)
    count = text.count("きみ")
    if count != 120:
        raise RuntimeError(f"きみの出現数が想定と違うため中止します: {count}件")
    text = text.replace("きみ", "あなた")
    TARGET.write_bytes(text.encode(ENCODING))
    print(f"CHAR59 呼称修正: きみ {count}件 -> あなた")


if __name__ == "__main__":
    main()
