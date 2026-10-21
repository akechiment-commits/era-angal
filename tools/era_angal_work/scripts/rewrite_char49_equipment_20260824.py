from pathlib import Path


TARGET = Path(r"C:\Users\guile\era-angal\ERB\CHAR\CHAR_49_小松ぼたん_COM.ERB")


# 各コマンドの「装着中／取り外し後」×「恋人／通常」×RAND3。
# ぼたんが道具を受けている視点を固定し、行為の説明ではなくその場の反応にする。
EQUIPMENT = {
    11: {
        "on": {
            "lover": (
                "「んっ……あ、振動が広がる……。転校生くん、そんなに嬉しそうに見ないでよ♪」",
                "「強さを変える指、見えてるよ……ふふ、次を待ってるわたし、ばれちゃった？」",
                "「まだ止めないで。身体がじんじんして、もう少しだけ甘やかされたいな」",
            ),
            "normal": (
                "「ひゃっ……なにこれ。身体の奥まで震えて、わたし、笑っていられないよ」",
                "「急に強くなると、声が追いつかない……。少しだけ、ゆっくりにしてね」",
                "「外すの？　……うん、落ち着くまで手を握っててくれる？」",
            ),
        },
        "off": {
            "lover": (
                "「外れても、まだじんじんする……。転校生くんの手で、ゆっくり戻してよ♪」",
                "「もう終わり？　ふふ、言わないつもりだったけど、少し名残惜しいな」",
                "「腰に力が戻らないや。ケーキを食べさせてくれたら、許してあげる」",
            ),
            "normal": (
                "「はぁ……やっと静かになった。身体がまだ追いかけてるみたい……」",
                "「もう十分だよ……でも、外してくれてありがと。少し恥ずかしかったから」",
                "「まだ熱が残ってるね。次は、始める前に教えてよね」",
            ),
        },
    },
    13: {
        "on": {
            "lover": (
                "「ひゃ……後ろ、来るんだね。怖いけど、転校生くんがゆっくりなら……」",
                "「押されるたびに、変なところまで熱くなる……。ふふ、見ないでよ」",
                "「もう少しだけ、手を握ってて。力が抜けても、笑わないでね」",
            ),
            "normal": (
                "「やっ……後ろはまだ、心の準備がないよ。急がないで……」",
                "「そこ、じんじんする……。痛くないように、わたしの顔を見てて」",
                "「ん……っ、もう無理そう。いったん止めて、落ち着かせてよね」",
            ),
        },
        "off": {
            "lover": (
                "「抜けても、後ろが熱い……。転校生くんに見られたこと、忘れられないね」",
                "「身体がまだ覚えてる。手を握ってくれたら、もう少し素直にできるかも」",
                "「今日はここまで？　ふふ、次はもう少し上手に甘えられそう♪」",
            ),
            "normal": (
                "「じんじんする……。外れたのに、まだそこだけ熱いよ」",
                "「もう今日は休ませて。続けるより、そばにいてくれるほうがいい」",
                "「次は始める前に声をかけてね。急に来ると、びっくりしちゃうから」",
            ),
        },
    },
    14: {
        "on": {
            "lover": (
                "「んっ……そこに触れられると、胸まできゅっとするね。転校生くん、わかってるなぁ♪」",
                "「小さな刺激なのに、ずっと気になっちゃう……。ふふ、外すのはまだだよ」",
                "「歩くたびに、そこだけ思い出しちゃう。こんなの、ずるいなぁ」",
            ),
            "normal": (
                "「ひゃっ……そこ、ずっと当たってるよ。声が変になったら、笑わないでね」",
                "「じっとしてても、ちくちくする……。わたし、どうしたらいいのかな」",
                "「んぅ……もう少し弱くできる？　気になって、何も考えられないよ」",
            ),
        },
        "off": {
            "lover": (
                "「外れても、そこだけ熱い……。転校生くんのいたずら、しばらく残りそうだね♪」",
                "「静かになったのに、身体はまだ待ってるみたい。もう、甘やかしすぎだよ」",
                "「ふふ、楽になったはずなのに、少し寂しいって思うのは内緒ね」",
            ),
            "normal": (
                "「はぁ……やっと楽になった。まだじんじんするけど、これで歩けるかな」",
                "「急に外れると、そこだけ取り残されたみたい……。少し待ってよね」",
                "「もう触らないでね。落ち着くまで、普通の顔に戻れそうにないから」",
            ),
        },
    },
    15: {
        "on": {
            "lover": (
                "「んっ……胸がつんってする。転校生くん、そんなに見つめたら恥ずかしいよ♪」",
                "「揺れるたびに、そこばかり気になっちゃう……。ふふ、責任取ってね」",
                "「外すまで、腕で隠しててもいい？　見られてると思うと、余計に熱くなるなぁ」",
            ),
            "normal": (
                "「ふえっ……なにつけたの？　ちょっと揺れただけで、声が出ちゃうよ」",
                "「胸がぴんってして、じっとしていられない……。そんなに見ないでね」",
                "「んぅ……歩くたびに当たるよ。わたし、こんなに敏感だったかなぁ」",
            ),
        },
        "off": {
            "lover": (
                "「あ……外れても、まだ胸がぴんとしてる。転校生くんのせいだからね♪」",
                "「少し軽くなったけど、熱は残ってるなぁ。今だけ、手で隠してくれる？」",
                "「ふふ、やっと普通に息ができる……でも、もう一回なんて言わないよ？」",
            ),
            "normal": (
                "「ねえ、もう外してよぉ……。このままだと、仕事のことなんて考えられないよ」",
                "「はぁ……やっと楽になった。外すところまで見られるの、やっぱり恥ずかしいね」",
                "「まだ胸がじんじんする。次は、つける前に教えてくれたら嬉しいな」",
            ),
        },
    },
    16: {
        "on": {
            "lover": (
                "「ひゃうっ……出てきちゃった。転校生くんに見られると、恥ずかしいのに隠せないね♪」",
                "「胸がきゅっとされるたび、身体までふわっとする……。もう少しだけ、見てて」",
                "「こんなにたくさんになるんだ……。ふふ、わたしのこと、困らせるの好きだね」",
            ),
            "normal": (
                "「ふえっ、これなぁに……？　胸から出てるよぉ。びっくりしちゃうから、ゆっくりね」",
                "「止まらない……っ。変な感じ、恥ずかしくて顔を見られないよ」",
                "「んっ、そんなに絞らないで……。胸が張って、息まで苦しくなりそう」",
            ),
        },
        "off": {
            "lover": (
                "「ぷはっ……はぁ。転校生くんの前だと、ほんとに隠せなくなるなぁ♪」",
                "「外れても胸が重いまま。少しだけ、そっと撫でてくれる？」",
                "「ふふ、すっきりした……。頑張ったご褒美、頭を撫でるだけでいいからね」",
            ),
            "normal": (
                "「も、もう十分だよぉ……。腰までふらふらで、立っていられないから」",
                "「はぁ……胸がまだ張ってる。水を飲んだら、少し落ち着くかな」",
                "「まだ出るからって、続けなくてもいいよね。今日はここまでにしよう？」",
            ),
        },
    },
    17: {
        "on": {
            "lover": (
                "「んっ……腰が勝手に跳ねる。こんなところ、転校生くんにだけは見せちゃうんだね♪」",
                "「道具なのに、触れられてるみたいに感じる……。もう少し近くにいてよ」",
                "「強くなると、声も身体も止まらないね。ふふ、変な顔してない？」",
            ),
            "normal": (
                "「ふえっ、やだ……腰がひとりでに動いちゃうよぉ！」",
                "「止めたいのに、力が入らない……。少しだけ弱くしてくれる？」",
                "「機械に負けてるみたいで悔しいのに、声が出ちゃう……」",
            ),
        },
        "off": {
            "lover": (
                "「外れても、身体がまだ追いかけちゃう……。ふふ、甘やかされすぎたかなぁ♪」",
                "「じんじんしたままだね。転校生くんの手で、ゆっくり落ち着かせてよ」",
                "「やっと静かになった……。でも、もう少しだけそばにいてほしいな」",
            ),
            "normal": (
                "「はぁ……もう限界だよぉ。小さいのに、こんなに力が抜けるなんて……」",
                "「やっと静かになった。まだふにゃふにゃだから、少し休ませてね」",
                "「止めてくれてありがと。次は、始める前に心の準備をさせてよね」",
            ),
        },
    },
}


def body_end(lines, start):
    for i in range(start + 1, len(lines)):
        s = lines[i].strip()
        if not s:
            continue
        if len(lines[i]) - len(lines[i].lstrip("\t")) == 0 and s.startswith("IF SELECTCOM =="):
            return i
    return len(lines)


def replace_branch(lines, start, end, speech):
    quote_indices = [
        i for i in range(start, end)
        if lines[i].lstrip("\t").startswith("PRINTFORMW ")
    ]
    if len(quote_indices) != 1:
        raise RuntimeError(f"branch quote count={len(quote_indices)} start={start} end={end}")
    i = quote_indices[0]
    indent = lines[i][:len(lines[i]) - len(lines[i].lstrip("\t"))]
    eol = "\r\n" if lines[i].endswith("\r\n") else "\n"
    lines[i] = indent + "PRINTFORMW " + speech + eol


def rewrite_branch_group(lines, marker_start, relation_end, speeches):
    markers = []
    for i in range(marker_start, relation_end):
        stripped = lines[i].strip()
        ind = len(lines[i]) - len(lines[i].lstrip("\t"))
        if ind == 3 and stripped in ("IF A == 0", "ELSEIF A == 1", "ELSE"):
            markers.append(i)
    if len(markers) != 3:
        raise RuntimeError(f"RAND3 markers={markers} start={marker_start}")
    bounds = [markers[0], markers[1], markers[2], relation_end]
    for speech, left, right in zip(speeches, bounds[:-1], bounds[1:]):
        replace_branch(lines, left + 1, right, speech)


def rewrite_state(lines, state_start, state_end, data):
    talent = []
    for i in range(state_start, state_end):
        stripped = lines[i].strip()
        ind = len(lines[i]) - len(lines[i].lstrip("\t"))
        if ind == 2 and stripped == "IF TALENT:TARGET:153":
            talent.append(i)
    if len(talent) != 1:
        raise RuntimeError(f"talent count={len(talent)} state={state_start}:{state_end}")
    talent_idx = talent[0]
    relation_else = None
    for i in range(talent_idx + 1, state_end):
        stripped = lines[i].strip()
        ind = len(lines[i]) - len(lines[i].lstrip("\t"))
        if ind == 2 and stripped == "ELSE":
            relation_else = i
            break
    if relation_else is None:
        raise RuntimeError(f"normal relation ELSE not found state={state_start}:{state_end}")
    rewrite_branch_group(lines, talent_idx + 1, relation_else, data["lover"])
    rewrite_branch_group(lines, relation_else + 1, state_end, data["normal"])


def rewrite_command(lines, com, data):
    command_idx = next(
        (i for i, line in enumerate(lines)
         if line.strip() == f"IF SELECTCOM == {com}"),
        None,
    )
    if command_idx is None:
        raise RuntimeError(f"COM{com} not found")
    command_end = body_end(lines, command_idx)
    tequip_idx = next(
        (i for i in range(command_idx + 1, command_end)
         if lines[i].strip() == f"IF TEQUIP:{com}"),
        None,
    )
    if tequip_idx is None:
        raise RuntimeError(f"TEQUIP:{com} not found")
    outer_else = next(
        (i for i in range(tequip_idx + 1, command_end)
         if lines[i].strip() == "ELSE"
         and len(lines[i]) - len(lines[i].lstrip("\t")) == 1),
        None,
    )
    if outer_else is None:
        raise RuntimeError(f"outer ELSE for COM{com} not found")
    rewrite_state(lines, tequip_idx + 1, outer_else, data["on"])
    rewrite_state(lines, outer_else + 1, command_end, data["off"])
    return 1


def main():
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    lines = text.splitlines(keepends=True)
    changed = 0
    for com, data in EQUIPMENT.items():
        changed += rewrite_command(lines, com, data)
    new_text = "".join(lines)
    TARGET.write_bytes(new_text.encode("cp932"))
    print(f"rewritten equipment commands: {changed}/6")
    print(f"bytes={TARGET.stat().st_size} CRLF={new_text.count(chr(13)+chr(10))}")


if __name__ == "__main__":
    main()
