import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_35_梅園かな_COM.ERB"


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    # 既に3回の「もう」を含む口癖は触らず、2回だけの箇所を補正する。
    pattern = re.compile(r"(?<!もう)もうもうっ")
    count = len(pattern.findall(text))
    if count != 1:
        raise ValueError(f"CHAR35の『もうもうっ』短縮形が想定外の件数です: {count}")
    text = pattern.sub("もうもうもうっ", text)
    encoded = text.replace("\r\n", "\n").replace("\r", "\n").encode("cp932")
    TARGET.write_bytes(encoded.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    print("CHAR_35の『もうもうっ』を『もうもうもうっ』へ統一しました。")


if __name__ == "__main__":
    main()
