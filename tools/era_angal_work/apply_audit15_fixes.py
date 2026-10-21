# -*- coding: utf-8 -*-
"""
apply_audit15_fixes.py

Audit #15 Fixes:
1. ERB/RANDOM_S_汎用キャラ素質生成.ERB:
   Fix SIF curiosity/optimism personality roll to IF...ELSEIF...ENDIF.
2. ERB/COMF/COMF392.ERB:
   Fix 9 talent checks in confession calculation from SIF to IF...ENDIF (preventing TIMES B from running unconditionally).
3. ERB/COMF/COMF72.ERB:
   Fix SIF TALENT:141 (爆乳) to IF...ENDIF (preventing SOURCE:6 = 500 from overwriting all breast sizes).
4. ERB/COMF/COMF28.ERB:
   Fix SIF TALENT:85 (恋慕) to IF...ENDIF (preventing TIMES SOURCE:7 and TIMES SOURCE:16 from running unconditionally).
5. ERB/COMF/COMF110.ERB:
   Fix 3 SIF blocks to IF...ENDIF (preventing TIMES SOURCE:14 from running unconditionally).
6. ERB/SELF_セルフトレーニング.ERB:
   Fix SIF ABL:6 >= 3 to IF...ENDIF (preventing GOTJUEL:6 += ... from running unconditionally when ABL:6 < 3).
7. ERB/EVENT_MORNING_朝イベント.ERB:
   Fix 4 SIF TALENT:MASTER:121 || TALENT:MASTER:122 blocks to IF...ENDIF (preventing FLAG:(5800+NO:TARGET) increment for female Masters).
8. ERB/AUTO_TRAIN_オート調教.ERB:
   Fix SIF TFLAG:44 to IF...ENDIF (preventing CHAR_UNDRESS from running when TFLAG:44 == 0).
9. ERB/SOURCE_ソース計算・口上呼び出し.ERB:
   Fix misplaced comment between SIF TEQUIP:15 and TRYCALL EQUIP_COM15.
10. ERB/COMF/COMF21.ERB:
    Remove blank line between SIF and BASE:PLAYER:2 += COURTESAN_EJAC_GAIN.
11. ERB/COMF/COMF22.ERB:
    Remove blank line between SIF and BASE:PLAYER:2 += COURTESAN_EJAC_GAIN.
12. ERB/COMF/COMF30.ERB:
    Remove blank line between SIF and BASE:PLAYER:2 += COURTESAN_EJAC_GAIN.
13. ERB/YU-CTION_オークション.ERB:
    Remove blank line between SIF and BASE:PLAYER:2 += COURTESAN_EJAC_GAIN.
14. ERB/AFTERTRA_後処理.ERB:
    Fix SIF SELECTCOM != 7 to IF...ENDIF in @CMD_VARIETY_TRACK.
"""

import os, glob
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def patch_file(rel_path, old_text, new_text):
    candidates = list(ROOT.glob(rel_path))
    if not candidates:
        raise FileNotFoundError(f"Cannot find {rel_path}")
    path = candidates[0]
    with open(path, "r", encoding="cp932", newline="") as f:
        content = f.read()
    if old_text not in content:
        if new_text in content:
            print(f"[ALREADY PATCHED] {path.name}")
            return
        raise ValueError(f"Target text not found in {path.name}:\n{repr(old_text[:100])}...")
    content = content.replace(old_text, new_text, 1)
    with open(path, "w", encoding="cp932", newline="") as f:
        f.write(content)
    print(f"[PATCHED] {path.name}")

def main():
    # 1. RANDOM_S
    old_random_s = (
        "\tELSEIF O == 5\r\n"
        "\t\t;好奇心・楽観的\r\n"
        "\t\tP = RAND:2\r\n"
        "\t\tSIF P == 0\r\n"
        "\t\t\tTALENT:23 = 1\r\n"
        "\t\t\tTALENT:25 = 0\r\n"
        "\t\tP = RAND:3\r\n"
        "\t\tSIF P == 0\r\n"
        "\t\t\tTALENT:25 = 1\r\n"
        "\t\t\tTALENT:23 = 0"
    )
    new_random_s = (
        "\tELSEIF O == 5\r\n"
        "\t\t;好奇心・楽観的\r\n"
        "\t\tP = RAND:3\r\n"
        "\t\tIF P == 0\r\n"
        "\t\t\tTALENT:23 = 1\r\n"
        "\t\t\tTALENT:25 = 0\r\n"
        "\t\tELSEIF P == 1\r\n"
        "\t\t\tTALENT:25 = 1\r\n"
        "\t\t\tTALENT:23 = 0\r\n"
        "\t\tENDIF"
    )
    patch_file("ERB/*RANDOM_S*.ERB", old_random_s, new_random_s)

    # 2. COMF392
    old_comf392 = (
        "\t;臆病\r\n"
        "\tSIF TALENT:10\t; 【[臆病]】\r\n"
        "\t\tTIMES A , 0.80\r\n"
        "\t\tTIMES B , 0.80\r\n"
        "\t;反抗的\r\n"
        "\tSIF TALENT:11 == 1\t; 【[反抗的]】\r\n"
        "\t\tTIMES A , 1.50\r\n"
        "\t\tTIMES B , 0.80\r\n"
        "\t;プライド高い\r\n"
        "\tSIF TALENT:15 == 1\t; 【[プライド高い]】\r\n"
        "\t\tTIMES A , 1.50\r\n"
        "\t;プライド低い\r\n"
        "\tSIF TALENT:17\t; 【[プライド低い]】\r\n"
        "\t\tTIMES A , 0.50\r\n"
        "\r\n"
        "\t;自制心\r\n"
        "\tSIF TALENT:20 == 1\t; 【[自制心]】\r\n"
        "\t\tTIMES A , 1.50\r\n"
        "\r\n"
        "\t;感情乏しい\r\n"
        "\tSIF TALENT:22\t; 【[感情乏しい]】\r\n"
        "\t\tTIMES A , 0.50\r\n"
        "\t\tTIMES B , 0.50\r\n"
        "\t;目立ちたがり\r\n"
        "\tSIF TALENT:28\t; 【[目立ちたがり]】\r\n"
        "\t\tTIMES A , 0.50\r\n"
        "\t\tTIMES B , 0.80\r\n"
        "\t;抑圧\r\n"
        "\tSIF TALENT:32 == 1\t; 【[抑圧]】\r\n"
        "\t\tTIMES A , 2.00\r\n"
        "\t\tTIMES B , 0.80\r\n"
        "\r\n"
        "\t;抵抗\r\n"
        "\tSIF TALENT:34 == 1\t; 【[抵抗]】\r\n"
        "\t\tTIMES A , 2.00\r\n"
        "\t\tTIMES B , 0.50\r\n"
        "\t;恥じらい\r\n"
        "\tSIF TALENT:35\t; 【[恥じらい]】\r\n"
        "\t\tTIMES A , 2.50\r\n"
        "\t\tTIMES B , 1.50\r\n"
        "\r\n"
        "\t;恥薄い\r\n"
        "\tSIF TALENT:36\t; 【[恥薄い]】\r\n"
        "\t\tTIMES A , 0.80\r\n"
        "\t\tTIMES B , 0.50\r\n"
        "\t;痛みに弱い\r\n"
        "\tSIF TALENT:40\t; 【[痛みに弱い]】\r\n"
        "\t\tTIMES A , 1.50\r\n"
        "\t;痛みに強い\r\n"
        "\tSIF TALENT:41\t; 【[痛みに強い]】\r\n"
        "\t\tTIMES A , 0.80\r\n"
        "\r\n"
        "\t;倒錯的\r\n"
        "\tSIF TALENT:80\t; 【[倒錯的]】\r\n"
        "\t\tTIMES A , 0.50\r\n"
        "\t\tTIMES B , 2.00"
    )
    new_comf392 = (
        "\t;臆病\r\n"
        "\tIF TALENT:10\t; 【[臆病]】\r\n"
        "\t\tTIMES A , 0.80\r\n"
        "\t\tTIMES B , 0.80\r\n"
        "\tENDIF\r\n"
        "\t;反抗的\r\n"
        "\tIF TALENT:11 == 1\t; 【[反抗的]】\r\n"
        "\t\tTIMES A , 1.50\r\n"
        "\t\tTIMES B , 0.80\r\n"
        "\tENDIF\r\n"
        "\t;プライド高い\r\n"
        "\tSIF TALENT:15 == 1\t; 【[プライド高い]】\r\n"
        "\t\tTIMES A , 1.50\r\n"
        "\t;プライド低い\r\n"
        "\tSIF TALENT:17\t; 【[プライド低い]】\r\n"
        "\t\tTIMES A , 0.50\r\n"
        "\r\n"
        "\t;自制心\r\n"
        "\tSIF TALENT:20 == 1\t; 【[自制心]】\r\n"
        "\t\tTIMES A , 1.50\r\n"
        "\r\n"
        "\t;感情乏しい\r\n"
        "\tIF TALENT:22\t; 【[感情乏しい]】\r\n"
        "\t\tTIMES A , 0.50\r\n"
        "\t\tTIMES B , 0.50\r\n"
        "\tENDIF\r\n"
        "\t;目立ちたがり\r\n"
        "\tIF TALENT:28\t; 【[目立ちたがり]】\r\n"
        "\t\tTIMES A , 0.50\r\n"
        "\t\tTIMES B , 0.80\r\n"
        "\tENDIF\r\n"
        "\t;抑圧\r\n"
        "\tIF TALENT:32 == 1\t; 【[抑圧]】\r\n"
        "\t\tTIMES A , 2.00\r\n"
        "\t\tTIMES B , 0.80\r\n"
        "\tENDIF\r\n"
        "\r\n"
        "\t;抵抗\r\n"
        "\tIF TALENT:34 == 1\t; 【[抵抗]】\r\n"
        "\t\tTIMES A , 2.00\r\n"
        "\t\tTIMES B , 0.50\r\n"
        "\tENDIF\r\n"
        "\t;恥じらい\r\n"
        "\tIF TALENT:35\t; 【[恥じらい]】\r\n"
        "\t\tTIMES A , 2.50\r\n"
        "\t\tTIMES B , 1.50\r\n"
        "\tENDIF\r\n"
        "\r\n"
        "\t;恥薄い\r\n"
        "\tIF TALENT:36\t; 【[恥薄い]】\r\n"
        "\t\tTIMES A , 0.80\r\n"
        "\t\tTIMES B , 0.50\r\n"
        "\tENDIF\r\n"
        "\t;痛みに弱い\r\n"
        "\tSIF TALENT:40\t; 【[痛みに弱い]】\r\n"
        "\t\tTIMES A , 1.50\r\n"
        "\t;痛みに強い\r\n"
        "\tSIF TALENT:41\t; 【[痛みに強い]】\r\n"
        "\t\tTIMES A , 0.80\r\n"
        "\r\n"
        "\t;倒錯的\r\n"
        "\tIF TALENT:80\t; 【[倒錯的]】\r\n"
        "\t\tTIMES A , 0.50\r\n"
        "\t\tTIMES B , 2.00\r\n"
        "\tENDIF"
    )
    patch_file("ERB/COMF/COMF392.ERB", old_comf392, new_comf392)

    # 3. COMF72
    old_comf72 = (
        ";爆乳\r\n"
        "SIF TALENT:141\t; 【[爆乳]】\r\n"
        "\tTIMES A , 0.80\r\n"
        "\tSOURCE:6 = 500\r\n"
        ";巨乳"
    )
    new_comf72 = (
        ";爆乳\r\n"
        "IF TALENT:141\t; 【[爆乳]】\r\n"
        "\tTIMES A , 0.80\r\n"
        "\tSOURCE:6 = 500\r\n"
        "ENDIF\r\n"
        ";巨乳"
    )
    patch_file("ERB/COMF/COMF72.ERB", old_comf72, new_comf72)

    # 4. COMF28
    old_comf28 = (
        "SIF TALENT:85\t; 【[恋慕]】\r\n"
        "\tTIMES SOURCE:3 , 3.00\r\n"
        "\tTIMES SOURCE:7 , 2.00\r\n"
        "\tTIMES SOURCE:16 , 2.00\r\n"
    )
    new_comf28 = (
        "IF TALENT:85\t; 【[恋慕]】\r\n"
        "\tTIMES SOURCE:3 , 3.00\r\n"
        "\tTIMES SOURCE:7 , 2.00\r\n"
        "\tTIMES SOURCE:16 , 2.00\r\n"
        "ENDIF\r\n"
    )
    patch_file("ERB/COMF/COMF28.ERB", old_comf28, new_comf28)

    # 5. COMF110
    old_comf110_1 = (
        "SIF TALENT:80\t; 【[倒錯的]】\r\n"
        "\tTIMES SOURCE:12 , 1.50\r\n"
        "\tTIMES SOURCE:14 , 1.20\r\n"
    )
    new_comf110_1 = (
        "IF TALENT:80\t; 【[倒錯的]】\r\n"
        "\tTIMES SOURCE:12 , 1.50\r\n"
        "\tTIMES SOURCE:14 , 1.20\r\n"
        "ENDIF\r\n"
    )
    patch_file("ERB/COMF/COMF110.ERB", old_comf110_1, new_comf110_1)

    old_comf110_2 = (
        "SIF TALENT:21\t; 【[無関心]】\r\n"
        "\tTIMES SOURCE:12 , 0.80\r\n"
        "\tTIMES SOURCE:14 , 0.80\r\n"
        ";倒錯的\r\n"
        "SIF TALENT:80\t; 【[倒錯的]】\r\n"
        "\tTIMES SOURCE:12 , 1.50\r\n"
        "\tTIMES SOURCE:14 , 1.20\r\n"
    )
    new_comf110_2 = (
        "IF TALENT:21\t; 【[無関心]】\r\n"
        "\tTIMES SOURCE:12 , 0.80\r\n"
        "\tTIMES SOURCE:14 , 0.80\r\n"
        "ENDIF\r\n"
        ";倒錯的\r\n"
        "IF TALENT:80\t; 【[倒錯的]】\r\n"
        "\tTIMES SOURCE:12 , 1.50\r\n"
        "\tTIMES SOURCE:14 , 1.20\r\n"
        "ENDIF\r\n"
    )
    patch_file("ERB/COMF/COMF110.ERB", old_comf110_2, new_comf110_2)

    # 6. SELF
    old_self = (
        "ELSE\r\n"
        "\tSIF ABL:6 >= 3\t; 【[奉仕精神]Lv>=3】\r\n"
        "\t\tPRINTFORML %PALAMNAME:6%の珠＋{N:1*150}\r\n"
        "\t\tGOTJUEL:6 += N:1*150\r\n"
        "ENDIF"
    )
    new_self = (
        "ELSE\r\n"
        "\tIF ABL:6 >= 3\t; 【[奉仕精神]Lv>=3】\r\n"
        "\t\tPRINTFORML %PALAMNAME:6%の珠＋{N:1*150}\r\n"
        "\t\tGOTJUEL:6 += N:1*150\r\n"
        "\tENDIF\r\n"
        "ENDIF"
    )
    patch_file("ERB/SELF_*.ERB", old_self, new_self)

    # 7. EVENT_MORNING (4 places)
    old_morn1 = (
        "\t\tSIF TALENT:MASTER:121 || TALENT:MASTER:122\t; 【MASTER:[ふたなり] / MASTER:[オトコ]】\r\n"
        "\t\t\tFLAG:5040 += A * (8 + RAND:5)\r\n"
        "\t\t\tFLAG:(5800 + NO:TARGET) += A * (8 + RAND:5)\r\n"
    )
    new_morn1 = (
        "\t\tIF TALENT:MASTER:121 || TALENT:MASTER:122\t; 【MASTER:[ふたなり] / MASTER:[オトコ]】\r\n"
        "\t\t\tFLAG:5040 += A * (8 + RAND:5)\r\n"
        "\t\t\tFLAG:(5800 + NO:TARGET) += A * (8 + RAND:5)\r\n"
        "\t\tENDIF\r\n"
    )
    path_morn = list(ROOT.glob("ERB/*EVENT_MORNING*.ERB"))[0]
    with open(path_morn, "r", encoding="cp932", newline="") as f:
        morn_content = f.read()
    
    old_morn2 = (
        "\t\t\tSIF TALENT:MASTER:121 || TALENT:MASTER:122\t; 【MASTER:[ふたなり] / MASTER:[オトコ]】\r\n"
        "\t\t\t\tFLAG:5040 += A * (4 + RAND:3)\r\n"
        "\t\t\t\tFLAG:(5800 + NO:TARGET) += A * (4 + RAND:3)\r\n"
    )
    new_morn2 = (
        "\t\t\tIF TALENT:MASTER:121 || TALENT:MASTER:122\t; 【MASTER:[ふたなり] / MASTER:[オトコ]】\r\n"
        "\t\t\t\tFLAG:5040 += A * (4 + RAND:3)\r\n"
        "\t\t\t\tFLAG:(5800 + NO:TARGET) += A * (4 + RAND:3)\r\n"
        "\t\t\tENDIF\r\n"
    )

    old_morn3 = (
        "\t\t\tSIF TALENT:MASTER:121 || TALENT:MASTER:122\t; 【MASTER:[ふたなり] / MASTER:[オトコ]】\r\n"
        "\t\t\t\tFLAG:5040 += A * (8 + RAND:5)\r\n"
        "\t\t\t\tFLAG:(5800 + NO:TARGET) += A * (8 + RAND:5)\r\n"
    )
    new_morn3 = (
        "\t\t\tIF TALENT:MASTER:121 || TALENT:MASTER:122\t; 【MASTER:[ふたなり] / MASTER:[オトコ]】\r\n"
        "\t\t\t\tFLAG:5040 += A * (8 + RAND:5)\r\n"
        "\t\t\t\tFLAG:(5800 + NO:TARGET) += A * (8 + RAND:5)\r\n"
        "\t\t\tENDIF\r\n"
    )
    
    old_morn4 = (
        "\t\t\tSIF TALENT:MASTER:121 || TALENT:MASTER:122\t; 【MASTER:[ふたなり] / MASTER:[オトコ]】\r\n"
        "\t\t\t\tFLAG:5040 += A * (16 + RAND:9)\r\n"
        "\t\t\t\tFLAG:(5800 + NO:TARGET) += A * (16 + RAND:9)\r\n"
    )
    new_morn4 = (
        "\t\t\tIF TALENT:MASTER:121 || TALENT:MASTER:122\t; 【MASTER:[ふたなり] / MASTER:[オトコ]】\r\n"
        "\t\t\t\tFLAG:5040 += A * (16 + RAND:9)\r\n"
        "\t\t\t\tFLAG:(5800 + NO:TARGET) += A * (16 + RAND:9)\r\n"
        "\t\t\tENDIF\r\n"
    )

    for o, n in [(old_morn1, new_morn1), (old_morn2, new_morn2), (old_morn3, new_morn3), (old_morn4, new_morn4)]:
        if o not in morn_content:
            if n in morn_content:
                continue
            raise ValueError(f"Could not find {repr(o[:40])} in EVENT_MORNING")
        morn_content = morn_content.replace(o, n, 1)

    with open(path_morn, "w", encoding="cp932", newline="") as f:
        f.write(morn_content)
    print(f"[PATCHED] {path_morn.name}")

    # 8. AUTO_TRAIN
    old_auto = (
        "SIF TFLAG:44\t; 【[ウフフ中]】\r\n"
        "\tCALL GET_OUT_MOVIE\r\n"
        "\tTRYCALLFORM CHAR_UNDRESS_{NO:TARGET}\r\n"
        "RETURN 0"
    )
    new_auto = (
        "IF TFLAG:44\t; 【[ウフフ中]】\r\n"
        "\tCALL GET_OUT_MOVIE\r\n"
        "\tTRYCALLFORM CHAR_UNDRESS_{NO:TARGET}\r\n"
        "ENDIF\r\n"
        "RETURN 0"
    )
    patch_file("ERB/*AUTO_TRAIN*.ERB", old_auto, new_auto)

    # 9. SOURCE
    old_source = (
        "SIF TEQUIP:15\t; 【[クリップローター]使用中】\r\n"
        ";二プルキャップ装着中\r\n"
        "\tTRYCALL EQUIP_COM15"
    )
    new_source = (
        ";ニプルキャップ装着中\r\n"
        "SIF TEQUIP:15\t; 【[クリップローター]使用中】\r\n"
        "\tTRYCALL EQUIP_COM15"
    )
    patch_file("ERB/*SOURCE*.ERB", old_source, new_source)

    # 10. COMF21
    old_comf21 = (
        "SIF TALENT:PLAYER:121 || TALENT:PLAYER:122\t; 【PLAYER:[ふたなり] / PLAYER:[オトコ]】\r\n"
        "\t\r\n"
        "BASE:PLAYER:2 += COURTESAN_EJAC_GAIN(B, TARGET, PLAYER)"
    )
    new_comf21 = (
        "SIF TALENT:PLAYER:121 || TALENT:PLAYER:122\t; 【PLAYER:[ふたなり] / PLAYER:[オトコ]】\r\n"
        "\tBASE:PLAYER:2 += COURTESAN_EJAC_GAIN(B, TARGET, PLAYER)"
    )
    patch_file("ERB/COMF/COMF21.ERB", old_comf21, new_comf21)

    # 11. COMF22
    old_comf22 = (
        "SIF TALENT:PLAYER:119 || TALENT:PLAYER:122  || TALENT:PLAYER:121\t; 【PLAYER:[半人半妖] / PLAYER:[オトコ] / PLAYER:[ふたなり]】\r\n"
        "\t\r\n"
        "BASE:PLAYER:2 += COURTESAN_EJAC_GAIN(B, TARGET, PLAYER)"
    )
    new_comf22 = (
        "SIF TALENT:PLAYER:122 || TALENT:PLAYER:121\t; 【PLAYER:[オトコ] / PLAYER:[ふたなり]】\r\n"
        "\tBASE:PLAYER:2 += COURTESAN_EJAC_GAIN(B, TARGET, PLAYER)"
    )
    patch_file("ERB/COMF/COMF22.ERB", old_comf22, new_comf22)

    # 12. COMF30
    old_comf30 = (
        "SIF TALENT:PLAYER:119 || TALENT:PLAYER:122  || TALENT:PLAYER:121\t; 【PLAYER:[半人半妖] / PLAYER:[オトコ] / PLAYER:[ふたなり]】\r\n"
        "\t\r\n"
        "BASE:PLAYER:2 += COURTESAN_EJAC_GAIN(B, TARGET, PLAYER)"
    )
    new_comf30 = (
        "SIF TALENT:PLAYER:122 || TALENT:PLAYER:121\t; 【PLAYER:[オトコ] / PLAYER:[ふたなり]】\r\n"
        "\tBASE:PLAYER:2 += COURTESAN_EJAC_GAIN(B, TARGET, PLAYER)"
    )
    patch_file("ERB/COMF/COMF30.ERB", old_comf30, new_comf30)

    # 13. YU-CTION
    old_yuction = (
        "\tSIF TALENT:PLAYER:119 || TALENT:PLAYER:122  || TALENT:PLAYER:121\t; 【PLAYER:[半人半妖] / PLAYER:[オトコ] / PLAYER:[ふたなり]】\r\n"
        "\t\t\r\n"
        "BASE:PLAYER:2 += COURTESAN_EJAC_GAIN(B, TARGET, PLAYER)"
    )
    new_yuction = (
        "\tSIF TALENT:PLAYER:122 || TALENT:PLAYER:121\t; 【PLAYER:[オトコ] / PLAYER:[ふたなり]】\r\n"
        "\t\tBASE:PLAYER:2 += COURTESAN_EJAC_GAIN(B, TARGET, PLAYER)"
    )
    patch_file("ERB/*YU-CTION*.ERB", old_yuction, new_yuction)

    # 14. AFTERTRA
    old_aftertra = (
        "@CMD_VARIETY_TRACK\r\n"
        ";未使用コマンドなら種類数カウント、FLAG:(16010+SELECTCOM)を使用済みマーク\r\n"
        "SIF SELECTCOM != 7 && FLAG:(16010 + SELECTCOM) == 0\t; 【コマンド:[何もしない]以外】\r\n"
        "\tFLAG:16002 += 1\r\n"
        "\tFLAG:(16010 + SELECTCOM) = 1\r\n"
        "RETURN 0"
    )
    new_aftertra = (
        "@CMD_VARIETY_TRACK\r\n"
        ";未使用コマンドなら種類数カウント、FLAG:(16010+SELECTCOM)を使用済みマーク\r\n"
        "IF SELECTCOM != 7 && FLAG:(16010 + SELECTCOM) == 0\t; 【コマンド:[何もしない]以外】\r\n"
        "\tFLAG:16002 += 1\r\n"
        "\tFLAG:(16010 + SELECTCOM) = 1\r\n"
        "ENDIF\r\n"
        "RETURN 0"
    )
    patch_file("ERB/*AFTERTRA*.ERB", old_aftertra, new_aftertra)

    print("\nAll 14 patches successfully processed!")

if __name__ == "__main__":
    main()
