# -*- coding: utf-8 -*-
import re, unicodedata
PATH='ERB/CHAR/CHAR_08_丸子みさき_COM.ERB'

def norm(s):
    # 波ダッシュは U+FF5E に正規化（cp932で0x8160）。半角~混入チェック。
    s=s.replace('〜','～')
    if '~' in s: raise SystemExit('半角~混入: '+s)
    s.encode('cp932')  # cp932不可なら例外
    return s

# 原作verbatim（tools/output/みさき_転校生.txt より一字一句）
V_KAIWA = {
 # COM301の PRINTFORMW 出現順 index: [0初,1恋失,2失,3-12恋,13-22親,23-32通]
 13: "先輩、ちょっとお時間よろしいですか？　お喋りしましょ～、あたし先輩に興味津々なんです！　頼みたいこともありますしっ、お暇でしたら♪",  # 親0 (シナリオ2039)
 25: "む、無言で背後に立たないでくださいよ。ビックリしたぁ、声ぐらいかけてくれてもいいのに～？",                                  # 通2 (シナリオ2305)
 27: "先輩は、どんな曲を聴くんですか？　オススメのバンドとか、アーティストとかいたら教えてくださいよ♪",                          # 通4 (シナリオ2040)
}
V_SKIN = {
 # COM303の PRINTFORMW 出現順 index: [0初,1恋失,2失,3-5恋,6-8親,9-11通]
 9: "（うああ……。先輩の手のひら、おっきいな。男のひとだもんね、何かこういうのって新鮮！　テンションあがるぅ～っ♪）",          # 通0 (シナリオ2305・心の声)
}

def patch_com(lines, com, repl):
    sel=[i for i,l in enumerate(lines) if re.search(r'IF SELECTCOM\s*(==|>=)\s*\d+',l)]
    for k,i in enumerate(sel):
        m=re.search(r'IF SELECTCOM\s*==\s*(\d+)',lines[i])
        if m and int(m.group(1))==com:
            end=sel[k+1] if k+1<len(sel) else len(lines)
            for x in range(i,end):
                if lines[x].startswith('@'): end=x; break
            pf=[j for j in range(i,end) if re.search(r'PRINTFORM[LW]\s+「',lines[j])]
            for idx,text in repl.items():
                j=pf[idx]
                old=lines[j]
                new=re.sub(r'「[^」]*」','「'+norm(text)+'」',old,count=1)
                lines[j]=new
            return
    raise SystemExit(f'COM{com}未検出')

c=open(PATH,'rb').read().decode('cp932')
assert '\r\n' in c
before_hash=hash(c)
lines=c.split('\r\n')
patch_com(lines,301,V_KAIWA)
patch_com(lines,303,V_SKIN)
out='\r\n'.join(lines)
data=out.encode('cp932')   # encode確定後に書く
assert out.count('「')==out.count('」')
assert out.count('「」')==0  # 空セリフ復活なし
open(PATH,'wb').write(data)
print('原作verbatim 追加仕込み 完了（会話3＋スキンシップ1）')
# 確認
for kw in ['お時間よろしいですか','無言で背後','どんな曲を聴く','手のひら、おっきい']:
    print('  ✓' if kw in out else '  ✗', kw)
