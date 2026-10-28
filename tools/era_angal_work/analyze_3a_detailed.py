import os
import glob
import re
import csv
import json
from collections import defaultdict

# 72 characters definitions
charas = [
    (1, "葵さくや", "葵", "さくや", 1),
    (2, "浅葱ゆな", "浅葱", "ゆな", 1),
    (3, "小野ちよ", "小野", "ちよ", 1),
    (4, "早川きこ", "早川", "きこ", 1),
    (5, "葉月まり", "葉月", "まり", 1),
    (6, "藍乃あいか", "藍乃", "あいか", 1),
    (7, "高原ちあき", "高原", "ちあき", 1),
    (8, "丸子みさき", "丸子", "みさき", 1),
    (9, "月永るか", "月永", "るか", 1),
    (10, "曽根ラピス", "曽根", "ラピス", 1),
    (11, "氷野くるみ", "氷野", "くるみ", 1),
    (12, "神樹いちか", "神樹", "いちか", 1),
    (13, "羽森つばさ", "羽森", "つばさ", 1),
    (14, "花音ことり", "花音", "ことり", 1),
    (15, "長町やえ", "長町", "やえ", 1),
    (16, "大虎いさみ", "大虎", "いさみ", 1),
    (17, "小鳩あずさ", "小鳩", "あずさ", 1),
    (18, "熊沢ひめの", "熊沢", "ひめの", 1),
    (19, "猫塚みけ", "猫塚", "みけ", 1),
    (20, "藤猪しずく", "藤猪", "しずく", 1),
    (21, "雉子すみれ", "雉子", "すみれ", 1),
    (22, "鯱いかり", "鯱", "いかり", 1),
    (23, "鶯木こはる", "鶯木", "こはる", 1),
    (24, "三波なつみ", "三波", "なつみ", 2),
    (25, "八朔つゆり", "八朔", "つゆり", 2),
    (26, "堀田さあや", "堀田", "さあや", 2),
    (27, "夏野ゆり", "夏野", "ゆり", 2),
    (28, "星海こよい", "星海", "こよい", 2),
    (29, "春風なな", "春風", "なな", 2),
    (30, "長居ゆう", "長居", "ゆう", 2),
    (31, "夢路まりあ", "夢路", "まりあ", 2),
    (32, "安条まい", "安条", "まい", 2),
    (33, "柊るな", "柊", "るな", 2),
    (34, "桐島かいり", "桐島", "かいり", 2),
    (35, "梅園かな", "梅園", "かな", 2),
    (36, "遠見ちか", "遠見", "ちか", 2),
    (37, "龍泉寺レンレン", "龍泉寺", "レンレン", 2),
    (38, "クー・カロア", "カロア", "クー", 2),
    (39, "冴木もも", "冴木", "もも", 2),
    (40, "夜霧はやて", "夜霧", "はやて", 2),
    (41, "悠木ともこ", "悠木", "ともこ", 2),
    (42, "榊むつみ", "榊", "むつみ", 2),
    (43, "砂賀みどり", "砂賀", "みどり", 2),
    (44, "笹芽ひよの", "笹芽", "ひよの", 2),
    (45, "円城寺れいか", "円城寺", "れいか", 3),
    (46, "双葉みづき", "双葉", "みづき", 3),
    (47, "双葉みなづき", "双葉", "みなづき", 3),
    (48, "四方みつる", "四方", "みつる", 3),
    (49, "小松ぼたん", "小松", "ぼたん", 3),
    (50, "山條ぎん", "山條", "ぎん", 3),
    (51, "御影かすみ", "御影", "かすみ", 3),
    (52, "湖南やこ", "湖南", "やこ", 3),
    (53, "花丘まり", "花丘", "まり", 3),
    (54, "久坂あやめ", "久坂", "あやめ", 3),
    (55, "伊藤さくら", "伊藤", "さくら", 3),
    (56, "八壁ひかる", "八壁", "ひかる", 3),
    (57, "岩戸サン", "岩戸", "サン", 3),
    (58, "天宮るり", "天宮", "るり", 3),
    (59, "水嶌うしお", "水嶌", "うしお", 3),
    (60, "瀬川かえで", "瀬川", "かえで", 3),
    (61, "鶴海ひまり", "鶴海", "ひまり", 3),
    (62, "黒森すず", "黒森", "すず", 3),
    (63, "八雲ちづる", "八雲", "ちづる", 3),
    (64, "峰山しおん", "峰山", "しおん", 3),
    (65, "時国そら", "時国", "そら", 3),
    (66, "曽根セイラ", "曽根", "セイラ", 3),
    (67, "日滝ましろ", "日滝", "ましろ", 3),
    (68, "深鳥ふみ", "深鳥", "ふみ", 3),
    (69, "神樹はじめ", "神樹", "はじめ", 3),
    (70, "神無月ほとり", "神無月", "ほとり", 3),
    (71, "棗ひびき", "棗", "ひびき", 3),
    (72, "あんず", "あんず", "あんず", 3),
]

target_3a = [
    (45, '円城寺れいか', 'れいか'),
    (46, '双葉みづき', 'みづき'),
    (47, '双葉みなづき', 'みなづき'),
    (48, '四方みつる', 'みつる'),
    (49, '小松ぼたん', 'ぼたん'),
    (50, '山條ぎん', 'ぎん'),
    (51, '御影かすみ', 'かすみ'),
    (52, '湖南やこ', 'やこ')
]

existing_erb = {
    45: {8: '丸子さん', 13: '羽森さん', 14: '花音さん', 26: '堀田さん', 34: '桐島さん', 40: '夜霧さん', 49: '小松さん', 52: '湖南さん', 59: '水嶌さん', 63: '八雲さん', 65: '時国さん', 67: '日滝さん', 69: 'はじめさん', 72: 'あんずさん'},
    46: {47: 'みなづき'},
    47: {22: 'いかりちゃん', 23: 'こはるちゃん', 28: 'こよいちゃん', 41: 'ともちゃん', 44: 'ひよのちゃん', 45: 'れいかちゃん', 46: 'みづき', 48: 'みつるちゃん', 50: 'ぎんちゃん', 51: 'かすみん', 59: 'うしおちゃん', 60: 'かえでちゃん', 61: 'ひまりちゃん', 65: 'そらちゃん'},
    48: {24: '三波さん', 25: '八朔さん', 27: '夏野さん', 31: 'まりあさん', 32: '安条さん', 35: '梅園さん', 36: '遠見さん', 52: '湖南さん', 57: '岩戸さん', 60: '瀬川さん', 63: '八雲さん', 66: '曽根さん', 68: '深鳥さん'},
    49: {},
    50: {24: '三波殿', 37: '龍泉寺殿', 45: '円城寺殿', 52: '湖南殿', 56: '八壁殿'},
    51: {},
    52: {36: 'トミコ'}
}

output_dir = 'tools/output'

report = []

for cid, fullname, callname in target_3a:
    report.append(f"\n=======================================================")
    report.append(f"【ID {cid:02d} : {fullname}】(CALLNAME: {callname})")
    
    # Read files
    f_main = os.path.join(output_dir, f"{callname}.txt")
    f_rel = os.path.join(output_dir, f"{callname}_関係性.txt")
    f_ten = os.path.join(output_dir, f"{callname}_転校生.txt")
    
    all_text = ""
    for fp in [f_main, f_rel, f_ten]:
        if os.path.exists(fp):
            with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                all_text += f.read() + "\n"
    
    # Also find files where callname appears in combo like みづき・みなづき.txt
    combo_files = glob.glob(os.path.join(output_dir, f"*{callname}*.txt"))
    for cf in combo_files:
        if cf not in [f_main, f_rel, f_ten]:
            with open(cf, 'r', encoding='utf-8', errors='replace') as f:
                all_text += f.read() + "\n"
    
    report.append(f"総テキスト長: {len(all_text)} 文字")
    report.append(f"既存ERB設定: {existing_erb.get(cid, {})}")
    
    # Scan for mentions of each other character
    mentions_by_char = defaultdict(lambda: defaultdict(list))
    
    for other_id, other_full, other_sur, other_cn, other_grade in charas:
        if other_id == cid:
            continue
        
        # Build search tokens
        # e.g. "円城寺", "れいか", "円城寺さん", "れいかちゃん", "会長", etc.
        patterns = []
        if len(other_sur) >= 2:
            patterns.append((rf'{other_sur}(?:さん|ちゃん|先輩|センパイ|君|くん|クン|様|さま|殿|氏)?', f"SUR:{other_sur}"))
        if len(other_cn) >= 2:
            patterns.append((rf'{other_cn}(?:さん|ちゃん|先輩|センパイ|君|くん|クン|様|さま|殿|氏)?', f"CN:{other_cn}"))
        
        # Check specific nickname in existing ERB
        if other_id in existing_erb.get(cid, {}):
            ex_call = existing_erb[cid][other_id]
            patterns.append((rf'{re.escape(ex_call)}', f"EX:{ex_call}"))
        
        for pat, tag in patterns:
            # find all occurrences with line context
            # split into lines
            for line in all_text.splitlines():
                line_str = line.strip()
                if not line_str:
                    continue
                matches = re.findall(pat, line_str)
                for m in matches:
                    mentions_by_char[other_id][m].append(line_str[:80])
    
    # Also search special titles/roles (部長, 会長, 閣下, 王子, etc.)
    special_titles = ['会長', '生徒会長', '部長', '副部長', '閣下', '王子', 'トミコ', 'ナガマチ', '双葉']
    for st in special_titles:
        for line in all_text.splitlines():
            line_str = line.strip()
            if st in line_str:
                mentions_by_char[999][st].append(line_str[:80])

    report.append("--- 検出された相手呼称・言及 ---")
    for other_id in sorted(mentions_by_char.keys()):
        if other_id == 999:
            report.append("【役職・特殊キーワード言及】:")
            for title, lines in mentions_by_char[999].items():
                report.append(f"  * 『{title}』({len(lines)}回): {lines[:2]}")
            continue
            
        other_info = [c for c in charas if c[0] == other_id][0]
        other_full = other_info[1]
        other_grade = other_info[4]
        calls_dict = mentions_by_char[other_id]
        
        call_summaries = []
        for call_word, lines in calls_dict.items():
            call_summaries.append(f"『{call_word}』({len(lines)}回)")
        
        report.append(f"  -> ID {other_id:02d} {other_full} ({other_grade}年): {', '.join(call_summaries)}")
        # Print sample line for top calls
        for call_word, lines in sorted(calls_dict.items(), key=lambda x: len(x[1]), reverse=True)[:2]:
            report.append(f"       例: {lines[0]}")

with open('tools/era_angal_work/3a_analysis_detailed.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

print("Saved detailed report to tools/era_angal_work/3a_analysis_detailed.txt")
