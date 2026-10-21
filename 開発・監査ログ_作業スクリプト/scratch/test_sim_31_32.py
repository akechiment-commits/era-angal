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

def sim_31(ai):
    sur = get_sur(ai)
    call = chara_dict[ai][1]
    if ai == 49: return '小松先輩'
    if ai == 61: return '生徒会長さま'
    if ai == 35: return '梅ちゃん'
    return f'{call}様'

def sim_32(ai):
    sur = get_sur(ai)
    call = chara_dict[ai][1]
    if ai == 61: return '生徒会長'
    if ai == 66: return 'セイラちゃん'
    if ai == 37: return 'レンレン'
    if ai == 38: return 'クー'
    if ai == 2: return 'ゆきちゃん'
    if get_grade(ai) > 2: return f'{sur}先輩'
    return f'{sur}ちゃん'

print("==================== CHAR_31 夢路まりあ 呼称テスト ====================")
for ai in [2, 11, 24, 25, 32, 35, 45, 49, 61, 72]:
    print(f"  AI_{ai:02d} {chara_dict[ai][0]} -> 「{sim_31(ai)}」")

print("\n==================== CHAR_32 安条まい 呼称テスト ====================")
for ai in [1, 2, 4, 8, 24, 25, 27, 28, 31, 35, 37, 38, 45, 46, 56, 61, 62, 66, 72]:
    print(f"  AI_{ai:02d} {chara_dict[ai][0]} -> 「{sim_32(ai)}」")
