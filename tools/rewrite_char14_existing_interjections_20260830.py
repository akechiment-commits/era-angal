"""CHAR14の既存台詞だけを対象に、過密な文頭相槌をことりの原作寄りへ整える。"""

from __future__ import annotations

import difflib
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_14_花音ことり_COM.ERB"
SOURCE = ROOT / "tools/backups/CHAR14_before_rand3_20260829/CHAR_14_花音ことり_COM.ERB"
BACKUP = ROOT / "tools/backups/CHAR14_before_existing_interjection_20260830/CHAR_14_花音ことり_COM.ERB"


# キーはRAND3化前バックアップの行番号。値は「えへ／んあ／んん」に代える文頭。
# 空文字は相槌だけを外し、後続の本文をそのまま残す。
REWRITES: dict[int, str] = {
    57: "うん、", 79: "よし、", 91: "", 116: "あのな、", 127: "あっ、",
    146: "うん、", 150: "", 211: "えっ、", 215: "",
    224: "", 255: "うん、", 262: "おぉ、", 275: "あっ、", 295: "なぁ、",
    313: "うん、", 331: "", 343: "おら、", 359: "", 387: "おら、",
    399: "よし、", 415: "おぉ、", 417: "", 427: "おら、", 443: "うん、",
    453: "うん、", 455: "おっと、", 492: "うん、", 534: "おら、", 573: "",
    583: "あぁ、", 585: "おぉ、", 601: "うん、", 603: "あぁ、", 609: "あっ、",
    641: "おぉ、", 648: "あっ、", 652: "うん、", 668: "おぉ、",
    676: "おら、", 680: "あっ、", 697: "うん、", 699: "おぉ、", 708: "うん、",
    710: "", 715: "", 719: "", 736: "おら、", 738: "あっ、", 749: "おぉ、",
    754: "", 758: "", 776: "おぉ、", 786: "あぁ、", 827: "",
    838: "うん、", 874: "あっ、", 876: "おぉ、", 887: "うん、", 901: "",
    906: "うん、", 1092: "あっ……っ、", 1120: "はぁ……っ、",
    1176: "ひゃっ……っ、", 1204: "あっ……っ、",
    1260: "ひゃっ……っ、", 1288: "あっ……っ、", 1307: "あっ……",
    1316: "あぅ……っ、", 1320: "うん、", 1372: "ひゃっ……っ、",
    1490: "おら、", 1500: "おぉ、", 1547: "おら、", 1558: "あっ、",
    1567: "あっ、", 1634: "", 1644: "", 1652: "", 1660: "", 1669: "",
    1683: "", 1693: "", 1703: "", 1713: "", 1723: "", 1940: "", 1985: "", 1997: "",
    2031: "", 2055: "", 2075: "", 2370: "", 2464: "", 2585: "", 2629: "", 2696: "",
    2708: "", 2720: "", 2732: "", 2811: "", 2814: "あっ……", 2847: "えっ、", 3026: "",
    3040: "", 3054: "", 3065: "うん、", 3076: "",
    3120: "あっ、", 3134: "うん、", 3166: "", 3169: "おぉ、", 3180: "えっ、",
    3245: "あっ……", 3248: "あっ……", 3605: "うん、", 3828: "うん、",
}


# 文頭だけを変えると重複する行は、既存行全体を自然な一文へ整える。
LINE_REPAIRS: dict[int, str] = {
    91: "PRINTFORMW 「転校生しゃんとお喋りだなぁ♪　おら、訛りがひどいげど……気にせず話してぐれて、嬉しいだよ☆」",
    138: "PRINTFORMW 「聞いでくれ、転校生しゃん。今日な、本屋さんで探してた本が見つかったんだ♪　すっごく嬉しくてなぁ！」",
    215: "PRINTFORMW 「転校生しゃんは、おらの欲しいものがよくわかるなぁ。なんだか、嬉しくなっちまうだ♪」",
    315: "PRINTFORMW 「転校生しゃん、何も話さなくても、一緒にいるだけで落ちつくなぁ……えへ♪」",
    632: "PRINTFORMW 「転校生しゃん、ゆっくり歩こうな。えへ、こうしてると、デートみてぇだなぁ……♪」",
    715: "PRINTFORMW 「転校生しゃん、今日は混んでるなぁ。えへ、おらが席取っとくがら、待っでてぐれ♪」",
    827: "PRINTFORMW 「お出かけだなぁ。本土の街は、何度来でも新鮮だぁ。転校生しゃん、いろいろ教えでぐれな♪」",
    1148: "PRINTFORMW 「あぅ……っ、こんな所で、ぎゅって……。でも、こんなとこなのに、こんなに感じちまう……っ」",
    1232: "PRINTFORMW 「あぅ……っ、自分で動くと、奥に……。衣装越しに見られて、恥ずかしいだよぉ……っ」",
    1344: "PRINTFORMW 「あぅ……っ、もぞもぞして、落ちつかねぇだよぉ……。おら、なんだか、変な気分だ……っ」",
    1492: "PRINTFORMW 「あぅ、この衣装……ちょっと際どいだよ転校生しゃん。でも、あんたが見たいなら……えへ♪」",
    1560: "PRINTFORMW 「転校生しゃん、こうやって見つめあってると、言葉なんていらねぇなぁ……♪」",
    3087: "PRINTFORMW 「%LOCALS%の中に出したやつ……？　あぅ、おらが飲むのが……。ん、ごく……変な気分だよ……♪」",
    3098: "PRINTFORMW 「調教者しゃんのやつ……？　あぅ、おらが飲むのが……。ん、ごく……うう、変な気分だなぁ……♪」",
}


def read_lines(path: Path) -> list[str]:
    return path.read_bytes().decode("cp932").splitlines()


def write_lines(path: Path, lines: list[str]) -> None:
    path.write_bytes("\r\n".join(lines).encode("cp932") + b"\r\n")


def normalize(line: str) -> str:
    return line.lstrip().replace("%CALLNAME:ASSI%", "%LOCALS%")


def opener_span(text: str) -> tuple[int, int] | None:
    """「えへ、」「んあ……っ、」など、文頭相槌の範囲を返す。"""
    start = text.find("「")
    if start < 0:
        return None
    if text.startswith("「えへ", start):
        index = start + 3
    elif text.startswith("「んあ", start):
        index = start + 3
    elif text.startswith("「んん", start):
        index = start + 3
    else:
        return None
    if text[index:index + 1] in ("、", "。"):
        return start, index + 1
    if text.startswith("……", index):
        index += 2
    elif text.startswith("…", index):
        index += 1
    else:
        return None
    if text[index:index + 1] == "っ":
        index += 1
    if text[index:index + 1] == "、":
        index += 1
    return start, index


def align_original_to_current(original: list[str], current: list[str]) -> dict[int, int]:
    old = [normalize(line) for line in original]
    new = [normalize(line) for line in current]
    mapping: dict[int, int] = {}
    matcher = difflib.SequenceMatcher(None, old, new, autojunk=False)
    for old_start, new_start, size in matcher.get_matching_blocks():
        for offset in range(size):
            mapping[old_start + offset] = new_start + offset
    return mapping


def apply_line_repairs(original: list[str], before_rewrite: list[str], current: list[str]) -> int:
    mapping = align_original_to_current(original, before_rewrite)
    changed = 0
    for line_no, replacement in sorted(LINE_REPAIRS.items()):
        current_index = mapping.get(line_no - 1)
        if current_index is None:
            raise RuntimeError(f"全体リライト対象の対応付けに失敗: {line_no}")
        current_line = current[current_index]
        indent = current_line[: len(current_line) - len(current_line.lstrip())]
        if normalize(current_line) != replacement:
            current[current_index] = indent + replacement
            changed += 1
    return changed


def main() -> None:
    if not SOURCE.exists():
        raise RuntimeError(f"既存部分の基準バックアップがありません: {SOURCE}")
    original = read_lines(SOURCE)
    current = read_lines(TARGET)
    mapping = align_original_to_current(original, current)
    if BACKUP.exists() and len(current) == len(read_lines(BACKUP)):
        # 初回適用後の再実行では変更済み行が一致ブロックから外れるため、
        # 変更前の同じ行番号を対応付けの補助に使う（行の追加・削除は許可しない）。
        before_rewrite = read_lines(BACKUP)
        backup_mapping = align_original_to_current(original, before_rewrite)
        for old_index, current_index in backup_mapping.items():
            mapping.setdefault(old_index, current_index)
    missing = [line_no for line_no in REWRITES if line_no - 1 not in mapping]
    if missing:
        raise RuntimeError(f"既存行との対応付けに失敗: {missing}")

    changed = 0
    for line_no, replacement in sorted(REWRITES.items()):
        if line_no in LINE_REPAIRS:
            continue
        old_index = line_no - 1
        current_index = mapping[old_index]
        old_text = normalize(original[old_index])
        span = opener_span(old_text)
        if span is None:
            raise RuntimeError(f"文頭相槌を認識できません: {line_no}: {old_text}")
        current_text = normalize(current[current_index])
        expected_text = old_text[: span[0]] + "「" + replacement + old_text[span[1] :]
        if current_text == expected_text:
            continue
        if line_no == 754 and "「おら、おら、" in current_text:
            current[current_index] = current[current_index].replace("「おら、おら、", "「おら、", 1)
            changed += 1
            continue
        current_span = opener_span(current_text)
        if current_span is None or current_text[current_span[0]:current_span[1]] != old_text[span[0]:span[1]]:
            raise RuntimeError(f"現在行が既存行と一致しません: {line_no}: {current_text}")
        indent = current[current_index][: len(current[current_index]) - len(current_text)]
        current[current_index] = indent + current_text[: current_span[0]] + "「" + replacement + current_text[current_span[1] :]
        changed += 1

    if BACKUP.exists():
        changed += apply_line_repairs(original, read_lines(BACKUP), current)

    if changed:
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        if not BACKUP.exists():
            shutil.copy2(TARGET, BACKUP)
        write_lines(TARGET, current)

    print(f"既存台詞の文頭相槌をリライト: {changed}件")


if __name__ == "__main__":
    main()
