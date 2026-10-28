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
    sur = name.replace(call, '')
    return sur if sur else call

def sim_24(ai):
    sur = get_sur(ai)
    call = chara_dict[ai][1]
    # 第2階層
    if ai == 49: return 'ぼたん先輩'
    if ai == 61: return '生徒会長'
    if ai == 67: return '日滝先輩'
    if ai == 31: return 'まりあさん'
    if ai == 32: return '安条さん'
    if ai == 34: return '桐島さん'
    if ai == 35: return '梅園さん'
    if ai == 36: return '遠見さん'
    if ai == 40: return '夜霧さん'
    if ai == 2: return 'ゆきちゃん'
    if ai == 4: return 'きこちゃん'
    if ai == 11: return 'くるみちゃん'
    if ai == 12: return 'いちかちゃん'
    if ai == 14: return 'ことりちゃん'
    if ai == 17: return 'あずさちゃん'
    if ai == 20: return 'しずくちゃん'
    if ai == 21: return 'すみれちゃん'
    # 第1階層
    if get_grade(ai) == 2:
        return f'{call}ちゃん'
    else:
        return f'{sur}さん'

def sim_25(ai):
    sur = get_sur(ai)
    call = chara_dict[ai][1]
    # 第2階層
    if ai == 24: return 'なつみちゃん'
    if ai == 26: return 'さあやちゃん'
    if ai == 27: return 'なっちゃん'
    if ai == 28: return 'こよちゃん'
    if ai == 29: return 'ななちゃん'
    if ai == 30: return 'ゆうちゃん'
    if ai == 31: return 'まりあちゃん'
    if ai == 38: return 'クーさん'
    if ai == 1: return 'かなえちゃん'
    if ai == 11: return 'くるみちゃん'
    if ai == 17: return 'あずさちゃん'
    if ai == 20: return 'しずくちゃん'
    if ai == 50: return 'ぎんさん'
    if ai == 61: return '生徒会長さん'
    if ai == 65: return '時国先輩'
    if ai == 66: return '曽根先輩'
    if ai == 67: return 'ましろさん'
    # 第1階層
    return f'{sur}さん'

def sim_26(ai):
    sur = get_sur(ai)
    call = chara_dict[ai][1]
    # 第2階層
    if ai == 61: return '生徒会長'
    if ai == 31: return '夢路さん'
    if ai == 33: return '柊さん'
    if ai == 36: return '遠見さん'
    if ai == 6: return 'あいかちゃん'
    if ai == 8: return '丸子さん'
    if ai == 10: return 'ゆゆちゃん'
    if ai == 15: return '長町さん'
    if ai == 23: return '鶯木さん'
    # 第1階層
    if get_grade(ai) > 2:
        return f'{sur}先輩'
    else:
        return sur

print("==================== CHAR_24 三波なつみ 呼称シミュレーション ====================")
for ai in sorted(chara_dict.keys()):
    if ai == 24: continue
    g = get_grade(ai)
    print(f"[{g}年] AI_{ai:02d} {chara_dict[ai][0]} -> 「{sim_24(ai)}」")

print("\n==================== CHAR_25 八朔つゆり 呼称シミュレーション ====================")
for ai in sorted(chara_dict.keys()):
    if ai == 25: continue
    g = get_grade(ai)
    print(f"[{g}年] AI_{ai:02d} {chara_dict[ai][0]} -> 「{sim_25(ai)}」")

print("\n==================== CHAR_26 堀田さあや 呼称シミュレーション ====================")
for ai in sorted(chara_dict.keys()):
    if ai == 26: continue
    g = get_grade(ai)
    print(f"[{g}年] AI_{ai:02d} {chara_dict[ai][0]} -> 「{sim_26(ai)}」")
