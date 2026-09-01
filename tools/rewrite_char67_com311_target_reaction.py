from pathlib import Path
import re


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")


def crlf(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\n", "\r\n")


replacement = """;--- COM311 甘い言葉 ---
; ▼【視点・発話者】転校生くんが甘い言葉を言う。主人公の台詞は表示せず、ましろが言われた反応だけを書く。
IF SELECTCOM == 311
\tIF CFLAG:TARGET:216 == 0
\t\tCFLAG:TARGET:216 = 1
\t\t;初回
\t\tPRINTFORMW 「えっ、そんなことを言うのか!?　うぅ、私、こういうの不慣れで……っ。まっすぐ見つめられると、どう返せばいいのだ……☆」
\tELSE
\t\tA = RAND:3
\t\t;--- 失敗時 ---
\t\tIF TFLAG:18 == -1
\t\t\tIF TALENT:TARGET:153
\t\t\t\t;恋人・失敗
\t\t\t\tPRINTFORMW 「ご、ごめん、今のは……っ。嬉しいのに、照れすぎて変な顔をしてしまった……。恋人の前だと、まだまだ不器用だな……」
\t\t\tELSE
\t\t\t\t;失敗
\t\t\t\tPRINTFORMW 「あぅ、そんなふうに言われるとは思わなかったぞ……。返事が遅くても、気を悪くしないでくれ……」
\t\t\tENDIF
\t\t;--- 成功時 ---
\t\tELSE
\t\t\t;--- 恋人 ---
\t\t\tIF TALENT:TARGET:153
\t\t\t\tIF A == 0
\t\t\t\t\tPRINTFORMW 「そ、そんなまっすぐな気持ちを……っ。恋人に向けてもらえると、胸がいっぱいで声が出なくなるぞ……♪」
\t\t\t\tELSEIF A == 1
\t\t\t\t\tPRINTFORMW 「私をそんなに大事に思ってくれていたのか……っ。うぅ、嬉しすぎて、ぎゅううってするしかないな☆」
\t\t\t\tELSE
\t\t\t\t\tPRINTFORMW 「うわぁ、また胸に響くことを言う……っ。何度聞いても慣れないぞ、でも、もっと聞いていたいな……♪」
\t\t\t\tENDIF
\t\t\t;--- 親密 ---
\t\t\tELSEIF ABL:TARGET:0 >= 6
\t\t\t\tIF A == 0
\t\t\t\t\tPRINTFORMW 「そんなふうに認めてもらえるのか？　えへへ、私の元気、ちゃんと届いていたのだな☆」
\t\t\t\tELSEIF A == 1
\t\t\t\t\tPRINTFORMW 「優しい言葉が胸の奥まで入ってくる……っ。転校生くん、私、ちゃんと受け取ったぞ♪」
\t\t\t\tELSE
\t\t\t\t\tPRINTFORMW 「そんなにまっすぐ言われたら、私まで素直になってしまうな……。今日は少しだけ、そばにいてくれ☆」
\t\t\t\tENDIF
\t\t\t;--- 通常 ---
\t\t\tELSE
\t\t\t\tIF A == 0
\t\t\t\t\tPRINTFORMW 「ま、ましろのことをそんなふうに……っ。う、嬉しいぞ！　団長、まだ顔が熱いではないか……☆」
\t\t\t\tELSEIF A == 1
\t\t\t\t\tPRINTFORMW 「おまえの言葉、あったかいな……。胸の奥までぽかぽかして、変な顔になってしまうぞ♪」
\t\t\t\tELSE
\t\t\t\t\tPRINTFORMW 「そんなに真正面から言われると、団長でも照れるな……っ。う、うむ、ありがとう、転校生くん☆」
\t\t\t\tENDIF
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF
"""

pattern = re.compile(r";--- COM311 甘い言葉 ---\r?\n.*?(?=;--- COM312 )", re.S)
matches = list(pattern.finditer(text))
assert len(matches) == 1, f"CHAR67 COM311 block is not unique ({len(matches)})"
text = text[: matches[0].start()] + crlf(replacement) + text[matches[0].end() :]
PATH.write_bytes(text.encode("cp932"))
