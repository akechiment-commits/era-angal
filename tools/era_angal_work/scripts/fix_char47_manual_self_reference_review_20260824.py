from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB" / "CHAR" / "CHAR_47_双葉みなづき_COM.ERB"


# Each pair was reviewed against its command context and the original voice.
# This is deliberately an exact full-line table: no token or regex replacement.
REPLACEMENTS = (
    (
        "「この問題？　あぁ、こうやって解くんだよ。……どう、わたし、頼りになるでしょ♪」",
        "「この問題？　あぁ、こうやって解くんだよ。……どう？　頼りになるでしょ♪」",
    ),
    (
        "「はぁ……ちゅ。……はぁ。ど、どきどきする……。わたしなのに、情けないなぁ……えへへ」",
        "「はぁ……ちゅ。……はぁ。ど、どきどきする……。先輩なのに、情けないなぁ……えへへ」",
    ),
    (
        "「あっ、ん。後ろから、なんて。わたし、けものみたいで、誰かに見られたら、恥ずかしいっ」",
        "「あっ、ん。後ろから、なんて。けものみたいになってる……誰かに見られたら、恥ずかしいっ」",
    ),
    (
        "「え、わたしが、上？　うにっ、こ、こんなとこで初めてで。あぁ、見つかったら。ふぇ、先輩なのに、わたわたしちゃう」",
        "「え、わたしが上？　うにっ、こ、こんなとこで初めてで。あぁ、見つかったら。ふぇ、先輩なのに、わたわたしちゃう」",
    ),
    (
        "「はぁ、んっ。こんなとこで奉仕されてるなんて、贅沢だなぁ。わたし、とろけちゃう？」",
        "「はぁ、んっ。こんなとこで奉仕されてるなんて、贅沢だなぁ。わたしまで、とろけちゃいそう……」",
    ),
    (
        "「書記席、狭いね……。君が近いと、わたしの余裕まで置く場所がなくなっちゃうよぉ」",
        "「書記席、狭いね……。君が近いと、先輩ぶってる余裕までなくなっちゃうよぉ」",
    ),
    (
        "「新妻ごっこ、わたしには少し早いよぉ。お茶を出すくらいから、ゆっくり練習しよっか」",
        "「新妻ごっこは、まだ少し早いよぉ。お茶を出すくらいから、ゆっくり練習しよっか」",
    ),
    (
        "「んっ……下からも、%LOCALS%の動きも……っ。転校生くん、二人分は、わたしには多いよ……♪」",
        "「んっ……下からも、%LOCALS%の動きも……っ。転校生くん、二人分は、さすがに多いよ……♪」",
    ),
)


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    for old, new in REPLACEMENTS:
        count = text.count(old)
        if count != 1:
            raise RuntimeError(f"expected exactly one occurrence ({count}): {old}")
        text = text.replace(old, new)
    TARGET.write_bytes(text.encode("cp932"))


if __name__ == "__main__":
    main()
