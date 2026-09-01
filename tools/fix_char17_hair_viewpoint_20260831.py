"""CHAR17・小鳩あずさの髪梳き／頭撫での視点混乱を修正する。"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_17_小鳩あずさ_COM.ERB"
SOURCE = ROOT / "tools/output/あずさ.txt"
BACKUP = ROOT / "tools/backups/CHAR17_before_hair_viewpoint_20260831/CHAR_17_小鳩あずさ_COM.ERB"


BLOCKS = {
    306: '''IF SELECTCOM == 306
\tIF CFLAG:TARGET:216 == 0
\t\tCFLAG:TARGET:216 = 1
\t\t;初回
\t\tPRINTFORMW 「あずさの髪、梳いてもらいますねっ☆　えへへ、じっとしてますから、優しくしてくださいっ☆」
\tELSE
\t\tA = RAND:3
\t\tIF TALENT:TARGET:153
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「あずさの髪、先輩の手でゆっくり整っていきますっ……。任せていると、肩の力まで抜けちゃいますね☆」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「んっ……髪に触れるお兄ちゃんの指、気持ちいいですっ。あずさ、じっとしてるだけで甘やかされちゃいます……♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「（お兄ちゃんに髪を梳いてもらってる……しあわせです）もう少し、このまま隣にいてもいいですか……☆」
\t\t\tENDIF
\t\tELSE
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「あっ、そこ、少し絡まってます……。先輩、痛くないようにゆっくりで大丈夫ですっ☆」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「あずさの髪、扱いにくくないですか？　先輩の手が通るたび、なんだか落ち着きます……」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「えへへ、梳いてもらうと、いつものあずさでも少しは女の子らしく見えますかね……？」
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF''',
    307: '''IF SELECTCOM == 307
\tIF CFLAG:TARGET:217 == 0
\t\tCFLAG:TARGET:217 = 1
\t\t;初回
\t\tPRINTFORMW 「今日は櫛で梳いてもらいますねっ☆　えへへ、あずさ、じっとしてますから……お願いしますっ☆」
\tELSE
\t\tA = RAND:3
\t\tIF TALENT:TARGET:153
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「櫛の先が髪をすべる音、落ち着きます……。お兄ちゃんに整えてもらう時間、好きですっ☆」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「んっ、そこを通ると頭まで気持ちいいです……。あずさ、眠っちゃったら起こしてくださいね♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「櫛を入れるたび、髪が軽くなりますねっ。先輩が丁寧にしてくれるの、嬉しいです☆」
\t\t\tENDIF
\t\tELSE
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「あっ、櫛が引っかかりましたね……。無理に引かなくて大丈夫です、あずさが少し頭を動かしますっ☆」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「櫛の歯が頭に当たると、くすぐったいです……。でも、痛くないようにしてくれてるのは分かりますっ」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「あずさの髪、ちゃんと整いましたか？　後ろは自分で見えないので、先輩に教えてほしいです……☆」
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF''',
    316: '''IF SELECTCOM == 316
\tIF CFLAG:TARGET:217 == 0
\t\tCFLAG:TARGET:217 = 1
\t\t;初回
\t\tPRINTFORMW 「お兄ちゃんの髪、あずさが梳くんですかっ☆　ふあ～、ちょっと緊張しますけど、嬉しいですっ☆」
\tELSE
\t\tA = RAND:3
\t\tIF TALENT:TARGET:153
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「お兄ちゃんの髪、こうして梳くと指の間をすべっていきます……。あずさ、もっと丁寧にしますねっ☆」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「んっ、髪を整えていると、あずさのお世話焼き心がうずうずしますっ。力を抜いて任せてくださいね♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「（お兄ちゃんの髪に触れてる……近いです）今日はあずさが甘やかす番ですねっ☆」
\t\t\tENDIF
\t\tELSE
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「あっ、先輩の髪、ここが少し絡まってます。痛くしないように、あずさがほどしますねっ」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「櫛の通り、これで大丈夫ですか？　あずさ、力があるから、引っぱらないように気をつけますっ☆」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「できましたっ☆　先輩の髪、ちゃんと整いましたよ。後ろも変じゃないか、見てみてくださいねっ」
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF''',
    318: '''IF SELECTCOM == 318
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「先輩、今日はあずさの膝で休んでください☆　頭を撫でていると、あずさまで落ち着きますっ」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「んっ、先輩の頭、あずさが撫でますね……。大事なひとを甘やかすのも、たまには素敵です☆」
\t\tELSE
\t\t\tPRINTFORMW 「髪を梳くんじゃなくて、今日は頭を撫でるだけですっ。先輩が眠るまで、そばにいますね♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「先輩、疲れているなら頭をこちらへ……。あずさ、撫でるときは優しくできますっ☆」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「よしよし……先輩の髪を、あずさの手でそっと撫でますね。少しは休めそうですか？」
\t\tELSE
\t\t\tPRINTFORMW 「わわっ、撫でていたら先輩が静かになりました……。あずさでよければ、もう少し続けますねっ♪」
\t\tENDIF
\tENDIF
ENDIF''',
}


def block_span(text: str, com: int) -> tuple[int, int]:
    match = __import__("re").search(rf"(?m)^IF SELECTCOM == {com}\s*$", text)
    if not match:
        raise ValueError(f"COM{com} が見つかりません")
    tail = __import__("re").search(r"(?m)^(?:;--- COM|;===|@)", text[match.end() :])
    end = match.end() + tail.start() if tail else len(text)
    return match.start(), end


def replace_block(text: str, com: int, block: str) -> str:
    start, end = block_span(text, com)
    original_chunk = text[start:end]
    last_endif = original_chunk.rfind("\nENDIF")
    trailer = original_chunk[last_endif + len("\nENDIF") :] if last_endif >= 0 else "\n"
    return text[:start] + block + trailer + text[end:]


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    if not source.startswith("# あずさ（全1880件）"):
        raise RuntimeError("あずさ.txt の原作見出しを確認できません")
    if "頭を撫で撫でしちゃってください☆" not in source:
        raise RuntimeError("あずさの頭撫で原作表現を確認できません")

    raw = TARGET.read_bytes().decode("cp932")
    text = raw.replace("\r\n", "\n")
    before = text
    for com, block in BLOCKS.items():
        text = replace_block(text, com, block)
    if text == before:
        print("変更なし")
        return 0

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)
    TARGET.write_bytes(text.replace("\n", "\r\n").encode("cp932"))
    print("COM306/307/316/318の髪梳き・頭撫で視点を整理")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
