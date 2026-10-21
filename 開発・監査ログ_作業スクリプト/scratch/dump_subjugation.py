# -*- coding: utf-8 -*-
with open('ERB/SHOP_ITEM_ショップアイテム定義.ERB', 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

with open('scratch_subjugation.txt', 'w', encoding='utf-8') as out:
    for i in range(1160, min(1260, len(lines))):
        out.write(f"{i+1}: {lines[i]}")
