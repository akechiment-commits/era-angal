# -*- coding: utf-8 -*-
import glob, re

speakers = set()
for f in glob.glob('tools/scenarios/*.txt'):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        for line in fp:
            m = re.match(r'【(.*?)】', line)
            if m:
                speakers.add(m.group(1))

print(f'Total unique speakers: {len(speakers)}')
sorted_speakers = sorted(list(speakers))
with open('tools/era_angal_work/all_scenario_speakers.txt', 'w', encoding='utf-8') as out:
    for s in sorted_speakers:
        out.write(s + '\n')

print('Wrote all_scenario_speakers.txt')
