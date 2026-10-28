#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rebuild @LOCATION_ENCOUNTER in LOCATION_EVENT.ERB with correct char mappings.
Reads character_data.csv to build club/class/committee → char number lists.
Also fixes SIF BASE:0 > MAXBASE:0 syntax error.
"""
import csv, re

# ---- Read character data -----------------------------------------------
# Columns: name,height,weight,three_sizes,birthday,blood_type,
#          club,committee,class,grade,...
chars = {}  # char_no → {club, committee, class}
with open('tools/character_data.csv', newline='', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, start=1):  # char numbers start at 1
        chars[i] = {
            'name': row['name'],
            'club': row['club'].strip(),
            'committee': row['committee'].strip(),
            'class': row['class'].strip(),
        }

# ---- Build maps ----------------------------------------------------------
# club_name → sorted list of char numbers
club_map = {}
for cno, d in chars.items():
    c = d['club']
    if c:
        club_map.setdefault(c, []).append(cno)

committee_map = {}
for cno, d in chars.items():
    cm = d['committee']
    if cm:
        committee_map.setdefault(cm, []).append(cno)

class_map = {}
for cno, d in chars.items():
    cl = d['class']
    if cl:
        class_map.setdefault(cl, []).append(cno)

print("Clubs found:")
for k, v in sorted(club_map.items()):
    print(f"  {k}: {v}")
print()
print("Committees found:")
for k, v in sorted(committee_map.items()):
    print(f"  {k}: {v}")
print()
print("Classes found:")
for k, v in sorted(class_map.items()):
    print(f"  {k}: {v}")

# ---- Define submenu order (must match LOCATION_EVENT.ERB submenus) ------
# From screenshot of LOCATION_SUBMENU_CLUB:
CLUB_ORDER = [
    "ラクロス部",        # 0
    "剣道部",            # 1
    "テニス部",          # 2
    "バスケットボール部",# 3
    "バレー部",          # 4
    "柔道部",            # 5
    "空手部",            # 6
    "弓道部",            # 7
    "ソフトボール部",    # 8
    "チアリーディング部",# 9
    "水泳部",            # 10
    "陸上部",            # 11
    "軽音部",            # 12
    "演劇部",            # 13
    "合唱部",            # 14
    "吹奏楽部",          # 15
    "美術部",            # 16
    "茶道部",            # 17
    "天文部",            # 18
    "文芸部",            # 19
    "新聞部",            # 20
    "料理研究部",        # 21
    "パソコン部",        # 22
    "オカルト研究部",    # 23
    "生物部",            # 24
    "放送部",            # 25
    "園芸部",            # 26
]

# Classes in order (matches LOCATION_SUBMENU_CLASS):
CLASS_ORDER = [
    "1-A",  # 0
    "1-B",  # 1
    "1-C",  # 2
    "2-A",  # 3
    "2-B",  # 4
    "2-C",  # 5
    "3-A",  # 6
    "3-B",  # 7
    "3-C",  # 8
]
CLASS_DISPLAY = [
    "1年1組(A組)", "1年2組(B組)", "1年3組(C組)",
    "2年1組(A組)", "2年2組(B組)", "2年3組(C組)",
    "3年1組(A組)", "3年2組(B組)", "3年3組(C組)",
]

# Committees (matches LOCATION_SUBMENU_COMMITTEE):
COMMITTEE_ORDER = [
    "生徒委員会",       # 0  (生徒会)
    "保健委員会",       # 1
    "マナー委員会",     # 2  (美化委員会?)
    "対外委員会",       # 3
    "奉仕委員会",       # 4  (風紀委員会?)
    "お楽しみ委員会",   # 5
    "選挙管理委員会",   # 6
]

# Check for partial/alternate committee name matches
def find_committee(name):
    """Find committee chars allowing partial match."""
    if name in committee_map:
        return committee_map[name]
    # Try contains match
    for k, v in committee_map.items():
        if name in k or k in name:
            return v
    return []

print("\n--- Checking club mappings ---")
for i, cn in enumerate(CLUB_ORDER):
    chars_list = club_map.get(cn, [])
    print(f"  [{i:2d}] {cn}: {chars_list}")

print("\n--- Checking committee mappings ---")
for i, cn in enumerate(COMMITTEE_ORDER):
    chars_list = find_committee(cn)
    print(f"  [{i}] {cn}: {chars_list}")

print("\n--- Checking class mappings ---")
for i, cn in enumerate(CLASS_ORDER):
    chars_list = class_map.get(cn, [])
    print(f"  [{i}] {cn} ({CLASS_DISPLAY[i]}): {chars_list}")
