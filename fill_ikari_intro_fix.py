# -*- coding: utf-8 -*-
# 導入喘ぎ型率の調整：冒頭「ひゃ」「ふぁ」を非該当形へ分散振替（いかり口調維持）
import re
PATH='ERB/CHAR/CHAR_22_鯱いかり_COM.ERB'
raw=open(PATH,'rb').read()
t=raw.decode('cp932')
lines=t.split('\r\n')
ke=st=None
for i,l in enumerate(lines):
    if re.match(r'@KOJO_MESSAGE_COM_22',l): ke=i
    if re.match(r'@CHAR_ORGASM_22',l): st=i;break

# ORGASM: 「ふぁ」→「あぁ」（全件）
for j in range(st,len(lines)):
    m=re.search(r'(PRINTFORMW\s*「)(.*)(」)$',lines[j])
    if not m: continue
    q=m.group(2)
    if q.startswith('ふぁ'):
        q2='あぁ'+q[2:]
        lines[j]=m.group(1)+q2+m.group(3)

# 通常: 「ひゃ*」を約7割、非該当形へローテーション振替
hyrep={'ひゃうっ':['うひゃっ','ふにゃっ'],
       'ひゃあっ':['うわぁっ','ふにゃあっ'],
       'ひゃんっ':['ふにゃんっ','うひゃんっ'],
       'ひゃっ':['わっ','うわっ','ふにゃっ']}
ci=0; conv=0; seen=0
for j in range(ke,st):
    m=re.search(r'(PRINTFORMW\s*「)(.*)(」)$',lines[j])
    if not m: continue
    q=m.group(2)
    key=None
    for k in ['ひゃうっ','ひゃあっ','ひゃんっ','ひゃっ']:
        if q.startswith(k): key=k;break
    if not key: continue
    seen+=1
    if seen%10<7:  # 約7割を変換
        opts=hyrep[key]; rep=opts[ci%len(opts)]; ci+=1
        q2=rep+q[len(key):]
        lines[j]=m.group(1)+q2+m.group(3)
        conv+=1
print('ひゃ変換',conv,'/',seen)
out='\r\n'.join(lines)
assert out.count('「」')==0
data=out.encode('cp932')
open(PATH,'wb').write(data)
print('done',len(data),'bytes')
