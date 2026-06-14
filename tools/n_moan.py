import re,glob,subprocess
from collections import Counter
EXEMPT={57,20,66}
SEX=re.compile(r'……っ|っ……|あぁ|はぁ|ふぁ|ちゅ|れろ|ぴちゃ|ぐちゅ|挿|奥|突|なか|イっ|イく|喘|射|びく|蜜|♡|舐|くぱ|ひぃ|あんっ|だめぇ|ダメぇ|ヤ……|あっ……|ぐぽ')
KANJI=re.compile(r'[一-龠々]')
BLOCK={'あんた','あなた','うち','ウチ','その','あの','これ','それ','わたし','わたくし','あたし','きみ','おまえ','みんな','ここ','どう','なに','なん','お','わ','ワタシ','パパ','ママ','君','なぁ','また','よろし'}
MOAN=['あっ','はぁ','ふぁ','あぁ','あん']
MOAN_DRAWL=['あぁ','はぁ','ふぁ','あ']
def convpool(t):
    c=Counter()
    for l in t.split('\r\n'):
        mm=re.search(r'PRINTFORMW 「(.+?)」',l)
        if not mm: continue
        b=mm.group(1)
        if SEX.search(b): continue
        m=re.match(r'^([ぁ-んァ-ヶ]{2,4}?)(?=[、。…♪☆！？\s]|$)',b)
        if not m: continue
        op=m.group(1)
        if op.startswith('ん') or op in BLOCK or KANJI.search(op): continue
        c[op]+=1
    return [o for o,_ in c.most_common(8)] or ['ふふ','あら','ねぇ']
def split_n(b):
    m=re.match(r'^(ん[んっぁぅ]*)([、…。～]*)(.*)$',b,re.S)
    return (m.group(1),m.group(2),m.group(3)) if m else None
def process(nn,target=0.13,write=False,preview=0):
    g=glob.glob(f'ERB/CHAR/CHAR_{nn}_*_COM.ERB') or glob.glob(f'ERB/CHAR/CHAR_{nn:02d}_*_COM.ERB')
    p=g[0]; t=open(p,'rb').read().decode('cp932'); lines=t.split('\r\n')
    cpool=convpool(t)
    idx=[i for i,l in enumerate(lines) if (mm:=re.search(r'PRINTFORMW 「(.*?)」',l)) and re.match(r'^ん[んっ、…。～ぁぅ]',mm.group(1))]
    tot=sum(1 for l in lines if re.search(r'PRINTFORMW 「.',l))
    need=max(0,len(idx)-int(tot*target))
    mc=cc=done=0; pv=[]
    for i in idx:
        if done>=need: break
        mm=re.search(r'PRINTFORMW 「(.*?)」',lines[i]); b=mm.group(1)
        sp=split_n(b)
        if not sp: continue
        nk,punct,rest=sp
        if not rest: continue
        if SEX.search(b):
            pool=MOAN_DRAWL if punct.startswith('～') else MOAN
            op=pool[mc%len(pool)]; mc+=1
        else:
            op=cpool[cc%len(cpool)]; cc+=1
            if punct.startswith('～') and op.endswith('ん'): op=op[:-1] or 'あ'
        nb=op+punct+rest
        if preview and len(pv)<preview: pv.append((b[:38],nb[:38]))
        ind=lines[i][:len(lines[i])-len(lines[i].lstrip())]
        lines[i]=f'{ind}PRINTFORMW 「{nb}」'; done+=1
    t2='\r\n'.join(lines)
    for x in t2.split('\r\n'): x.encode('cp932')
    assert chr(0x7e) not in t2
    nif=sum(1 for l in lines if re.match(r'^\s*IF\b',l)); ne=sum(1 for l in lines if re.match(r'^\s*ENDIF\b',l)); assert nif==ne
    ns=sum(1 for l in lines if re.search(r'PRINTFORMW 「ん[んっ、…。～ぁぅ]',l))
    if write: open(p,'wb').write(t2.encode('cp932'))
    return tot,len(idx),done,100*ns/tot,pv
