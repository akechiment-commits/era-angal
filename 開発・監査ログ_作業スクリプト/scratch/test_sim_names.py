# -*- coding: utf-8 -*-
import sys, csv

# キャラ名簿読み込み
chara_names = {}
chara_grades = {}
with open('tools/era_angal_work/misc/character_data.csv', 'r', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        cid = int(row['id'])
        chara_names[cid] = row['name']
        chara_grades[cid] = int(row['grade'])
chara_names[72] = 'あんず'
chara_grades[72] = 3

# ERBのAITE_YOBIロジックをPythonで忠実に再現してシミュレーション
def get_grade(cid):
    if 1 <= cid <= 23:
        return 1
    elif 24 <= cid <= 44:
        return 2
    elif 45 <= cid <= 72:
        return 3
    return 0

def get_sur_callname(cid):
    name = chara_names[cid]
    # 例: 三波なつみ -> 三波, なつみ
    # あんず -> あんず, あんず
    if cid == 72:
        return 'あんず', 'あんず'
    # 苗字と名前の分離（2文字姓・名前等）
    # 簡易ルール
    first_names = [
        'かなえ', 'ゆき', 'ちよ', 'きこ', 'あすか', 'あいか', 'ちあき', 'みさき', 'るか', 'ゆゆ', 'くるみ',
        'いちか', 'つばさ', 'ことり', 'やえ', 'いさみ', 'あずさ', 'ひめの', 'みけ', 'しずく', 'すみれ', 'いかり', 'こはる',
        'なつみ', 'つゆり', 'さあや', 'ゆり', 'こよい', 'なな', 'ゆう', 'まりあ', 'まい', 'るな', 'かいり', 'かな',
        'ちか', 'レンレン', 'カロア', 'もも', 'はやて', 'ともこ', 'むつみ', 'みどり', 'ひよの',
        'れいか', 'みづき', 'みなづき', 'みつる', 'ぼたん', 'ぎん', 'かすみ', 'やこ', 'まり', 'あやめ',
        'さくら', 'ひかる', 'サン', 'るり', 'うしお', 'かえで', 'ひまり', 'すず', 'ちづる', 'しおん',
        'そら', 'セイラ', 'ましろ', 'ふみ', 'はじめ', 'ほとり', 'ひびき', 'あんず'
    ]
    for fn in first_names:
        if name.endswith(fn):
            sur = name[:-len(fn)]
            return sur if sur else fn, fn
    return name, name

print("Testing Name Parsing for some chars:")
for c in [2, 24, 25, 26, 27, 28, 49, 61, 65, 66, 72]:
    print(f"{c}: {chara_names[c]} -> SUR={get_sur_callname(c)[0]}, CALLNAME={get_sur_callname(c)[1]}")
