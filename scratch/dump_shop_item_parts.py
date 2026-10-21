# -*- coding: utf-8 -*-
with open('ERB/SHOP_ITEM_ショップアイテム定義.ERB', 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

def dump_range(start, end, label):
    print(f"=== {label} ({start}-{end}) ===")
    for i in range(start - 1, min(len(lines), end)):
        print(f"{i+1}: {lines[i].rstrip()}")

dump_range(200, 218, "ITEMSALES 86, 87")
dump_range(570, 590, "ITEM DESCRIPTION 86, 87")
dump_range(620, 632, "TARGET SELECT 86, 87")
dump_range(1148, 1262, "ITEM USE 86, 87")
