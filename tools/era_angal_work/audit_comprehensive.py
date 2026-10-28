import os, glob, re

all_erbs = glob.glob('ERB/**/*.ERB', recursive=True)
print(f'Total ERB files: {len(all_erbs)}')

# 1. Audit GOTO labels
missing_gotos = []
for erb in all_erbs:
    with open(erb, 'r', encoding='cp932', errors='replace') as f:
        lines = f.readlines()
    labels = set()
    gotos = []
    for idx, l in enumerate(lines, 1):
        clean = l.strip()
        if clean.startswith(';') or clean.startswith('['):
            continue
        m_label = re.match(r'^\$([A-Za-z0-9_]+)', clean)
        if m_label:
            labels.add(m_label.group(1).upper())
        m_goto = re.search(r'\bGOTO\s+([A-Za-z0-9_]+)', clean, re.IGNORECASE)
        if m_goto:
            gotos.append((idx, m_goto.group(1).upper(), clean))
    for idx, target, clean in gotos:
        if target not in labels:
            missing_gotos.append((erb, idx, target, clean))

print(f'=== GOTO to undefined label: {len(missing_gotos)} ===')
for m in missing_gotos:
    print(f'  {m[0]}:{m[1]}: target ${m[2]} in: {m[3]}')

# 2. Block nesting check: IF/ENDIF, SELECTCASE/ENDSELECT, REPEAT/REND, FOR/NEXT, WHILE/WEND
nesting_errors = []
for erb in all_erbs:
    with open(erb, 'r', encoding='cp932', errors='replace') as f:
        lines = f.readlines()
    stack = [] # (type, idx, line)
    for idx, l in enumerate(lines, 1):
        clean = l.strip()
        if clean.startswith(';') or clean.startswith('['):
            continue
        # Strip string literals and inline comments
        code = re.sub(r';.*$', '', clean).strip()
        if not code:
            continue
        # Function header resets stack
        if code.startswith('@'):
            if stack:
                nesting_errors.append((erb, idx, f'Unclosed blocks at function header: {stack}'))
                stack = []
            continue
        
        # Starts
        if re.match(r'^(IF\b|SIF\b)', code, re.IGNORECASE):
            if re.match(r'^IF\b', code, re.IGNORECASE):
                stack.append(('IF', idx, code))
        elif re.match(r'^SELECTCASE\b', code, re.IGNORECASE):
            stack.append(('SELECTCASE', idx, code))
        elif re.match(r'^REPEAT\b', code, re.IGNORECASE):
            stack.append(('REPEAT', idx, code))
        elif re.match(r'^FOR\b', code, re.IGNORECASE):
            stack.append(('FOR', idx, code))
        elif re.match(r'^WHILE\b', code, re.IGNORECASE):
            stack.append(('WHILE', idx, code))
        elif re.match(r'^DO\b', code, re.IGNORECASE):
            stack.append(('DO', idx, code))
        
        # Ends
        elif re.match(r'^ENDIF\b', code, re.IGNORECASE):
            if not stack or stack[-1][0] != 'IF':
                nesting_errors.append((erb, idx, f'Mismatched ENDIF, stack was {stack[-1] if stack else "empty"}'))
            else:
                stack.pop()
        elif re.match(r'^ENDSELECT\b', code, re.IGNORECASE):
            if not stack or stack[-1][0] != 'SELECTCASE':
                nesting_errors.append((erb, idx, f'Mismatched ENDSELECT, stack was {stack[-1] if stack else "empty"}'))
            else:
                stack.pop()
        elif re.match(r'^REND\b', code, re.IGNORECASE):
            if not stack or stack[-1][0] != 'REPEAT':
                nesting_errors.append((erb, idx, f'Mismatched REND, stack was {stack[-1] if stack else "empty"}'))
            else:
                stack.pop()
        elif re.match(r'^NEXT\b', code, re.IGNORECASE):
            if not stack or stack[-1][0] != 'FOR':
                nesting_errors.append((erb, idx, f'Mismatched NEXT, stack was {stack[-1] if stack else "empty"}'))
            else:
                stack.pop()
        elif re.match(r'^WEND\b', code, re.IGNORECASE):
            if not stack or stack[-1][0] != 'WHILE':
                nesting_errors.append((erb, idx, f'Mismatched WEND, stack was {stack[-1] if stack else "empty"}'))
            else:
                stack.pop()
        elif re.match(r'^LOOP\b', code, re.IGNORECASE):
            if not stack or stack[-1][0] != 'DO':
                nesting_errors.append((erb, idx, f'Mismatched LOOP, stack was {stack[-1] if stack else "empty"}'))
            else:
                stack.pop()
    if stack:
        nesting_errors.append((erb, len(lines), f'Unclosed blocks at EOF: {stack}'))

print(f'\n=== Block nesting errors: {len(nesting_errors)} ===')
for m in nesting_errors[:15]:
    print(f'  {m[0]}:{m[1]}: {m[2]}')
# 3. Check for single '=' in IF condition (e.g. IF A = B)
single_eq_ifs = []
# 4. Check for unclosed % or { in PRINTFORM* lines
unclosed_macros = []
# 5. Check SIF followed by empty line, comment, or block start
sif_anomalies = []

for erb in all_erbs:
    with open(erb, 'r', encoding='cp932', errors='replace') as f:
        lines = f.readlines()
    for idx, l in enumerate(lines, 1):
        clean = l.strip()
        if clean.startswith(';') or clean.startswith('['):
            continue
        code = re.sub(r';.*$', '', clean).strip()
        if not code:
            continue
        
        # Single equal in IF
        # Match IF var = val where '=' is not '==', '<=', '>=', '!=', '+=', '-=', '*=', '/='
        if re.match(r'^(IF|SIF|ELSEIF)\b', code, re.IGNORECASE):
            # Strip string literals "..."
            cond = re.sub(r'"[^"]*"', '', code)
            # Find any '=' not preceded by <, >, !, =, +, -, *, /, % and not followed by =
            # But beware of string assignments or Ternary operators ? :
            if '?' not in cond:
                m_single_eq = re.search(r'(?<![<>=!+\-*/%])=(?![=])', cond)
                if m_single_eq:
                    single_eq_ifs.append((erb, idx, code))
        
        # SIF anomalies: check what follows SIF
        if re.match(r'^SIF\b', code, re.IGNORECASE):
            # Check next line in file
            next_idx = idx
            while next_idx < len(lines):
                next_l = lines[next_idx].strip()
                if next_l.startswith(';'):
                    sif_anomalies.append((erb, idx, f'SIF followed by comment on line {next_idx+1}: {next_l}'))
                    break
                elif not next_l:
                    sif_anomalies.append((erb, idx, f'SIF followed by blank line on line {next_idx+1}'))
                    break
                else:
                    # Valid statement after SIF
                    # But if statement is IF, SIF, FOR, REPEAT, SELECTCASE, ENDIF, etc. that is invalid in ERB
                    if re.match(r'^(IF|SIF|FOR|REPEAT|WHILE|DO|SELECTCASE|ENDIF|NEXT|REND|WEND|LOOP|ENDSELECT)\b', next_l, re.IGNORECASE):
                        sif_anomalies.append((erb, idx, f'SIF followed by control block statement: {next_l}'))
                    break
                next_idx += 1

        # Unclosed % or { in PRINTFORM* or '@...' or general strings
        if re.match(r'^PRINTFORM', code, re.IGNORECASE):
            # Count %
            pct_count = code.count('%')
            if pct_count % 2 != 0:
                unclosed_macros.append((erb, idx, f'Odd number of % ({pct_count}): {code}'))
            # Count { and }
            brace_open = code.count('{')
            brace_close = code.count('}')
            if brace_open != brace_close:
                unclosed_macros.append((erb, idx, f'Unmatched braces ({{ {brace_open} vs }} {brace_close}): {code}'))

print(f'\n=== Single "=" in IF/SIF/ELSEIF condition: {len(single_eq_ifs)} ===')
for m in single_eq_ifs[:15]:
    print(f'  {m[0]}:{m[1]}: {m[2]}')

print(f'\n=== SIF anomalies (comment/blank/control block immediately after): {len(sif_anomalies)} ===')
for m in sif_anomalies[:15]:
    print(f'  {m[0]}:{m[1]}: {m[2]}')

print(f'\n=== Unclosed macros in PRINTFORM: {len(unclosed_macros)} ===')
for m in unclosed_macros[:15]:
    print(f'  {m[0]}:{m[1]}: {m[2]}')
