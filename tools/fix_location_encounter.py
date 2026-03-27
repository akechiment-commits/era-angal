#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix LOCATION_EVENT.ERB:
- @LOCATION_ENCOUNTER: Replace REPEAT CHARANUM loop with direct char number arrays
  (CHARANUM is only 2, so the loop never finds characters 1-71)
- Add @LOCATION_SOLO_EVENT: Random reward events when nobody is found
"""

import re

SRC = 'ERB/LOCATION_EVENT.ERB'
DST = 'ERB/LOCATION_EVENT.ERB'

# ---------------------------------------------------------------------------
# Character number lists per room (extracted from existing code)
# ---------------------------------------------------------------------------
CLASS_ROOMS = [
    {"name": "1年1組(A組)", "chars": [2,12,24,32,40,60,66]},
    {"name": "1年2組(B組)", "chars": [4,37,38,46,53,57,59,64,71]},
    {"name": "1年3組(C組)", "chars": [20,25,50,51,61,65,67,68]},
    {"name": "2年1組(A組)", "chars": [3,8,16,17,33,34,63]},
    {"name": "2年2組(B組)", "chars": [19,22,39,41,42,62]},
    {"name": "2年3組(C組)", "chars": [1,11,18,30,44,52,56]},
    {"name": "3年1組(A組)", "chars": [10,13,14,15,23,26,29,48,58]},
    {"name": "3年2組(B組)", "chars": [5,6,7,21,27,45,49,69,70]},
    {"name": "3年3組(C組)", "chars": [9,28,31,35,36,43,47,54,55]},
]

CLUB_ROOMS = [
    {"name": "陸上部",             "chars": [1,39,66]},
    {"name": "柔道部",             "chars": [26,30,53]},
    {"name": "テニス部",           "chars": [25,50,58]},
    {"name": "バスケットボール部", "chars": [23,40]},
    {"name": "バレー部",           "chars": [16,42,51]},
    {"name": "弓道部",             "chars": [7,20]},
    {"name": "空手部",             "chars": [71]},
    {"name": "ポーロ部",           "chars": [54]},
    {"name": "ソフトボール部",     "chars": [18,64]},
    {"name": "チアリーディング部", "chars": [31,34,59]},
    {"name": "剣道部",             "chars": [43,45,67]},
    {"name": "水泳部",             "chars": [15,27,44]},
    {"name": "吹奏楽部",           "chars": [36,37,61,70]},
    {"name": "軽音部",             "chars": [9,48,62]},
    {"name": "演劇部",             "chars": [41,57,63]},
    {"name": "料理研究部",         "chars": [2,17,32]},
    {"name": "美術部",             "chars": [3,11,65]},
    {"name": "生物部",             "chars": [6,10]},
    {"name": "書道部",             "chars": [21,33,55]},
    {"name": "図書部",             "chars": [38,60,69]},
    {"name": "写真部",             "chars": [47,56]},
    {"name": "オカルト研究部",     "chars": [24,29,68]},
    {"name": "パソコン部",         "chars": [12]},
    {"name": "放送部",             "chars": [13,14,35]},
    {"name": "文芸部",             "chars": [5,70]},
    {"name": "ラクロス部",         "chars": [4,66]},
    {"name": "天文部",             "chars": [46,52]},
]

COMMITTEE_ROOMS = [
    {"name": "生徒委員会",       "chars": [18,53]},
    {"name": "保健委員会",       "chars": [8,19,25,46]},
    {"name": "マナー委員会",     "chars": [28,55]},
    {"name": "対外委員会",       "chars": [9,52]},
    {"name": "奉仕委員会",       "chars": [6,17,54]},
    {"name": "お楽しみ委員会",   "chars": [4,61]},
    {"name": "選挙管理委員会",   "chars": [40,49,68]},
]

CATEGORY_NAMES = ["教室", "部室", "委員会室"]


def make_room_block(room_id, room_info, is_first):
    """Build IF/ELSEIF block for one room in @LOCATION_ENCOUNTER."""
    chars = room_info["chars"]
    name  = room_info["name"]
    lines = []
    kw = "IF" if is_first else "ELSEIF"
    lines.append(f"\t{kw} TFLAG:84 == {room_id}")
    lines.append(f"\t\tPRINTFORML \u2500\u2500 {name} \u2500\u2500")
    # Set LOCAL:1..N to char numbers, LOCAL:0 = count
    for i, c in enumerate(chars, 1):
        lines.append(f"\t\tLOCAL:{i} = {c}")
    lines.append(f"\t\tLOCAL:0 = {len(chars)}")
    return "\r\n".join(lines)


def make_location_encounter():
    """Generate the full @LOCATION_ENCOUNTER function."""
    L = []
    L.append(";---------------------------------------------------------")
    L.append("; 場所遭遇処理（キャラ番号を直接配列に格納してランダム選択）")
    L.append(";---------------------------------------------------------")
    L.append("@LOCATION_ENCOUNTER")
    L.append("LOCAL:0 = 0")
    L.append("")

    for cat_idx, (rooms, cat_name) in enumerate([
            (CLASS_ROOMS, "教室"),
            (CLUB_ROOMS,  "部室"),
            (COMMITTEE_ROOMS, "委員会室")]):
        kw = "IF" if cat_idx == 0 else "ELSEIF"
        L.append(f"{kw} TFLAG:86 == {cat_idx}\t;{cat_name}")
        for room_id, room_info in enumerate(rooms):
            L.append(make_room_block(room_id, room_info, room_id == 0))
        L.append("\tENDIF")
        L.append("")

    L.append("ENDIF")
    L.append("")
    L.append("; 誰もいなかった→ソロイベント")
    L.append("SIF LOCAL:0 == 0")
    L.append("\tCALL LOCATION_SOLO_EVENT")
    L.append("\tRETURN RESULT")
    L.append("")
    L.append("; ランダムに1人選ぶ（LOCAL:1..N に格納されたキャラ番号から）")
    L.append("A = LOCAL:(RAND:LOCAL:0 + 1)")
    L.append("")
    L.append("; キャラが未ロードなら追加し、インデックスを取得")
    L.append("LOCAL:98 = -1")
    L.append("REPEAT CHARANUM")
    L.append("\tIF NO:COUNT == A")
    L.append("\t\tLOCAL:98 = COUNT")
    L.append("\tENDIF")
    L.append("REND")
    L.append("IF LOCAL:98 < 0")
    L.append("\tADDCHARA A")
    L.append("\tLOCAL:98 = CHARANUM - 1")
    L.append("ENDIF")
    L.append("TFLAG:85 = LOCAL:98")
    L.append("")
    L.append("CALL ENCOUNTER_SCENE")
    L.append("RETURN RESULT")
    L.append("")
    return "\r\n".join(L)


def make_location_solo_event():
    """Generate @LOCATION_SOLO_EVENT with 5 random reward events."""
    L = []
    L.append(";---------------------------------------------------------")
    L.append("; 誰もいない時のランダムご褒美イベント")
    L.append(";---------------------------------------------------------")
    L.append("@LOCATION_SOLO_EVENT")
    L.append("DRAWLINE")
    L.append("A = RAND:5")
    L.append("")
    L.append("IF A == 0")
    L.append("\t; 古い教材発見→知識技能+1")
    L.append("\tPRINTFORML 誰もいなかったが、棚の奥に古い参考書を見つけた。")
    L.append("\tPRINTFORML 読み込んでみると意外な発見があった。")
    L.append("\tPRINTL")
    L.append("\tABL:95 += 1")
    L.append("\tPRINTFORML （知識技能 +1）")
    L.append("ELSEIF A == 1")
    L.append("\t; 自主練→運動技能+1")
    L.append("\tPRINTFORML 誰もいなかった。せっかくなので一人で自主トレをすることにした。")
    L.append("\tPRINTL")
    L.append("\tABL:93 += 1")
    L.append("\tPRINTFORML （運動技能 +1）")
    L.append("ELSEIF A == 2")
    L.append("\t; インスピレーション→表現技能+1")
    L.append("\tPRINTFORML 誰もいなかったが、窓から見える景色に何かを感じた。")
    L.append("\tPRINTFORML 自分の中に新しいイメージが浮かんだ気がする。")
    L.append("\tPRINTL")
    L.append("\tABL:94 += 1")
    L.append("\tPRINTFORML （表現技能 +1）")
    L.append("ELSEIF A == 3")
    L.append("\t; 休憩→体力回復")
    L.append("\tPRINTFORML 誰もいなかった。静かな空間で少し休憩することにした。")
    L.append("\tPRINTFORML 気分がすっきりした。")
    L.append("\tPRINTL")
    L.append("\tIF BASE:0 > 0")
    L.append("\t\tIF PARAM:0 < BASE:0")
    L.append("\t\t\tPARAM:0 += BASE:0 / 5 + 1")
    L.append("\t\t\tSIF PARAM:0 > BASE:0  PARAM:0 = BASE:0")
    L.append("\t\tENDIF")
    L.append("\tENDIF")
    L.append("\tPRINTFORML （体力 少し回復）")
    L.append("ELSE")
    L.append("\t; 不思議な体験→全技能+1（ラッキー）")
    L.append("\tPRINTFORML 誰もいなかった。")
    L.append("\tPRINTFORML しばらくぼーっとしていると、なんだか力が湧いてくる気がした。")
    L.append("\tPRINTL")
    L.append("\tABL:93 += 1")
    L.append("\tABL:94 += 1")
    L.append("\tABL:95 += 1")
    L.append("\tPRINTFORML （ラッキー！ 全技能 +1）")
    L.append("ENDIF")
    L.append("")
    L.append("PRINTL")
    L.append("PRINTFORMW （ターン消費）")
    L.append("RETURN 1")
    L.append("")
    return "\r\n".join(L)


def main():
    # Read existing file
    with open(SRC, 'rb') as f:
        raw = f.read()
    text = raw.decode('cp932').replace('\r\n', '\n').replace('\r', '\n')

    # Split into function blocks by "@" markers
    # Keep everything before @LOCATION_ENCOUNTER
    # Keep @ENCOUNTER_SCENE (and anything after) from original

    # Find position of @LOCATION_ENCOUNTER
    loc_enc_start = text.find('\n@LOCATION_ENCOUNTER')
    if loc_enc_start == -1:
        loc_enc_start = text.find('@LOCATION_ENCOUNTER')
        prefix = ""
    else:
        loc_enc_start += 1  # skip the \n
        prefix = text[:loc_enc_start]

    # Find position of @ENCOUNTER_SCENE
    enc_scene_pos = text.find('\n@ENCOUNTER_SCENE')
    if enc_scene_pos == -1:
        enc_scene_pos = text.find('@ENCOUNTER_SCENE')
        enc_scene = text[enc_scene_pos:]
    else:
        enc_scene = text[enc_scene_pos + 1:]  # skip the \n

    print(f"Prefix ends at:     {loc_enc_start}")
    print(f"ENCOUNTER_SCENE at: {enc_scene_pos}")

    # Build new content
    new_text = (
        prefix
        + make_location_encounter()
        + "\r\n"
        + make_location_solo_event()
        + "\r\n"
        + ";---------------------------------------------------------\r\n"
        + "; 遭遇シーン本体\r\n"
        + "; TFLAG:85 = キャラインデックス\r\n"
        + ";---------------------------------------------------------\r\n"
        + enc_scene
    )

    # Normalise line endings to CRLF
    new_text = new_text.replace('\r\n', '\n').replace('\r', '\n')
    new_text = new_text.replace('\n', '\r\n')

    with open(DST, 'wb') as f:
        f.write(new_text.encode('cp932'))

    print(f"Written {DST} ({len(new_text)} chars)")


if __name__ == '__main__':
    main()
