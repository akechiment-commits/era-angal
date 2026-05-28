# -*- coding: utf-8 -*-
# こよい(28) COM301会話をRAND:10へ拡張＋原作verbatim仕込み（304/399にも）
import re

PATH = 'ERB/CHAR/CHAR_28_星海こよい_COM.ERB'
NL = '\r\n'
T = '\t'

def load():
    with open(PATH, 'rb') as f:
        return f.read().decode('cp932')

def save(text):
    assert NL in text
    for s in re.findall(r'PRINTFORM[LW]\s+「(.*?)」', text):
        s.encode('cp932')  # cp932不可なら例外
    data = text.encode('cp932')
    with open(PATH, 'wb') as f:
        f.write(data)

# ---- COM301 新ブロック（RAND:10）----
KOI = [  # 恋人10
 'なぁ転校生くん、今日あったこと聞いて？　うちな、つゆちゃんとケーキ屋さん行ってきてん♪',
 '転校生くんの声、うち好きやわぁ。なんや、ずっと聞いてたくなるねん',
 'あんな、今度の新月の夜、流れ星がよう見えるんやて。ふたりで見にいこ？',
 'なんでもないことでも、転校生くんとやと話が弾むなぁ。……うち、おしゃべりになってもた？',
 'こうやって、なんでもない話をずっとできたらええなぁ。……これからも、ずっとな♪',
 '転校生くんと一緒のときはいつも、星を見てる気がするわぁ',                         # verbatim
 'すくなくとも、うちは転校生くんと会えて、すこしだけ変われた、って思ってるねんよ♪',   # verbatim
 'うちの好きな鉱石な、転校生くんにも見せたいねん。今度いっしょに、石ころ探しにいかへん？　えへへ',
 'お父やんがな、いっぺん転校生くんを家に呼べって言うねん。……ちょ、ちょっと怖いけど、来てくれる？',
 'うちが落ちこんで屋上におったらな、転校生くんはきっと見つけてくれるやろ？　……えへへ、なんとなく、そう思てん',
]
SHIN = [  # 親密10
 'あ、転校生くん。ちょうど話し相手ほしかってん。ちょっと付きおうて？',
 'うちな、きれいな石集めるのが趣味やねん。鉱石見てると、つい時間忘れてまうわぁ',
 'お父やんがな、また心配して電話してきてん。過保護で、ちょっと困るわぁ。あはは',
 '転校生くんって、聞き上手やね。うち、いつもより喋りすぎてもうたかも',
 '天文部、よかったら見学きてや。屋上から見る星、ほんまにきれいやで',
 'あ、ごめんな。ばぁっと話してもて、何か転校生くんは喋りやすいわぁ',                 # verbatim
 'って、何か愚痴ってもうたな。ほんま、転校生くんは喋りやすいわぁ。ごめんな、変なこと言うて',  # verbatim
 '最近な、夏野さんとお昼いっしょに食べるようになってん。ちょっとずつ、友達増えてきたわぁ♪',
 '月ちゃん先輩、また天文部サボってん。……もう、世話の焼ける先輩やわぁ。あはは',
 '星海ラーメンいうお店な、流れ星の写メ見せたら割引してくれるねん。今度、いっしょにいこ？',
]
TUJO = [  # 通常10
 'えっと……お話、やんね。な、なに話したらええんやろ……',
 'う、うち、あんまり話すの得意やないねん。でも、聞いてくれるんやったら頑張る',
 '（なんか喋らな……。あかん、緊張して言葉がでてこーへん）',
 '天気の話とか……べ、べたすぎるかな。うち、こういうの慣れてへんくて',
 '……あはは。なんやうち、また借りてきた猫みたいになってもうたなぁ',
 'て、転校生くんは、なんの話が好きなん？　うち、合わせるから……えっと',
 '（あ、また困り顔やて言われそう……でも、ほんまは困ってへんねんよ？）',
 'うち、天文部やねん。星の話やったら、なんぼでもできるんやけど……興味、ないかな？',
 'あの、あんまり見つめられると……は、話しづらいわぁ。えと、ちょっとよそ見ててくれる？',
 'えっと、えっと……。あ、あかん、なに話そうとしてたか、忘れてもた……ごめんな？',
]
KOI_FAIL = 'ごめんな、転校生くん。今日はちょっと……ひとりに、させてくれへん？　（なんでやろ、虫の居所が悪いみたい……）'
FAIL = '……ごめんな。今はあんまり、話す気分やないねん。……べつに、転校生くんが嫌とかちゃうよ？　ほんまに'

def build_com301():
    L = []
    a = L.append
    a('IF SELECTCOM == 301')
    a(T+'IF CFLAG:TARGET:211 == 0')
    a(T*2+'CFLAG:TARGET:211 = 1')
    a(T*2+';初回')
    a(T*2+'PRINTFORMW 「うちとお話……？　えっと、なに話そ。あ、あのな、今日の星空はな――って、いきなり星の話はあかんか。あはは」')
    a(T+'ELSE')
    a(T*2+'A = RAND:10')
    a(T*2+';--- 失敗 ---')
    a(T*2+'IF TFLAG:18 == -1')
    a(T*3+'IF TALENT:TARGET:153')
    a(T*4+';恋人・失敗')
    a(T*4+f'PRINTFORMW 「{KOI_FAIL}」')
    a(T*3+'ELSE')
    a(T*4+';失敗')
    a(T*4+f'PRINTFORMW 「{FAIL}」')
    a(T*3+'ENDIF')
    a(T*2+';--- 成功 ---')
    a(T*2+'ELSE')
    def layer(comment, arr, extra_if=None):
        if extra_if is None:
            a(T*3+'IF TALENT:TARGET:153')
        else:
            a(T*3+extra_if)
        a(T*3+comment)
        for i, line in enumerate(arr):
            if i == 0:
                a(T*4+'IF A == 0')
            elif i == 9:
                a(T*4+'ELSE')
            else:
                a(T*4+f'ELSEIF A == {i}')
            a(T*5+f'PRINTFORMW 「{line}」')
        a(T*4+'ENDIF')
    # 恋人
    a(T*3+';--- 恋人 ---')
    a(T*3+'IF TALENT:TARGET:153')
    for i, line in enumerate(KOI):
        a((T*4+'IF A == 0') if i==0 else (T*4+'ELSE') if i==9 else (T*4+f'ELSEIF A == {i}'))
        a(T*5+f'PRINTFORMW 「{line}」')
    a(T*4+'ENDIF')
    # 親密
    a(T*3+';--- 親密（ABL6以上） ---')
    a(T*3+'ELSEIF ABL:TARGET:0 >= 6')
    for i, line in enumerate(SHIN):
        a((T*4+'IF A == 0') if i==0 else (T*4+'ELSE') if i==9 else (T*4+f'ELSEIF A == {i}'))
        a(T*5+f'PRINTFORMW 「{line}」')
    a(T*4+'ENDIF')
    # 通常
    a(T*3+';--- 通常 ---')
    a(T*3+'ELSE')
    for i, line in enumerate(TUJO):
        a((T*4+'IF A == 0') if i==0 else (T*4+'ELSE') if i==9 else (T*4+f'ELSEIF A == {i}'))
        a(T*5+f'PRINTFORMW 「{line}」')
    a(T*4+'ENDIF')
    a(T*3+'ENDIF')
    a(T*2+'ENDIF')
    a(T+'ENDIF')
    a('ENDIF')
    return NL.join(L)

def main():
    t = load()
    lines = t.split(NL)
    # COM301ブロックの範囲特定（IF SELECTCOM == 301 ～ 次の ;--- COM302 直前）
    s = next(i for i,l in enumerate(lines) if l.strip()=='IF SELECTCOM == 301')
    e = next(i for i in range(s+1,len(lines)) if lines[i].lstrip().startswith(';--- COM302'))
    # s..e-1 がCOM301（末尾の空行含む）。空行は残す
    # 末尾の空行を保持するため、最後の非空行までを置換
    last = e-1
    while last>s and lines[last].strip()=='':
        last-=1
    newblock = build_com301().split(NL)
    lines2 = lines[:s] + newblock + lines[last+1:]
    t2 = NL.join(lines2)

    # ---- verbatim仕込み: COM304まったり 恋人A0 ----
    t2 = t2.replace(
      '「転校生くんと一緒やと、なんもせんでも幸せやなぁ。……ずっとこうしてたいわぁ」',
      '「なぁんか、転校生くんと一緒にいると落ちつくねんなぁ」')  # verbatim
    # ---- verbatim仕込み: COM399告白 恋人A0/A1 ----
    t2 = t2.replace(
      '「うちも、転校生くんのこと好きやで。……えへへ、ほんまは、ずっと前からそう言いたかってん♪」',
      '「……転校生くん。君咲学院に来てくれて、おおきに♪」')  # verbatim
    t2 = t2.replace(
      '「なんべん言われても、嬉しいなぁ……。うちも、おんなじ気持ちやで、転校生くん」',
      '「でも、そんな転校生くんが――うち、好っきゃで♪」')  # verbatim(――はcp932安全に正規化)

    save(t2)
    print('COM301をRAND:10へ拡張＋verbatim仕込み（301/304/399）完了')

if __name__ == '__main__':
    main()
