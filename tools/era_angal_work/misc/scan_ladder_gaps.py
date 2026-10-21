import os
import re

erb_files = []
for root, dirs, files in os.walk('ERB'):
    for f in files:
        if f.lower().endswith('.erb'):
            erb_files.append(os.path.join(root, f))

ladder_pat = re.compile(r'^\s*(?:IF|ELSEIF)\s+(ABL|EXP|MARK|PALAM|JUEL)(?::[A-Z0-9]+)*:(\d+)\s*==\s*(\d+)', re.IGNORECASE)

ladder_issues = []

for path in erb_files:
    with open(path, 'r', encoding='cp932') as fp:
        lines = fp.readlines()
        
    current_chain = []
    current_var = None
    
    for idx, line in enumerate(lines, 1):
        clean = line.split(';')[0].strip()
        m = ladder_pat.match(clean)
        if m:
            var_key = (m.group(1).upper(), int(m.group(2)))
            val = int(m.group(3))
            if clean.startswith('IF '):
                # Start new chain
                if len(current_chain) > 2:
                    # check previous chain
                    vals = [v for _, v in current_chain]
                    expected = list(range(vals[0], vals[0] + len(vals)))
                    if vals != expected and sorted(vals) != expected:
                        ladder_issues.append((path, current_var, current_chain))
                current_chain = [(idx, val)]
                current_var = var_key
            elif clean.startswith('ELSEIF ') and var_key == current_var:
                current_chain.append((idx, val))
            else:
                # Different var or construct
                if len(current_chain) > 2:
                    vals = [v for _, v in current_chain]
                    expected = list(range(vals[0], vals[0] + len(vals)))
                    if vals != expected and sorted(vals) != expected:
                        ladder_issues.append((path, current_var, current_chain))
                current_chain = []
                current_var = None
        else:
            if not clean.startswith('ELSE'):
                if len(current_chain) > 2:
                    vals = [v for _, v in current_chain]
                    expected = list(range(vals[0], vals[0] + len(vals)))
                    if vals != expected and sorted(vals) != expected:
                        ladder_issues.append((path, current_var, current_chain))
                current_chain = []
                current_var = None

print(f'Ladder issues found: {len(ladder_issues)}')
for p, var, chain in ladder_issues:
    vals = [v for _, v in chain]
    lines_str = ', '.join([f'L{l}:{v}' for l, v in chain])
    print(f'{p}: {var} -> [{lines_str}]')
