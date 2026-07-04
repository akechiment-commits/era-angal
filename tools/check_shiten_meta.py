# -*- coding: utf-8 -*-
"""女子相手COMの「転校生観客メタ」「コマンド解説」台詞 検出 lint。
相手=女子(%LOCALS%)のCOMで、台詞が主人公の観覧/命令に言及(メタ)、または行為の種類/立場を解説していないかを洗い出す。
使い方: python3 tools/check_shiten_meta.py [NN ...]  (既定=全CHAR)
"""
import re, sys, glob
try:
    from kojo_util import join_kojo
except ImportError:
    from tools.kojo_util import join_kojo

TG={23,61,63,65,68,192,200,203,193,194,195,196,381}
META=re.compile(r'転校生.{0,8}(見|ご覧|興奮|楽し)|君に見られ|見ててね|見てて[？\?]|命令だ|見たいんでしょ|見て興奮|見て楽しん|見たいって言うから')
KAI=re.compile(r'攻める番|挿れる側|ペニバン|攻守|組み敷かれ|女の子同士')
def run(paths):
    tot=0
    for f in paths:
        t=join_kojo(open(f,'rb').read().decode('cp932')); cur=None; out=[]
        for i,l in enumerate(t.split('\n'),1):
            m=re.search(r'SELECTCOM\s*==\s*(\d+)',l)
            if m: cur=int(m.group(1))
            if cur in TG and 'PRINTFORMW' in l and '「' in l:
                tag=''
                if META.search(l): tag+='[メタ]'
                if KAI.search(l): tag+='[解説]'
                if tag: out.append(f'{f}:{i} C{cur}{tag} {l.strip()}')
        if out:
            print('\n'.join(out)); tot+=len(out)
    print(f'\n--- 該当 {tot} 件 ---')
if __name__=='__main__':
    args=sys.argv[1:]
    if args:
        paths=[g for a in args for g in glob.glob(f'ERB/CHAR/CHAR_{int(a)}_*_COM.ERB')]
    else:
        paths=sorted(glob.glob('ERB/CHAR/CHAR_*_COM.ERB'))
    run(paths)
