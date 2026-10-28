from pathlib import Path
import re


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")


def crlf(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\n", "\r\n")


def replace_block(source: str, start: str, end: str, replacement: str) -> str:
    pattern = re.compile(re.escape(start) + r".*?(?=" + re.escape(end) + r")", re.S)
    matches = list(pattern.finditer(source))
    assert len(matches) == 1, f"block is not unique: {start} ({len(matches)})"
    return source[: matches[0].start()] + crlf(replacement) + source[matches[0].end() :]


old307 = "PRINTFORMW 「櫛で梳かしてくれるのか☆　わざわざありがとうな転校生くん！　ほら、痛かったら言ってくれよ……って、私がか♪」"
new307 = "PRINTFORMW 「櫛で梳かしてくれるのか☆　わざわざありがとうな転校生くん！　私の髪、痛くないようにゆっくり頼むぞ♪」"
assert text.count(old307) == 1, "CHAR67 COM307 mixed line is not unique"
text = text.replace(old307, new307, 1)

for marker, note in (
    (";--- COM306 髪梳き ---\r\n", ";--- COM306 髪梳き ---\r\n; ▼【視点】PLAYERがましろの髪を手で梳く。ましろは梳かれる側。\r\n"),
    (";--- COM307 櫛で梳かす ---\r\n", ";--- COM307 櫛で梳かす ---\r\n; ▼【視点】PLAYERがましろの髪を櫛で梳く。ましろは梳かれる側。\r\n"),
):
    assert text.count(marker) == 1, f"annotation anchor is not unique: {marker}"
    text = text.replace(marker, note, 1)

new311 = """;--- COM311 甘い言葉 ---
; ▼【視点・発話者】転校生くんがましろへ甘い言葉を言う。以下は転校生くんの発話。
IF SELECTCOM == 311
\tIF CFLAG:TARGET:216 == 0
\t\tCFLAG:TARGET:216 = 1
\t\t;初回
\t\tPRINTFORMW 「ましろ、今日もよく頑張ったな。おまえの笑顔が好きだ」
\tELSE
\t\tA = RAND:3
\t\t;--- 失敗時 ---
\t\tIF TFLAG:18 == -1
\t\t\tIF TALENT:TARGET:153
\t\t\t\t;恋人・失敗
\t\t\t\tPRINTFORMW 「ごめん、ましろ。今の言葉、重かったか？　無理に返事をしなくていいからな」
\t\t\tELSE
\t\t\t\t;失敗
\t\t\t\tPRINTFORMW 「悪かった、ましろ。暑苦しく聞こえたな。嫌なら、もう無理に言わないから」
\t\t\tENDIF
\t\t;--- 成功時 ---
\t\tELSE
\t\t\t;--- 恋人 ---
\t\t\tIF TALENT:TARGET:153
\t\t\t\tIF A == 0
\t\t\t\t\tPRINTFORMW 「愛してるよ、ましろ。おまえと一緒にいる時間が、俺は一番好きだ」
\t\t\t\tELSEIF A == 1
\t\t\t\t\tPRINTFORMW 「ましろは俺の大切な人だ。頑張りすぎるところも、まっすぐなところも全部好きだよ」
\t\t\t\tELSE
\t\t\t\t\tPRINTFORMW 「ましろの笑顔を見ると、俺まで元気になる。これからも俺の隣にいてくれ」
\t\t\t\tENDIF
\t\t\t;--- 親密 ---
\t\t\tELSEIF ABL:TARGET:0 >= 6
\t\t\t\tIF A == 0
\t\t\t\t\tPRINTFORMW 「ましろ、おまえといると元気が出る。俺にとって大事な仲間だよ」
\t\t\t\tELSEIF A == 1
\t\t\t\t\tPRINTFORMW 「頑張ってるましろを、俺はちゃんと見てる。無理なときは頼ってくれ」
\t\t\t\tELSE
\t\t\t\t\tPRINTFORMW 「ましろが笑ってると安心する。今日は少しだけ、俺の隣にいてくれ」
\t\t\t\tENDIF
\t\t\t;--- 通常 ---
\t\t\tELSE
\t\t\t\tIF A == 0
\t\t\t\t\tPRINTFORMW 「ましろはすごいやつだよ。誰かを応援できるその元気、ちゃんと伝わってる」
\t\t\t\tELSEIF A == 1
\t\t\t\t\tPRINTFORMW 「おまえの笑顔は、周りまで明るくする。自信を持っていいぞ、ましろ」
\t\t\t\tELSE
\t\t\t\t\tPRINTFORMW 「今日もよく頑張ったな、ましろ。今は何も考えず、少し休んでくれ」
\t\t\t\tENDIF
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF
"""
text = replace_block(text, ";--- COM311 甘い言葉 ---\r\n", ";--- COM312 頭を撫でる ---\r\n", new311)

new312 = """;--- COM312 頭を撫でる ---
; ▼【視点】PLAYERがましろの頭を撫でる。ましろは撫でられる側。COM311の甘い言葉は混ぜない。
IF SELECTCOM == 312
\tIF CFLAG:TARGET:217 == 0
\t\tCFLAG:TARGET:217 = 1
\t\t;初回
\t\tPRINTFORMW 「おっ、頭を撫でてくれるのか？　ふむふむ、力加減が優しいな、転校生くん☆」
\tELSE
\t\tA = RAND:3
\t\t;--- 失敗時 ---
\t\tIF TFLAG:18 == -1
\t\t\tIF TALENT:TARGET:153
\t\t\t\t;恋人・失敗
\t\t\t\tPRINTFORMW 「あっ、手が止まったか？　嫌ではないぞ、ちょっと驚いただけだ。恋人なら、もう一度ゆっくり頼む♪」
\t\t\tELSE
\t\t\t\t;失敗
\t\t\t\tPRINTFORMW 「うわっ、子ども扱いは苦手だぞ！　……でも、手を離すなら、ちゃんとそう言ってくれ！」
\t\t\tENDIF
\t\t;--- 成功時 ---
\t\tELSE
\t\t\t;--- 恋人 ---
\t\t\tIF TALENT:TARGET:153
\t\t\t\tIF A == 0
\t\t\t\t\tPRINTFORMW 「んっ……頭を撫でられると、心まで力を抜いてしまうな。恋人の手、ずっとここに置いてくれ♪」
\t\t\t\tELSEIF A == 1
\t\t\t\t\tPRINTFORMW 「ふぁ……撫でる手が優しいぞ。私が元気を配るはずなのに、今日は私が受け取ってしまうな☆」
\t\t\t\tELSE
\t\t\t\t\tPRINTFORMW 「あぁ、そこだ……っ。頭を撫でられていると、おまえのそばにいる安心が身体まで広がるな……♪」
\t\t\t\tENDIF
\t\t\t;--- 親密 ---
\t\t\tELSEIF ABL:TARGET:0 >= 6
\t\t\t\tIF A == 0
\t\t\t\t\tPRINTFORMW 「ふむふむ、頭を撫でられると肩まで軽くなるな。転校生くん、もう少し続けてくれ☆」
\t\t\t\tELSEIF A == 1
\t\t\t\t\tPRINTFORMW 「うぅ、団長でも疲れる日はあるのだ。手が触れていると、ひとりで頑張らなくていい気がするぞ……」
\t\t\t\tELSE
\t\t\t\t\tPRINTFORMW 「なでなで……っ、ふふ、髪が乱れても今日は気にしない。転校生くんの手なら任せる♪」
\t\t\t\tENDIF
\t\t\t;--- 通常 ---
\t\t\tELSE
\t\t\t\tIF A == 0
\t\t\t\t\tPRINTFORMW 「おやっ、私の頭を撫でるのか？　よし、今日は力を抜いて受けてみるぞ☆」
\t\t\t\tELSEIF A == 1
\t\t\t\t\tPRINTFORMW 「ふぇっ、急に優しくするな!?　頭だけなのに、応援の掛け声が出なくなるではないか……！」
\t\t\t\tELSE
\t\t\t\t\tPRINTFORMW 「んん～、そこを撫でると眠くなるな。私が寝たら、ちゃんと起こしてくれよ転校生くん♪」
\t\t\t\tENDIF
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF
"""
text = replace_block(text, ";--- COM312 頭を撫でる ---\r\n", ";--- COM313 願掛け ---\r\n", new312)

PATH.write_bytes(text.encode("cp932"))
