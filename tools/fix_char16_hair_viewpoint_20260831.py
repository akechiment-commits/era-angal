"""CHAR16・大虎いさみの髪梳き／頭撫での視点混乱を修正する。"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_16_大虎いさみ_COM.ERB"
SOURCE = ROOT / "tools/output/いさみ.txt"
BACKUP = ROOT / "tools/backups/CHAR16_before_hair_viewpoint_20260831/CHAR_16_大虎いさみ_COM.ERB"


BLOCKS = {
    306: '''IF SELECTCOM == 306
\tIF CFLAG:TARGET:216 == 0
\t\tCFLAG:TARGET:216 = 1
\t\t;初回
\t\tPRINTFORMW 「あたいの髪、梳かしてくれます？　えへへ、弟妹にやってもらったことはありますけど、先輩にされるの新鮮っす♪」
\tELSE
\t\tA = RAND:3
\t\tIF TALENT:TARGET:153
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「あたいの髪、先輩の手でゆっくり整っていくっす……。こうして任せてると、肩の力まで抜けるっす♪」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「んっ……髪に触れる先輩の指、気持ちいいっす。あたい、じっとしてるだけで甘やかされてる気分っす……♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「（先輩に髪を梳いてもらってる……しあわせっす）もう少し、このまま隣にいてもいいっすか……♪」
\t\t\tENDIF
\t\tELSE
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「あっ、そこ、少し絡まってるっす……。先輩、痛くないようにゆっくりで大丈夫っすから」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「あたいの髪、扱いにくくないっすか？　先輩の手が通るたび、なんだか落ち着くっす……」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「えへへ、梳いてもらうと、いつものあたいでも少しは女の子らしく見えるっすかね……？」
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF''',
    307: '''IF SELECTCOM == 307
\tIF CFLAG:TARGET:217 == 0
\t\tCFLAG:TARGET:217 = 1
\t\t;初回
\t\tPRINTFORMW 「今度は櫛で梳いてもらうっすね♪　あたい、じっとしてるっすから……えへへ、お願いします」
\tELSE
\t\tA = RAND:3
\t\tIF TALENT:TARGET:153
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「櫛の先が髪をすべる音、落ち着くっす……。先輩に整えてもらう時間、好きっす♪」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「んっ、そこを通ると頭皮まで気持ちいいっす……。あたい、眠っちまいそうっすよ♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「櫛を入れるたび、髪が軽くなるっすね……。先輩に見てもらうためなら、もう少し丁寧にしてほしいっす♪」
\t\t\tENDIF
\t\tELSE
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「あっ、櫛が引っかかったっすね……。無理に引かなくて大丈夫っす、あたいが少し頭を動かすっす」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「櫛の歯が頭に当たると、くすぐったいっす……。でも、痛くないようにしてくれてるのは分かるっすよ」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「あたいの髪、ちゃんと整ったっすか？　自分じゃ後ろまで見えないから、先輩に教えてほしいっす」
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF''',
    316: '''IF SELECTCOM == 316
\tIF CFLAG:TARGET:217 == 0
\t\tCFLAG:TARGET:217 = 1
\t\t;初回
\t\tPRINTFORML 「えっ、先輩の髪、あたいが梳くんすか……？　わわっ、ちょっと緊張するっす……。
\t\tPRINTFORMW ゴワゴワしてないっすかね……？　えへへ、優しくしますね」
\tELSE
\t\tA = RAND:3
\t\tIF TALENT:TARGET:153
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「先輩の髪、こうして梳くと指の間をすべっていくっす……。あたい、もっと丁寧にやるっすね♪」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「んっ、先輩の髪を整えてると、世話焼きの血が騒ぐっす……。あたいに任せて、力抜いてください♪」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「（先輩の髪に触れてる……近いっす）えへへ、今日はあたいが甘やかす番っすね♪」
\t\t\tENDIF
\t\tELSE
\t\t\tIF A == 0
\t\t\t\tPRINTFORMW 「あっ、先輩の髪、ここが少し絡んでるっす。痛くしないように、あたいがほどくっすね」
\t\t\tELSEIF A == 1
\t\t\t\tPRINTFORMW 「櫛の通り、こんな感じで大丈夫っすか？　あたい、力があるから、引っぱらないよう気をつけるっす」
\t\t\tELSE
\t\t\t\tPRINTFORMW 「できたっす♪　先輩の髪、ちゃんと整ったっすよ。後ろも変じゃないか、見てほしいっす」
\t\t\tENDIF
\t\tENDIF
\tENDIF
ENDIF''',
    318: '''IF SELECTCOM == 318
\tA = RAND:3
\tIF TALENT:TARGET:85
\t\tIF A == 0
\t\t\tPRINTFORMW 「先輩、今日はあたいの膝で休んでいいっすよ。髪を撫でてると、あたいまで落ち着くっす♪」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「んっ、先輩の頭、あたいが撫でるっす……。大事なひとを甘やかすのも、たまにはいいっすよね♪」
\t\tELSE
\t\t\tPRINTFORMW 「髪を梳くんじゃなくて、今日は頭を撫でるだけっす。先輩が眠るまで、あたいがそばにいるっす♪」
\t\tENDIF
\tELSE
\t\tIF A == 0
\t\t\tPRINTFORMW 「先輩、疲れてるなら頭をこっちへ……。あたい、力仕事の手でも、撫でるときは優しくできるっす」
\t\tELSEIF A == 1
\t\t\tPRINTFORMW 「よしよし……先輩の髪、あたいの手で整えるっす。少しは休めそうっすか？」
\t\tELSE
\t\t\tPRINTFORMW 「わっ、撫でてたら先輩が静かになったっすね。あたいでよければ、もう少し続けるっす♪」
\t\tENDIF
\tENDIF
ENDIF''',
}


def replace_block(text: str, com: int, block: str) -> str:
    marker = f"IF SELECTCOM == {com}\n"
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"COM{com} が見つかりません")
    next_start = text.find("\nIF SELECTCOM == ", start + len(marker))
    if next_start < 0:
        next_start = len(text)
    else:
        next_start += 1
    original_chunk = text[start:next_start]
    last_endif = original_chunk.rfind("\nENDIF")
    trailer = original_chunk[last_endif + len("\nENDIF") :] if last_endif >= 0 else "\n"
    return text[:start] + block + trailer + text[next_start:]


def ensure_following_annotations(text: str) -> str:
    # COM306/307/316の全ブロック置換で、直後の既存見出しコメントが境界内に
    # 入る場合があるため、失われた隣接COMの注釈だけを補う。
    labels = {307: "櫛で梳かす", 309: "素材探し", 320: "学食に行く"}
    for com, label in labels.items():
        marker = f"IF SELECTCOM == {com}\n"
        start = text.find(marker)
        if start < 0:
            raise ValueError(f"COM{com} が見つかりません")
        before = text[max(0, start - 120) : start]
        if f"COM{com}" not in before:
            text = text[:start] + f";--- COM{com} {label} ---\n" + text[start:]
    return text


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    if not source.startswith("# いさみ（全1346件）"):
        raise RuntimeError("いさみ.txt の原作見出しを確認できません")
    raw = TARGET.read_bytes().decode("cp932")
    text = raw.replace("\r\n", "\n")
    before = text
    for com, block in BLOCKS.items():
        text = replace_block(text, com, block)
    text = ensure_following_annotations(text)
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
