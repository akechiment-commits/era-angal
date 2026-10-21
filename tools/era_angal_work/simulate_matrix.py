import sys, os, glob, re

sys.stdout.reconfigure(encoding='utf-8')

# Load chara info
chara_dict = {}
for cid in range(1, 73):
    files = glob.glob(f"CSV/Chara{cid}_*.csv") + glob.glob(f"CSV/Chara0{cid}_*.csv")
    if not files:
        continue
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

# Parse AITE_YOBI logic in python
with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
    text = f.read()

def get_grade(cid):
    if 1 <= cid <= 23:
        return 1
    elif 24 <= cid <= 44:
        return 2
    elif 45 <= cid <= 72:
        return 3
    return 0

def get_sur(cid):
    full = chara_dict[cid]['full']
    call = chara_dict[cid]['call']
    sur = full.replace(call, '').replace('・', '').replace(' ', '').replace('　', '').strip()
    if not sur:
        sur = call
    return sur

# Simulate full matrix
print("Testing all 72x72 = 5184 calling combinations...")
empty_count = 0
results_sample = []

# Parse Tier 2 overrides from text
t2_overrides = {}
for sp in range(1, 73):
    m = re.search(rf'^\t\tCASE {sp}\r?\n\t\t\t;([^\r\n]+)\r?\n\t\t\tSELECTCASE AI([\s\S]*?)^\t\t\tENDSELECT', text, re.MULTILINE)
    if m:
        body = m.group(2)
        matches = re.findall(r'CASE\s+(\d+)\s*\r?\n(?:\t+;[^\r\n]*\r?\n)?\t+RESULTS \'= @"([^"]+)"', body)
        t2_overrides[sp] = {int(ai): res for ai, res in matches}
    else:
        t2_overrides[sp] = {}

# Tier 1 rules map
t1_map = {
    # 苗字+先輩 / 苗字+さん
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

def simulate_call(sp, ai):
    # Tier 1
    t1_func = None
    for group, func in t1_map.items():
        if sp in group:
            t1_func = func
            break
    res = t1_func(sp, ai) if t1_func else chara_dict[ai]['call']
    # Tier 2 override
    if sp in t2_overrides and ai in t2_overrides[sp]:
        res = t2_overrides[sp][ai]
    return res

for sp in range(1, 73):
    for ai in range(1, 73):
        if sp == ai:
            continue
        c = simulate_call(sp, ai)
        if not c or len(c.strip()) == 0:
            print(f"[FAIL] Empty call: {sp} -> {ai}")
            empty_count += 1

if empty_count == 0:
    print(f"[PASS] All 5,112 active pairs generated non-empty, valid callings!")

# Sample checks for 64 to 72
print("\nSample checks for newly updated 3-C characters:")
sample_targets = [
    (64, 6, "あいかくん"),
    (64, 8, "ゆゆくん"),
    (64, 72, "少年"),
    (64, 68, "深鳥くん"),
    (65, 46, "みづきちゃん"),
    (65, 47, "みなづきちゃん"),
    (65, 69, "生き神さま"),
    (65, 4, "早川さん"),
    (66, 62, "クロちゃん"),
    (66, 9, "ルカちゃん"),
    (66, 20, "シズちゃん"),
    (66, 35, "梅ちゃん"),
    (67, 29, "春風団員"),
    (67, 14, "花音団員"),
    (67, 72, "転校生くん"),
    (68, 44, "ひよの"),
    (68, 64, "しおん部長"),
    (68, 40, "はやてちゃん"),
    (68, 61, "生徒会長"),
    (69, 12, "いちか"),
    (69, 61, "ひ～ちゃん"),
    (69, 72, "転校生くん"),
    (70, 28, "星ちゃん"),
    (70, 58, "るり"),
    (70, 72, "転校生くん"),
    (71, 22, "しゃっちん"),
    (71, 59, "金魚ちん"),
    (71, 53, "まり姐さん"),
    (71, 65, "とっき～"),
    (71, 72, "転校生くん"),
    (72, 24, "なつみ"),
    (72, 52, "やこ"),
    (72, 62, "すず"),
    (72, 63, "ちづる"),
]

for sp, ai, expected in sample_targets:
    actual = simulate_call(sp, ai)
    status = "OK" if actual == expected else f"MISMATCH (got {actual})"
    print(f"  {sp:2d} ({chara_dict[sp]['call']}) -> {ai:2d} ({chara_dict[ai]['call']}): {actual} [{status}]")
