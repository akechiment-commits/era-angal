from pathlib import Path
import re
import hashlib


TARGET = Path(r"C:\Users\guile\era-angal\ERB\CHAR\CHAR_46_双葉みづき_COM.ERB")
text = TARGET.read_bytes().decode("cp932").replace("\r\n", "\n")
lines = text.replace("\r\n", "\n").splitlines()

stack = []
for line_no, line in enumerate(lines, 1):
    stripped = line.strip()
    if not stripped or stripped.startswith(";"):
        continue
    if re.match(r"^IF(?:\s|$)", stripped):
        stack.append((line_no, stripped))
    elif stripped.startswith("ENDIF"):
        if not stack:
            raise SystemExit(f"ENDIF without IF at {line_no}")
        stack.pop()
if stack:
    raise SystemExit(f"IF without ENDIF: {stack[-10:]}")

markers = list(re.finditer(r"(?m)^;--- COM(\d+)", text))
blocks = {}
for idx, marker in enumerate(markers):
    number = int(marker.group(1))
    end = markers[idx + 1].start() if idx + 1 < len(markers) else len(text)
    blocks[number] = text[marker.start():end]

expected = [4, 7, 8, 9, 10, 18, 19, 26, 27, 28, 29, 35, 37, 38, 39, 42, 43, 45, 46, 53, 54, 56, 57, 58, 59, 61, 63, 65, 66, 67, 68, 69, 71, 75, 80, 85, 90, 110, 130, 131, 132, 181, 182, 183, 184, 185, 186, 187, 196, 197, 198, 199, 200, 201, 203, 204, 205, 160, 189, 188, 255, 256, 257, 390, 11, 13, 14, 15, 16]
for number in expected:
    block = blocks[number]
    if block.count("A = RAND:3") < 1:
        raise SystemExit(f"COM{number} has no RAND:3")
    if number not in {11, 13, 14, 15, 16}:
        else_count = len(re.findall(r"(?m)^\t\tELSE$", block))
        if block.count("IF A == 0") < 2 or block.count("ELSEIF A == 1") < 2 or else_count < 2:
            raise SystemExit(f"COM{number} is not 3-way branched: IF0={block.count('IF A == 0')}, IF1={block.count('ELSEIF A == 1')}, ELSE2={else_count}")
    quoted = re.findall(r"PRINTFORMW? (「.*?」)", block)
    if len(quoted) < 6 and number not in {11, 13, 14, 15, 16}:
        raise SystemExit(f"COM{number} has too few dialogue variants: {len(quoted)}")

for prefix in ("COM280-284", "COM410-414"):
    start = text.index(f";--- {prefix}")
    end = text.find(";--- COM", start + 5)
    block = text[start:] if end < 0 else text[start:end]
    if block.count("A = RAND:3") != 5:
        raise SystemExit(f"{prefix} RAND count={block.count('A = RAND:3')}")

if "転校生" not in blocks[56] or "%CALLNAME:ASSI%" not in blocks[56]:
    raise SystemExit("COM56 viewpoint markers missing")
for number in (66, 68):
    if "%CALLNAME:ASSI%" not in blocks[number]:
        raise SystemExit(f"COM{number} assistant reference missing")
if "足で、わたしのを" not in blocks[67] and "足でわたしのを" not in blocks[67]:
    raise SystemExit("COM67 does not show character as receiver")

# COM130-132 are passive menu labels, but the engine stores the equipment on
# PLAYER and calls the target character's reaction.  Keep the speaker as the
# actor applying it to the player; reject the common reverse-viewpoint slips.
viewpoint_contract = {
    130: {
        "marker": "視点: 転校生が目隠しされる側。みづきが装着する",
        "forbidden": ["わたしが目隠しされ", "わたしを目隠しされ", "わたしが見えない", "わたしの目が見えない"],
    },
    131: {
        "marker": "視点: 転校生が拘束される側。みづきが縛る",
        "forbidden": ["わたしが縛られ", "わたしを縛られ", "わたしが拘束され", "わたしは動けない"],
    },
    132: {
        "marker": "視点: 転校生が口枷される側。みづきが装着する",
        "forbidden": ["わたしが口枷", "わたしに口枷", "わたしが口を塞がれ", "わたしがしゃべれない", "わたしが喋れない", "むぐっ", "むぐ……"],
    },
}
for number, contract in viewpoint_contract.items():
    block = blocks[number]
    if contract["marker"] not in block:
        raise SystemExit(f"COM{number} viewpoint marker is missing or ambiguous")
    for forbidden in contract["forbidden"]:
        if forbidden in block:
            raise SystemExit(f"COM{number} reverse viewpoint marker found: {forbidden}")

for number, block in blocks.items():
    variants = re.findall(r"PRINTFORMW? (「.*?」)", block)
    duplicates = [item for item in set(variants) if variants.count(item) > 1]
    if duplicates:
        raise SystemExit(f"COM{number} duplicate dialogue: {duplicates[:2]}")

print("balanced; custom RAND=5+5; selected commands have distinct variants")
print("sha256", hashlib.sha256(TARGET.read_bytes()).hexdigest())
