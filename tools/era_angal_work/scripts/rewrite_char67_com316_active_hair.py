from pathlib import Path
import re


PATH = Path(r"ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB")
text = PATH.read_bytes().decode("cp932")


def crlf(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\n", "\r\n")


replacement = """;--- COM316 髪を梳く ---
; ▼【視点】ましろが転校生くんの髪を梳く。ましろが行う側。
IF SELECTCOM == 316
\tIF CFLAG:TARGET:217 == 0
\t\tCFLAG:TARGET:217 = 1
\t\t;初回
\t\tPRINTFORMW 「よし、私が梳いてやるぞ☆　転校生くんの髪、少し跳ねてるな……痛くしないから任せてくれ♪」
\tELSE
\t\tA = RAND:3
\t\tIF TALENT:TARGET:153
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「恋人の髪を梳くの、最高にしあわせだなぁ☆　手ぐしで整えてやると、ますます近くなった気がするぞ♪」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「ふふ、転校生くんの髪を梳くと、私もちょっとは女の子らしくなるかな？　……えへへ、気持ちいいか♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「なぁ、私が梳くから力を抜けよ。転校生くんの髪を整えていると、心まであったかくなるな☆」
\t\t\tENDIF
\t\tELSE
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「髪を梳いてやるぞ、任せろ☆　転校生くん、じっとしていろよ、すぐに整えてやるからな！」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「おぉ、髪が跳ねてるな☆　私の手ぐしで直してやるぞ、午後の応援も気合いが入るな、フレーフレー！」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「髪を整えると気持ちいいか？　おまえが眠くなるまで、私がゆっくり梳いてやるぞ♪」
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF
"""

pattern = re.compile(r";--- COM316 .*?\r?\n.*?(?=;--- COM320 )", re.S)
matches = list(pattern.finditer(text))
assert len(matches) == 1, f"CHAR67 COM316 block is not unique ({len(matches)})"
text = text[: matches[0].start()] + crlf(replacement) + text[matches[0].end() :]
PATH.write_bytes(text.encode("cp932"))
