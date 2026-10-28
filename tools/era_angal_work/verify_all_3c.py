import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Comprehensive Verification for AITE_YOBI_相手呼称.ERB ===")

# 1. Read binary
with open('ERB/AITE_YOBI_相手呼称.ERB', 'rb') as f:
    raw = f.read()

# 2. Check encoding
try:
    text = raw.decode('cp932')
    print("[PASS] cp932 decode successful.")
except Exception as e:
    print(f"[FAIL] cp932 decode error: {e}")
    sys.exit(1)

# 3. Check line endings
if b'\r\r\n' in raw:
    print("[FAIL] Corrupted CRLF (\\r\\r\\n) found!")
    sys.exit(1)
if b'\n' in raw.replace(b'\r\n', b''):
    print("[FAIL] Bare LF found!")
    sys.exit(1)
print(f"[PASS] CRLF integrity verified. Total lines: {len(text.splitlines())}")

# 4. Check SELECTCASE / ENDSELECT nesting
select_cnt = len(re.findall(r'^\s*SELECTCASE\b', text, re.MULTILINE))
endselect_cnt = len(re.findall(r'^\s*ENDSELECT\b', text, re.MULTILINE))
print(f"SELECTCASE count: {select_cnt}, ENDSELECT count: {endselect_cnt}")
if select_cnt != endselect_cnt:
    print(f"[FAIL] Mismatched SELECTCASE ({select_cnt}) and ENDSELECT ({endselect_cnt})!")
    sys.exit(1)
print("[PASS] SELECTCASE / ENDSELECT count matches perfectly.")

# 5. Check Tier 1 coverage for all 72 characters
lines = text.splitlines()
t1_cases = []
in_t1 = False
for l in lines:
    if 'SELECTCASE SP' in l and not in_t1:
        in_t1 = True
        continue
    elif ';--- (2) 個別の特別呼称' in l:
        in_t1 = False
        break
    if in_t1 and l.strip().startswith('CASE '):
        # parse case numbers
        m = re.findall(r'\d+', l)
        t1_cases.extend([int(x) for x in m])

missing_t1 = [i for i in range(1, 73) if i not in t1_cases]
print(f"Tier 1 registered characters: {len(set(t1_cases))}/72")
if missing_t1:
    print(f"[FAIL] Missing in Tier 1: {missing_t1}")
    sys.exit(1)
print("[PASS] Tier 1 has 100% coverage (all 72 characters).")

# 6. Check Tier 2 SP cases for all 72 characters
t2_cases = []
in_t2 = False
for l in lines:
    if ';--- (2) 個別の特別呼称' in l:
        in_t2 = True
    elif '@GET_CHARA_GRADE' in l:
        in_t2 = False
        break
    if in_t2 and re.match(r'^\t\tCASE \d+', l):
        m = re.findall(r'\d+', l)
        t2_cases.extend([int(x) for x in m])

missing_t2 = [i for i in range(1, 73) if i not in t2_cases]
print(f"Tier 2 SP cases count: {len(t2_cases)}/72")
if missing_t2:
    print(f"[FAIL] Missing in Tier 2: {missing_t2}")
    sys.exit(1)
print("[PASS] Tier 2 has all 72 characters defined as speakers (SP)!")

# 7. Print summary for 64 to 72
print("\n--- Summary of Tier 2 special overrides for 64 to 72 ---")
for sp in range(64, 73):
    m = re.search(rf'^\t\tCASE {sp}\r?\n\t\t\t;([^\r\n]+)\r?\n\t\t\tSELECTCASE AI([\s\S]*?)^\t\t\tENDSELECT', text, re.MULTILINE)
    if m:
        name_comment = m.group(1).strip()
        body = m.group(2)
        # extract each AI case and result
        ai_matches = re.findall(r'CASE\s+(\d+)\s*\r?\n(?:\t+;[^\r\n]*\r?\n)?\t+RESULTS \'= @"([^"]+)"', body)
        ai_str = ", ".join([f"{ai}->{res}" for ai, res in ai_matches])
        print(f"SP {sp} ({name_comment}): {len(ai_matches)} overrides [{ai_str}]")
    else:
        print(f"SP {sp}: NOT FOUND OR PARSE ERROR!")

print("\n[ALL PASS] Verification completely successful!")
