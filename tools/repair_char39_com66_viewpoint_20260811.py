from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COM_PATH = ROOT / "ERB/CHAR/CHAR_39_冴木もも_COM.ERB"
REPAIRS = {
    "ふたりがかり……？　ん、ちゅ。となりの娘の舌と、ぶつかって……ん、あんた、とろけ顔だね♪":
        "ん、ちゅ……あんたの熱と%CALLNAME:ASSI%の熱が、左右から来る……。あたし、息が忙しくて、でぇへへなんて言ってられないよ♪",
    "ふぅん……？　ん、ちゅぷ。あんたの、二枚の舌に挟まれて……いい顔してる、でぇへへ♪":
        "ふぅん……二人分を、あたし一人で？　ん、ちゅ……順番に息を合わせてよ。あたし、むせちゃうからさ♪",
}


def main() -> None:
    raw = COM_PATH.read_bytes()
    text = raw.decode("cp932")
    changed = 0
    for old, new in REPAIRS.items():
        count = text.count(old)
        if count == 0:
            continue
        if count != 1:
            raise ValueError(f"COM66修正対象が想定外です: {count}件 / {old}")
        text = text.replace(old, new)
        changed += 1
    if changed:
        COM_PATH.write_bytes(text.encode("cp932").replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))
    print(f"CHAR39 COM66の既存混線口上を{changed}件修正しました。")


if __name__ == "__main__":
    main()
