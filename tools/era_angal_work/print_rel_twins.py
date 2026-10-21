for fname in ['みづき_関係性.txt', 'みなづき_関係性.txt']:
    print(f"=== {fname} ===")
    with open(f"tools/output/{fname}", 'r', encoding='utf-8', errors='replace') as f:
        print(f.read())
