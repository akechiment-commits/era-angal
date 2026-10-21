import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
    text = f.read()

# Check how many SP cases exist
sp_cases = re.findall(r'^\t\tCASE (\d+)\r?\n\t\t\t;([^\r\n]+)\r?\n\t\t\tSELECTCASE AI', text, re.MULTILINE)
print(f"Total SP cases with SELECTCASE AI: {len(sp_cases)}")

# Let's inspect the first 3 and last 3
for sp, comment in sp_cases[:3]:
    print(f"SP {sp}: {comment}")
for sp, comment in sp_cases[-3:]:
    print(f"SP {sp}: {comment}")
