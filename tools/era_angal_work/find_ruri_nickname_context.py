# -*- coding: utf-8 -*-
import glob, re

def main():
    files = glob.glob('tools/scenarios/*.txt')
    targets = [
        '忍者のひと', '生き神', 'つゆちゃん', 'つゆりのひと', '月ちゃん先輩',
        '桃太郎のひと', 'ダニエルのひと', 'サチエのひと', 'ゆんゆん', 'ゆゆゆ',
        '新聞部のひと', '耳がいいだけのひと', '花嫁のひと', '魔人のひと'
    ]

    results = []
    for f in files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
            if '【るり】' in content:
                for t in targets:
                    if t in content:
                        lines = content.splitlines()
                        for i, l in enumerate(lines):
                            if t in l:
                                # get context lines around it
                                start = max(0, i - 4)
                                end = min(len(lines), i + 5)
                                ctx = '\n'.join(lines[start:end])
                                results.append(f'=== [{os.path.basename(f)}] Target: {t} ===\n{ctx}\n')

    with open('tools/era_angal_work/ruri_unique_nicknames_context.txt', 'w', encoding='utf-8') as out:
        out.write('\n'.join(results))
    print('Wrote ruri_unique_nicknames_context.txt, count:', len(results))

if __name__ == '__main__':
    import os
    main()
