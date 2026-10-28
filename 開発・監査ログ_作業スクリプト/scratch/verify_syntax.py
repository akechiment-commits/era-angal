# -*- coding: utf-8 -*-
with open('ERB/SHOP_ITEM_ショップアイテム定義.ERB', 'r', encoding='cp932') as f:
    lines = f.readlines()

if_stack = []
repeat_stack = []
for i, line in enumerate(lines, 1):
    code = line.split(';')[0].strip()
    if not code: continue
    tokens = code.split()
    cmd = tokens[0].upper()
    
    if cmd == 'IF':
        if_stack.append((i, code))
    elif cmd == 'ENDIF':
        if not if_stack:
            print(f"Error: Unexpected ENDIF at line {i}")
        else:
            if_stack.pop()
    elif cmd == 'REPEAT' or cmd == 'FOR':
        repeat_stack.append((i, code))
    elif cmd == 'REND' or cmd == 'NEXT':
        if not repeat_stack:
            print(f"Error: Unexpected REND/NEXT at line {i}")
        else:
            repeat_stack.pop()

print(f"Remaining IFs: {len(if_stack)}")
for l, c in if_stack:
    print(f"  Unclosed IF at line {l}: {c}")

print(f"Remaining Loops: {len(repeat_stack)}")
for l, c in repeat_stack:
    print(f"  Unclosed Loop at line {l}: {c}")

if not if_stack and not repeat_stack:
    print("Syntax verification passed! All blocks are perfectly balanced.")
