# ⛔【封印・使用禁止 2026-06-14】機械的ん一括sweepは自然な喘ぎ/含み笑い/ハミングまで巻き込みニュアンスを損なうため全面撤回。
# ん始まりは「会話フィラーのん、」だけを各キャラ整合作業中に人の判断で散らすこと（ガイド§現行最新仕様C参照）。
import re,glob
from collections import Counter
SEXMARK=re.compile(r'っ……|あぁ|はぁ|ちゅ|れろ|ぴちゃ|挿れ|奥|イ[くっ]|気持ち|感じ|乱れ|貫|腰|犯|喘|射|びく|とろ|ぐちゅ|お尻|胸')
BLOCK={'あんた','あなた','うち','ウチ','その','あの','これ','それ','わたし','わたくし','あたし','きみ','おまえ','みんな','ここ','どう','なに','なん','お','わ','ワタシ','パパ','ママ','パパは','君','ゆん','なぁ'}
KANJI=re.compile(r'[一-龠々]')
def valid(op):
    if len(op)<2 or len(op)>4: return False
    if op in BLOCK: return False
    if KANJI.search(op): return False
    if '%' in op or '＜' in op: return False
    if not re.match(r'^[ぁ-んァ-ヶ]', op): return False  # 括弧・…・記号始まり除外
    if any(c in op for c in '（）…。、'): return False
    return True
def build_pools(t):
    conv=Counter(); sex=Counter()
    for l in t.split('\r\n'):
        mm=re.search(r'PRINTFORMW 「(.+?)」',l)
        if not mm: continue
        b=mm.group(1)
        m=re.match(r'^([^、。…♪☆！？\s]{1,4}?)(?=[、。…♪☆！？\s]|$)',b)
        op=m.group(1) if m else b[:3]
        if op.startswith('ん') or not valid(op): continue
        (sex if SEXMARK.search(b) else conv)[op]+=1
    convp=[o for o,_ in conv.most_common(8)] or ['ふふ','あら','ねぇ']
    sexp =[o for o,_ in sex.most_common(8)] or ['あっ','はぁ','ふぁ','あぁ']
    return convp,sexp
def split_n(b):
    m=re.match(r'^(ん[んっぁぅ]*)([、…。～]*)(.*)$',b,re.S)
    return (m.group(1),m.group(2),m.group(3)) if m else None
def sweep(nn,target=0.14,write=True):
    g=glob.glob(f'ERB/CHAR/CHAR_{nn}_*_COM.ERB') or glob.glob(f'ERB/CHAR/CHAR_{nn:02d}_*_COM.ERB')
    P=g[0]
    t=open(P,'rb').read().decode('cp932'); lines=t.split('\r\n')
    convp,sexp=build_pools(t)
    idx=[i for i,l in enumerate(lines) if re.search(r'PRINTFORMW 「ん[んっ、…。～ぁぅ]',l)]
    tot=sum(1 for l in lines if re.search(r'PRINTFORMW 「.',l))
    need=max(0,len(idx)-int(tot*target))
    cc=sc=done=0
    for i in idx:
        if done>=need: break
        mm=re.search(r'PRINTFORMW 「(.*)」',lines[i]); b=mm.group(1)
        sp=split_n(b)
        if not sp: continue
        nk,punct,rest=sp
        if not rest: continue
        if SEXMARK.search(b):
            op=sexp[sc%len(sexp)]; sc+=1
        else:
            op=convp[cc%len(convp)]; cc+=1
        # 長音~の後に ふぅん 等ん終わりは違和感→ん終わりopener回避
        if punct.startswith('～') and op.endswith('ん'): op=op[:-1] or 'あ'
        ind=lines[i][:len(lines[i])-len(lines[i].lstrip())]
        lines[i]=f'{ind}PRINTFORMW 「{op}{punct}{rest}」'; done+=1
    t2='\r\n'.join(lines)
    for x in t2.split('\r\n'): x.encode('cp932')
    assert chr(0x7e) not in t2 and chr(0x2014) not in t2
    nif=sum(1 for l in lines if re.match(r'^\s*IF\b',l)); ne=sum(1 for l in lines if re.match(r'^\s*ENDIF\b',l))
    assert nif==ne,f'IF/ENDIF {nif}/{ne}'
    nstart=sum(1 for l in lines if re.search(r'PRINTFORMW 「ん[んっ、…。～ぁぅ]',l))
    if write: open(P,'wb').write(t2.encode('cp932'))
    return nn,tot,len(idx),done,100*nstart/tot,convp[:4],sexp[:4]
