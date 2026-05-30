# -*- coding: utf-8 -*-
# CHAR_22 鯱いかり 蓬莱の薬口上 @HOURAI_KOJO_22（4枠・LF改行維持）
import re
PATH='ERB/KOUJO/KOJO_HOURAI_蓬莱薬口上.ERB'
t=open(PATH,'rb').read().decode('cp932')
assert '\r\n' not in t, 'このファイルはLF。CRLF混入禁止'
# @HOURAI_KOJO_22 区間の4つの空「」を順に埋める
S=[
# CASE0 プレイヤーが先に飲むのを目撃
"え、ししょ～、その薬……不老不死になるやつし!?　うわぁ、本気だしか……。にし、ししょ～がずっと生きるなら、あたしも追いかけるし。ずっと一緒に、泳ぎ続けるしっ！",
# CASE1 自らの意志で飲む（山場・%CALLNAME:PLAYER%）
"にしし、あたしも飲むし！　……ごくん。これで、あたしも不老不死だしっ。%CALLNAME:PLAYER%、これであたしたち、ずっとずっと一緒だし。何百年でも、何千年でも、隣で並んで泳いでいくしっ。『人間魚雷』だって笑われたあたしが、永遠をあなたと過ごせるなんて……にし、しあわせすぎて、また目から水があふれてくるし……っ。約束だし、ぜったい離れないしっ！",
# CASE2 無理やり飲まされる
"んぐっ……ごほっ、な、なに飲ませるし!?　これ、不老不死の薬……!?　うぅ、勝手にこんな……。でも、にし、もう飲んじゃったものは仕方ないし。だったら、この体で精いっぱい生きてやるしっ！",
# CASE3 拒否する
"いらないし！　あたし、不老不死なんていらないしっ。だって、限りがあるから、一瞬一瞬が輝くんだし。あたしは、いまを全力で泳ぐし。永遠なんかより、いまが大事だしっ！",
]
S=[s.replace('〜','～').replace('—','―') for s in S]
for s in S:
    s.encode('cp932')
    assert '私' not in s and 'わたし' not in s and '僕' not in s and '俺' not in s
m=re.search(r'(@HOURAI_KOJO_22\b.*?)(?=@HOURAI_KOJO_|\Z)', t, re.S)
seg=m.group(1)
assert seg.count('「」')==len(S), f"{seg.count('「」')}!={len(S)}"
parts=seg.split('「」')
newseg=parts[0]
for i,s in enumerate(S):
    newseg+='「'+s+'」'+parts[i+1]
t=t[:m.start(1)]+newseg+t[m.end(1):]
assert '\r\n' not in t
data=t.encode('cp932')
open(PATH,'wb').write(data)
print('蓬莱4枠記入 done',len(data),'bytes; @22残り空',newseg.count('「」'))
