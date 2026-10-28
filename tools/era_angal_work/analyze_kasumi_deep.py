import re

with open('tools/era_angal_work/kasumi_all_dialogue.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Patterns of vocative:
# e.g., 「...、○○...」 or 「○○、...」 or 「...○○さん」 etc.
# Also search every character name in the game (all 72 characters)
with open('tools/era_angal_work/check_3a_files.py', 'r', encoding='utf-8') as f:
    code = f.read()
exec(code.split('# Output files mapping')[0])

calls_by_chara = {}
for cid, full, sur, cn, grade in chara_names:
    if cid == 51:
        continue
    # search mentions
    pats = [sur, cn]
    found = []
    for l in lines:
        for p in pats:
            if len(p) >= 2 and p in l:
                # find the whole phrase around p
                m = re.findall(rf'([^。！？\n「」]{{0,10}}{re.escape(p)}[^。！？\n「」]{{0,10}})', l)
                for match in m:
                    found.append((match.strip(), l.strip()))
    if found:
        calls_by_chara[cid] = (full, grade, found)

with open('tools/era_angal_work/kasumi_calls_detailed.txt', 'w', encoding='utf-8') as out:
    out.write("=== 御影かすみ 全キャラ呼称精密解析 ===\n")
    for cid in sorted(calls_by_chara.keys()):
        full, grade, found = calls_by_chara[cid]
        out.write(f"\nID {cid:02d}: {full} ({grade}年) - {len(found)}件\n")
        # count phrases
        phrase_counts = {}
        for phr, l in found:
            phrase_counts[phr] = phrase_counts.get(phr, 0) + 1
        for phr, c in sorted(phrase_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            out.write(f"   フレーズ: 『{phr}』 ({c}回)\n")
        for phr, l in found[:3]:
            out.write(f"      セリフ例: {l[:80]}\n")

# Also check Kasumi's general tone, 2nd person pronouns (お前, あんた, あなた, 貴女, きみ, おぬし, そなた, 主, etc.)
pronouns = {}
for pro in ['あなた', '貴方', '貴女', 'あんた', 'お前', 'きみ', '君', 'おぬし', 'そなた', '主', '其方', '汝', '自分', '妾', '私', 'わたし', 'わたくし', '魔人', '閣下']:
    cnt = sum(l.count(pro) for l in lines)
    if cnt > 0:
        pronouns[pro] = cnt

print("Pronouns in Kasumi lines:", pronouns)
print("Saved kasumi_calls_detailed.txt")
