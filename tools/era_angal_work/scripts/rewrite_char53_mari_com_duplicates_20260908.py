"""CHAR53まりの標準COM間に残る完全一致台詞を、行為ごとに分ける。"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ERB/CHAR/CHAR_53_花丘まり_COM.ERB"


REPLACEMENTS = {
    'PRINTFORMW 「あっ……肌を狙うとは、なかなかやるねぇ。少し待っておくれ、息が追いつかないよ……♪」': [
        'PRINTFORMW 「%LOCALS%の熱が直接返ってくるとは、なかなか乙なラリーだねぇ……。ふふ、まだ息を整えちゃいけないのかい♪」',
    ],
    'PRINTFORMW 「お尻が敏感になってるねぇ。ほら、言葉より先に声が出ちまう……♪」': [
        'PRINTFORMW 「後ろへ振動が届くたび、声まで先に飛び出しちまうねぇ……。おやまぁ、あたしも隠せないじゃないか♪」',
    ],
    'PRINTFORMW 「お尻が跳ねるたび、強がりがひとつずつ消えるねぇ。少しゆるめておくれ……♪」': [
        'PRINTFORMW 「受け止めるたびに、身体が勝手に返事しちまうねぇ……。あんた、加減は顔色を見ておくれよ♪」',
    ],
    'PRINTFORMW 「お尻へ来るたび、声がひとつ遅れるねぇ。急がず、そのまま続けておくれ……♪」': [
        'PRINTFORMW 「後ろから押されるたび、息の返事が遅くなっちまうねぇ……。ふふ、あんたも急がず付きあっておくれ♪」',
        'PRINTFORMW 「泡のなかでお尻まで熱くなるとはねぇ……。あたしも年甲斐なく、声を隠せなくなっちまうよ♪」',
    ],
    'PRINTFORMW 「ふふ……奥がじわじわ熱くなるねぇ。あんた、まだ手をゆるめちゃ嫌だよ……♪」': [
        'PRINTFORMW 「深いところまで届くと、あたしの息も長く続かないねぇ……。ふふ、もう少しだけ丁寧におくれ♪」',
    ],
    'PRINTFORMW 「ふふ、後ろがほどけていくねぇ……。あたしをこんなに甘やかすの、あんただけだよ♪」': [
        'PRINTFORMW 「後ろから受ける熱が、まだ消えないよ……。あんたに甘やかされたぶん、今夜はひとりで眠れそうにないねぇ♪」',
    ],
    'PRINTFORMW 「んっ……身体に触れられると、言葉が途切れちまうよ。ふふ、困ったねぇ……♪」': [
        'PRINTFORMW 「薬のせいかねぇ、指先まで熱が回っちまったよ……。ふふ、あんたも心配そうな顔をしなさんな♪」',
    ],
    'PRINTFORMW 「後ろが熱を持ってきたねぇ……。甘えたいって顔に出ちまってるかい？♪」': [
        'PRINTFORMW 「お尻の奥がまだ火照ってるねぇ……。あんた、責任を持って、あたしの手を引いておくれ♪」',
    ],
    'PRINTFORMW 「肌がくすぐったくて、笑っていられないよ……。あんたの手、好きだねぇ♪」': [
        'PRINTFORMW 「針のあとがちくちく残って、笑うどころじゃないねぇ……。おやまぁ、手つきは丁寧におくれ♪」',
        'PRINTFORMW 「湯気のなかで背中をなぞられると、のぼせる前に力が抜けちまうねぇ……。ふふ、困ったもんだよ♪」',
    ],
    'PRINTFORMW 「肌に来ると、つい声を飲み込んじまうよ。……ん、まだ続けるんだねぇ♪」': [
        'PRINTFORMW 「見せるだけのつもりだったのに、舌が触れると息まで隠れちまうねぇ……。%LOCALS%、もう少しだけ頼めるかい？♪」',
        'PRINTFORMW 「嫁の真似事をしてるだけなのに、肌に触れられると本気になっちまうねぇ……。あはは、困ったねぇ♪」',
    ],
    'PRINTFORMW 「肌へ来るたび、声がひとつ遅れるねぇ。急がず、そのまま続けておくれ……♪」': [
        'PRINTFORMW 「機械を外したあとも、肌がまだ覚えてるねぇ……。あんた、次は優しい手で落ち着かせておくれ♪」',
    ],
    'PRINTFORMW 「胸の奥が熱を持ってきたねぇ……。甘えたいって顔に出ちまってるかい？♪」': [
        'PRINTFORMW 「薬を飲んだせいかねぇ、胸までぽかぽかしてきたよ……。あんた、急かさず様子を見ておくれ♪」',
    ],
    'PRINTFORMW 「舌に残る熱、消さないでおくれよ。まだあんたを感じていたいねぇ……♪」': [
        'PRINTFORMW 「お互いの舌を離しても、唇の先がまだ熱いねぇ……。ふふ、もう一度なら、付きあってあげようか♪」',
    ],
    'PRINTFORMW 「身体が敏感になってるねぇ。ほら、言葉より先に声が出ちまう……♪」': [
        'PRINTFORMW 「力をかけられるたび、身体が先に返事しちまうねぇ……。ほら、あんたの手を止めないでおくれ♪」',
        'PRINTFORMW 「自分で動かしてるのを見てると、あたしまでつられて息が熱くなるねぇ……。ふふ、もう少し続けておみせ♪」',
    ],
    'PRINTFORMW 「身体へ来るたび、声がひとつ遅れるねぇ。急がず、そのまま続けておくれ……♪」': [
        'PRINTFORMW 「薬が身体に回るたび、声が遅れて出ちまうねぇ……。無理はしないで、ゆっくり付きあっておくれ♪」',
    ],
}

COM131_OLD = 'PRINTFORMW 「あらまぁ、ずいぶんおとなしくなったねぇ。縛られたぶん、あたしの言うことを聞いておくれ♪」'
COM131_NEW = 'PRINTFORMW 「あらまぁ、ずいぶんおとなしくなったねぇ。あたしの縛り方が効いたなら、言うことを聞いておくれ♪」'


def replace_after_first(data: str, old: str, replacements: list[str]) -> str:
    positions: list[int] = []
    cursor = 0
    while True:
        position = data.find(old, cursor)
        if position < 0:
            break
        positions.append(position)
        cursor = position + len(old)
    if len(positions) != len(replacements) + 1:
        raise RuntimeError(f"expected {len(replacements) + 1} occurrences, found {len(positions)}: {old}")
    for position, replacement in reversed(list(zip(positions[1:], replacements))):
        data = data[:position] + replacement + data[position + len(old) :]
    return data


def main() -> None:
    data = PATH.read_text(encoding="cp932")
    for old, replacements in REPLACEMENTS.items():
        data = replace_after_first(data, old, replacements)
    if data.count(COM131_OLD) != 1:
        raise RuntimeError(f"expected one COM131 line, found {data.count(COM131_OLD)}")
    data = data.replace(COM131_OLD, COM131_NEW)
    PATH.write_bytes(data.replace("\n", "\r\n").encode("cp932"))
    print(f"rewrote {sum(len(value) for value in REPLACEMENTS.values())} cross-COM duplicates and COM131")


if __name__ == "__main__":
    main()
