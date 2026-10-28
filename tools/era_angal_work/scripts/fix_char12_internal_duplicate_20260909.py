"""CHAR12 COM66/68の再構成で発生した同一文面を分離する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_12_神樹いちか_COM.ERB"
ENCODING = "cp932"

OLD = "%LOCALS%と一緒に口でしてると、先輩の顔がどんどん緩んでいきますね……ふふ、わかりやすいです♪"
NEW = "%LOCALS%と口を合わせてると、先輩の反応がどんどん返ってきます……あたし、ちゃんと息を合わせますね♪"


def main() -> None:
    text = TARGET.read_bytes().decode(ENCODING)
    if text.count(OLD) != 2:
        raise RuntimeError(f"分離前の重複数が不正です: {text.count(OLD)}件")
    text = text.replace(OLD, NEW, 1)
    TARGET.write_bytes(text.encode(ENCODING))
    print("CHAR12 internal duplicate: COM66/68 wording separated")


if __name__ == "__main__":
    main()
