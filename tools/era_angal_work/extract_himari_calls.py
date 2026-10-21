# -*- coding: utf-8 -*-
import re
from collections import Counter

def main():
    with open('tools/output/ひまり.txt', 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    # Load character list from ERB
    # We will search how Himari calls each character
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

    seen_id = set()
    unique_charas = []
    for cid, fname, sur, cname in chara_info:
        if cid not in seen_id:
            seen_id.add(cid)
            unique_charas.append((cid, fname, sur, cname))

    output_lines = []

    for cid, fname, sur, cname in unique_charas:
        # Search patterns for calls
        # 1. cname with suffixes or plain
        # e.g., cname, cnameちゃん, cnameくん, cnameさん, cname先輩
        # Also check nicknames
        patterns = [
            rf'{cname}(?:ちゃん|さん|くん|先輩|殿|氏|先生|公)?',
        ]
        if sur:
            patterns.append(rf'{sur}(?:ちゃん|さん|くん|先輩|殿|氏|先生)?')
        
        counts = Counter()
        for p in patterns:
            found = re.findall(p, text)
            for item in found:
                counts[item] += 1
        
        output_lines.append(f'=== CHAR_{cid} {fname} ===')
        for k, v in counts.most_common(10):
            output_lines.append(f'  {k}: {v}')

    # Also search for "くろりん" and other unique nicknames in text
    special_nicknames = ['くろりん', 'アンジー', 'るる', 'もっちー', 'かっちゃん', 'よっちゃん', 'まっちゃん', 'あっちゃん', 'さっちゃん']
    output_lines.append('\n=== Special Nickname Search in himari.txt ===')
    for sn in special_nicknames:
        c = text.count(sn)
        if c > 0:
            output_lines.append(f'  {sn}: {c}')

    with open('tools/era_angal_work/himari_calls_detailed.txt', 'w', encoding='utf-8') as out:
        out.write('\n'.join(output_lines))

    print('Wrote himari_calls_detailed.txt successfully!')

if __name__ == '__main__':
    main()
