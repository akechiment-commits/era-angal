"""CHAR11 氷野くるみの原作外一人称・語尾を是正する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "ERB/CHAR/CHAR_11_氷野くるみ.ERB"
COM = ROOT / "ERB/CHAR/CHAR_11_氷野くるみ_COM.ERB"


def cleanup(path: Path, *, replace_first_person: bool) -> tuple[int, int]:
    text = path.read_bytes().decode("cp932")
    first_person = text.count("あたし")
    if replace_first_person and first_person != 1:
        raise SystemExit(f"一人称の想定件数が不一致: {path.name} {first_person}")
    if not replace_first_person and first_person != 0:
        raise SystemExit(f"COMに予期しない一人称: {path.name} {first_person}")
    if replace_first_person:
        text = text.replace("あたし", "わたし")
    bad_yo = text.count("ですよぉ")
    bad_su = text.count("ですぅ")
    text = text.replace("ですよぉ～", "ですよ～")
    text = text.replace("ですよぉ……", "ですよ……")
    text = text.replace("ですよぉっ", "ですよっ")
    text = text.replace("ですよぉ！", "ですよ！")
    text = text.replace("ですよぉ♪", "ですよ♪")
    text = text.replace("ですよぉ、", "ですよ、")
    text = text.replace("ですぅ", "です～")
    data = text.encode("cp932")
    if data.count(b"\r\n") != data.count(b"\n"):
        raise SystemExit(f"CRLF検査失敗: {path.name}")
    path.write_bytes(data)
    return bad_yo, bad_su


def main() -> None:
    base_yo, base_su = cleanup(BASE, replace_first_person=True)
    com_yo, com_su = cleanup(COM, replace_first_person=False)
    if (base_yo, base_su, com_yo, com_su) != (1, 0, 10, 2):
        raise SystemExit(f"想定外の汚染語件数: {(base_yo, base_su, com_yo, com_su)}")
    print(f"CHAR11: 一人称1件・原作外語尾{base_yo + com_yo + base_su + com_su}件を是正")


if __name__ == "__main__":
    main()
