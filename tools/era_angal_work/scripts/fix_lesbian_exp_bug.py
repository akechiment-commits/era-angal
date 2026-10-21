# -*- coding: utf-8 -*-
"""
朝イベント（EVENT_MORNING）および一部コマンドで、
男性主人公時にもかかわらずレズ経験（EXP:40）が誤加算されてしまう不具合を修正するスクリプト。
"""

def fix_morning_events():
    path = 'ERB/EVENT_MORNING_朝のイベント.ERB'
    with open(path, 'rb') as f:
        text = f.read().decode('cp932').replace('\r\n', '\n')

    # Case 1: Line 1957-1963
    old_block_1 = '''\t\tEXP:23 += A
\t\tEXP:96 += A
\t\tEXP:40 += A
\t\tEXP:MASTER:96 += A
\t\tPRINTFORML %EXPNAME:23%＋{A}
\t\tPRINTFORML %EXPNAME:96%＋{A}
\t\tPRINTFORML %EXPNAME:40%＋{A}'''

    new_block_1 = '''\t\tEXP:23 += A
\t\tEXP:96 += A
\t\tEXP:MASTER:96 += A
\t\tPRINTFORML %EXPNAME:23%＋{A}
\t\tPRINTFORML %EXPNAME:96%＋{A}
\t\tIF (TALENT:MASTER:122 == 0) && (TALENT:122 == 0)
\t\t\tEXP:40 += A
\t\t\tEXP:MASTER:40 += A
\t\t\tPRINTFORML %EXPNAME:40%＋{A}
\t\tENDIF'''

    assert old_block_1 in text, "old_block_1 not found in EVENT_MORNING"
    text = text.replace(old_block_1, new_block_1, 1)

    # Case 2: Line 2049-2055
    old_block_2 = '''\t\tEXP:23 += A
\t\tEXP:96 += A*2
\t\tEXP:40 += A
\t\tEXP:MASTER:96 += A*2
\t\tPRINTFORML %EXPNAME:23%＋{A}
\t\tPRINTFORML %EXPNAME:96%＋{A*2}
\t\tPRINTFORML %EXPNAME:40%＋{A}'''

    new_block_2 = '''\t\tEXP:23 += A
\t\tEXP:96 += A*2
\t\tEXP:MASTER:96 += A*2
\t\tPRINTFORML %EXPNAME:23%＋{A}
\t\tPRINTFORML %EXPNAME:96%＋{A*2}
\t\tIF (TALENT:MASTER:122 == 0) && (TALENT:122 == 0)
\t\t\tEXP:40 += A
\t\t\tEXP:MASTER:40 += A
\t\t\tPRINTFORML %EXPNAME:40%＋{A}
\t\tENDIF'''

    assert old_block_2 in text, "old_block_2 not found in EVENT_MORNING"
    text = text.replace(old_block_2, new_block_2, 1)

    # Case 3: Line 2141-2147
    old_block_3 = '''\t\tEXP:23 += A
\t\tEXP:96 += A*2
\t\tEXP:40 += A*2
\t\tEXP:MASTER:96 += A*2
\t\tPRINTFORML %EXPNAME:23%＋{A}
\t\tPRINTFORML %EXPNAME:96%＋{A*2}
\t\tPRINTFORML %EXPNAME:40%＋{A*2}'''

    new_block_3 = '''\t\tEXP:23 += A
\t\tEXP:96 += A*2
\t\tEXP:MASTER:96 += A*2
\t\tPRINTFORML %EXPNAME:23%＋{A}
\t\tPRINTFORML %EXPNAME:96%＋{A*2}
\t\tIF (TALENT:MASTER:122 == 0) && (TALENT:122 == 0)
\t\t\tEXP:40 += A*2
\t\t\tEXP:MASTER:40 += A*2
\t\t\tPRINTFORML %EXPNAME:40%＋{A*2}
\t\tENDIF'''

    assert old_block_3 in text, "old_block_3 not found in EVENT_MORNING"
    text = text.replace(old_block_3, new_block_3, 1)

    with open(path, 'wb') as f:
        f.write(text.replace('\n', '\r\n').encode('cp932'))
    print("EVENT_MORNING_朝のイベント.ERB fixed.")

def fix_comf160():
    path = 'ERB/COMF/COMF160.ERB'
    with open(path, 'rb') as f:
        text = f.read().decode('cp932').replace('\r\n', '\n')

    old = ''';レズ経験（助手）
PRINTS EXPNAME:40
PRINTL +8
EXP:40 += 8
EXP:PLAYER:40 += 8'''

    new = ''';レズ経験（助手）
IF TALENT:PLAYER:122 == 0 && TALENT:TARGET:122 == 0
\tPRINTS EXPNAME:40
\tPRINTL +8
\tEXP:40 += 8
\tEXP:PLAYER:40 += 8
ENDIF'''

    if old in text:
        text = text.replace(old, new, 1)
        with open(path, 'wb') as f:
            f.write(text.replace('\n', '\r\n').encode('cp932'))
        print("COMF160.ERB fixed.")

def fix_comf188():
    path = 'ERB/COMF/COMF188.ERB'
    with open(path, 'rb') as f:
        text = f.read().decode('cp932').replace('\r\n', '\n')

    old = ''';ふたなり同士のV挿入（助手） 挿入行為でともに+10
PRINTS EXPNAME:40
PRINTL +10
EXP:40 += 10
EXP:PLAYER:40 += 10'''

    new = ''';ふたなり同士のV挿入（助手） 挿入行為でともに+10
IF TALENT:PLAYER:122 == 0 && TALENT:TARGET:122 == 0
\tPRINTS EXPNAME:40
\tPRINTL +10
\tEXP:40 += 10
\tEXP:PLAYER:40 += 10
ENDIF'''

    if old in text:
        text = text.replace(old, new, 1)
        with open(path, 'wb') as f:
            f.write(text.replace('\n', '\r\n').encode('cp932'))
        print("COMF188.ERB fixed.")

def main():
    fix_morning_events()
    fix_comf160()
    fix_comf188()
    print("All lesbian exp bugs fixed.")

if __name__ == '__main__':
    main()
