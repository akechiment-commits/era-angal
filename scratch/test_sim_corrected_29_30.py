# -*- coding: utf-8 -*-
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

chara_dict = {}
for fname in os.listdir('CSV'):
    if fname.startswith('Chara') and fname.endswith('.csv'):
        m = re.match(r'Chara(\d+)', fname)
        if m:
            cid = int(m.group(1))
            cf = os.path.join('CSV', fname)
            name = ''
            callname = ''
            with open(cf, 'rb') as f:
                for l in f.read().splitlines():
                    t = l.decode('cp932', errors='ignore')
                    if t.startswith('NAME,') or t.startswith('名前,'):
                        name = t.split(',')[1].strip()
                    elif t.startswith('CALLNAME,') or t.startswith('呼び名,'):
                        callname = t.split(',')[1].strip()
            if name and callname:
                chara_dict[cid] = (name, callname)

chara_dict[72] = ('あんず', 'あんず')

def get_grade(cid):
    if 1 <= cid <= 23: return 1
    if 24 <= cid <= 44: return 2
    if 45 <= cid <= 72: return 3
    return 0

def get_sur(ai):
    name, call = chara_dict[ai]
    sur = name.replace(call, '').replace('・', '')
    return sur if sur else call

def sim_29(ai):
    sur = get_sur(ai)
    call = chara_dict[ai][1]
    if ai == 61: return '生徒会長さん'
    if ai == 67: return '団長'
    if ai == 27: return '夏野さん'
    if ai == 35: return '梅園さん'
    if ai == 41: return '悠木さん'
    if ai == 2: return '北川さん'
    if ai == 8: return '丸子さん'
    if get_grade(ai) > 2: return f'{sur}先輩'
    return f'{call}ちゃん'

def sim_30(ai):
    sur = get_sur(ai)
    call = chara_dict[ai][1]
    if ai == 52: return '湖南先輩'
    if ai == 61: return '生徒会長'
    if ai == 34: return 'かいりちゃん'
    if ai == 37: return 'レンレンちゃん'
    if ai == 8: return 'マルちゃん'
    if ai == 2: return 'ゆきちゃん'
    if ai == 11: return 'くるみちゃん'
    if ai == 13: return 'つばさちゃん'
    if ai == 14: return 'ことりちゃん'
    if get_grade(ai) > 2: return f'{sur}先輩'
    if get_grade(ai) == 2: return f'{call}ちゃん'
    return f'{sur}さん'

print("==================== CHAR_29 春風なな (修正後) ====================")
for ai in [2, 8, 14, 24, 25, 26, 27, 28, 30, 35, 41, 61, 67, 72]:
    print(f"  AI_{ai:02d} {chara_dict[ai][0]} -> 「{sim_29(ai)}」")

print("\n==================== CHAR_30 長居ゆう (修正後) ====================")
for ai in [2, 8, 11, 13, 14, 24, 25, 26, 27, 28, 29, 34, 37, 52, 61, 68, 72]:
    print(f"  AI_{ai:02d} {chara_dict[ai][0]} -> 「{sim_30(ai)}」")
