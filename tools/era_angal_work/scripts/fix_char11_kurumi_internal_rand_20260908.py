"""CHAR11くるみ自身のRAND枝内重複を解消する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ERB/CHAR/CHAR_11_氷野くるみ_COM.ERB"


REPLACEMENTS = {
    'PRINTFORMW 「%LOCALS%の先っぽ、わたしのとぴったり重なります～♪　んっ、同じところが一緒に熱くなりますね」':
        'PRINTFORMW 「先輩の先端が、わたしの内側を押すたび、ぴたりと重なって……あったかいです～♪」',
    'PRINTFORMW 「%LOCALS%の先っぽ、わたしのとぴったり重なります～♪　同じところが一緒に熱くなりますね」':
        'PRINTFORMW 「こんなに同じ場所を探し当てるなんて……先輩とわたし、身体の相性もばっちりですね～♪」',
    'PRINTFORMW 「あぁ～、ぜんぶ出ちゃいました……！　先輩の前だと、身体まで隠しごとができませんね～♪」':
        'PRINTFORMW 「あぁ～、いっぱい出ました……！　先輩の熱、まだわたしの中に残っていますよ～♪」',
    'PRINTFORMW 「ぜんぶ出ちゃいました……先輩の前だと、身体まで隠しごとができませんね～♪」':
        'PRINTFORMW 「身体の力が抜けちゃいました……先輩にこんなふうに甘やかされると、もう立てません～♪」',
    'PRINTFORMW 「んぅっ、%LOCALS%が揺れるたび、わたしの奥まで響きます～……♪　ちゃんと繋がってるんですね」':
        'PRINTFORMW 「んぅっ、先輩が動くたび、身体の奥がきゅっと掴まれます～……♪　もっと近くで感じたいです」',
    'PRINTFORMW 「%LOCALS%が揺れるたび、わたしの奥まで響きます～……ちゃんとつながってるんですね♪」':
        'PRINTFORMW 「%LOCALS%の揺れが、わたしの中を何度も撫でて……先輩のこと、全部受け止めてるみたいです～♪」',
}


def main() -> None:
    data = PATH.read_text(encoding="cp932")
    for old, new in REPLACEMENTS.items():
        count = data.count(old)
        if count != 1:
            raise RuntimeError(f"expected one occurrence, found {count}: {old}")
        data = data.replace(old, new)
    PATH.write_bytes(data.replace("\n", "\r\n").encode("cp932"))
    print(f"rewrote {len(REPLACEMENTS)} internal RAND branches")


if __name__ == "__main__":
    main()
