import glob, os, sys

sys.stdout.reconfigure(encoding='utf-8')
for cid in range(1, 73):
    files = glob.glob(f'CSV/Chara{cid}_*.csv') + glob.glob(f'CSV/Chara0{cid}_*.csv')
    if files:
        f = files[0]
        with open(f, 'r', encoding='cp932', errors='ignore') as fp:
            for l in fp:
                if l.startswith('名前,'):
                    print(f"{cid:02d}: {l.strip().split(',')[1]} ({os.path.basename(f)})")
                    break
