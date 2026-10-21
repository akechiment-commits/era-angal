"""CHAR26-37のCOM258「助手顔面騎乗」の視点を統一する。"""

from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
BACKUP_DIR = ROOT / "tools/backups/COM258_viewpoint_before_repair_20260810"


# 恋人A=1/A=2、通常A=1/A=2。A=0を含む6本を、
# 「対象キャラはPLAYERに騎乗」「助手はPLAYERの顔に跨る」構図で書き直す。
LINES: dict[int, tuple[list[str], list[str]]] = {
    26: (
        [
            "%LOCALS%があんたの顔にまたがっている間も、あんたの中であたしは腰を動かしてる……。二人分、ちゃんと受け止めなさいよ♪",
            "顔を塞ぐのは%LOCALS%、あんたの中にいるのはあたし。どっちの熱も逃がさないでよね……♪",
            "%LOCALS%があんたの顔で動くたび、下のあたしまで揺れる……っ。二人とも、あたしを置いていくなってば。",
        ],
        [
            "%LOCALS%、あんたの顔に乗るなら、苦しくないか先に聞きなさいよ。あたしも上で動くから、急に合わせないで。",
            "あたしはあんたの中にいるんだから、腰を勝手に突き上げないで。%LOCALS%も、顔から落ちないようにしなさいよ！",
            "上は%LOCALS%が顔、下はあたしがあんたの中……二人分なんて聞いてないわよ。加減しなさい！",
        ],
    ),
    27: (
        [
            "%LOCALS%があんたの顔に跨っていても、わたしはあんたの中で動いている。二人とも、わたしを置いていくな……♪",
            "顔を覆う%LOCALS%と、あんたの中にいるわたし。見えなくても、腰でちゃんと返事をしろ……♪",
            "%LOCALS%が顔の上で揺れるたび、わたしの脚まで震える。……二人分を相手にするなら、最後まで支えろ。",
        ],
        [
            "%LOCALS%、あんたの顔に乗るなら、勝手に動くな。わたしもあんたの中にいる、息を合わせろ。",
            "わたしが上で動いているのに、下から急に押すな……。%LOCALS%も、顔を塞ぐなら加減しろ。",
            "顔の上は%LOCALS%、あんたの中はわたしだ。二人同時は聞いていない……でも、降りるとは言っていない。",
        ],
    ),
    28: (
        [
            "%LOCALS%が転校生くんの顔に跨って、うちは転校生くんの中で腰を動かしてるん……。二人とも、うちを置いていかんといて♪",
            "顔を隠してるんは%LOCALS%、奥で揺れてるんはうち。転校生くん、どっちの熱もちゃんと感じてや♪",
            "%LOCALS%が顔の上で動くたび、うちの腰まで跳ねるやん……っ。三人で息を合わせるん、難しすぎるわぁ♪",
        ],
        [
            "%LOCALS%、転校生くんの顔に乗るんやったら、苦しくないか聞いたって。うちも上で動くから、急にせんといてな！",
            "うちは転校生くんの中におるんやから、下から急に来たらびっくりするやん！　%LOCALS%も顔から落ちんようにしてや！",
            "顔の上は%LOCALS%、中で動くんはうち……二人分いっぺんは無理やって！　転校生くん、ちょっと加減してな！",
        ],
    ),
    29: (
        [
            "%LOCALS%が転校生くんのお顔にまたがって、あたしは転校生くんの中で動いてるんですねーっ……！　二人とも、置いていかないでくださいよーっ♪",
            "お顔を塞いでるのは%LOCALS%、あたしがいるのは転校生くんの中ですーっ。どっちの熱も、ちゃんと受け止めてくださいねーっ♪",
            "%LOCALS%がお顔の上で揺れるたび、あたしの腰まで動いちゃいますーっ……！　三人ぶん、息を合わせるの大変ですよーっ！",
        ],
        [
            "%LOCALS%、転校生くんのお顔に乗るなら、苦しくないか聞いてくださいねーっ。あたしも上で動きますから、急に合わせないでくださいよーっ！",
            "あたしは転校生くんの中にいるんですから、下から急に動かないでくださいーっ！　%LOCALS%も、お顔から落ちないでくださいねーっ！",
            "お顔の上は%LOCALS%、中で動くのはあたしですーっ……二人ぶんなんて聞いてませんよーっ！　ちゃんと加減してくださいーっ！",
        ],
    ),
    30: (
        [
            "%LOCALS%が転校生くんの顔に乗っている間、わたしは転校生くんの中で腰を動かしていますねぇ……。二人とも、置いていかないでくださいよぉ♪",
            "顔を塞いでいるのは%LOCALS%、中で揺れているのはわたしですぅ。転校生くん、どちらの動きも受け止めてくださいねぇ♪",
            "%LOCALS%が顔の上で動くと、その揺れがわたしの腰まで伝わりますねぇ……。三人で合わせるのは、思ったより忙しいですよぉ♪",
        ],
        [
            "%LOCALS%が転校生くんの顔に乗るなら、苦しくないか確認してくださいねぇ。わたしも上で動きますから、急には動かないでくださいよぉ！",
            "わたしは転校生くんの中にいるんですから、下から勝手に動かないでくださいねぇ。%LOCALS%も、顔から落ちないようにしてくださいよぉ！",
            "顔の上は%LOCALS%、中で動くのはわたしですぅ……二人分なんて聞いていませんよぉ。加減くらいしてくださいねぇ！",
        ],
    ),
    31: (
        [
            "%LOCALS%が転校生さんのお顔に跨って、わたくしは転校生さんの中で騎乗しております……。どうか、二人ともお支えくださいませ♪",
            "お顔を覆っているのは%LOCALS%、転校生さんの中で動いているのはわたくしです。見えなくても、どうぞ両方を感じてくださいませ♪",
            "%LOCALS%がお顔の上で揺れるたび、わたくしの腰まで揺れてしまいます……。三人で息を合わせるのは、なかなか難しゅうございますね♪",
        ],
        [
            "%LOCALS%が転校生さんのお顔に乗るのでしたら、苦しくないかお尋ねくださいませ。わたくしも上で動きますから、急がないでくださいね。",
            "わたくしは転校生さんの中におりますから、下から急に動かないでくださいませ。%LOCALS%も、お顔から落ちないようになさって。",
            "お顔の上は%LOCALS%、中で動くのはわたくしです……二人分とは伺っておりません。どうか、丁寧にお願いいたします。",
        ],
    ),
    32: (
        [
            "%LOCALS%があんたの顔にまたがって、あたしはあんたの中で騎乗してる。上も下も、ちゃんと感じてね♪",
            "あんたの顔を塞いでるのは%LOCALS%、あんたの中で腰を動かしてるのはあたし。二人分、まとめて受け止めてよ♪",
            "%LOCALS%が顔の上で動くたび、あたしの身体まで跳ねる……。あんた、どっちかだけに夢中にならないでね。",
        ],
        [
            "%LOCALS%、あんたの顔に乗るなら、苦しくないか聞いて。あたしも上で動くから、急に動かないでよね。",
            "あたしはあんたの中にいるんだから、下から勝手に動かさない。%LOCALS%も、顔から落ちないように合わせて。",
            "顔の上は%LOCALS%、中で動くのはあたし……二人分を同時に受けるのは大変だよね。みんなで無理しないで。",
        ],
    ),
    33: (
        [
            "%LOCALS%が転校生の顔にまたがって、ウチは転校生の中で腰を動かしとる……。二人とも、ウチを置いてくなや♪",
            "顔を塞いどるんは%LOCALS%、転校生の中におるんはウチや。見えんでも、どっちの熱も感じぃや♪",
            "%LOCALS%が顔の上で動くたび、ウチの腰まで揺れるんや……。三人で合わせるん、思ったより忙しいな♪",
        ],
        [
            "%LOCALS%が転校生の顔に乗るんやったら、苦しくないか聞きぃや。ウチも上で動くから、急には動くなよ！",
            "ウチは転校生の中におるんやから、下から勝手に突き上げるなや。%LOCALS%も、顔から落ちんように合わせぇ！",
            "顔の上は%LOCALS%、中で動くんはウチ……二人分とは聞いてへんで。転校生、ちゃんと加減しいや！",
        ],
    ),
    34: (
        [
            "%LOCALS%が転校生くんのお顔にまたがって、かいりは転校生くんの中で騎乗していますの……。二人とも、置いていかないでくださいまし♪",
            "お顔を塞いでいるのは%LOCALS%、転校生くんの中で動いているのはかいりですの。どちらの熱も、ちゃんと受け止めてくださいまし♪",
            "%LOCALS%がお顔の上で揺れるたび、かいりの腰まで揺れてしまいますの……。三人で合わせるのは大変ですのね♪",
        ],
        [
            "%LOCALS%が転校生くんのお顔に乗るなら、苦しくないか聞いてくださいまし。かいりも上で動きますから、急には動かないでくださいましね！",
            "かいりは転校生くんの中におりますから、下から勝手に動かさないでくださいまし。%LOCALS%も、お顔から落ちないように合わせてくださいまし！",
            "お顔の上は%LOCALS%、中で動くのはかいりですの……二人分だなんて聞いてませんのっ。どうか加減してくださいまし！",
        ],
    ),
    35: (
        [
            "%LOCALS%があんたの顔にまたがって、あたしはあんたの中で騎乗してる……。二人とも、あたしを置いてくなよね♪",
            "あんたの顔を塞いでるのは%LOCALS%、あんたの中で動いてるのはあたし。上も下も、ちゃんと受け止めなさいよ♪",
            "%LOCALS%が顔の上で揺れるたび、あたしの腰まで跳ねる……。三人で合わせるなんて、忙しすぎるでしょ♪",
        ],
        [
            "%LOCALS%があんたの顔に乗るなら、苦しくないか確認しなさいよ。あたしも上で動くから、急に合わせるんじゃないわよ！",
            "あたしはあんたの中にいるんだから、下から勝手に動かさない。%LOCALS%も、顔から落ちないようにしなさいよね！",
            "顔の上は%LOCALS%、中で動くのはあたし……二人分なんて聞いてないっ。ちゃんと加減しなさいよ！",
        ],
    ),
    36: (
        [
            "%LOCALS%がヘルプマンの顔にまたがって、わたしはヘルプマンの中で騎乗してますよぉ……。二人とも、置いていかないでくださいねぇ♪",
            "ヘルプマンの顔を塞いでるのは%LOCALS%、中で動いてるのはわたしですぅ。上も下も、ちゃんと感じてくださいねぇ♪",
            "%LOCALS%が顔の上で動くたび、わたしの腰まで揺れますよぉ……。三人で合わせるの、思ったより忙しいですねぇ♪",
        ],
        [
            "%LOCALS%がヘルプマンの顔に乗るなら、苦しくないか聞いてくださいねぇ。わたしも上で動くから、急には動かないでくださいよぉ！",
            "わたしはヘルプマンの中にいるんですから、下から勝手に動かさないでくださいねぇ。%LOCALS%も、顔から落ちないように合わせてくださいよぉ！",
            "顔の上は%LOCALS%、中で動くのはわたしですぅ……二人分なんて聞いてないですよぉ。ちゃんと加減してくださいねぇ！",
        ],
    ),
    37: (
        [
            "%LOCALS%が転校生の顔にまたがって、ワタシは転校生の中で騎乗しているアル……。二人とも、ワタシを支えるアル♪",
            "転校生の顔を塞いでいるのは%LOCALS%、転校生の中で腰を動かしているのはワタシアル。上も下も、ちゃんと受け止めるアルよ♪",
            "%LOCALS%が顔の上で動くたび、ワタシの腰まで揺れるアルね……。三人で息を合わせるのは、思ったより大変アル♪",
        ],
        [
            "%LOCALS%が転校生の顔に乗るなら、苦しくないか聞くアルよ。ワタシも上で動くから、急には合わせないアルね！",
            "ワタシは転校生の中にいるんだから、下から勝手に動かさないアル。%LOCALS%も、顔から落ちないようにするアルよ！",
            "顔の上は%LOCALS%、中で動くのはワタシ……二人分なんて聞いてないアル！　転校生、ちゃんと加減するアルね！",
        ],
    ),
}


def matching_endif(lines: list[str], start: int) -> int:
    depth = 0
    for i in range(start, len(lines)):
        token = lines[i].strip().split(" ", 1)[0] if lines[i].strip() else ""
        if token == "IF":
            depth += 1
        elif token == "ENDIF":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError(f"COM258のENDIFが見つかりません: {start}")


def repair_file(path: Path, character: int) -> None:
    raw = path.read_bytes()
    text = raw.decode("cp932").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    starts = [i for i, line in enumerate(lines) if re.match(r"\s*(?:IF|ELSEIF) SELECTCOM == 258\s*$", line)]
    if not starts:
        raise ValueError(f"{path.name}: COM258がありません")
    start = starts[-1]
    end = matching_endif(lines, start)
    talent_start = next(i for i in range(start, end + 1) if lines[i].strip() == "IF TALENT:TARGET:85" or lines[i].strip() == "IF TALENT:TARGET:153")
    talent_end = matching_endif(lines, talent_start)
    talent_indent = len(lines[talent_start]) - len(lines[talent_start].lstrip("\t "))
    talent_else = next(
        i
        for i in range(talent_start + 1, talent_end)
        if lines[i].strip() == "ELSE"
        and len(lines[i]) - len(lines[i].lstrip("\t ")) == talent_indent
    )
    love_indices = [i for i in range(talent_start + 1, talent_else) if lines[i].strip().startswith("PRINTFORM")]
    normal_indices = [i for i in range(talent_else + 1, talent_end) if lines[i].strip().startswith("PRINTFORM")]
    if len(love_indices) != 3 or len(normal_indices) != 3:
        raise ValueError(f"{path.name}: COM258の台詞本数が想定外です love={love_indices} normal={normal_indices}")
    love, normal = LINES[character]
    for indexes, values in ((love_indices, love), (normal_indices, normal)):
        for index, value in zip(indexes, values):
            indent = lines[index][: len(lines[index]) - len(lines[index].lstrip("\t "))]
            lines[index] = f'{indent}PRINTFORMW 「{value}」'
    comment = "\t; 視点：対象キャラは転校生に騎乗し、助手は転校生の顔に跨る"
    if comment.strip() not in text:
        lines.insert(start + 1, comment)
    updated = "\n".join(lines).rstrip("\n") + "\n"
    encoded = updated.encode("cp932")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / path.name
    if not backup.exists():
        backup.write_bytes(raw)
    path.write_bytes(encoded.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n"))


def main() -> None:
    for character in range(26, 38):
        paths = list((ROOT / "ERB/CHAR").glob(f"CHAR_{character:02d}_*_COM.ERB"))
        if not paths:
            raise FileNotFoundError(f"CHAR{character}のCOMファイルがありません")
        repair_file(paths[0], character)
    print("CHAR26-37 COM258の視点を統一しました。")


if __name__ == "__main__":
    main()
