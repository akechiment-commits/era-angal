# -*- coding: utf-8 -*-
import sys, re
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

# 公式名簿
chars = [
    (27, '夏野ゆり', 'ゆり', '2-A / 吹奏楽部・美化委員会'),
    (28, '星海こよい', 'こよい', '2-A / 天文部'),
    (29, '春風なな', 'なな', '2-A / チアリーディング部'),
    (30, '長居ゆう', 'ゆう', '2-A / 合唱部')
]

# 調査対象キーワード（学年別）
third_years = [
    'れいか', '円城寺', 'みづき', '双葉', 'みなづき', 'みつる', '四方', 'ぼたん', '小松',
    'ぎん', '山條', 'かすみ', '御影', 'やこ', '湖南', 'まり', '花丘', 'あやめ', '久坂',
    'さくら', '伊藤', 'ひかる', '八壁', 'サン', '岩戸', 'るり', '天宮', 'うしお', '水嶌',
    'かえで', '瀬川', 'ひまり', '鶴海', 'すず', '黒森', 'ちづる', '八雲', 'しおん', '峰山',
    'そら', '時国', 'セイラ', '曽根', 'ましろ', '日滝', 'ふみ', '深鳥', 'はじめ', '神樹',
    'ほとり', '神無月', 'ひびき', '棗', 'あんず'
]

second_years = [
    'なつみ', '三波', 'つゆり', '八朔', 'さあや', '堀田', 'ゆり', '夏野', 'こよい', '星海',
    'なな', '春風', 'ゆう', '長居', 'まりあ', '夢路', 'まい', '安条', 'るな', '柊',
    'かいり', '桐島', 'かな', '梅園', 'ちか', '遠見', 'レンレン', '龍泉寺', 'クー', 'カロア',
    'もも', '冴木', 'はやて', '夜霧', 'ともこ', '悠木', 'むつみ', '榊', 'みどり', '砂賀', 'ひよの', '笹芽'
]

first_years = [
    'かなえ', '三善', 'ゆき', '北川', 'ちよ', '小野', 'きこ', '早川', 'あすか', '桃智', 'あいか', '藍乃', 'ちあき', '高原',
    'みさき', '丸子', 'るか', '月永', 'ゆゆ', '木之下', 'くるみ', '氷野', 'いちか', '神樹', 'つばさ', '羽森', 'ことり', '花音', 'やえ', '長町',
    'いさみ', '大虎', 'あずさ', '小鳩', 'ひめの', '熊沢', 'みけ', '猫塚', 'しずく', '藤猪', 'すみれ', '雉子', 'いかり', '鯱', 'こはる', '鶯木'
]

def analyze_char(cid, full_name, callname, info):
    print(f"==================== CHAR_{cid:02d} {full_name} ({info}) ====================")
    with open(f'tools/output/{callname}.txt', 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # 3年生
    print("\n--- 3RD YEARS (上級生) ---")
    for name in third_years:
        matches = re.findall(rf'({name}[ぁ-んァ-ヶーa-zA-Z0-9_]{{0,6}})', text)
        if matches:
            c = Counter(matches)
            filtered = [(k, v) for k, v in c.most_common(4) if not any(k.endswith(x) for x in ['から', 'けど', 'こと', 'かも', 'ない', 'たい', 'たら', 'てる'])]
            if filtered:
                print(f"  {name}: {filtered}")

    # 2年生
    print("\n--- 2ND YEARS (同級生) ---")
    for name in second_years:
        if name in [callname, full_name]: continue
        matches = re.findall(rf'({name}[ぁ-んァ-ヶーa-zA-Z0-9_]{{0,6}})', text)
        if matches:
            c = Counter(matches)
            filtered = [(k, v) for k, v in c.most_common(4) if not any(k.endswith(x) for x in ['から', 'けど', 'こと', 'かも', 'ない', 'たい', 'たら', 'てる'])]
            if filtered:
                print(f"  {name}: {filtered}")

    # 1年生
    print("\n--- 1ST YEARS (下級生) ---")
    for name in first_years:
        matches = re.findall(rf'({name}[ぁ-んァ-ヶーa-zA-Z0-9_]{{0,6}})', text)
        if matches:
            c = Counter(matches)
            filtered = [(k, v) for k, v in c.most_common(4) if not any(k.endswith(x) for x in ['から', 'けど', 'こと', 'かも', 'ない', 'たい', 'たら', 'てる'])]
            if filtered:
                print(f"  {name}: {filtered}")

with open('scratch/analyze_27_to_30_out.txt', 'w', encoding='utf-8') as out:
    orig = sys.stdout
    sys.stdout = out
    for cid, full_name, callname, info in chars:
        analyze_char(cid, full_name, callname, info)
    sys.stdout = orig

print("Analysis done. Output saved to scratch/analyze_27_to_30_out.txt")
