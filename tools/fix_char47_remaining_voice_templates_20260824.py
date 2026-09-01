from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"

REPLACEMENTS = {
    '「ふふ～ん、%LOCALS%、もっとこっち来て。わたしが、奥まで可愛がってあげる。んっ、あぁ」': '「ふふ〜ん、%LOCALS%、もっとこっち来て。わたしが、奥までゆっくり触れるね。んっ、あぁ」',
    '「はぁ、んっ……。ふたなりのわたしを、君が可愛がってくれてる……。変な気分だけど……好き……」': '「はぁ、んっ……。ふたなりのわたしを、君がこんなふうにしてる……。変な気分だけど……好き……」',
    '「ん……今日は手も足も、わたしに預けて。ちゃんと様子を見ながら、ゆっくり可愛がってあげるね」': '「ん……今日は手も足も、わたしに預けて。様子を見ながら、ゆっくり触れてあげるね」',
    '「指先まで可愛がってあげる。君が嬉しそうにするから、やめられなくなるなぁ♪」': '「指先まで丁寧に触れてあげる。君が嬉しそうにするから、やめられなくなるね♪」',
    '「%LOCALS%が力を抜いてくれると、わたしまで嬉しくなるよ。今日は丁寧に可愛がってあげる♪」': '「%LOCALS%が力を抜いてくれると、わたしまで嬉しくなるよ。今日は丁寧に触れてあげる♪」',
}


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    for old, new in REPLACEMENTS.items():
        if text.count(old) != 1:
            raise SystemExit(f"expected one occurrence: {old!r}")
        text = text.replace(old, new, 1)
    lines = []
    for line in text.splitlines():
        if "PRINTFORM" in line:
            line = line.replace("可愛い", "かわいい")
        lines.append(line)
    result = "\n".join(lines) + ("\n" if text.endswith(("\n", "\r")) else "")
    TARGET.write_bytes(result.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
