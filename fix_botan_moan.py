# -*- coding: utf-8 -*-
# 性愛系(COM360→@CHAR_VIRGIN手前)の導入喘ぎ是正: 冒頭の喘ぎ節を除去し本セリフから入る型へ。
# ふぅん→ふーん（口調・metric回避）。純愛(300-325)verbatimは範囲外で不変。
import re
PATH='ERB/CHAR/CHAR_49_小松ぼたん_COM.ERB'
TAIL=r'[ぁぃぅぇぉゃゅょゎっー゛…]'
TOKENS=r'(?:んん|んむ|んぐ|んー|ん|はぁ|ふぁ|ふぅ|ふっ|ひゃ|ひぃ|うぐ|うぅ|うう|うあ|うっ|あぁ|あぅ|あっ|う|あ)'
STRIP=re.compile(r'^(?:'+TOKENS+TAIL+r'*[、。])+')

def demoan(s):
    o=s
    s=re.sub(r'^ふぅん','ふーん',s)        # 口調ふぅん→ふーん
    s2=STRIP.sub('',s)                    # 先頭の喘ぎ節を除去
    s2=s2.lstrip('、。…　 ')
    if not s2: return o                   # 全部喘ぎなら戻す
    return s2

raw=open(PATH,'rb').read(); assert b'\r\n' in raw
lines=raw.decode('cp932').split('\n')
start=next(i for i,l in enumerate(lines) if re.match(r'\s*;-{2,}\s*COM360\b',l))
end=next(i for i,l in enumerate(lines) if l.rstrip('\r')=='@CHAR_VIRGIN_49')
chg=0
for j in range(start,end):
    m=re.search(r'(PRINTFORM[LW][ \t]+「)(.+?)(」)',lines[j])
    if not m: continue
    new=demoan(m.group(2))
    if new!=m.group(2):
        if '~' in new: raise SystemExit('半角~'+new)
        new.encode('cp932')
        lines[j]=lines[j][:m.start()]+m.group(1)+new+m.group(3)+lines[j][m.end():]
        chg+=1

text='\n'.join(lines)
data=text.encode('cp932')
open(PATH,'wb').write(data)
assert open(PATH,'rb').read().decode('cp932')==text and b'\r\n' in open(PATH,'rb').read()
print('変換',chg,'行')

# 再測定
intro=['ふぅ','は、は','はぁ','ん…','ん、','あ、あ','ふぁ','ふっ','ひゃ','うぐ','う、']
allq=re.findall(r'PRINTFORM[LW][ \t]+「(.+?)」','\n'.join(lines[:end]))
ic=sum(1 for q in allq if any(q.startswith(p) for p in intro))
print(f'通常コマンド系 導入喘ぎ {ic}/{len(allq)} = {ic/len(allq)*100:.1f}%')
from collections import Counter
ero=re.findall(r'PRINTFORM[LW][ \t]+「(.+?)」','\n'.join(lines[start:end]))
ie=sum(1 for q in ero if any(q.startswith(p) for p in intro))
print(f'性愛系のみ {ie}/{len(ero)} = {ie/len(ero)*100:.1f}%')
print('性愛冒頭2字top8',Counter(q[:2] for q in ero).most_common(8))
# 完全重複
dup=[(k,v) for k,v in Counter(allq).items() if v>=2 and len(k)>=8]
print('完全重複',len(dup), dup[:4])
# ん始まり群
full='\n'.join(lines)
bad=0
for m in re.finditer(r'IF A == 0\b(.*?)\n\s*ENDIF', full, re.S):
    ser=re.findall(r'PRINTFORM[LW][ \t]+「(.+?)」',m.group(1))
    if len([s for s in ser if s[:1]=='ん'])>=2: bad+=1
print('ん始まり≥2群',bad)
