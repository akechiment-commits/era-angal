# -*- coding: utf-8 -*-
with open('CSV/Palam.csv', 'r', encoding='cp932') as f:
    text = f.read()

with open('scratch_palam.txt', 'w', encoding='utf-8') as out:
    out.write(text)
