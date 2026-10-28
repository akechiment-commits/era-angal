# -*- coding: utf-8 -*-
import glob, os, re
from collections import Counter, defaultdict

def main():
    scenario_files = glob.glob('tools/scenarios/*.txt')
    print(f'Total scenario files: {len(scenario_files)}')

    ruri_lines = []
    himari_lines = []

    for fpath in scenario_files:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
            fname = os.path.basename(fpath)
            for line in fp:
                line = line.strip()
                if line.startswith('【るり】') or line.startswith('【天宮るり】') or line.startswith('【るり/'):
                    ruri_lines.append((fname, line))
                elif line.startswith('【ひまり】') or line.startswith('【鶴海ひまり】') or line.startswith('【ひまり/'):
                    himari_lines.append((fname, line))

    print(f'Ruri lines found: {len(ruri_lines)}')
    print(f'Himari lines found: {len(himari_lines)}')

    # 1. Analyze Ruri
    # Find all "〜のひと" patterns
    ruri_nohito = Counter()
    for fname, line in ruri_lines:
        for m in re.findall(r'([^\s「」()（）……!?！？\n]*のひと)', line):
            ruri_nohito[m] += 1

    # Also search character mentions in Ruri lines
    # Load 72 character names
    chara_info = [
        (1, '鶴海ひまり', '鶴海', 'ひまり'), (2, '花音ことり', '花音', 'ことり'), (3, '羽森つばさ', '羽森', 'つばさ'),
        (4, '長町やえ', '長町', 'やえ'), (5, '大虎いさみ', '大虎', 'いさみ'), (6, '藍乃あいか', '藍乃', 'あいか'),
        (7, '小鳩あずさ', '小鳩', 'あずさ'), (8, '熊沢ひめの', '熊沢', 'ひめの'), (9, '月永るか', '月永', 'るか'),
        (10, '木之下ゆゆ', '木之下', 'ゆゆ'), (11, '猫塚みけ', '猫塚', 'みけ'), (12, '神樹いちか', '神樹', 'いちか'),
        (13, '羽森つばさ', '羽森', 'つばさ'), (14, '花音ことり', '花音', 'ことり'), (15, '長町やえ', '長町', 'やえ'),
        (16, '大虎いさみ', '大虎', 'いさみ'), (17, '小鳩あずさ', '小鳩', 'あずさ'), (18, '熊沢ひめの', '熊沢', 'ひめの'),
        (19, '猫塚みけ', '猫塚', 'みけ'), (20, '藤猪しずく', '藤猪', 'しずく'), (21, '雉子すみれ', '雉子', 'すみれ'),
        (22, '鯱いかり', '鯱', 'いかり'), (23, '鶯木こはる', '鶯木', 'こはる'), (24, '三波なつみ', '三波', 'なつみ'),
        (25, '八朔つゆり', '八朔', 'つゆり'), (26, '堀田さあや', '堀田', 'さあや'), (27, '夏野ゆり', '夏野', 'ゆり'),
        (28, '星海こよい', '星海', 'こよい'), (29, '春風なな', '春風', 'なな'), (30, '長居ゆう', '長居', 'ゆう'),
        (31, '夢路まりあ', '夢路', 'まりあ'), (32, '安条まい', '安条', 'まい'), (33, '柊るな', '柊', 'るな'),
        (34, '桐島かいり', '桐島', 'かいり'), (35, '梅園かな', '梅園', 'かな'), (36, '遠見ちか', '遠見', 'ちか'),
        (37, '龍泉寺レンレン', '龍泉寺', 'レンレン'), (38, 'クー・カロア', '', 'カロア'), (39, '冴木もも', '冴木', 'もも'),
        (40, '夜霧はやて', '夜霧', 'はやて'), (41, '悠木ともこ', '悠木', 'ともこ'), (42, '榊むつみ', '榊', 'むつみ'),
        (43, '砂賀みどり', '砂賀', 'みどり'), (44, '笹芽ひよの', '笹芽', 'ひよの'), (45, '円城寺れいか', '円城寺', 'れいか'),
        (46, '双葉みづき', '双葉', 'みづき'), (47, '双葉みなづき', '双葉', 'みなづき'), (48, '四方みつる', '四方', 'みつる'),
        (49, '小松ぼたん', '小松', 'ぼたん'), (50, '山條ぎん', '山條', 'ぎん'), (51, '御影かすみ', '御影', 'かすみ'),
        (52, '湖南やこ', '湖南', 'やこ'), (53, '花丘まり', '花丘', 'まり'), (54, '久坂あやめ', '久坂', 'あやめ'),
        (55, '伊藤さくら', '伊藤', 'さくら'), (56, '八壁ひかる', '八壁', 'ひかる'), (57, '岩戸サン', '岩戸', 'サン'),
        (58, '天宮るり', '天宮', 'るり'), (59, '水嶌うしお', '水嶌', 'うしお'), (60, '瀬川かえで', '瀬川', 'かえで'),
        (61, '鶴海ひまり', '鶴海', 'ひまり'), (62, '黒森すず', '黒森', 'すず'), (63, '八雲ちづる', '八雲', 'ちづる'),
        (64, '峰山しおん', '峰山', 'しおん'), (65, '時国そら', '時国', 'そら'), (66, '曽根セイラ', '曽根', 'セイラ'),
        (67, '日滝ましろ', '日滝', 'ましろ'), (68, '深鳥ふみ', '深鳥', 'ふみ'), (69, '神樹はじめ', '神樹', 'はじめ'),
        (70, '神無月ほとり', '神無月', 'ほとり'), (71, '棗ひびき', '棗', 'ひびき'), (72, 'あんず', '', 'あんず')
    ]

    seen = set()
    unique_charas = []
    for cid, fn, sur, cn in chara_info:
        if cid not in seen:
            seen.add(cid)
            unique_charas.append((cid, fn, sur, cn))

    # Write Ruri analysis
    with open('tools/era_angal_work/scenarios_ruri_analysis.txt', 'w', encoding='utf-8') as out:
        out.write('=== Ruri Nohito Counts (from scenarios) ===\n')
        for k, v in ruri_nohito.most_common(50):
            out.write(f'{k}: {v}\n')

        out.write('\n=== Character Mentions by Ruri ===\n')
        for cid, fn, sur, cn in unique_charas:
            matches = []
            for fname, l in ruri_lines:
                if (sur and sur in l) or cn in l:
                    matches.append((fname, l))
            if matches:
                out.write(f'--- CHAR_{cid} {fn} ({len(matches)} mentions) ---\n')
                for f, l in matches[:5]:
                    out.write(f'  [{f}] {l}\n')

    # 2. Analyze Himari
    with open('tools/era_angal_work/scenarios_himari_analysis.txt', 'w', encoding='utf-8') as out:
        out.write('=== Character Mentions and Nicknames by Himari (from scenarios) ===\n')
        for cid, fn, sur, cn in unique_charas:
            matches = []
            for fname, l in himari_lines:
                if (sur and sur in l) or cn in l:
                    matches.append((fname, l))
            if matches:
                out.write(f'--- CHAR_{cid} {fn} ({len(matches)} mentions) ---\n')
                # Count calls
                sub_counts = Counter()
                for f, l in matches:
                    # search calls like cn+something or sur+something
                    for p in [rf'{cn}(?:ちゃん|さん|くん|先輩|殿|氏|先生|っぺ|りん|っち)?', rf'{sur}(?:ちゃん|さん|くん|先輩|殿|氏|先生)?']:
                        for m in re.findall(p, l):
                            sub_counts[m] += 1
                for k, v in sub_counts.most_common(5):
                    out.write(f'    call: {k}: {v}\n')
                for f, l in matches[:3]:
                    out.write(f'    [{f}] {l}\n')

    print('Scenarios analysis completed!')

if __name__ == '__main__':
    main()
