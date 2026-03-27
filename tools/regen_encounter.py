#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenerate @LOCATION_ENCOUNTER in LOCATION_EVENT.ERB using correct
character→club/class/committee mappings from character_data.csv.
Also fixes: SIF BASE:0 > MAXBASE:0  BASE:0 = MAXBASE:0 syntax error.
"""

# ---- Correct data from actual CSV/Chara*.csv files ----------------------
# Classes (character numbers from game CSV, cross-referenced with class data)
CLASS_ROOMS = [
    {"name": "1年A組", "chars": [1, 2, 3, 4, 5, 6, 7]},
    {"name": "1年B組", "chars": [8, 9, 10, 11, 12, 13, 14, 15]},
    {"name": "1年C組", "chars": [16, 17, 18, 19, 20, 21, 22, 23]},
    {"name": "2年A組", "chars": [24, 25, 26, 27, 28, 29, 30]},
    {"name": "2年B組", "chars": [31, 32, 33, 34, 35, 36, 37]},
    {"name": "2年C組", "chars": [38, 39, 40, 41, 42, 43, 44]},
    {"name": "3年A組", "chars": [45, 46, 47, 48, 49, 50, 51, 52, 53]},
    {"name": "3年B組", "chars": [54, 55, 56, 57, 58, 59, 60, 61, 62]},
    {"name": "3年C組", "chars": [63, 64, 65, 66, 67, 68, 69, 70, 71]},
]

# Clubs in submenu order (from CSTR,25 in each Chara CSV file)
CLUB_ROOMS = [
    {"name": "ラクロス部",        "chars": [7, 33, 38]},
    {"name": "剣道部",            "chars": [12, 41, 50]},
    {"name": "テニス部",          "chars": [17, 18, 53]},
    {"name": "バスケットボール部","chars": [5, 49]},
    {"name": "バレー部",          "chars": [19, 26, 35]},
    {"name": "柔道部",            "chars": [16, 56]},
    {"name": "空手部",            "chars": [37]},
    {"name": "弓道部",            "chars": [69]},
    {"name": "ソフトボール部",    "chars": [15, 40]},
    {"name": "チアリーディング部","chars": [14, 29, 67]},
    {"name": "水泳部",            "chars": [22, 59, 71]},
    {"name": "陸上部",            "chars": [42, 48, 57]},
    {"name": "軽音部",            "chars": [9, 20, 62, 66]},
    {"name": "演劇部",            "chars": [36, 52, 63]},
    {"name": "合唱部",            "chars": [13, 30, 34]},
    {"name": "吹奏楽部",          "chars": [1, 4, 27]},
    {"name": "美術部",            "chars": [21, 24, 39]},
    {"name": "茶道部",            "chars": [45, 55]},
    {"name": "天文部",            "chars": [28, 58, 70]},
    {"name": "文芸部",            "chars": [6, 10, 61]},
    {"name": "新聞部",            "chars": [44, 68]},
    {"name": "料理研究部",        "chars": [3, 23, 51]},
    {"name": "パソコン部",        "chars": [2]},
    {"name": "オカルト研究部",    "chars": [46, 47, 65]},
    {"name": "生物部",            "chars": [54]},
    {"name": "放送部",            "chars": [8]},
    {"name": "園芸部",            "chars": [11, 43]},
]

# Committees: submenu order, mapped from character_data.csv committee fields
# (体育→生徒委員会, 美化→マナー委員会, 緑化→対外委員会,
#  風紀→奉仕委員会, 図書→お楽しみ委員会)
COMMITTEE_ROOMS = [
    {"name": "生徒委員会",      "chars": [12, 40]},         # 体育委員会
    {"name": "保健委員会",      "chars": [11, 17, 25, 31]},
    {"name": "マナー委員会",    "chars": [27, 55, 69]},     # 美化委員会
    {"name": "対外委員会",      "chars": [43, 63]},         # 緑化委員会
    {"name": "奉仕委員会",      "chars": [5, 23, 60]},      # 風紀委員会
    {"name": "お楽しみ委員会",  "chars": [64, 70]},         # 図書委員会
    {"name": "選挙管理委員会",  "chars": [8, 20]},
]

CATEGORIES = [
    ("教室",    CLASS_ROOMS),
    ("部室",    CLUB_ROOMS),
    ("委員会室", COMMITTEE_ROOMS),
]


def make_room_block(room_id, room_info, is_first):
    chars = room_info["chars"]
    name  = room_info["name"]
    lines = []
    kw = "\tIF" if is_first else "\tELSEIF"
    lines.append(f"{kw} TFLAG:84 == {room_id}")
    lines.append(f"\t\tPRINTFORML \u2500\u2500 {name} \u2500\u2500")
    for i, c in enumerate(chars, 1):
        lines.append(f"\t\tLOCAL:{i} = {c}")
    lines.append(f"\t\tLOCAL:0 = {len(chars)}")
    return "\r\n".join(lines)


def make_encounter():
    L = []
    L.append(";---------------------------------------------------------")
    L.append("; 場所遭遇処理（キャラ番号を直接配列に格納してランダム選択）")
    L.append(";---------------------------------------------------------")
    L.append("@LOCATION_ENCOUNTER")
    L.append("LOCAL:0 = 0")
    L.append("")

    for cat_idx, (cat_name, rooms) in enumerate(CATEGORIES):
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
    L.append("B = LOCAL:0")
    L.append("A = LOCAL:(RAND:B + 1)")
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


def make_solo_event():
    L = []
    L.append(";---------------------------------------------------------")
    L.append("; 誰もいない時のランダムご褒美イベント")
    L.append(";---------------------------------------------------------")
    L.append("@LOCATION_SOLO_EVENT")
    L.append("DRAWLINE")
    L.append("A = RAND:5")
    L.append("")
    L.append("IF A == 0")
    L.append("\tPRINTFORML 誰もいなかったが、棚の奥に古い参考書を発見した。")
    L.append("\tPRINTFORML 読み込んでみると意外な発見があった。")
    L.append("\tPRINTL")
    L.append("\tABL:95 += 1")
    L.append("\tPRINTFORML （知識技能 +1）")
    L.append("ELSEIF A == 1")
    L.append("\tPRINTFORML 誰もいなかった。せっかくなので一人で自主トレをすることにした。")
    L.append("\tPRINTL")
    L.append("\tABL:93 += 1")
    L.append("\tPRINTFORML （運動技能 +1）")
    L.append("ELSEIF A == 2")
    L.append("\tPRINTFORML 誰もいなかったが、窓から見える景色に何かを感じた。")
    L.append("\tPRINTFORML 自分の中に新しいイメージが浮かんだ気がする。")
    L.append("\tPRINTL")
    L.append("\tABL:94 += 1")
    L.append("\tPRINTFORML （表現技能 +1）")
    L.append("ELSEIF A == 3")
    L.append("\tPRINTFORML 誰もいなかった。静かな空間で少し休憩することにした。")
    L.append("\tPRINTFORML 気分がすっきりした。")
    L.append("\tPRINTL")
    L.append("\tIF BASE:0 < MAXBASE:0")
    L.append("\t\tBASE:0 += MAXBASE:0 / 5 + 1")
    # FIX: use IF/ENDIF instead of SIF for assignment
    L.append("\t\tIF BASE:0 > MAXBASE:0")
    L.append("\t\t\tBASE:0 = MAXBASE:0")
    L.append("\t\tENDIF")
    L.append("\tENDIF")
    L.append("\tPRINTFORML （体力 少し回復）")
    L.append("ELSE")
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
    import re

    with open('ERB/LOCATION_EVENT.ERB', 'rb') as f:
        text = f.read().decode('cp932')

    # Find prefix (everything up to @LOCATION_ENCOUNTER)
    # Use line-start match to avoid matching inside comments
    pos = text.find('\r\n@LOCATION_ENCOUNTER\r\n')
    if pos == -1:
        pos = text.find('\n@LOCATION_ENCOUNTER\n')
        crlf = False
    else:
        crlf = True

    if pos == -1:
        print("ERROR: @LOCATION_ENCOUNTER not found")
        return

    prefix = text[:pos + 2]  # include the \r\n before the label

    # Find @ENCOUNTER_SCENE
    enc_pos = text.find('\r\n@ENCOUNTER_SCENE\r\n')
    if enc_pos == -1:
        enc_pos = text.find('\n@ENCOUNTER_SCENE\n')
    enc_section = text[enc_pos + 2:]  # from @ENCOUNTER_SCENE onwards

    print(f"Prefix ends at {pos}, ENCOUNTER_SCENE at {enc_pos}")

    separator = (
        ";---------------------------------------------------------\r\n"
        "; 遭遇シーン本体\r\n"
        "; TFLAG:85 = キャラインデックス\r\n"
        ";---------------------------------------------------------\r\n"
    )

    new_text = (
        prefix
        + make_encounter().replace('\n', '\r\n').replace('\r\r\n', '\r\n')
        + "\r\n"
        + make_solo_event().replace('\n', '\r\n').replace('\r\r\n', '\r\n')
        + "\r\n"
        + separator
        + enc_section
    )

    with open('ERB/LOCATION_EVENT.ERB', 'wb') as f:
        f.write(new_text.encode('cp932'))
    print("LOCATION_EVENT.ERB rewritten.")


if __name__ == '__main__':
    main()
