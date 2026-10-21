# -*- coding: utf-8 -*-
import os, re, shutil

with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
    text = f.read()

# Normalize newlines to \n during processing
text = text.replace('\r\n', '\n')

def modify_speaker_block(sp_id, modifier_func):
    global text
    # Find the specific speaker block
    m = re.search(rf'(\t\tCASE {sp_id}\s*\n\t\t\t;[^\n]*\n\t\t\tSELECTCASE AI\n)(.*?)(\t\t\tENDSELECT)', text, re.DOTALL)
    if not m:
        raise ValueError(f"Could not find speaker block for CASE {sp_id}")
    
    header = m.group(1)
    body = m.group(2)
    footer = m.group(3)
    
    new_body = modifier_func(body)
    
    old_full = m.group(0)
    new_full = header + new_body + footer
    text = text.replace(old_full, new_full, 1)

def remove_case(body, ai_id):
    # Matches optional whitespace, CASE ai_id, optional comments, RESULTS '= @"...", and trailing whitespace
    p = rf'\s*CASE {ai_id}\s*\n(?:\s*;[^\n]*\n)*\s*RESULTS \'= @"[^"]*"\s*\n?'
    new_b, n = re.subn(p, '\n', body)
    if n != 1:
        raise ValueError(f"Failed to remove CASE {ai_id} (matches={n}):\n{body}")
    return new_b

def update_case(body, ai_id, new_call):
    # Matches CASE ai_id and updates RESULTS '= @"..."
    p = rf'(\s*CASE {ai_id}\s*\n(?:\s*;[^\n]*\n)*\s*RESULTS \'= @")[^"]*(")'
    new_b, n = re.subn(p, rf'\g<1>{new_call}\g<2>', body)
    if n != 1:
        raise ValueError(f"Failed to update CASE {ai_id} to {new_call} (matches={n}):\n{body}")
    return new_b

# 1. CHAR_01 (三善かなえ): remove CASE 61
modify_speaker_block(1, lambda b: remove_case(b, 61))

# 2. CHAR_05 (桃智あすか): CASE 0 "せんぱい" -> "先輩"
modify_speaker_block(5, lambda b: update_case(b, 0, "先輩"))

# 3. CHAR_08 (丸子みさき): remove CASE 61
modify_speaker_block(8, lambda b: remove_case(b, 61))

# 4. CHAR_15 (長町やえ): remove CASE 47
modify_speaker_block(15, lambda b: remove_case(b, 47))

# 5. CHAR_24 (三波なつみ): remove CASE 4
modify_speaker_block(24, lambda b: remove_case(b, 4))

# 6. CHAR_27 (夏野ゆり): CASE 72 "アンジー" -> "あんずさん"
modify_speaker_block(27, lambda b: update_case(b, 72, "あんずさん"))

# 7. CHAR_35 (梅園かな): remove CASE 37
modify_speaker_block(35, lambda b: remove_case(b, 37))

# 8. CHAR_40 (夜霧はやて): CASE 44 "ひよの" -> "笹芽さん"
modify_speaker_block(40, lambda b: update_case(b, 44, "笹芽さん"))

# 9. CHAR_44 (笹芽ひよの): CASE 46 "みづき先輩" -> "双葉先輩"
modify_speaker_block(44, lambda b: update_case(b, 46, "双葉先輩"))

# 10. CHAR_45 (円城寺れいか):
def mod_45(b):
    b = update_case(b, 48, "四方")
    b = update_case(b, 67, "日滝さん")
    b = update_case(b, 69, "神樹さん")
    b = update_case(b, 26, "堀田さん")
    b = update_case(b, 28, "星海さん")
    return b
modify_speaker_block(45, mod_45)

# 11. CHAR_46 (双葉みづき):
def mod_46(b):
    b = update_case(b, 61, "鶴海")
    b = remove_case(b, 48)
    b = remove_case(b, 12)
    b = remove_case(b, 44)
    return b
modify_speaker_block(46, mod_46)

# 12. CHAR_47 (双葉みなづき):
def mod_47(b):
    b = update_case(b, 51, "かすみちゃん")
    b = update_case(b, 41, "ともこちゃん")
    b = update_case(b, 56, "八壁さん")
    return b
modify_speaker_block(47, mod_47)

# 13. CHAR_48 (四方みつる):
def mod_48(b):
    b = update_case(b, 31, "まりあちゃん")
    b = update_case(b, 69, "神樹さん")
    return b
modify_speaker_block(48, mod_48)

# 14. CHAR_49 (小松ぼたん):
def mod_49(b):
    b = update_case(b, 67, "日滝さん")
    b = remove_case(b, 72)
    return b
modify_speaker_block(49, mod_49)

# 15. CHAR_50 (山條ぎん):
def mod_50(b):
    b = update_case(b, 52, "湖南ちゃん")
    b = update_case(b, 12, "イチ")
    b = update_case(b, 41, "トモ")
    b = remove_case(b, 69)
    return b
modify_speaker_block(50, mod_50)

# 16. CHAR_52 (湖南やこ):
def mod_52(b):
    b = update_case(b, 0, "あんた")
    b = update_case(b, 12, "神樹さん")
    b = update_case(b, 38, "カロアさん")
    return b
modify_speaker_block(52, mod_52)

# 17. CHAR_53 (花丘まり):
def mod_53(b):
    b = update_case(b, 0, "転校生くん")
    b = update_case(b, 18, "ひめのさん")
    b = update_case(b, 17, "あずささん")
    b = update_case(b, 36, "ちかさん")
    b = update_case(b, 31, "まりあさん")
    # In earlier edits, 34 and 38 may or may not be present; let's check
    for bad in [34, 38, 37, 43, 44, 72]:
        if re.search(rf'\s*CASE {bad}\b', b):
            b = remove_case(b, bad)
    return b
modify_speaker_block(53, mod_53)

# 18. CHAR_54 (久坂あやめ):
def mod_54(b):
    b = update_case(b, 57, "岩戸さん")
    b = update_case(b, 16, "大虎さん")
    b = update_case(b, 69, "神樹さん")
    for bad in [29, 72]:
        if re.search(rf'\s*CASE {bad}\b', b):
            b = remove_case(b, bad)
    return b
modify_speaker_block(54, mod_54)

# 19. CHAR_55 (伊藤さくら):
def mod_55(b):
    b = update_case(b, 61, "鶴海さん")
    b = update_case(b, 69, "神樹さん")
    b = update_case(b, 45, "陛下")
    return b
modify_speaker_block(55, mod_55)

# 20. CHAR_56 (八壁ひかる):
def mod_56(b):
    b = update_case(b, 16, "大虎")
    b = update_case(b, 12, "神樹")
    for bad in [69, 72]:
        if re.search(rf'\s*CASE {bad}\b', b):
            b = remove_case(b, bad)
    return b
modify_speaker_block(56, mod_56)

# 21. CHAR_57 (岩戸サン):
def mod_57(b):
    b = update_case(b, 48, "みぃくん")
    for bad in [42, 12, 69, 72]:
        if re.search(rf'\s*CASE {bad}\b', b):
            b = remove_case(b, bad)
    return b
modify_speaker_block(57, mod_57)

# 22. CHAR_58 (天宮るり):
def mod_58(b):
    for bad in [51, 65, 69, 72]:
        if re.search(rf'\s*CASE {bad}\b', b):
            b = remove_case(b, bad)
    return b
modify_speaker_block(58, mod_58)

# 23. CHAR_59 (水嶌うしお):
def mod_59(b):
    b = update_case(b, 51, "かすみちゃん")
    if re.search(r'\s*CASE 72\b', b):
        b = remove_case(b, 72)
    return b
modify_speaker_block(59, mod_59)

# 24. CHAR_60 (瀬川かえで):
def mod_60(b):
    b = update_case(b, 57, "岩戸さん")
    if re.search(r'\s*CASE 72\b', b):
        b = remove_case(b, 72)
    return b
modify_speaker_block(60, mod_60)

# 25. CHAR_62 (黒森すず):
modify_speaker_block(62, lambda b: remove_case(b, 12))

# 26. CHAR_63 (八雲ちづる):
def mod_63(b):
    b = update_case(b, 62, "黒森ちゃん")
    b = update_case(b, 6, "藍乃さん")
    if re.search(r'\s*CASE 69\b', b):
        b = remove_case(b, 69)
    return b
modify_speaker_block(63, mod_63)

# 27. CHAR_65 (時国そら):
def mod_65(b):
    b = update_case(b, 0, "転校生くん")
    b = update_case(b, 69, "神樹さん")
    return b
modify_speaker_block(65, mod_65)

# Convert to CRLF
text = text.replace('\n', '\r\n')

# Verify syntax balance
num_select = len(re.findall(r'SELECTCASE', text))
num_endselect = len(re.findall(r'ENDSELECT', text))
print(f"Syntax validation: SELECTCASE={num_select}, ENDSELECT={num_endselect}")
assert num_select == num_endselect, "SELECTCASE and ENDSELECT count mismatch!"

# Verify CP932 encoding
encoded = text.encode('cp932')
with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
    f.write(encoded)

print("ERB/AITE_YOBI_相手呼称.ERB updated and verified successfully!")
