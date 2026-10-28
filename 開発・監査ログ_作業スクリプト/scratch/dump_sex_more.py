# -*- coding: utf-8 -*-
with open('scratch_com_sex.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(100, min(len(lines), 300)):
    print(lines[i].strip())
