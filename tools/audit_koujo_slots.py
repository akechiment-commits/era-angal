# -*- coding: utf-8 -*-
"""口上枠カバレッジ監査：各キャラのSELECTCOM枠数を完成系ぼたん(49)と比較し欠落を検出。
使い方:
  python3 tools/audit_koujo_slots.py        # 全キャラ一覧（ぼたん基準の不足を表示）
  python3 tools/audit_koujo_slots.py 12     # cno=12 の詳細（不足COMと独自10の内訳）
基準ぼたん=152枠（うち独自コマンド280-284/410-414の10枠）。差分は独自枠のみが正常。
"""
import glob,os,re,sys
def load(path):
    t=open(path,'rb').read().decode('cp932')
    coms=set(int(x) for x in re.findall(r'SELECTCOM\s*==\s*(\d+)', t))
    bfun=set(re.findall(r'(?m)^@([A-Z_]+?)_\d+\s*$', t))
    return coms,bfun
comf={}; basef={}
for f in glob.glob('ERB/CHAR/CHAR_*_COM.ERB'):
    b=os.path.basename(f)
    if 'TEMPLATE' in b: continue
    comf[int(re.match(r'CHAR_(\d+)_',b).group(1))]=f
for f in glob.glob('ERB/CHAR/CHAR_*.ERB'):
    b=os.path.basename(f)
    if '_COM' in b or 'TEMPLATE' in b: continue
    basef[int(re.match(r'CHAR_(\d+)_',b).group(1))]=f
def base_empty(c):
    if c not in basef: return None
    bt=open(basef[c],'rb').read().decode('cp932')
    import re as _re
    return len(_re.findall(r'PRINTFORM[LW]?\s*「」', bt))
REF=49
ref_com,_=load(comf[REF])
ref_bfun=load(basef[REF])[1] if REF in basef else set()
DOKUJI=[280,281,282,283,284,410,411,412,413,414]
def name(c):
    return os.path.basename(comf[c]).replace('_COM.ERB','')
if len(sys.argv)>1:
    c=int(sys.argv[1])
    cc,_=load(comf[c])
    bf=load(basef[c])[1] if c in basef else set()
    miss=sorted(ref_com-cc); miss_b=sorted(ref_bfun-bf)
    print(f'== {name(c)} ==')
    print(f'  SELECTCOM枠数: {len(cc)} / 基準ぼたん {len(ref_com)}')
    print(f'  不足COM（ぼたんにあって無い）: {miss if miss else "なし(完全一致)"}')
    print(f'  base関数不足: {miss_b if miss_b else "なし"}')
    have=[d for d in DOKUJI if d in cc]
    print(f'  独自コマンド枠: {len(have)}/10 あり {have}')
    be=base_empty(c)
    print(f'  基本口上ファイルの空「」(道具反応等): {be}'+(' ★要記入' if be else ' (なし=良)'))
else:
    print(f'基準ぼたん(49)=SELECTCOM {len(ref_com)}枠（独自10含む）')
    print('cno | 枠数 | 不足(独自以外があれば異常) | 独自枠')
    for c in sorted(comf):
        cc,_=load(comf[c])
        bf=load(basef[c])[1] if c in basef else set()
        miss=ref_com-cc; miss_b=ref_bfun-bf
        nondokuji_miss=sorted(miss-set(DOKUJI))
        have=len([d for d in DOKUJI if d in cc])
        warn=' ★独自以外の欠落!' if (nondokuji_miss or miss_b) else ''
        be=base_empty(c)
        bewarn=(f' 基本口上空{be}' if be else '')
        print(f'{c:>2} | {len(cc):>3} | 独自{have}/10{(" 他欠落"+str(nondokuji_miss)) if nondokuji_miss else ""}{(" base関数"+str(sorted(miss_b))) if miss_b else ""}{bewarn}{warn}')
