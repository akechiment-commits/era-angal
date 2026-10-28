# -*- coding: utf-8 -*-
with open('ERB/SOURCE_ソース計算・口上呼び出し.ERB', 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

for i in range(820, 880):
    print(f"{i+1}: {lines[i].strip()}")
