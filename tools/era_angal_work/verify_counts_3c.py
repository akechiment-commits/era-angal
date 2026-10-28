import sys, re
sys.stdout.reconfigure(encoding='utf-8')

# Verify specific checks for 64-72
print("=== Verifying 64-72 details ===")

# 64 Shion: check any other special nicknames
with open('tools/output/しおん.txt', 'r', encoding='utf-8') as f:
    t = f.read()
    # Check if Shion calls anyone something without くん
    chans = re.findall(r'([一-龥ぁ-んァ-ヶa-zA-Zー・]+ちゃん)', t)
    print("Shion ちゃん calls top 10:", [x for x in chans if 'お姉ちゃん' not in x][:10])

# 67 Mashiro: check calls to Nana and Kotori
with open('tools/output/ましろ.txt', 'r', encoding='utf-8') as f:
    t = f.read()
    print("Mashiro 春風団員 count:", len(re.findall(r'春風団員', t)))
    print("Mashiro ななちゃん count:", len(re.findall(r'ななちゃん', t)))
    print("Mashiro 花音団員 count:", len(re.findall(r'花音団員', t)))
    print("Mashiro ことりちゃん count:", len(re.findall(r'ことりちゃん', t)))

# 68 Fumi: check calls to Shion and Hiyono
with open('tools/output/ふみ.txt', 'r', encoding='utf-8') as f:
    t = f.read()
    print("Fumi しおん部長 count:", len(re.findall(r'しおん部長', t)))
    print("Fumi しおんさん count:", len(re.findall(r'しおんさん', t)))
    print("Fumi ひよの count:", len(re.findall(r'ひよの', t)))

# 69 Hajime: check calls to Himari
with open('tools/output/はじめ.txt', 'r', encoding='utf-8') as f:
    t = f.read()
    print("Hajime ひ～ちゃん count:", len(re.findall(r'ひ～ちゃん', t)))
    print("Hajime ひ〜ちゃん count:", len(re.findall(r'ひ〜ちゃん', t)))
    print("Hajime いちか count:", len(re.findall(r'いちか', t)))

# 71 Hibiki: check calls to Ikari, Ushio, etc.
with open('tools/output/ひびき.txt', 'r', encoding='utf-8') as f:
    t = f.read()
    print("Hibiki しゃっちん count:", len(re.findall(r'しゃっちん', t)))
    print("Hibiki 金魚ちん count:", len(re.findall(r'金魚ちん', t)))
    print("Hibiki まり姐さん count:", len(re.findall(r'まり姐さん', t)))
    print("Hibiki とっき～ count:", len(re.findall(r'とっき[～〜]', t)))
