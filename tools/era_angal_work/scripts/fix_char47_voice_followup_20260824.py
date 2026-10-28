from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"

REPLACEMENTS = {
    "「ん、あ……っ。二人分は、さすがに頭が追いつかないな。%LOCALS%、いったん息を合わせよ？」": "「ん、あ……っ。ちょっと待って、早いよ。%LOCALS%、わたしの息に合わせてね」",
    "「ひゃわわっ……っ、待って。気持ちいいのが重なると、どっちが自分のかわからなくなるね」": "「ひゃわわわっ!?　待って。気持ちいいのが重なると、自分の声までわからなくなるね」",
    "「うにっ……いまの、%LOCALS%？　びっくりしただけだからね。ふたりで同じものを感じるの、変な気分だな」": "「うにっ……%LOCALS%？　ごめん、いまの声、忘れて。こんなに近いと、変な気分になるね」",
    "「えっ、わたしの胸から？　あんまり期待されるようなものじゃないよ。……って、もう飲んでるんだね」": "「えっ、わたしの胸から？　これで足りるのかな。……って、もう飲んでるんだね」",
    "「あっ、強いよ……っ。胸は大きくないんだから、そんなに頑張らなくても……」": "「あっ、強いよ……っ。そんなに頑張られると、くすぐったくて、どこを見ればいいかわからなくなるな」",
    "「んっ、あ……っ。奥まで響く……。お姉さんだって言ってたのに、もう声が隠せないね」": "「んっ、あ……っ。奥まで響く……。お姉さんだよって言ってたのに、もう声が隠せないね」",
    "「ひゃっ……胸の先が触れると、こんなになるんだ。%LOCALS%、もう少しだけ、このままでいよ」": "「ひゃっ……っ、胸の先、そこに当たってる。%LOCALS%、もう少しだけ、このままでいよ」",
    "「うにっ？　%LOCALS%と胸を合わせるの？　わたし、あんまり大きくないけど、それでもいいのかな」": "「うにっ？　%LOCALS%と胸を合わせるの？　近いね……わたし、どんな顔をしてればいいのかな」",
    "「%LOCALS%ばかり見ないで……っ。わたしのことも、ちゃんと感じてるって声にして」": "「%LOCALS%ばかり見ないで……っ。わたしのことも忘れないで、こっちを見てよ」",
    "「ひゃわわっ!?　わたしが上なの？　%LOCALS%まで顔の上って、転校生くん、急すぎるよ……っ」": "「ひゃわわわっ!?　わたしが上なの？　%LOCALS%まで顔の上って、転校生くん、急すぎるよ……っ」",
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
