from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"

REPLACEMENTS = {
    "思ったより緊張するなぁ。転校生くん、そんなにじっと見ないでよ～": "思ったより緊張するね。転校生くん、そんなにじっと見ないでよ",
    "そんなの聞いてないよ～っ！": "そんなの聞いてないよっ！",
    "わたしまで困らせないでよぉ": "わたしまで困らせないでよ",
    "息が合いすぎだよ～っ": "息が合いすぎだよっ",
    "ずるいなぁ。%LOCALS%": "ずるいな。%LOCALS%",
    "変な呪具だねぇ……っ": "変な呪具だね……っ",
    "急に強くしないでよぉ……っ": "急に強くしないでよ……っ",
    "甘えんぼさんだなぁ。": "甘えんぼさんだね。",
    "困るよぉ……って": "困るよ……って",
    "びっくりするよぉ。": "びっくりするよ。",
    "恥ずかしいなぁ♪": "恥ずかしいな♪",
    "見ないでよ～っ！": "見ないでよっ！",
    "そこは強いよぉ……っ": "そこは強いよ……っ",
    "幼くなるよぉ……": "幼くなるよ……",
    "力が入らないなぁ……": "力が入らないな……",
    "止まらないよぉ……。": "止まらないよ……。",
    "止まらないよぉ～っ！": "止まらないよっ！",
    "意地悪したくなるなぁ": "意地悪したくなるな",
    "期待されると困るんだけどなぁ……": "期待されると困るんだけどね……",
    "押しつけないでよぉ……っ": "押しつけないでよ……っ",
    "ちゃんと感じてるんだから……ほら、こっちも見て": "ちゃんと感じてるんだから……ほら、こっちも見て",
    "困らせないでよ～っ！": "困らせないでよっ！",
    "動かないでよぉ。": "動かないでよ。",
    "変になっちゃうよ～っ！": "変になっちゃうよっ！",
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    start = text.index(";--- COM60 助手にキスさせる ---")
    end = text.index("\n@TRAIN_MESSAGE_B280_47", start)
    block = text[start:end]
    for old, new in REPLACEMENTS.items():
        count = block.count(old)
        if count != 1:
            raise SystemExit(f"expected one occurrence in CHAR47 additional block: {old!r} ({count})")
        block = block.replace(old, new, 1)
    text = text[:start] + block + text[end:]
    TARGET.write_bytes(text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
