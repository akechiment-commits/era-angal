# -*- coding: utf-8 -*-
targets = [
    ('ERB/SHOP_ITEM_ショップアイテム定義.ERB', 1138),
    ('ERB/SYS_THREE_MONTHS_3ヶ月サイクル処理.ERB', 226),
    ('ERB/COMF/COMF302.ERB', 443),
    ('ERB/COMF/COMF302.ERB', 478),
]

with open('scratch_souai_details.txt', 'w', encoding='utf-8') as out:
    for path, line_no in targets:
        out.write(f"\n====================\n{path}:{line_no}\n====================\n")
        with open(path, 'r', encoding='cp932', errors='ignore') as f:
            lines = f.readlines()
            start = max(0, line_no - 25)
            end = min(len(lines), line_no + 15)
            for idx in range(start, end):
                prefix = ">>> " if idx + 1 == line_no else "    "
                out.write(f"{prefix}{idx+1}: {lines[idx]}")

    # Also let's check ITEMSALES:85 (エンゲージリングの販売条件)
    out.write("\n====================\nITEMSALES:85 (エンゲージリング販売条件)\n====================\n")
    with open('ERB/SHOP_ITEM_ショップアイテム定義.ERB', 'r', encoding='cp932', errors='ignore') as f:
        lines = f.readlines()
        for idx in range(185, 205):
            if idx < len(lines):
                out.write(f"{idx+1}: {lines[idx]}")
