import os
import re

# Check for potential typos in variable names across non-CHAR files
# Common Emuera variables:
# A-Z, COUNT, LOCAL, LOCALS, RESULT, RESULTS
# BASE, MAXBASE, PALAM, UP, DOWN, CUP, CDOWN, LOSEBASE
# ABL, EXP, MARK, TALENT, JUEL, CFLAG, TFLAG, FLAG, ITEM, ITEMSALES, ITEMPRICE, NOITEM
# TEQUIP, EQUIP, STAIN, TIME, DAY, MONEY, CHARANUM, TARGET, MASTER, ASSI, PLAYER
# STR, TSTR, SAVESTR, CSTR, CDFLAG
# PBAND, SELECTCOM, PREVCOM, NEXTCOM

system_files = []
for root, dirs, files in os.walk('ERB'):
    if 'CHAR' in root.upper():
        continue
    for f in files:
        if f.lower().endswith('.erb'):
            system_files.append(os.path.join(root, f))

print(f'Total non-CHAR ERB files: {len(system_files)}')

# Check for undefined variables or suspicious patterns
# In ERB, identifiers starting with alphanumeric that are not commands or defined functions or variables
# Let's check for SELECTCASE without ENDSELECT or CASE without SELECTCASE
select_case_issues = []
for p in system_files:
    with open(p, 'r', encoding='cp932') as fp:
        lines = fp.readlines()
    stack = []
    for idx, line in enumerate(lines, 1):
        clean = line.split(';')[0].strip()
        if re.match(r'^\s*SELECTCASE\b', clean, re.IGNORECASE):
            stack.append((idx, clean))
        elif re.match(r'^\s*ENDSELECT\b', clean, re.IGNORECASE):
            if not stack:
                select_case_issues.append((p, idx, 'ENDSELECT without SELECTCASE', clean))
            else:
                stack.pop()
    for s_idx, s_txt in stack:
        select_case_issues.append((p, s_idx, 'SELECTCASE without ENDSELECT', s_txt))

print(f'Select case issues: {len(select_case_issues)}')

# Check for FOR without NEXT, REPEAT without REND
loop_issues = []
for p in system_files:
    with open(p, 'r', encoding='cp932') as fp:
        lines = fp.readlines()
    for_stack = []
    repeat_stack = []
    while_stack = []
    for idx, line in enumerate(lines, 1):
        clean = line.split(';')[0].strip()
        if re.match(r'^\s*FOR\s+', clean, re.IGNORECASE):
            for_stack.append((idx, clean))
        elif re.match(r'^\s*NEXT\b', clean, re.IGNORECASE):
            if not for_stack:
                loop_issues.append((p, idx, 'NEXT without FOR', clean))
            else:
                for_stack.pop()
        elif re.match(r'^\s*REPEAT\s+', clean, re.IGNORECASE):
            repeat_stack.append((idx, clean))
        elif re.match(r'^\s*REND\b', clean, re.IGNORECASE):
            if not repeat_stack:
                loop_issues.append((p, idx, 'REND without REPEAT', clean))
            else:
                repeat_stack.pop()
        elif re.match(r'^\s*WHILE\s+', clean, re.IGNORECASE):
            while_stack.append((idx, clean))
        elif re.match(r'^\s*WEND\b', clean, re.IGNORECASE):
            if not while_stack:
                loop_issues.append((p, idx, 'WEND without WHILE', clean))
            else:
                while_stack.pop()
                
    for s_idx, s_txt in for_stack:
        loop_issues.append((p, s_idx, 'FOR without NEXT', s_txt))
    for s_idx, s_txt in repeat_stack:
        loop_issues.append((p, s_idx, 'REPEAT without REND', s_txt))
    for s_idx, s_txt in while_stack:
        loop_issues.append((p, s_idx, 'WHILE without WEND', s_txt))

print(f'Loop balance issues: {len(loop_issues)}')
for p, l, kind, txt in loop_issues:
    print(f'  {p}:{l} -> {kind} ({txt})')
