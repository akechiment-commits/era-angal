with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
    lines = f.readlines()

for i in range(19, 145):
    print(f"{i+1}: {lines[i]}", end='')
