import csv
import glob
import os
import re
import sys

# 1. CSV data
print("=== CHARACTER CSV DATA ===")
with open('tools/era_angal_work/misc/character_data.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    csv_rows = list(reader)

chars_3a_names = [
    '円城寺れいか',
    '双葉みづき',
    '双葉みなづき',
    '四方みつる',
    '小松ぼたん',
    '山條ぎん',
    '御影かすみ',
    '湖南やこ'
]

for row in csv_rows:
    for name in chars_3a_names:
        if name in row['name']:
            print(f"Name: {row['name']} | Class: {row.get('class')} | Grade: {row.get('grade')} | Club: {row.get('club')} | Committee: {row.get('committee')}")

# 2. 既存の ERB/AITE_YOBI_相手呼称.ERB の CASE 45〜52 を確認
print("\n=== CURRENT ERB CASE 45-52 ===")
with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932', errors='replace') as f:
    erb_text = f.read()

m = re.search(r'(CASE 45\s+;[^\n]*\n.*?)(?=\s+CASE 53|\Z)', erb_text, re.DOTALL)
if m:
    # cp932セーフな出力
    print(m.group(1).encode('cp932', errors='replace').decode('cp932'))

