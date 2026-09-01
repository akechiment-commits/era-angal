"""CHAR15・長町やえのCOM311を、甘い言葉を受ける側の反応へ修正する。"""

from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_15_長町やえ_COM.ERB"
BACKUP = ROOT / "tools/backups/CHAR15_before_com311_recipient_20260830/CHAR_15_長町やえ_COM.ERB"


DIALOGUES = [
    "「あ、甘い言葉……？　うへぇ、そんなまっすぐ言われたら、あたし、どこ見ればいいのっ……！　おに～さんの顔、見られないよぉ……っ！」",
    "「むぅ……おに～さんに何か言われるだけで胸がいっぱいになって、返事がうまくできないっ……。ごめんねっ！」",
    "「あっ、そんなこと急に言われたらっ……あたし、返す言葉が出てこないよぉ……っ。顔が熱くて、どうしようっ！」",
    "「おに～さんにそんなふうに言われると……胸がきゅうってなるっ。あたしも大好きっ、ほんとだよっ……♪」",
    "「えへへ……おに～さんの声、耳のそばで聞くと、胸の奥までぽかぽかするんだっ。もう一回、聞きたいなぁ……♪」",
    "「そんなに好きって言われたら、あたし、嬉しくて跳ねちゃうっ！　……でも、今はおに～さんのそばから動きたくないよっ☆」",
    "「おに～さんの優しい声、あたしのこと見てくれてるって思うと、どきどきするっ……♪」",
    "「あははっ、そんなこと言われると、あたしまでおに～さんのこと、もっと好きになっちゃうよっ☆」",
    "「えっと……おに～さんにいいなって言ってもらえるの、すっごく嬉しいっ。あたしも、もっと一緒にいたいっ……♪」",
    "「あたしのこと、いい子だって？　うへぇ……そんな顔で言われたら、照れて走り出しちゃうよっ☆」",
    "「そんな優しくされたら、嫌いになんてなれないよっ……。おに～さん、ずるいなぁっ♪」",
    "「頼りになるって言われるの、嬉しいっ！　おに～さんに褒めてもらえると、胸がぽかぽかするよっ☆」",
]


def read_lines() -> list[str]:
    return TARGET.read_bytes().decode("cp932").splitlines()


def write_lines(lines: list[str]) -> None:
    TARGET.write_bytes("\r\n".join(lines).encode("cp932") + b"\r\n")


def main() -> None:
    lines = read_lines()
    start = next(i for i, line in enumerate(lines) if line.startswith(";--- COM311 "))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith(";--- COM"))
    units: list[list[int]] = []
    index = start + 1
    while index < end:
        if re.search(r"PRINTFORM[LMW]\s+「", lines[index]):
            unit = [index]
            if "PRINTFORML" in lines[index] and index + 1 < end and "PRINTFORMW" in lines[index + 1]:
                unit.append(index + 1)
            units.append(unit)
            index = unit[-1] + 1
        else:
            index += 1
    if len(units) != len(DIALOGUES):
        raise RuntimeError(f"COM311台詞数が不一致です: 実ファイル={len(units)} 予定={len(DIALOGUES)}")

    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)

    for unit, dialogue in reversed(list(zip(units, DIALOGUES))):
        first = lines[unit[0]]
        indent = first[: len(first) - len(first.lstrip())]
        lines[unit[0]] = indent + "PRINTFORMW " + dialogue
        for line_index in reversed(unit[1:]):
            del lines[line_index]
    write_lines(lines)
    print(f"CHAR15 COM311を受け手側へ修正: {len(units)}件")


if __name__ == "__main__":
    main()
