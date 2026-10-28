# -*- coding: utf-8 -*-
import glob

f_target = glob.glob('ERB/*EVENT_M*')[1]
with open(f_target, 'r', encoding='cp932', errors='ignore') as f:
    lines = f.readlines()

def find_com_messages(com_list):
    inside_com = None
    output = []
    for i, line in enumerate(lines, 1):
        for c in com_list:
            if line.strip().startswith(f'@TRAIN_MESSAGE_{c}'):
                inside_com = c
                output.append(f"=== {inside_com} at line {i} ===")
                break
        if inside_com:
            output.append(f"{i}: {line.strip()}")
            if len(output) > 200: # limit per check
                pass
            if line.strip().startswith('@') and not line.strip().startswith(f'@TRAIN_MESSAGE_{inside_com}'):
                inside_com = None

with open('scratch_com_sex.txt', 'w', encoding='utf-8') as out:
    inside = None
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('@TRAIN_MESSAGE_COM20') or \
           line.strip().startswith('@TRAIN_MESSAGE_COM21') or \
           line.strip().startswith('@TRAIN_MESSAGE_COM24') or \
           line.strip().startswith('@TRAIN_MESSAGE_COM25') or \
           line.strip().startswith('@TRAIN_MESSAGE_COM34'):
            inside = True
            out.write(f"\n====================\nLine {i}: {line.strip()}\n====================\n")
        elif inside and line.strip().startswith('@TRAIN_MESSAGE_'):
            inside = False
        if inside:
            out.write(f"{i}: {line.strip()}\n")
