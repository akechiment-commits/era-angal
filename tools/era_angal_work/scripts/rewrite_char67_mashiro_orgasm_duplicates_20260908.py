"""CHAR67ましろの絶頂条件間に重複している36枝を分離する。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB"


REPLACEMENTS = {
    'PRINTFORMW 「あっ、そこは団長の好きなところだ。覚えておけよ、恋人くん♪」': 'PRINTFORMW 「あっ……そこを押されると、団長の声も作戦も飛んでいく……恋人くん、もう一度来い♪」',
    'PRINTFORMW 「はうう、こんな場所まで覚えてしまうのか……もう少し、そばにいてくれ」': 'PRINTFORMW 「はうう……こんな場所まで届くんだな……。もう少しだけ、そばにいてくれよ」',
    'PRINTFORMW 「はうう、今の声、忘れるなよ。私も忘れないから……」': 'PRINTFORMW 「はうう……今の声は、応援じゃなくて本音だ……。忘れるなよ、恋人くん……」',
    'PRINTFORMW 「はうう、変な場所なのに次を待ってる……団長、鍛えられすぎではないか？」': 'PRINTFORMW 「はうう……変な場所ほど、次を待つ自分が悔しいぞ……。団長、まだまだ鍛えられるな……」',
    'PRINTFORMW 「は、ひ、お尻の奥がじんじんする……！」': 'PRINTFORMW 「は、ひっ……っ、お尻の奥が波打ってる……！　きみ、そこから離れるな……！」',
    'PRINTFORMW 「は、ひ、ゆっくりなのに奥まで届くのか……声を抑えられないぞ！」': 'PRINTFORMW 「は、ひっ……ゆっくりなのに、奥から頭まで突き抜ける……。声を抑える応援、誰か教えてくれ……！」',
    'PRINTFORMW 「ひゃっ、中がじんってする……！」': 'PRINTFORMW 「ひゃっ……中がきゅうっと締まる……！　そこ、もっと確認してくれ……！」',
    'PRINTFORMW 「ひゃっ、奥が熱いっ！　うう、身体の中まで揺れてるぞ……！」': 'PRINTFORMW 「ひゃっ……奥から全身にびりびり来るっ！　きみ、今のは強烈すぎるぞ……！」',
    'PRINTFORMW 「ひゃっ、後ろが変に熱い……！」': 'PRINTFORMW 「ひゃっ……後ろの熱が抜けない……っ。私の腰、勝手に逃げるな……！」',
    'PRINTFORMW 「ひゃっ、後ろが熱い！？　うう、奥までびりびりするぞ……！」': 'PRINTFORMW 「ひゃっ……後ろから押し上げられる……！　きみ、奥まで震わせる気か……！」',
    'PRINTFORMW 「ふぁ……おまえの熱が残っていくぞ☆」': 'PRINTFORMW 「ふぁ……っ、熱がずっと残ってる……。転校生くん、次の応援も頼むぞ☆」',
    'PRINTFORMW 「ふぁ……お尻がきゅっと返事してる。団長、正直すぎるぞ☆」': 'PRINTFORMW 「ふぁ……お尻が勝手に返事する……っ。団長の身体、素直すぎて困るぞ♪」',
    'PRINTFORMW 「ふぁ……こんなところで身体が勝手に締まるとは、団長も知らなかった……」': 'PRINTFORMW 「ふぁ……っ、身体が締まるたび、チアの掛け声まで忘れる……。団長、どうしたんだ……」',
    'PRINTFORMW 「ふぁ……こんな声を出すつもりではなかったのに、団長失格だな」': 'PRINTFORMW 「ふぁ……っ、こんな声、応援席では絶対に出せない……。団長失格じゃなくて、秘密にしてくれ……」',
    'PRINTFORMW 「ふぁ……まだ慣れてないのに、次を待ってる。変だぞ転校生くん……」': 'PRINTFORMW 「ふぁ……まだ慣れてないのに、身体が先に次を欲しがる……。変なのは転校生くんのせいだぞ……」',
    'PRINTFORMW 「ふぁ……まだ慣れないのに、待ってしまうのは困ったな……」': 'PRINTFORMW 「ふぁ……まだ何も分からないのに、待つほうが長く感じる……。これも団長の根性か……」',
    'PRINTFORMW 「ふぁ……力を抜きたいのに、きゅっと締まる。お尻まで応援に参加してるぞ☆」': 'PRINTFORMW 「ふぁ……力を抜くほど、奥がきゅっと締まる……。お尻まで全力応援とは、私も驚いたぞ☆」',
    'PRINTFORMW 「ふぁ……変なのに、次を待つのはどうしてだ転校生くん……」': 'PRINTFORMW 「ふぁ……変な場所なのに、次の刺激を探してしまう……。きみ、これが団長の中毒性か……？」',
    'PRINTFORMW 「ふぁ……深いところで跳ねた。団長、もう強がる旗を振れないな☆」': 'PRINTFORMW 「ふぁ……っ、深いところで跳ねると、旗どころか腕まで上がらない……。恋人くん、支えてくれ☆」',
    'PRINTFORMW 「ふぁ……背中まで震えるぞ。後ろからの応援、ずいぶん効くな☆」': 'PRINTFORMW 「ふぁ……背中から震えが広がる……。後ろからの応援、想像以上に効くな……！」',
    'PRINTFORMW 「ふぁ……腰が小さく跳ねるたび、もっと近づきたくなるな☆」': 'PRINTFORMW 「ふぁ……腰が勝手に追いかける……。もっと近づくなら、団長の合図を待てよ☆」',
    'PRINTFORMW 「ふぁ……身体が勝手に締まるなんて、団長、こんなの初めてだぞ……」': 'PRINTFORMW 「ふぁ……っ、身体が勝手に締まる……。初めてでも、こんなに素直になるのか……！」',
    'PRINTFORMW 「んっ、あ……奥がじわっと甘いな♪」': 'PRINTFORMW 「んっ……あ、奥がじわっとほどける……。転校生くん、まだ続けるぞ♪」',
    'PRINTFORMW 「んっ、そこに触れると背中まで熱いぞ……」': 'PRINTFORMW 「んっ……そこから背中まで熱が走る……。きみ、触れる場所を覚えたな……！」',
    'PRINTFORMW 「んっ、力が抜ける……私、こんなふうに待ってしまうんだな……」': 'PRINTFORMW 「んっ……力が抜けたまま、次を待ってしまう……。私、団長なのにおかしいな……」',
    'PRINTFORMW 「んっ、奥まで来るたび腰が追いかける……恋人くん、そこ、好きだぞ♪」': 'PRINTFORMW 「んっ……奥を追いかける腰が止まらない……。恋人くん、今度は私から応援するぞ♪」',
    'PRINTFORMW 「んっ、強すぎる……離れたら嫌なのに、受け止めきれないぞ……！」': 'PRINTFORMW 「んっ……っ、強さに身体が追いつかない……！　離れたくないが、少しだけ呼吸をくれ……！」',
    'PRINTFORMW 「んっ、待て、深いと声が出ない……でも、離れるな……！」': 'PRINTFORMW 「んっ……深く来ると、声が喉でつかえる……っ。でも、手は離すなよ……！」',
    'PRINTFORMW 「んっ、後ろがゆっくりほどける……おまえの手、あったかいな♪」': 'PRINTFORMW 「んっ……後ろの奥がほどけて、膝までふわふわする……。おまえの手、ずるいな♪」',
    'PRINTFORMW 「んっ、後ろの奥まで熱い……恋人くん、そこを私の弱点にする気か♪」': 'PRINTFORMW 「んっ……後ろの奥が熱で満ちる……。恋人くん、そこを弱点にするなら、最後まで面倒見ろ♪」',
    'PRINTFORMW 「んっ、触られるたび身体が小さく跳ねるぞ……」': 'PRINTFORMW 「んっ……触れるたび、背中がびくっと跳ねる……。私の身体、応援に素直すぎるぞ☆」',
    'PRINTFORMW 「んっ、触れるたび奥が小さく跳ねるぞ……」': 'PRINTFORMW 「んっ……奥に触れられるたび、腰が勝手に返事する……。きみ、見逃すなよ……！」',
    'PRINTFORMW 「んん、お尻の奥がじんじんしてる……おまえ、手加減しないな♪」': 'PRINTFORMW 「んん……っ、お尻の奥がじんじんする……。おまえ、団長を本気で鍛える気か……♪」',
    'PRINTFORMW 「んん、まだ始まったばかりなのに、腰がもう待ってるな……」': 'PRINTFORMW 「んん……始まったばかりなのに、腰が先に走りたがる……。恋人くん、急かすなよ……♪」',
    'PRINTFORMW 「んん、まだ少し怖いのに、もう一度って思ってしまうな……」': 'PRINTFORMW 「んん……少し怖いのに、もう次を待ってる……。団長、好奇心まで全力なんだな……」',
    'PRINTFORMW 「んん、奥がじんわり熱くなる……おまえのリズム、好きだぞ♪」': 'PRINTFORMW 「んん……奥がじわじわ熱くなる……。おまえのリズム、団長の合図より正確だな♪」',
}


def replace_second(data: str, old: str, new: str) -> str:
    positions: list[int] = []
    cursor = 0
    while True:
        position = data.find(old, cursor)
        if position < 0:
            break
        positions.append(position)
        cursor = position + len(old)
    if len(positions) != 2:
        raise RuntimeError(f"expected two occurrences, found {len(positions)}: {old}")
    position = positions[1]
    return data[:position] + new + data[position + len(old) :]


def main() -> None:
    data = PATH.read_text(encoding="cp932")
    for old, new in REPLACEMENTS.items():
        data = replace_second(data, old, new)
    PATH.write_bytes(data.replace("\n", "\r\n").encode("cp932"))
    print(f"rewrote {len(REPLACEMENTS)} duplicate orgasm branches")


if __name__ == "__main__":
    main()
