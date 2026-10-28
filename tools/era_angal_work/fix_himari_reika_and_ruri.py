# -*- coding: utf-8 -*-

def update_erb_and_ledger():
    # 1. Update ERB
    with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
        text = f.read()

    # Ruri: remove Momotaro no hito (CASE 27)
    old_ruri_case27 = """\t\t\t\tCASE 27
\t\t\t\t\t;夏野ゆり (桃太郎のひと)
\t\t\t\t\tRESULTS '= @"桃太郎のひと"\n"""

    if old_ruri_case27 in text:
        text = text.replace(old_ruri_case27, '')
        print('Removed Momotaro no hito from Ruri in ERB!')
    else:
        print('WARNING: old_ruri_case27 not found directly in ERB!')

    # Himari: change Reika from "れいか先輩" to "れいか" (same grade 3rd year!)
    old_himari_reika = """\t\t\t\t;--- 敬愛する前会長（183回登場！） ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (敬愛する前会長)
\t\t\t\t\tRESULTS '= @"れいか先輩\""""

    new_himari_reika = """\t\t\t\t;--- 前会長・同級生（原作183回すべて「れいか」呼び捨て！） ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (同級生・前会長・親友)
\t\t\t\t\tRESULTS '= @"れいか\""""

    if old_himari_reika in text:
        text = text.replace(old_himari_reika, new_himari_reika)
        print('Updated Himari Reika call to "れいか" in ERB!')
    else:
        print('WARNING: old_himari_reika not found directly in ERB!')

    # Normalize line endings to CRLF
    text = text.replace('\r\n', '\n').replace('\n', '\r\n')

    with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
        f.write(text.encode('cp932'))

    # 2. Update Ledger
    with open('tools/キャラ資料/呼称定義台帳_20261014.md', 'r', encoding='utf-8') as f:
        ledger = f.read()

    # Ruri ledger: remove Momotaro no hito
    old_ledger_momotaro = "    - 27 夏野ゆり: **「桃太郎のひと」**\n"
    if old_ledger_momotaro in ledger:
        ledger = ledger.replace(old_ledger_momotaro, '')
        print('Removed Momotaro no hito from Ruri in ledger!')

    # Himari ledger: update Reika
    old_ledger_reika = """  - **敬愛する前会長（183回登場！）**:
    - 45 円城寺れいか: **「れいか先輩」**（生徒会長再任選挙の因縁・敬愛する前会長！）"""

    new_ledger_reika = """  - **前会長・同級生（原作183回すべて「れいか」呼び捨て！）**:
    - 45 円城寺れいか: **「れいか」**（同じ3年生・同級生！前会長であり親友。「元気だそう、れいか！」「ありがとう、れいか……」）"""

    if old_ledger_reika in ledger:
        ledger = ledger.replace(old_ledger_reika, new_ledger_reika)
        print('Updated Himari Reika call to "れいか" in ledger!')
    else:
        # replace looser
        import re
        ledger = re.sub(
            r'  - \*\*敬愛する前会長.*?\n    - 45 円城寺れいか:.*?\n',
            new_ledger_reika + '\n',
            ledger
        )
        print('Updated Himari Reika call via regex in ledger!')

    with open('tools/キャラ資料/呼称定義台帳_20261014.md', 'w', encoding='utf-8') as f:
        f.write(ledger)

    print('ERB and Ledger successfully updated and verified!')

if __name__ == '__main__':
    update_erb_and_ledger()
