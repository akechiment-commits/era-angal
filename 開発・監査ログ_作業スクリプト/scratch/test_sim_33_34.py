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

def sim_33(ai):
    sur = get_sur(ai)
    call = chara_dict[ai][1]
    if ai == 45: return '円城寺のお嬢'
    if ai == 61: return '会長はん'
    if ai == 26: return '堀田ちゃん'
    if ai == 6: return 'あいかちゃん'
    if get_grade(ai) > 2: return f'{sur}先輩'
    return sur

def sim_34(ai):
    sur = get_sur(ai)
    call = chara_dict[ai][1]
    if ai == 52: return '湖南先輩'
    if ai == 60: return 'かえでちゃん'
    if ai == 61: return '生徒会長'
    if ai == 24: return '三波さん'
    if ai == 26: return '堀田さん'
    if ai == 8: return 'マルちゃん'
    if ai == 3: return '小野さん'
    if ai == 17: return '小鳩さん'
    if get_grade(ai) > 2: return f'{sur}先輩'
    return f'{call}ちゃん'

print("==================== CHAR_33 柊るな 呼称テスト ====================")
for ai in [6, 7, 19, 24, 26, 31, 35, 36, 38, 45, 46, 61, 72]:
    print(f"  AI_{ai:02d} {chara_dict[ai][0]} -> 「{sim_33(ai)}」")

print("\n==================== CHAR_34 桐島かいり 呼称テスト ====================")
for ai in [2, 3, 8, 13, 14, 17, 24, 26, 30, 31, 32, 35, 38, 45, 49, 52, 60, 61, 72]:
    print(f"  AI_{ai:02d} {chara_dict[ai][0]} -> 「{sim_34(ai)}」")
