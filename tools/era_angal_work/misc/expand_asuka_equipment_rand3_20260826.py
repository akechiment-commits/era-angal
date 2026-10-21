from pathlib import Path
import re


PATH = Path(r"ERB/CHAR/CHAR_05_桃智あすか_COM.ERB")


# Each tuple is (恋慕追加1, 恋慕追加2, 非恋慕追加1, 非恋慕追加2).
# A=0 remains the existing line in the character file; the four additions
# are written separately for the two equipment states.
EXTRA = {
    11: {
        "on": (
            "「う、うにに……っ、揺れるたびに、先輩のことばっかり考えちゃうっす……。このまま、そばにいてほしいっす♪」",
            "「あたし、こんな道具にも負けないっす……たぶん。先輩が見ててくれるなら、もっと頑張れるっすよ」",
            "「せ、先輩っ、これ止めてほしいっす～っ! 体の中でずっと跳ねてるっすよ～っ!?」",
            "「うににっ、揺らすたびに変なとこまで響くっす! からかってないで、ちゃんと外してほしいっす～っ!」",
        ),
        "off": (
            "「ふぅ……先輩の手、あったかいっす……。どきどき、まだ残ってるっすけど、そばにいてくれるなら平気っす」",
            "「終わったのに、先輩の顔を見るとまた熱くなるっす……。あたし、ほんと先輩のこと好きっすね……えへへ」",
            "「はぁ……っ、やっと外れたっす……! もう、急に着けたり外したりするの禁止っすよ、先輩～っ!」",
            "「うにに……まだ体が揺れてる気がするっす……。先輩、次からはもっと普通の練習にしてほしいっす～っ!」",
        ),
    },
    13: {
        "on": (
            "「お尻の奥まで、先輩に覚えられちゃうみたいっす……。へ、変な感じっすけど、先輩になら任せてもいいっすよ……♪」",
            "「んぅ……っ、これが動くたびに先輩の顔が浮かぶっす……。あたし、ちゃんと耐えてるから、見ててほしいっす」",
            "「ひゃあっ、そこはバスケで使うとこじゃないっすよ～っ! 先輩、冗談なら早くやめてほしいっす～っ!」",
            "「うににっ、変なところを勝手に揺らさないでほしいっす! あたし、走るどころじゃなくなっちゃうっすよ～っ!?」",
        ),
        "off": (
            "「あぅ……っ。まだ奥がきゅってしてるっす……。先輩の前でこんなになっちゃうの、恥ずかしいっすよ……」",
            "「外れても、先輩に触られた感じが残ってるっす……。あたし、先輩のこと、もっと近くに感じたいっす……」",
            "「はぁっ……や、やっと取れたっす! もうお尻を変にいじるのは、なしにしてほしいっすよ～っ!」",
            "「まだむずむずするっす……。先輩、これであたしが変になったら、ちゃんと責任取ってほしいっす～っ!」",
        ),
    },
    14: {
        "on": (
            "「クリをずっとくすぐられてるみたいで、力が抜けちゃうっす……。先輩、もう少しだけ、このままにしてほしいっす♪」",
            "「んっ、そこ、先輩に触られるとすぐ反応しちゃうっす……。あたしの弱いとこ、ぜんぶ知ってるみたいっすね……」",
            "「ひゃっ、そこはだめっすってば～っ! 変な声が出るから、先輩、早く外してほしいっす～っ!」",
            "「うににっ、そんなとこばっかり狙うの、反則っすよ! あたし、もうまともに立てないっす～っ!?」",
        ),
        "off": (
            "「あぅ……っ、まだひくひくしてるっす……。先輩のせいで、体がすっかり素直になっちゃったっすよ……」",
            "「ものたりないなんて言ったら、先輩、また意地悪するっすよね……。でも、もう少しだけ甘えてもいいっすか……♪」",
            "「は、はぁ……っ、やっと外れたっす……。敏感にしすぎっすよ、先輩～っ!」",
            "「うぅ、まだそこが変な感じするっす……。しばらく、からかうのは禁止っすからね～っ!」",
        ),
    },
    15: {
        "on": (
            "「乳首まで先輩に見られて、つんってしてるっす……。恥ずかしいけど、先輩になら見せてもいいっすよ……♪」",
            "「ん、んっ……先輩が触ると、ここだけ熱くなるっす……。あたし、もっと可愛くなれてるっすか……?」",
            "「ふぇっ、な、なにするんすか先輩～っ! へ、変な声が出るから、もうやめてほしいっす～っ!」",
            "「うににっ、そんなに引っぱったら痛いっすよ! あたしをおもちゃにしないでほしいっす～っ!」",
        ),
        "off": (
            "「まだつんってしてるっす……。先輩の前でこんなに意識しちゃうの、あたしだけっすか……?」",
            "「外したのに、胸の奥までどきどきしてるっす……。先輩、ちゃんと最後までそばにいてほしいっす」",
            "「あ、ぅ……もう、やっと取れたっすよ～っ! これ以上、変なとこを見ないでほしいっす～っ!」",
            "「はぁ……っ、まだ変な感じが残ってるっす……。先輩、次はもっと普通に話すだけにするっすよ～っ!」",
        ),
    },
    16: {
        "on": (
            "「ん、ぁ……乳首からじゅわって出ちゃうっす……。先輩が見ててくれると、もっと頑張れそうっす♪」",
            "「あたしのが、先輩のためにいっぱいになってくっす……。こんな顔、先輩にしか見せないっすからね」",
            "「ひぃっ、な、なんすかこれ～っ! あたし、そんなに出るわけないっすよ……って、うそぉ!?」",
            "「うににっ、勝手に吸わないでほしいっす～っ! もう胸が変になっちゃうっすよ、先輩～っ!」",
        ),
        "off": (
            "「まだ胸がじんとしてるっす……。先輩に見られながらだと、あたし、すぐ熱くなっちゃうっすね……」",
            "「あぅ……っ、先輩のために出たって思うと、恥ずかしいけど嬉しいっす……。えへへ♪」",
            "「は、はぁ……っ、もう見ちゃやだっす～っ! こんなの、あたし、どうしたらいいっすか～っ!」",
            "「うぅ、胸がまだへんな感じっす……。先輩、搾乳器はもう練習メニューに入れないでほしいっす～っ!」",
        ),
    },
    17: {
        "on": (
            "「ん、ぁ……こ、こんなところまで先輩に預けるの、どきどきするっす……。あたし、先輩にならいいっすよ……♪」",
            "「ふわふわして、変に力が抜けるっす……。先輩が見ててくれるなら、あたし、もっと耐えてみせるっす」",
            "「うひゃっ!? な、なんすかこれ～っ……! こ、こんなの、あたしに使うなんて聞いてないっすよ～っ!」",
            "「うににっ、こんなので練習できるわけないっす! 先輩、からかってないで、早く外してほしいっす～っ!」",
        ),
        "off": (
            "「あぅ……っ、まだうずうずしてるっす……。先輩に触られたとこ、ぜんぶ覚えてるみたいっすよ……」",
            "「もう終わりなのに、先輩の顔を見るとまた熱くなるっす……。あたし、先輩のこと好きすぎるっすね……えへへ」",
            "「はぁ……っ、やっと取れたっす! もう、いじわるな道具はナシにしてほしいっすよ～っ!」",
            "「へろへろっす……。先輩、次はあたしがちゃんと動ける練習にしてほしいっす～っ!」",
        ),
    },
}


def rand_branch(old_love: str, old_normal: str, additions: tuple[str, str, str, str]) -> str:
    love1, love2, normal1, normal2 = additions
    return "\n".join(
        [
            "\t\tIF TALENT:TARGET:153",
            "\t\t\tIF A == 0",
            f"\t\t\t\tPRINTFORMW {old_love}",
            "\t\t\tELSEIF A == 1",
            f"\t\t\t\tPRINTFORMW {love1}",
            "\t\t\tELSE",
            f"\t\t\t\tPRINTFORMW {love2}",
            "\t\t\tENDIF",
            "\t\tELSE",
            "\t\t\tIF A == 0",
            f"\t\t\t\tPRINTFORMW {old_normal}",
            "\t\t\tELSEIF A == 1",
            f"\t\t\t\tPRINTFORMW {normal1}",
            "\t\t\tELSE",
            f"\t\t\t\tPRINTFORMW {normal2}",
            "\t\t\tENDIF",
            "\t\tENDIF",
        ]
    )


def expand_block(block: str, number: int) -> str:
    state_header = re.compile(
        rf"(\t(?:IF TEQUIP:{number}|ELSE)\r?\n(?:\t\t;[^\r\n]*\r?\n)?)(?=\t\tIF TALENT:TARGET:153)"
    )
    block, state_count = state_header.subn(r"\1\t\tA = RAND:3\n", block, count=2)
    if state_count != 2:
        raise RuntimeError(f"COM{number}: state headers found={state_count}")

    relation = re.compile(
        r"\t\tIF TALENT:TARGET:153\r?\n"
        r"\t\t\tPRINTFORMW (?P<love>[^\r\n]*)\r?\n"
        r"\t\tELSE\r?\n"
        r"\t\t\tPRINTFORMW (?P<normal>[^\r\n]*)\r?\n"
        r"\t\tENDIF"
    )
    additions = EXTRA[number]
    index = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal index
        state = "on" if index == 0 else "off"
        index += 1
        return rand_branch(match.group("love"), match.group("normal"), additions[state])

    block, relation_count = relation.subn(replace, block, count=2)
    if relation_count != 2 or index != 2:
        raise RuntimeError(f"COM{number}: relation branches found={relation_count}")
    return block


def main() -> None:
    text = PATH.read_bytes().decode("cp932")
    text = text.replace("\r\n", "\n")
    for number in EXTRA:
        pattern = re.compile(
            rf"(?P<block>;--- COM{number}[^\n]*\n"
            rf"IF SELECTCOM == {number}\n.*?)(?=\n;--- COM|\nRETURN 0)",
            re.DOTALL,
        )
        match = pattern.search(text)
        if not match:
            raise RuntimeError(f"COM{number}: block not found")
        expanded = expand_block(match.group("block"), number)
        text = text[: match.start()] + expanded + text[match.end() :]

    PATH.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print(f"expanded equipment RAND3: {len(EXTRA)} commands")


if __name__ == "__main__":
    main()
