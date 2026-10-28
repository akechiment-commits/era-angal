import csv
import json

with open('tools/era_angal_work/misc/character_data.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

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

data = {}
for r in rows:
    for n in chars_3a_names:
        if n in r['name']:
            data[n] = {
                'name': r['name'],
                'class': r.get('class'),
                'grade': r.get('grade'),
                'club': r.get('club'),
                'committee': r.get('committee'),
                'family': r.get('family'),
                'hobbies': r.get('hobbies'),
                'intro': r.get('intro')
            }

with open('tools/era_angal_work/3a_profiles.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved to 3a_profiles.json")
