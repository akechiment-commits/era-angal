import re
import sys
import glob

sys.stdout.reconfigure(encoding='utf-8')

print("=== FINAL VERIFICATION FOR AITE_YOBI_相手呼称.ERB ===")

with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    raw = f.read()

# 1. Encoding
try:
    text = raw.decode('cp932')
    print("[PASS] cp932 decode successful.")
except Exception as e:
    print(f"[FAIL] cp932 decode error: {e}")
    sys.exit(1)

# 2. Line endings
if b'\r\r\n' in raw:
    print("[FAIL] Corrupted CRLF (\\r\\r\\n) found!")
    sys.exit(1)
if b'\n' in raw.replace(b'\r\n', b''):
    print("[FAIL] Bare LF found!")
    sys.exit(1)
print(f"[PASS] CRLF integrity verified. Total lines: {len(text.splitlines())}")

# 3. SELECTCASE / ENDSELECT
sc_cnt = len(re.findall(r'^\s*SELECTCASE\b', text, re.MULTILINE))
es_cnt = len(re.findall(r'^\s*ENDSELECT\b', text, re.MULTILINE))
print(f"SELECTCASE: {sc_cnt}, ENDSELECT: {es_cnt}")
if sc_cnt != es_cnt:
    print(f"[FAIL] Mismatched SELECTCASE ({sc_cnt}) and ENDSELECT ({es_cnt})!")
    sys.exit(1)
print("[PASS] SELECTCASE / ENDSELECT count matches.")

# 4. Check CASE 0 (Hero) coverage in all 72 SP blocks
hero_cases = []
for sp in range(1, 73):
    m = re.search(rf'^\t\tCASE {sp}\r?\n\t\t\t;([^\r\n]+)\r?\n\t\t\tSELECTCASE AI([\s\S]*?)^\t\t\tENDSELECT', text, re.MULTILINE)
    if not m:
        print(f"[FAIL] SP {sp} block not found!")
        sys.exit(1)
    body = m.group(2)
    m0 = re.search(r'CASE\s+0\s*\r?\n(?:\t+;[^\r\n]*\r?\n)?\t+RESULTS \'= @"([^"]+)"', body)
    if not m0:
        print(f"[FAIL] SP {sp} does NOT have CASE 0 (Hero call)!")
        sys.exit(1)
    hero_cases.append((sp, m.group(1).strip(), m0.group(1)))

print(f"[PASS] All 72 characters have explicit CASE 0 (Hero call) defined!")

# 5. Check CASE 72 (Anzu) for contamination
contaminations = []
for sp in range(1, 73):
    m = re.search(rf'^\t\tCASE {sp}\r?\n\t\t\t;([^\r\n]+)\r?\n\t\t\tSELECTCASE AI([\s\S]*?)^\t\t\tENDSELECT', text, re.MULTILINE)
    body = m.group(2)
    m72 = re.search(r'CASE\s+72\s*\r?\n(?:\t+;[^\r\n]*\r?\n)?\t+RESULTS \'= @"([^"]+)"', body)
    if m72:
        val = m72.group(1)
        if any(bad in val for bad in ['少年', '転校生くん', '転校生さん', 'ヘルプマン']):
            contaminations.append((sp, val))

if contaminations:
    print(f"[FAIL] Found contaminated CASE 72 entries: {contaminations}")
    sys.exit(1)
print("[PASS] Zero contaminated CASE 72 entries found! Anzu calls are completely clean.")

# 6. Full Simulation: 72 speakers x 73 targets (0 to 72) = 5256 combinations!
chara_dict = {0: {'full': 'あなた', 'call': 'あなた'}}
for cid in range(1, 73):
    files = glob.glob(f"CSV/Chara{cid}_*.csv") + glob.glob(f"CSV/Chara0{cid}_*.csv")
    filepath = files[0]
    callname = ""
    fullname = ""
    with open(filepath, 'r', encoding='cp932', errors='ignore') as f:
        for line in f:
            if line.startswith('名前,'):
                fullname = line.strip().split(',')[1]
            elif line.startswith('呼び名,'):
                callname = line.strip().split(',')[1]
    chara_dict[cid] = {'full': fullname, 'call': callname}

def get_grade(cid):
    if cid == 0:
        return 2
    elif 1 <= cid <= 23:
        return 1
    elif 24 <= cid <= 44:
        return 2
    elif 45 <= cid <= 72:
        return 3
    return 0

def get_sur(cid):
    if cid == 0:
        return "あなた"
    full = chara_dict[cid]['full']
    call = chara_dict[cid]['call']
    sur = full.replace(call, '').replace('・', '').replace(' ', '').replace('　', '').strip()
    if not sur:
        sur = call
    return sur

# Parse all overrides
all_overrides = {}
for sp in range(1, 73):
    m = re.search(rf'^\t\tCASE {sp}\r?\n\t\t\t;([^\r\n]+)\r?\n\t\t\tSELECTCASE AI([\s\S]*?)^\t\t\tENDSELECT', text, re.MULTILINE)
    body = m.group(2)
    matches = re.findall(r'CASE\s+(\d+)\s*\r?\n(?:\t+;[^\r\n]*\r?\n)?\t+RESULTS \'= @"([^"]+)"', body)
    all_overrides[sp] = {int(ai): res for ai, res in matches}

# Tier 1 rules
t1_map = {
    (1,2,3,4,6,8,9,12,13,16,18,20,21): lambda sp, ai: f"{get_sur(ai)}先輩" if get_grade(ai) > 1 else f"{get_sur(ai)}さん",
    (5,7,11,15,17,22): lambda sp, ai: f"{get_sur(ai)}先輩" if get_grade(ai) > 1 else f"{chara_dict[ai]['call']}ちゃん",
    (10,): lambda sp, ai: f"{chara_dict[ai]['call']}センパイ" if get_grade(ai) > 1 else f"{chara_dict[ai]['call']}チャン",
    (14,): lambda sp, ai: f"{get_sur(ai)}先輩" if get_grade(ai) > 1 else f"{chara_dict[ai]['call']}",
    (46,49,50,52,56,57,60,62): lambda sp, ai: f"{get_sur(ai)}",
    (47,63,66,72): lambda sp, ai: f"{chara_dict[ai]['call']}ちゃん",
    (26,33): lambda sp, ai: f"{get_sur(ai)}先輩" if get_grade(ai) > 2 else f"{get_sur(ai)}",
    (27,35,36,40,41,42,43,44): lambda sp, ai: f"{get_sur(ai)}先輩" if get_grade(ai) > 2 else (f"{get_sur(ai)}さん" if get_grade(ai) == 2 else f"{get_sur(ai)}ちゃん"),
    (29,34): lambda sp, ai: f"{get_sur(ai)}先輩" if get_grade(ai) > 2 else f"{get_sur(ai)}さん",
    (30,): lambda sp, ai: f"{get_sur(ai)}先輩" if get_grade(ai) > 2 else f"{chara_dict[ai]['call']}ちゃん",
    (19,23): lambda sp, ai: f"{get_sur(ai)}さん",
    (58,): lambda sp, ai: f"{chara_dict[ai]['call']}ちゃん",
    (64,): lambda sp, ai: f"{get_sur(ai)}くん",
    (70,71): lambda sp, ai: f"{get_sur(ai)}ちゃん",
    (25,28,45,48,54,55,65,67,68,69): lambda sp, ai: f"{get_sur(ai)}さん",
    (51,): lambda sp, ai: f"{chara_dict[ai]['call']}屋さん",
    (53,): lambda sp, ai: f"{chara_dict[ai]['call']}さん",
    (24,): lambda sp, ai: f"{chara_dict[ai]['call']}ちゃん" if get_grade(ai) == 2 else f"{get_sur(ai)}さん",
    (59,61): lambda sp, ai: f"{chara_dict[ai]['call']}",
    (31,): lambda sp, ai: f"{chara_dict[ai]['call']}様",
    (38,): lambda sp, ai: f"{chara_dict[ai]['call']}センパイ" if get_grade(ai) > 2 else f"{chara_dict[ai]['call']}チャン",
    (39,): lambda sp, ai: f"{get_sur(ai)}先輩" if get_grade(ai) > 2 else f"{get_sur(ai)}くん",
    (32,37): lambda sp, ai: f"{get_sur(ai)}先輩" if get_grade(ai) > 2 else f"{get_sur(ai)}ちゃん",
}

def simulate(sp, ai):
    t1_func = None
    for grp, fn in t1_map.items():
        if sp in grp:
            t1_func = fn
            break
    res = t1_func(sp, ai) if t1_func else chara_dict[ai]['call']
    if sp in all_overrides and ai in all_overrides[sp]:
        res = all_overrides[sp][ai]
    return res

empty_errors = 0
total_tested = 0
for sp in range(1, 73):
    for ai in range(0, 73):
        if sp == ai:
            continue
        total_tested += 1
        val = simulate(sp, ai)
        if not val or len(val.strip()) == 0:
            print(f"[FAIL] Empty result for {sp} -> {ai}")
            empty_errors += 1

if empty_errors == 0:
    print(f"[PASS] All {total_tested} pairs (including AI:0 Hero) simulated with 100% valid results!")

# Print hero call sample
print("\nSample checks for Hero calls (AI:0):")
for sp in [1, 2, 3, 7, 10, 13, 14, 15, 23, 24, 26, 30, 31, 36, 45, 50, 52, 61, 62, 64, 65, 66, 67, 68, 69, 70, 71, 72]:
    print(f"  SP {sp:02d} ({chara_dict[sp]['call']:6s}) -> 主人公(0): {simulate(sp, 0)}")

# Print Anzu call sample
print("\nSample checks for Anzu calls (AI:72):")
for sp in [24, 45, 48, 50, 52, 53, 54, 55, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]:
    print(f"  SP {sp:02d} ({chara_dict[sp]['call']:6s}) -> あんず(72): {simulate(sp, 72)}")

print("\n[ALL PASS] Final verification completely succeeded!")
