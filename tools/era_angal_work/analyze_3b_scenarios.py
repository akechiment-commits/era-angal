# -*- coding: utf-8 -*-
import glob, re
from collections import Counter

def main():
    files = glob.glob('tools/scenarios/*.txt')
    # 3-B characters:
    # 53 まり, 54 あやめ, 55 さくら, 56 ひかる, 57 サン, 58 るり, 59 うしお, 60 かえで, 61 ひまり, 62 すず, 63 ちづる

    speakers = {
        53: ['まり', '花丘まり'],
        54: ['あやめ', '久坂あやめ'],
        55: ['さくら', '伊藤さくら'],
        56: ['ひかる', '八壁ひかる'],
        57: ['サン', '岩戸サン'],
        58: ['るり', '天宮るり'],
        59: ['うしお', '水嶌うしお'],
        60: ['かえで', '瀬川かえで'],
        61: ['ひまり', '鶴海ひまり'],
        62: ['すず', '黒森すず'],
        63: ['ちづる', '八雲ちづる']
    }

    speaker_lines = {cid: [] for cid in speakers}

    for f in files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            for l in fp:
                for cid, names in speakers.items():
                    if any(l.startswith(f'【{n}】') for n in names):
                        speaker_lines[cid].append(l.strip())

    for cid, lines in speaker_lines.items():
        print(f'CHAR_{cid} ({speakers[cid][0]}): {len(lines)} lines')

    # Analyze Kaede (60)
    # Kaede calls to Sakura, Reika, Hikaru, Sun, Anzu, Protagonist
    print('\n=== Analyzing Kaede (60) ===')
    kaede_sakura = Counter()
    for l in speaker_lines[60]:
        for m in re.findall(r'([^。\n]*さくら[^。\n]*)', l):
            kaede_sakura[m.strip()] += 1
    print('Kaede calls to Sakura count:', len(kaede_sakura))
    for k, v in kaede_sakura.most_common(5):
        print(f'  {k}: {v}')

    # Analyze Ushio (59)
    print('\n=== Analyzing Ushio (59) ===')
    ushio_miduki = Counter()
    for l in speaker_lines[59]:
        for m in re.findall(r'([^。\n]*みづき[^。\n]*)', l):
            ushio_miduki[m.strip()] += 1
    print('Ushio calls to Miduki count:', len(ushio_miduki))
    for k, v in ushio_miduki.most_common(5):
        print(f'  {k}: {v}')

    # Analyze Ayame (54)
    print('\n=== Analyzing Ayame (54) ===')
    ayame_hikaru = Counter()
    for l in speaker_lines[54]:
        for m in re.findall(r'([^。\n]*ひかる[^。\n]*)', l):
            ayame_hikaru[m.strip()] += 1
    print('Ayame calls to Hikaru count:', len(ayame_hikaru))
    for k, v in ayame_hikaru.most_common(5):
        print(f'  {k}: {v}')

if __name__ == '__main__':
    main()
