# -*- coding: utf-8 -*-
import os, re

def apply_fixes():
    # 1. CHAR_09 月永るか.ERB:779 (already done or check)
    path_09 = 'ERB/CHAR/CHAR_09_月永るか.ERB'
    with open(path_09, 'r', encoding='cp932') as f:
        t09 = f.read()
    if 'わたしの種' in t09:
        t09 = t09.replace('わたしの種', 'ぼくの種')
        with open(path_09, 'wb') as f:
            f.write(t09.replace('\r\n', '\n').replace('\n', '\r\n').encode('cp932'))
        print("Fixed CHAR_09")
    else:
        print("CHAR_09 already fixed")

    # 2. CHAR_32 安条まい_COM.ERB:1704
    path_32 = 'ERB/CHAR/CHAR_32_安条まい_COM.ERB'
    with open(path_32, 'r', encoding='cp932') as f:
        t32 = f.read()
    if '「うち、晩ご飯いつも独りでさ……。' in t32:
        t32 = t32.replace('「うち、晩ご飯いつも独りでさ……。', '「あたし、晩ご飯いつも独りでさ……。')
        with open(path_32, 'wb') as f:
            f.write(t32.replace('\r\n', '\n').replace('\n', '\r\n').encode('cp932'))
        print("Fixed CHAR_32")
    else:
        print("CHAR_32 already fixed")

    # 3. CHAR_67 日滝ましろ_COM.ERB:3621
    path_67 = 'ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB'
    with open(path_67, 'r', encoding='cp932') as f:
        t67 = f.read()
    if '「わっ、あたしが%LOCALS%に！？' in t67:
        t67 = t67.replace('「わっ、あたしが%LOCALS%に！？', '「わっ、私が%LOCALS%に！？')
        with open(path_67, 'wb') as f:
            f.write(t67.replace('\r\n', '\n').replace('\n', '\r\n').encode('cp932'))
        print("Fixed CHAR_67")
    else:
        print("CHAR_67 already fixed")

    # 4. CHAR_46 双葉みづき_COM.ERB:403 (COM307 視点逆転)
    path_46 = 'ERB/CHAR/CHAR_46_双葉みづき_COM.ERB'
    with open(path_46, 'r', encoding='cp932') as f:
        t46 = f.read()
    if '「ほら、櫛でとかしてやる～。ありがたく思え、みづき様の手づからだぞ☆」' in t46:
        t46 = t46.replace('「ほら、櫛でとかしてやる～。ありがたく思え、みづき様の手づからだぞ☆」',
                          '「ふふん、丁寧に梳かせよ～？　髪は女の子の命なんだからな、ありがたく思えよ☆」')
        with open(path_46, 'wb') as f:
            f.write(t46.replace('\r\n', '\n').replace('\n', '\r\n').encode('cp932'))
        print("Fixed CHAR_46 COM307 viewpoint")
    else:
        print("CHAR_46 already fixed")

    # 5. %LOCALS%さん -> %LOCALS% in CHAR_28, 29, 53, 55
    locals_targets = [
        'ERB/CHAR/CHAR_28_星海こよい_COM.ERB',
        'ERB/CHAR/CHAR_29_春風なな_COM.ERB',
        'ERB/CHAR/CHAR_53_花丘まり_COM.ERB',
        'ERB/CHAR/CHAR_55_伊藤さくら_COM.ERB',
    ]

    for fpath in locals_targets:
        with open(fpath, 'r', encoding='cp932') as f:
            content = f.read()
        cnt = content.count('%LOCALS%さん')
        if cnt > 0:
            content = content.replace('%LOCALS%さん', '%LOCALS%')
            with open(fpath, 'wb') as f:
                f.write(content.replace('\r\n', '\n').replace('\n', '\r\n').encode('cp932'))
            print(f"Fixed {cnt} occurrences of '%LOCALS%さん' in {os.path.basename(fpath)}")
        else:
            print(f"No occurrences in {os.path.basename(fpath)}")

    print("All fixes applied successfully!")

if __name__ == '__main__':
    apply_fixes()
