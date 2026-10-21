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

def sim_27(ai):
    sur = get_sur(ai)
    call = chara_dict[ai][1]
    if ai == 61: return '生徒会長'
    if ai == 72: return 'あんずさん'
    if ai == 24: return 'なつみちゃん'
    if ai == 25: return 'つゆりちゃん'
    if ai == 26: return 'さあやちゃん'
    if ai == 29: return 'ななちゃん'
    if ai == 30: return 'ゆうちゃん'
    if ai == 1: return '三善'
    if ai == 4: return '早川'
    if get_grade(ai) > 2: return f'{sur}先輩'
    return f'{sur}さん'

def sim_28(ai):
    sur = get_sur(ai)
    call = chara_dict[ai][1]
    if ai == 58: return 'るりちゃん部長'
    if ai == 61: return '生徒会長さん'
    if ai == 70: return '月ちゃん先輩'
    if ai == 25: return 'つゆりちゃん'
    if ai == 38: return 'クーさん'
    if ai == 10: return 'ゆゆちゃん'
    if ai == 11: return 'くるみちゃん'
    if ai == 20: return 'しずくちゃん'
    return f'{sur}さん'

def sim_29(ai):
    sur = get_sur(ai)
    call = chara_dict[ai][1]
    if ai == 61: return '生徒会長さん'
    if ai == 67: return 'ましろさん'
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
    if ai == 61: return '生徒会長'
    if ai == 68: return '部長さん'
    if ai == 34: return 'かいりちゃん'
    if ai == 37: return 'レンレンちゃん'
    if ai == 2: return 'ゆきちゃん'
    if ai == 11: return 'くるみちゃん'
    if ai == 13: return 'つばさちゃん'
    if ai == 14: return 'ことりちゃん'
    if get_grade(ai) > 2: return f'{sur}先輩'
    if get_grade(ai) == 2: return f'{call}ちゃん'
    return f'{sur}さん'

for cid, func, name in [(27, sim_27, '夏野ゆり'), (28, sim_28, '星海こよい'), (29, sim_29, '春風なな'), (30, sim_30, '長居ゆう')]:
    print(f"\n==================== CHAR_{cid} {name} 呼称シミュレーション ====================")
    for ai in [1, 2, 4, 10, 11, 13, 14, 20, 24, 25, 26, 27, 28, 29, 30, 34, 35, 37, 38, 41, 45, 58, 61, 67, 68, 70, 72]:
        if ai == cid: continue
        print(f"  AI_{ai:02d} {chara_dict[ai][0]} -> 「{func(ai)}」")
