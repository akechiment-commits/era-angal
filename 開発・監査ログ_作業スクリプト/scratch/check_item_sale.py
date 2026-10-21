# -*- coding: utf-8 -*-
with open('ERB/SHOP_ITEM_ショップアイテム定義.ERB', 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

with open('scratch_item_sale.txt', 'w', encoding='utf-8') as out:
    for i, line in enumerate(lines, 1):
        if 'ITEMSALES:86' in line or 'ITEMSALES:87' in line or 'ITEM:86' in line or 'ITEM:87' in line or 'BOUGHT == 86' in line:
            for j in range(max(0, i - 5), min(len(lines), i + 10)):
                out.write(f"{j+1}: {lines[j]}")
            out.write("---------------------\n")
