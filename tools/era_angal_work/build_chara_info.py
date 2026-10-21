import os
import glob
import re
import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load CSV/Chara*.csv to get ID, NAME, CALLNAME
chara_dict = {}
for filepath in glob.glob('CSV/Chara*.csv'):
    filename = os.path.basename(filepath)
    m = re.match(r'Chara(\d+)_(.+)\.csv', filename)
    if not m:
        continue
    cid = int(m.group(1))
    cname = m.group(2)
    
    # read content
    callname = cname
    name = cname
    with open(filepath, 'r', encoding='cp932', errors='ignore') as f:
        for line in f:
            if line.startswith('名前,'):
                name = line.strip().split(',')[1]
            elif line.startswith('呼び名,'):
                callname = line.strip().split(',')[1]
    chara_dict[cid] = {
        'id': cid,
        'full_name': name,
        'callname': callname,
        'file_name': cname
    }

# 2. Load character_data.csv for club, committee, grade, class
with open('tools/era_angal_work/misc/character_data.csv', 'r', encoding='utf-8-sig') as f:
    r = csv.DictReader(f)
    csv_rows = list(r)

# Match by full_name or parts
for cid, info in chara_dict.items():
    found = False
    for row in csv_rows:
        r_name = row['name'].replace(' ', '').replace('　', '')
        f_name = info['full_name'].replace(' ', '').replace('　', '')
        c_name = info['callname'].replace(' ', '').replace('　', '')
        if r_name == f_name or c_name in r_name:
            try:
                info['grade'] = int(row['grade'])
            except:
                info['grade'] = 3
            info['class'] = row['class']
            info['club'] = row['club']
            info['committee'] = row['committee']
            info['intro'] = row['intro']
            found = True
            break
    if not found:
        if cid == 72:
            info['grade'] = 3
            info['class'] = 'C'
            info['club'] = '茶道部'
            info['committee'] = ''
            info['intro'] = '転校生'
        else:
            print(f"Warning: Chara {cid} {info['full_name']} not matched in character_data.csv")

# Print 64 to 72
for cid in range(64, 73):
    c = chara_dict[cid]
    print(f"ID {c['id']:2d}: {c['full_name']} (呼称: {c['callname']}) - {c.get('grade')}年{c.get('class')}組 | 部活: {c.get('club')} | 委員会: {c.get('committee')}")
