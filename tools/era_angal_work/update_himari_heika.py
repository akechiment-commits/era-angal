# -*- coding: utf-8 -*-

def update_to_heika():
    # 1. Update ERB
    with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
        text = f.read()

    old_target = """\t\t\t\t;--- 前会長・同級生（原作183回すべて「れいか」呼び捨て！） ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (同級生・前会長・親友)
\t\t\t\t\tRESULTS '= @"れいか\""""

    new_target = """\t\t\t\t;--- 敬愛する前会長（「陛下」原作91回登場・最重要固有呼称！） ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (敬愛する前会長・君主「陛下」)
\t\t\t\t\tRESULTS '= @"陛下\""""

    if old_target in text:
        text = text.replace(old_target, new_target)
        print('Updated Himari Reika call to "陛下" in ERB!')
    else:
        print('WARNING: old_target not found directly in ERB!')

    # Normalize line endings to CRLF
    text = text.replace('\r\n', '\n').replace('\n', '\r\n')

    with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
        f.write(text.encode('cp932'))

    # 2. Update Ledger
    with open('tools/キャラ資料/呼称定義台帳_20261014.md', 'r', encoding='utf-8') as f:
        ledger = f.read()

    old_ledger_target = """  - **前会長・同級生（原作183回すべて「れいか」呼び捨て！）**:
    - 45 円城寺れいか: **「れいか」**（同じ3年生・同級生！前会長であり親友。「元気だそう、れいか！」「ありがとう、れいか……」）"""

    new_ledger_target = """  - **敬愛する前会長・絶対的君主（原作91回登場・最重要固有呼称！）**:
    - 45 円城寺れいか: **「陛下」**（「へぇぇぇいかぁぁぁああ！」「陛下ぁ陛下ぁへぇいぃかぁあ～ん♪」「陛下～陛下ぁ～♪ ごろごろ♪」「ずっと陛下付きの女中だったからなあ」前生徒会長であり絶対的君主。※対等な場面や真面目な場面では「れいか」とも呼ぶ）"""

    if old_ledger_target in ledger:
        ledger = ledger.replace(old_ledger_target, new_ledger_target)
        print('Updated Himari Reika call to "陛下" in ledger!')
    else:
        import re
        ledger = re.sub(
            r'  - \*\*前会長・同級生.*?\n    - 45 円城寺れいか:.*?\n',
            new_ledger_target + '\n',
            ledger
        )
        print('Updated Himari Reika call via regex in ledger!')

    with open('tools/キャラ資料/呼称定義台帳_20261014.md', 'w', encoding='utf-8') as f:
        f.write(ledger)

    print('Successfully updated ERB and ledger to 陛下!')

if __name__ == '__main__':
    update_to_heika()
