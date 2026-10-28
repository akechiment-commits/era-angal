import csv
import os
import re

# Load character data
chara_list = []
with open('tools/era_angal_work/misc/character_data.csv', 'r', encoding='utf-8-sig') as f:
    for i, row in enumerate(csv.DictReader(f)):
        chara_list.append({
            'id': i + 1,
            'name': row['name'],
            'grade': row['grade'],
            'class': row['class'],
            'club': row['club'],
            'committee': row['committee'],
            'intro': row['intro']
        })

print(f"Total characters loaded: {len(chara_list)}")
for c in chara_list:
    if c['id'] >= 64:
        print(f"ID {c['id']}: {c['name']} | {c['grade']}年{c['class']}組 | 部活: {c['club']} | 委員会: {c['committee']}")
