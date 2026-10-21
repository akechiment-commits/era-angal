with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
    lines = f.readlines()

# Print lines 400 to 520
print("=== Section 1 (around 400-520) ===")
for i in range(410, 520):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')

# Print lines 1260 to 1460
print("\n=== Section 2 (around 1260-1460) ===")
for i in range(1260, 1460):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
