from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_54_久坂あやめ_COM.ERB"

# 恋人側の既存文は保持し、完全一致していた通常側／通常A=2だけを置き換える。
REPLACEMENTS = {
    3039: (
        'PRINTFORMW 「んっ……道具越しでも、あんたの声が手に返ってくる。もっと乱れてみなさい♪」',
        'PRINTFORMW 「あら、もう手に力が入りすぎよ。そんなに慌てなくても、あたしがちゃんと可愛がってあげるわ♪」',
    ),
    3159: (
        'PRINTFORMW 「あっ……その目、近いわね。撮るなら、あたしから逸らさないでよ……♪」',
        'PRINTFORMW 「録画を始めるなら、ひと声かけてちょうだい？　あたしだって、いきなりはびっくりするんだから……♪」',
    ),
    3233: (
        'PRINTFORMW 「ん……そんなこと言わせて、あたしの顔を見てるの？　ふぅん、意地悪ね……♪」',
        'PRINTFORMW 「あやめ先生にそんなことを言わせるなんて、悪い生徒ね。……でも、ちゃんと聞いてなさいよ♪」',
    ),
    3517: (
        'PRINTFORMW 「あっ……その声、耳に残るじゃない。もう一度、あたしに言ってみなさいよ……♪」',
        'PRINTFORMW 「べつに、あんたの言葉なんか効いてないわよ？　……って言いたいのに、耳だけは正直なのね♪」',
    ),
    3566: (
        'PRINTFORMW 「や、やだ……っ。そんな目で見られたら、隠す暇もないじゃない……♪」',
        'PRINTFORMW 「ふふ、あたしのことをそんなに熱心に見つめて……。うさちゃんを眺めるときより、ずいぶん嬉しそうじゃない♪」',
    ),
    3622: (
        'PRINTFORMW 「ひゃっ……そこ、冷たい……。ふふ、あんたの顔まで熱くなってるわよ……♪」',
        'PRINTFORMW 「あたし、こういうのは初めてなのよ？　……ふふ、だからそんなに嬉しそうな顔をしないでちょうだい♪」',
    ),
    4044: (
        'PRINTFORMW 「ん……%LOCALS%の息が返ってくる。もう少しだけ、ゆっくり開かせてあげる♪」',
        'PRINTFORMW 「まぁ、そんなに身構えなくても大丈夫よ。あたし、かわいい子には優しいんだから♪」',
    ),
    4097: (
        'PRINTFORMW 「ふふ……そんなところを見せるのね。あたしから目を逸らしちゃだめよ……♪」',
        'PRINTFORMW 「まぁ、ずいぶん素直に見せてくれるのね。ふふ、そんな良い子には、あとでちゃんとご褒美をあげなくちゃ♪」',
    ),
}


def main() -> None:
    lines = TARGET.read_bytes().decode("cp932").splitlines()
    for line_number, (before, _after) in REPLACEMENTS.items():
        actual = lines[line_number - 1].strip()
        if actual != before:
            raise SystemExit(
                f"想定外の行内容: L{line_number}\n期待: {before}\n実際: {actual}"
            )
    for line_number, (_before, after) in REPLACEMENTS.items():
        indent = lines[line_number - 1][: len(lines[line_number - 1]) - len(lines[line_number - 1].lstrip())]
        lines[line_number - 1] = indent + after
    TARGET.write_bytes(("\r\n".join(lines) + "\r\n").encode("cp932"))
    print(f"updated {TARGET}: {len(REPLACEMENTS)} lines")


if __name__ == "__main__":
    main()
