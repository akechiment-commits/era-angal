# -*- coding: utf-8 -*-
import glob, os, re

def main():
    cooccur_files = [
        '10.txt', '1168.txt', '1171.txt', '1190.txt', '1326.txt', '149.txt', '159.txt',
        '1736.txt', '183.txt', '186.txt', '1929.txt', '1930.txt', '1931.txt', '1932.txt',
        '1933.txt', '1934.txt', '1935.txt', '2270.txt', '2567.txt', '2568.txt', '2724.txt',
        '2725.txt', '2726.txt', '2815.txt', '2816.txt', '2817.txt', '2862.txt', '524.txt',
        '58.txt', '73.txt'
    ]

    output_lines = []
    for fn in cooccur_files:
        fpath = os.path.join('tools', 'scenarios', fn)
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
            lines = fp.readlines()

        output_lines.append(f'==============================')
        output_lines.append(f'=== Scenario {fn} ===')
        output_lines.append(f'==============================')
        for i, l in enumerate(lines):
            l_str = l.strip()
            # print lines around Himari or Reika speaking
            if l_str.startswith('【ひまり】') or l_str.startswith('【れいか】'):
                output_lines.append(l_str)

    with open('tools/era_angal_work/himari_reika_conversations.txt', 'w', encoding='utf-8') as out:
        out.write('\n'.join(output_lines))

    print('Wrote himari_reika_conversations.txt')

if __name__ == '__main__':
    main()
