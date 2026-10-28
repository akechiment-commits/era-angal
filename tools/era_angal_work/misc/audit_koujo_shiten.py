# -*- coding: utf-8 -*-
"""視点取り違え監査（§C）。女性限定COM(193正常位/194後背位/195騎乗位/196ペニバン/381着衣SEX)は
相手＝%LOCALS%(助手/他の女子)で、主人公は観客。本文が主人公を相手にしていたら視点取り違えの疑い。
COM204(アナル)だけは主人公相手でOK＝対象外。
使い方:
  python3 tools/audit_koujo_shiten.py        # 全キャラ（疑いに★）
  python3 tools/audit_koujo_shiten.py 23     # cno=23 の該当COM本文を表示
判定ヒント: %LOCALS%が0で主人公呼称>0＝強い疑い。%LOCALS%多数＋主人公少数は観客言及で正常なことが多い(要目視)。
"""
import re,glob,os,sys
SHITEN={193:'正常位させる',194:'後背位させる',195:'騎乗位する',196:'ペニバン挿入',381:'着衣セックスさせる'}
YOBI=['先輩','あなた','お兄ちゃん','転校生','ご主人','旦那','きみ','君']
comf={}
for f in glob.glob('ERB/CHAR/CHAR_*_COM.ERB'):
    b=os.path.basename(f)
    if 'TEMPLATE' in b: continue
    comf[int(re.match(r'CHAR_(\d+)_',b).group(1))]=f
def body(path,com):
    t=open(path,'rb').read().decode('cp932')
    on=False; out=[]
    for l in t.split('\r\n'):
        m=re.search(r'IF\s+SELECTCOM\s*==\s*(\d+)',l)
        if m:
            if on: break
            if int(m.group(1))==com: on=True
        s=l.strip()
        if on and re.match(r'PRINTFORM',s) and not s.startswith(';') and '「' in s:
            out.append(s)
    return out
def name(c): return os.path.basename(comf[c]).replace('_COM.ERB','')
if len(sys.argv)>1:
    c=int(sys.argv[1])
    print(f'== {name(c)} 視点チェック ==')
    for com,lbl in SHITEN.items():
        b=body(comf[c],com)
        print(f'--- COM{com} {lbl} ---')
        for l in b:
            yob=[y for y in YOBI if y in l]
            mark=' ★主人公呼称' if (yob and '%LOCALS%' not in l) else ''
            print(f'   {l[:100]}{mark}')
else:
    print('cno | 各COM[%LOCALS%/主人公呼称] | 疑い(女性限定なのに主人公相手)')
    for c in sorted(comf):
        flag=False; cells=[]
        for com in SHITEN:
            b='\n'.join(body(comf[c],com))
            loc=b.count('%LOCALS%'); yob=sum(b.count(y) for y in YOBI)
            cells.append(f'{com}[{loc}/{yob}]')
            if b and loc==0 and yob>0: flag=True
        print(f'{c:>2} | {" ".join(cells)} |{" ★要確認" if flag else ""}')
