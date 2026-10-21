import os
import re

# Inspect characters 45 to 52
chars_3a = [
    (45, 'れいか', '円城寺れいか'),
    (46, 'みづき', '双葉みづき'),
    (47, 'みなづき', '双葉みなづき'),
    (48, 'みつる', '四方みつる'),
    (49, 'ぼたん', '小松ぼたん'),
    (50, 'ぎん', '山條ぎん'),
    (51, 'かすみ', '御影かすみ'),
    (52, 'やこ', '湖南やこ')
]

# We want to see how each of these 8 characters addresses EVERY other character in the school.
# Let's inspect the files of each character, searching for how they call people.
# Also print out their general calling policy (1st person, 2nd person, honorifics used).

for cid, callname, fullname in chars_3a:
    text = ""
    for suffix in ["", "_関係性", "_転校生"]:
        p = f"tools/output/{callname}{suffix}.txt"
        if os.path.exists(p):
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                text += f.read() + "\n"
    
    # Also find files where callname is part of filename
    for p in os.listdir('tools/output'):
        if callname in p and p not in [f"{callname}.txt", f"{callname}_関係性.txt", f"{callname}_転校生.txt"]:
            with open(f"tools/output/{p}", 'r', encoding='utf-8', errors='replace') as f:
                text += f.read() + "\n"
                
    # First person
    fp_watashi = len(re.findall(r'わたし', text))
    fp_watakushi = len(re.findall(r'わたくし', text))
    fp_boku = len(re.findall(r'ボク|ぼく|僕', text))
    fp_ore = len(re.findall(r'オレ|おれ|俺', text))
    fp_jibun = len(re.findall(r'自分', text))
    fp_name = len(re.findall(callname, text))
    
    # 2nd person to player
    player_calls = re.findall(r'([^。！？\n]{0,15}(?:転校生|お前|あんた|貴方|あなた|きみ|君|プロデューサー)[^。！？\n]{0,15})', text)
    
    # Summary of character
    print(f"\n=======================================================")
    print(f"ID {cid}: {fullname} ({callname})")
    print(f"一人称: わたし({fp_watashi}), わたくし({fp_watakushi}), ボク({fp_boku}), 俺({fp_ore}), 自分({fp_jibun}), 名前({fp_name})")
    print(f"プレイヤー呼称サンプル: {list(set(player_calls))[:3]}")

