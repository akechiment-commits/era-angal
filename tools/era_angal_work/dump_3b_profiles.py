import csv
import json

with open('tools/era_angal_work/misc/character_data.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

target_3b_ids = [
    (53, '花丘まり'),
    (54, '久坂あやめ'),
    (55, '伊藤さくら'),
    (56, '八壁ひかる'),
    (57, '岩戸サン'),
    (58, '天宮るり'),
    (59, '水嶌うしお'),
    (60, '瀬川かえで'),
    (61, '鶴海ひまり'),
    (62, '黒森すず'),
    (63, '八雲ちづる')
]

data = {}
for r in rows:
    for cid, name in target_3b_ids:
        if name in r['name']:
            data[cid] = {
                'id': cid,
                'name': r['name'],
                'class': r.get('class'),
                'grade': r.get('grade'),
                'club': r.get('club'),
                'committee': r.get('committee'),
                'family': r.get('family'),
                'hobbies': r.get('hobbies'),
                'intro': r.get('intro')
            }

with open('tools/era_angal_work/3b_profiles.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved 3b_profiles.json")
