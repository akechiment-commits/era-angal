# -*- coding: utf-8 -*-
# CHAR_30 長居ゆう 蓬莱の薬 @HOURAI_KOJO_30 (4枠) ※このファイルのみLF維持
import re
PATH = 'ERB/KOUJO/KOJO_HOURAI_蓬莱薬口上.ERB'

# CASE0 目撃 / CASE1 自ら飲む(名前呼び山場) / CASE2 飲まされる / CASE3 拒否
slots = [
"……え。今の、不老不死の薬……？　あなた、飲んじゃったんですか……？　……ふぅん。永遠なんて、面倒くさそうですけどねぇ。……でも。あなたが、ずっといなくならないっていうなら。……わたしも、ちょっとは、気が楽かも。一度くっついたら離れられない、わたしには、ね？",
"ねぇ、%CALLNAME:PLAYER%。……わたしも、飲みます。その、永遠の薬。……笑わないでくださいよ？　面倒くさがりのわたしが、自分から永遠を選ぶなんて。……でもね。わたし、ずっと怖かったんです。大事なものから、引きはがされるのが。お姉ちゃんを手放したときみたいに、また、独りになるのが。……だから、決めました。あなたと、ずっと一緒にいる。何百年でも、何千年でも。隣で居眠りして、屋上で歌って……あなたに、聞いててもらう。……これで、もう、離れられませんねぇ。覚悟、してくださいよ……うふふ〜♪",
"ん、ぐ……っ。……な、何を飲ませたんですか……？　……えっ。不老不死、って……。は……？　わたしの同意もなく、こんな……。……はぁ。マジウゼェですよ、ほんと。……でも。……まぁ、いいです。あなたと、嫌でも永遠に付きあわされるってことでしょう？　……それなら、悪くない。……ふふ。責任、一生、とってくださいねぇ……っ",
"永遠の命……？　うふふ〜、遠慮しときます。……だって、面倒じゃないですか、終わりがないなんて。……それにね。限りがあるから、今が愛おしいんですよ。あなたと過ごす時間が、いつか終わるって知ってるから……。だから、わたしは、ふつうに生きて、ふつうに歳をとります。あなたと、隣で。……それでいい。それが、いいんです。……ね？",
]
slots = [s.replace('—','―').replace('~','〜') for s in slots]
for s in slots:
    try: s.encode('cp932')
    except UnicodeEncodeError as e: raise SystemExit(f'cp932不可: {e} in: {s}')

with open(PATH,'rb') as f: raw=f.read()
assert b'\r\n' not in raw, 'このファイルはLFのはず'
t = raw.decode('cp932')

# @HOURAI_KOJO_30 ブロックを特定（次の @HOURAI_KOJO_ または末尾まで）
m = re.search(r'(@HOURAI_KOJO_30\b.*?)(?=@HOURAI_KOJO_\d|\Z)', t, re.S)
assert m, 'HOURAI_KOJO_30 not found'
block = m.group(1)
assert block.count('「」') == 4, f'空枠が4でない: {block.count(chr(0x300C)+chr(0x300D))}'
parts = block.split('「」')
newblock = parts[0]
for i in range(4):
    newblock += '「'+slots[i]+'」'+parts[i+1]
t2 = t[:m.start(1)] + newblock + t[m.end(1):]
data = t2.encode('cp932')
assert b'\r\n' not in data, 'CRLFが混入した'
with open(PATH,'wb') as f: f.write(data)
print('蓬莱記入完了。ブロック内残り空枠:', newblock.count('「」'))
