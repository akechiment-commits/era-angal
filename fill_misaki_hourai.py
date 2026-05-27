# -*- coding: utf-8 -*-
P='ERB/KOUJO/KOJO_HOURAI_蓬莱薬口上.ERB'
# @HOURAI_KOJO_8 4枠（TFLAG:91 CASE0-3）。このファイルはLF維持。
texts=[
 # CASE0 プレイヤーが先に飲むのを目撃→不老不死の決断を受け止める
 "せ、先輩……それ、不老不死のお薬って……っ。ほ、本気で飲んだんですか……？　……えへへ、しょうがないなぁ、先輩は。じゃあ、あたしも一緒です。先輩だけ永遠に置いていかれるなんて、絶対いやですから。あたしの放送、永遠に聞いてもらいますからねっ♪",
 # CASE1 自らの意志で飲む→プレイヤーとともに永遠を生きると決めた
 "あたし、決めました。このお薬、飲みます。……だって、先輩とずっと一緒にいたいから。考えに考えて、出した答えなんです。永遠に、先輩のそばで、お世話を焼かせてください。……えへへ、これからもよろしくお願いしますね、先輩♪",
 # CASE2 無理やり飲まされる→同意なく不死の運命を強いられた反応
 "ん……っ、な、なに、これ……っ。む、無理やり飲ませるなんて、ひどいですよぉ……っ。……不老不死、なんて。あたし、こんなの望んでなかったのに……。でも……先輩も一緒にいてくれるなら……この永遠も、受け入れます。ひとりじゃ、ないですもんね……？",
 # CASE3 拒否する→永遠の命を断る
 "……ごめんなさい、先輩。あたし、それは飲めません。永遠なんて、あたしには重すぎます。……限りある時間だからこそ、一日一日を全力で、先輩と過ごしたいんです。だから……今のあたしのまま、精いっぱい、先輩を愛させてくださいね？",
]
for s in texts:
    if '~' in s: raise SystemExit('半角~')
    s.encode('cp932')
t=open(P,'rb').read().decode('cp932')
assert '\r\n' not in t, 'このファイルはLF維持'
lines=t.split('\n')
i=next(j for j,l in enumerate(lines) if l.strip()=='@HOURAI_KOJO_8')
end=next((j for j in range(i+1,len(lines)) if lines[j].startswith('@HOURAI_KOJO_')), len(lines))
idx=[j for j in range(i,end) if '「」' in lines[j]]
assert len(idx)==4, len(idx)
it=iter(texts)
for j in idx: lines[j]=lines[j].replace('「」','「'+next(it)+'」',1)
out='\n'.join(lines)
assert '\r\n' not in out
data=out.encode('cp932')
open(P,'wb').write(data)
print('蓬莱 @HOURAI_KOJO_8 記入完了 残り', out.count('「」'),'(全体)')
