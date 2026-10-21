from pathlib import Path
import re


PATH = Path(r"ERB/CHAR/CHAR_06_藍乃あいか_COM.ERB")


# Per equipment state: (恋人追加1, 恋人追加2, 通常追加1, 通常追加2).
EXTRA = {
    11: {
        "on": (
            "「んっ、揺れるたびに先輩のことを考えちゃう……。こんな道具でも、先輩となら物語にできますね♪」",
            "「震えが奥まで届く……。先輩、怖くないように手を握っていてください……」",
            "「ひゃっ、止めてくださいっ！　体のなかでずっと跳ねてる……うう、無理です～っ」",
            "「うう、わたし、平気なふりできません……。先輩、早く外して、息をさせてください……っ」",
        ),
        "off": (
            "「まだ身体が揺れてる気がします……。先輩の手が触れると、また寂しくなくなる……♪」",
            "「終わったのに、先輩の顔を見ると熱くなる……。続きって言ったら、困りますか？」",
            "「やっと外れた……。もう急に着けたり外したりしないでください、心臓に悪いです～っ」",
            "「膝に力が入らないです……。先輩、支えてほしいですけど、自分で立てるって言わないと……」",
        ),
    },
    13: {
        "on": (
            "「お尻の奥まで震えて……先輩に知られていくみたいで、恥ずかしいけど嬉しいです♪」",
            "「ん、ふるえるたびに、わたしの強がりがほどける……先輩、そばにいてください」",
            "「ひゃっ、そこは聞いてないです！　お尻は本当に弱いんです、止めてください～っ」",
            "「うう、走るどころか立てない……。こんなこと、わたしの本にも書けません……っ」",
        ),
        "off": (
            "「まだ奥がぞくぞくしてます……。先輩、こんな顔を見て笑わないでくださいね……」",
            "「外れても、触れられた感じが残ってる……。わたし、先輩に甘えすぎでしょうか」",
            "「ほっ……やっと取れた……。もう、お尻を勝手にいじめるのは禁止です～っ」",
            "「まだふるえてます……。先輩、責任って言っても、変な意味じゃなくて、ちゃんと心配してくださいね！」",
        ),
    },
    14: {
        "on": (
            "「クリがずっとじんじんして……。先輩のいじわる、嫌いになれないのが困ります……♪」",
            "「小さいところなのに、身体ぜんぶに響くんですね……。わたし、もう本を読めません」",
            "「ひゃうっ、そこばかりは駄目です！　変な声が出るから、先輩、止めてください～っ」",
            "「うう、集中できない……。わたしの弱いところを、そんなに狙わないでください……っ」",
        ),
        "off": (
            "「まだ脈打ってます……。先輩の手の記憶まで残るなんて、身体が正直すぎますね♪」",
            "「あぅ、もう少し続けてほしかったなんて……。わたし、今のは忘れてください……」",
            "「やっと外れた……。あんなにいじっておいて、急に知らんぷりはひどいです、先輩！」",
            "「まだ敏感なんですから、そっとしてください……。からかうの、しばらく禁止ですよ～っ」",
        ),
    },
    15: {
        "on": (
            "「カーディガンの下で乳首がきゅっとして……。先輩だけの秘密にしてくださいね♪」",
            "「見られると恥ずかしいのに、先輩が嬉しそうだと、わたしも満たされます……」",
            "「ひゃんっ、こんな声……誰かに聞かれたら、わたし、もう部室に来られません～っ」",
            "「うう、引っぱらないで……。痛くないように、もっと静かにしてください……っ」",
        ),
        "off": (
            "「外したのに、胸の先がまだきゅっとしてます……。先輩にだけ見せた余韻ですね……♪」",
            "「あぅ、平気な顔をしたいのに……先輩の前だと、すぐ素直になっちゃいます」",
            "「う、余韻が引かないです……。今日はもう、何も手につかないかも……」",
            "「もう見ないでください、こんなの恥ずかしすぎます……。先輩、あっち向いてて～っ」",
        ),
    },
    16: {
        "on": (
            "「乳首から出ちゃう……。先輩に見られてると、恥ずかしいのに満たされます……♪」",
            "「あたしの身体、先輩の前では言葉より正直です……。いっぱいになっていくの、見ててください」",
            "「やっ、出るわけ……って、嘘、出てる!?　先輩、見ないでください～っ」",
            "「ひゃっ、何ですかこれ！　わたし、そんなに出るなんて聞いてません……っ」",
        ),
        "off": (
            "「まだ胸がじんとしてます……。先輩のために出たと思うと、恥ずかしいけど嬉しい……♪」",
            "「外れても、身体が覚えてる……。先輩、もう少しそばにいてください」",
            "「はぁ……やっと終わった……。こんなの、誰にも見せないでくださいね！」",
            "「うう、まだ変な感じです……。もう搾乳器は練習メニューに入れないでほしいです～っ」",
        ),
    },
    17: {
        "on": (
            "「腰が勝手に揺れる……。先輩に見られてると、物語の女の子みたいです……♪」",
            "「ひとりで動くのに、先輩が見ていてくれると安心します……。もう少し、お願いします」",
            "「ひゃうっ、何これ……！　身体が言うことをきかないです、先輩、止めてください～っ」",
            "「うう、こんなの練習じゃないです！　わたし、ちゃんと歩けなくなっちゃいます……っ」",
        ),
        "off": (
            "「あぅ、こんなにとろとろにされて……。先輩、責任を取って、そばにいてくださいね♪」",
            "「終わっても身体が寂しがってる……。先輩の顔を見たら、また欲しくなっちゃいます……」",
            "「う、もう……先輩のばか。こんなにからかって……嫌いです、ううん、嘘ですけど……っ」",
            "「へろへろです……。次は、わたしがちゃんと動ける普通の練習にしてください～っ」",
        ),
    },
}


def relation_block(old_love: str, old_normal: str, additions: tuple[str, str, str, str], love_comment: str, normal_comment: str) -> str:
    love1, love2, normal1, normal2 = additions
    lines = [
        "\t\tIF TALENT:TARGET:153",
        "\t\t\tIF A == 0",
    ]
    if love_comment:
        lines.append(f"\t\t\t{love_comment.strip()}")
    lines.extend(
        [
            f"\t\t\t\tPRINTFORMW {old_love}",
            "\t\t\tELSEIF A == 1",
            f"\t\t\t\tPRINTFORMW {love1}",
            "\t\t\tELSE",
            f"\t\t\t\tPRINTFORMW {love2}",
            "\t\t\tENDIF",
            "\t\tELSE",
            "\t\t\tIF A == 0",
        ]
    )
    if normal_comment:
        lines.append(f"\t\t\t{normal_comment.strip()}")
    lines.extend(
        [
            f"\t\t\t\tPRINTFORMW {old_normal}",
            "\t\t\tELSEIF A == 1",
            f"\t\t\t\tPRINTFORMW {normal1}",
            "\t\t\tELSE",
            f"\t\t\t\tPRINTFORMW {normal2}",
            "\t\t\tENDIF",
            "\t\tENDIF",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    text = PATH.read_bytes().decode("cp932").replace("\r\n", "\n")
    for number, state_data in EXTRA.items():
        lines = text.splitlines()
        marker = f"IF SELECTCOM == {number}"
        start = next(i for i, line in enumerate(lines) if line == marker)
        end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("IF SELECTCOM == ") or lines[i] == "RETURN 0")
        block = "\n".join(lines[start:end])
        if "A = RAND:3" in block:
            continue

        state_header = re.compile(
            rf"(\t(?:IF TEQUIP:{number}|ELSE)\n(?:\t\t;[^\n]*\n)?)(?=\t\tIF TALENT:TARGET:153)"
        )
        block, count = state_header.subn(r"\1\t\tA = RAND:3\n", block, count=2)
        if count != 2:
            raise RuntimeError(f"COM{number}: state headers={count}")

        relation = re.compile(
            r"\t\tIF TALENT:TARGET:153\n"
            r"(?P<love_comment>\t\t\t;[^\n]*\n)?"
            r"\t\t\tPRINTFORMW (?P<love>[^\n]*)\n"
            r"\t\tELSE\n"
            r"(?P<normal_comment>\t\t\t;[^\n]*\n)?"
            r"\t\t\tPRINTFORMW (?P<normal>[^\n]*)\n"
            r"\t\tENDIF"
        )
        index = 0

        def replace(match: re.Match[str]) -> str:
            nonlocal index
            state = "on" if index == 0 else "off"
            index += 1
            return relation_block(
                match.group("love"),
                match.group("normal"),
                state_data[state],
                match.group("love_comment") or "",
                match.group("normal_comment") or "",
            )

        block, relation_count = relation.subn(replace, block, count=2)
        if relation_count != 2:
            raise RuntimeError(f"COM{number}: relation branches={relation_count}")
        text = "\n".join(lines[:start] + block.splitlines() + lines[end:])

    PATH.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print(f"CHAR06 equipment RAND3 added: {len(EXTRA)} commands")


if __name__ == "__main__":
    main()
