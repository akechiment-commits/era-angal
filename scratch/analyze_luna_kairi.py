# -*- coding: utf-8 -*-
import sys, re
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

chara_list = [
    'かなえ', '三善', 'ゆき', '北川', 'ちよ', '小野', 'きこ', '早川', 'あすか', '桃智', 'あいか', '藍乃', 'ちあき', '高原',
    'みさき', '丸子', 'るか', '月永', 'ゆゆ', '木之下', 'くるみ', '氷野', 'いちか', '神樹', 'つばさ', '羽森', 'ことり', '花音', 'やえ', '長町',
    'いさみ', '大虎', 'あずさ', '小鳩', 'ひめの', '熊沢', 'みけ', '猫塚', 'しずく', '藤猪', 'すみれ', '雉子', 'いかり', '鯱', 'こはる', '鶯木',
    'なつみ', '三波', 'つゆり', '八朔', 'さあや', '堀田', 'ゆり', '夏野', 'こよい', '星海', 'なな', '春風', 'ゆう', '長居',
    'まりあ', '夢路', 'まい', '安条', 'るな', '柊', 'かいり', '桐島', 'かな', '梅園', 'ちか', '遠見', 'レンレン', '龍泉寺', 'クー', 'カロア',
    'もも', '冴木', 'はやて', '夜霧', 'ともこ', '悠木', 'むつみ', '榊', 'みどり', '砂賀', 'ひよの', '笹芽',
    'れいか', '円城寺', 'みづき', '双葉', 'みなづき', 'みつる', '四方', 'ぼたん', '小松', 'ぎん', '山條', 'かすみ', '御影',
    'やこ', '湖南', 'まり', '花丘', 'あやめ', '久坂', 'さくら', '伊藤', 'ひかる', '八壁', 'サン', '岩戸', 'るり', '天宮',
    'うしお', '水嶌', 'かえで', '瀬川', 'ひまり', '鶴海', 'すず', '黒森', 'ちづる', '八雲', 'しおん', '峰山', 'そら', '時国',
    'セイラ', '曽根', 'ましろ', '日滝', 'ふみ', '深鳥', 'はじめ', 'ほとり', '神無月', 'ひびき', '棗', 'あんず'
]

def analyze_character(cname):
    print(f"==================== {cname} 呼称分析 ====================")
    with open(f'tools/output/{cname}.txt', 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    lines = text.splitlines()
    print(f"Total lines: {len(lines)}")
    
    # 全キャラ名ヒット
    found = {}
    for name in chara_list:
        if name in [cname, 'るな', 'かいり']: continue
        m = re.findall(rf'({name}[^\s「」、。！？]{{0,6}})', text)
        if m:
            c = Counter(m)
            filtered = [(k, v) for k, v in c.most_common(5) if not any(k.endswith(x) for x in ['から', 'けど', 'こと', 'かも', 'ない', 'たい', 'たら', 'てる'])]
            if filtered:
                found[name] = filtered
                
    for name, hits in sorted(found.items(), key=lambda x: -sum(h[1] for h in x[1]))[:25]:
        print(f"  {name}: {hits}")

    # 先輩、さん、ちゃん、呼び捨て傾向
    pats = [r'([^\s「」]*(?:先輩|さん|ちゃん|先生|部長|会長|くん|君)[^\s「」]*)']
    term_hits = []
    for l in lines:
        for p in pats:
            for m in re.finditer(p, l):
                w = m.group(1)
                if w not in ['お父さん', 'お母さん', 'お姉ちゃん', 'お兄さん', 'たくさん']:
                    term_hits.append(w)
    c_terms = Counter(term_hits)
    print("\n--- 呼称頻出語 TOP 20 ---")
    for term, count in c_terms.most_common(20):
        print(f"  {term}: {count}回")

analyze_character('るな')
print("\n" + "="*60 + "\n")
analyze_character('かいり')
