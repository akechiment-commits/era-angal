#!/usr/bin/env python3
"""
tools/prompt_*.txt からキャラプロフィール表示ERBを生成する

使い方:
  cd tools
  python generate_profile_erb.py

出力:
  ../ERB/PROFILE_キャラプロフィール.ERB
"""

import re
import glob
from pathlib import Path

OUT_ERB = Path("../ERB/PROFILE_キャラプロフィール.ERB")

FIELDS = ["身長", "体重", "スリーサイズ", "誕生日", "血液型", "部活", "クラス", "好きな色", "家族構成", "趣味", "紹介文"]
UNITS = {"身長": "cm", "体重": "kg"}

def extract_profile(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'【[^】]+のゲーム内プロフィール】\n(.*?)(?=\n【|\Z)', content, re.DOTALL)
    if not m:
        return {}
    profile = {}
    for line in m.group(1).strip().split("\n"):
        line = line.strip()
        if not line.startswith("- "):
            continue
        line = line[2:]
        if ": " in line:
            key, val = line.split(": ", 1)
            key = key.strip()
            val = val.strip()
            if key in FIELDS:
                profile[key] = val
    return profile

def build_char_map():
    """呼び名 → キャラNo"""
    callname_to_no = {}
    for f in sorted(glob.glob("../CSV/Chara[0-9]*.csv")):
        m = re.search(r'Chara(\d+)_', Path(f).name)
        if not m:
            continue
        no = int(m.group(1))
        if no == 0:
            continue
        with open(f, "rb") as fh:
            content = fh.read().decode("cp932", errors="replace")
        for line in content.split("\n"):
            if line.startswith("呼び名,"):
                callname = line.strip().split(",")[1]
                callname_to_no[callname] = no
                break
    return callname_to_no

def wrap_text(text, prefix, width=36):
    """長いテキストを複数のPRINTFORMLに分割"""
    lines_out = []
    # 36文字以内に収まる場合はそのまま
    if len(text) <= width:
        lines_out.append(f'PRINTFORML {prefix}{text}')
        return lines_out
    # 分割
    lines_out.append(f'PRINTFORML {prefix}')
    while text:
        chunk = text[:width]
        text = text[width:]
        lines_out.append(f'PRINTFORML   {chunk}')
    return lines_out

def main():
    callname_to_no = build_char_map()

    # 各キャラのプロフィールを読み込む
    profiles = {}  # キャラNo → {field: value}
    missing = []

    for txt_path in sorted(glob.glob("prompt_*.txt")):
        name = Path(txt_path).stem.replace("prompt_", "")
        if "・" in name:
            continue  # 複数人ファイルはスキップ
        if name not in callname_to_no:
            continue
        no = callname_to_no[name]
        profile = extract_profile(txt_path)
        if profile:
            profiles[no] = profile
        else:
            missing.append(name)

    print(f"プロフィール読み込み: {len(profiles)}人")
    if missing:
        print(f"プロフィールなし: {missing}")

    L = []
    L += [
        ";==================================================",
        "; PROFILE_キャラプロフィール.ERB  (自動生成 - 編集不要)",
        "; generate_profile_erb.py で再生成",
        ";==================================================",
        "",
        "@SHOW_CHAR_PROFILE(ARG)",
        "; ARG:0 = キャラインデックス (CHARANUM内のインデックス)",
        "LOCAL:8 = TARGET",
        "TARGET = ARG:0",
        "LOCAL:1 = NO:TARGET  ;キャラNo(1-71)",
        "DRAWLINE",
        "PRINTFORML 【%NAME:TARGET% プロフィール】",
        "DRAWLINE",
        "SELECTCASE LOCAL:1",
    ]

    for no in sorted(profiles.keys()):
        p = profiles[no]
        L.append(f"CASE {no}")
        for field in FIELDS:
            val = p.get(field, "")
            if not val:
                continue
            unit = UNITS.get(field, "")
            display = f"{field}: {val}{unit}"
            if field == "紹介文":
                L.append(f'PRINTL ')
                L += wrap_text(val, "  ", 38)
            else:
                L.append(f'PRINTFORML {display}')

    L += [
        "CASEELSE",
        "\tPRINTL プロフィールデータなし",
        "ENDSELECT",
        "PRINTL",
        "WAIT",
        "TARGET = LOCAL:8",
        "RETURN 1",
        "",
    ]

    text = "\r\n".join(L) + "\r\n"
    with open(OUT_ERB, "w", encoding="cp932", newline="") as f:
        f.write(text)
    print(f"出力: {OUT_ERB}")

if __name__ == "__main__":
    main()
