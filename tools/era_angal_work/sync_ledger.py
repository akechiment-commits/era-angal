# -*- coding: utf-8 -*-
import re

with open('tools/キャラ資料/呼称定義台帳_20261014.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. CHAR_01: 鶴海会長削除
text = re.sub(r'\|\s*61\s*\|\s*鶴海ひまり\s*\|\s*鶴海会長\s*\|[^\n]*\n', '', text)

# 2. CHAR_05: せんぱい -> 先輩
text = re.sub(r'(\|\s*0\s*\|\s*あなた\s*\|\s*)せんぱい(\s*\|)', r'\g<1>先輩\g<2>', text)

# 3. CHAR_08: 鶴海会長削除
text = re.sub(r'(\|\s*CHAR_08.*?)(\|\s*61\s*\|\s*鶴海ひまり\s*\|\s*鶴海会長\s*\|[^\n]*\n)', r'\1', text, flags=re.DOTALL)

# 4. CHAR_15: みなづき先輩削除
text = re.sub(r'\|\s*47\s*\|\s*双葉みなづき\s*\|\s*みなづき先輩\s*\|[^\n]*\n', '', text)

# 5. CHAR_24: きこちゃん削除
text = re.sub(r'(\|\s*CHAR_24.*?)(\|\s*4\s*\|\s*早川きこ\s*\|\s*きこちゃん\s*\|[^\n]*\n)', r'\1', text, flags=re.DOTALL)

# 6. CHAR_27: 夏野ゆり -> あんず: アンジー -> あんずさん
text = re.sub(r'(\|\s*72\s*\|\s*あんず\s*\|\s*)アンジー(\s*\|)', r'\g<1>あんずさん\g<2>', text)

# 7. CHAR_35: 龍泉寺削除
text = re.sub(r'\|\s*37\s*\|\s*龍泉寺レンレン\s*\|\s*龍泉寺\s*\|[^\n]*\n', '', text)

# 8. CHAR_40: ひよの -> 笹芽さん
text = re.sub(r'(\|\s*44\s*\|\s*笹芽ひよの\s*\|\s*)ひよの(\s*\|)', r'\g<1>笹芽さん\g<2>', text)

# 9. CHAR_44: みづき先輩 -> 双葉先輩
text = re.sub(r'(\|\s*46\s*\|\s*双葉みづき\s*\|\s*)みづき先輩(\s*\|)', r'\g<1>双葉先輩\g<2>', text)

# 10. CHAR_45:
# 48 四方, 67 日滝さん, 69 神樹さん, 26 堀田さん, 28 星海さん
text = re.sub(r'(\|\s*48\s*\|\s*四方みつる\s*\|\s*)みつる(\s*\|)', r'\g<1>四方\g<2>', text)
text = re.sub(r'(\|\s*67\s*\|\s*日滝ましろ\s*\|\s*)ましろさん(\s*\|)', r'\g<1>日滝さん\g<2>', text)
text = re.sub(r'(\|\s*69\s*\|\s*神樹はじめ\s*\|\s*)はじめさん(\s*\|)', r'\g<1>神樹さん\g<2>', text)
text = re.sub(r'(\|\s*26\s*\|\s*堀田さあや\s*\|\s*)さあや(\s*\|)', r'\g<1>堀田さん\g<2>', text)
text = re.sub(r'(\|\s*28\s*\|\s*星海こよい\s*\|\s*)こよい(\s*\|)', r'\g<1>星海さん\g<2>', text)

# 11. CHAR_46:
text = re.sub(r'(\|\s*61\s*\|\s*鶴海ひまり\s*\|\s*)ひまり(\s*\|)', r'\g<1>鶴海\g<2>', text)
for bad in [48, 12, 44]:
    text = re.sub(rf'\|\s*{bad}\s*\|[^\n]+\|[^\n]+\|[^\n]*\n', '', text)

# 12. CHAR_47:
text = re.sub(r'(\|\s*51\s*\|\s*御影かすみ\s*\|\s*)かすみん(\s*\|)', r'\g<1>かすみちゃん\g<2>', text)
text = re.sub(r'(\|\s*41\s*\|\s*悠木ともこ\s*\|\s*)ともちゃん(\s*\|)', r'\g<1>ともこちゃん\g<2>', text)
text = re.sub(r'(\|\s*56\s*\|\s*八壁ひかる\s*\|\s*)八壁ちゃん(\s*\|)', r'\g<1>八壁さん\g<2>', text)

# 13. CHAR_48:
text = re.sub(r'(\|\s*31\s*\|\s*夢路まりあ\s*\|\s*)まりあさん(\s*\|)', r'\g<1>まりあちゃん\g<2>', text)
text = re.sub(r'(\|\s*69\s*\|\s*神樹はじめ\s*\|\s*)はじめさん(\s*\|)', r'\g<1>神樹さん\g<2>', text)

# 14. CHAR_49:
text = re.sub(r'(\|\s*67\s*\|\s*日滝ましろ\s*\|\s*)ましろさん(\s*\|)', r'\g<1>日滝さん\g<2>', text)

# 15. CHAR_50:
text = re.sub(r'(\|\s*52\s*\|\s*湖南やこ\s*\|\s*)湖南さん(\s*\|)', r'\g<1>湖南ちゃん\g<2>', text)
text = re.sub(r'(\|\s*12\s*\|\s*神樹いちか\s*\|\s*)いちか(\s*\|)', r'\g<1>イチ\g<2>', text)
text = re.sub(r'(\|\s*41\s*\|\s*悠木ともこ\s*\|\s*)ともこ(\s*\|)', r'\g<1>トモ\g<2>', text)

# 16. CHAR_52:
text = re.sub(r'(\|\s*0\s*\|\s*あなた\s*\|\s*)アンタ(\s*\|)', r'\g<1>あんた\g<2>', text)
text = re.sub(r'(\|\s*12\s*\|\s*神樹いちか\s*\|\s*)いちか(\s*\|)', r'\g<1>神樹さん\g<2>', text)
text = re.sub(r'(\|\s*38\s*\|\s*クー・カロア\s*\|\s*)カロア(\s*\|)', r'\g<1>カロアさん\g<2>', text)

# 17. CHAR_53:
text = re.sub(r'(\|\s*0\s*\|\s*あなた\s*\|\s*)転校生さん(\s*\|)', r'\g<1>転校生くん\g<2>', text)
text = re.sub(r'(\|\s*18\s*\|\s*熊沢ひめの\s*\|\s*)ひめのちゃん(\s*\|)', r'\g<1>ひめのさん\g<2>', text)
text = re.sub(r'(\|\s*17\s*\|\s*小鳩あずさ\s*\|\s*)あずさちゃん(\s*\|)', r'\g<1>あずささん\g<2>', text)
text = re.sub(r'(\|\s*36\s*\|\s*遠見ちか\s*\|\s*)ちかちゃん(\s*\|)', r'\g<1>ちかさん\g<2>', text)
text = re.sub(r'(\|\s*31\s*\|\s*夢路まりあ\s*\|\s*)まりあ様(\s*\|)', r'\g<1>まりあさん\g<2>', text)

# 18. CHAR_54:
text = re.sub(r'(\|\s*57\s*\|\s*岩戸サン\s*\|\s*)サンちゃん(\s*\|)', r'\g<1>岩戸さん\g<2>', text)
text = re.sub(r'(\|\s*16\s*\|\s*大虎いさみ\s*\|\s*)いさみちゃん(\s*\|)', r'\g<1>大虎さん\g<2>', text)
text = re.sub(r'(\|\s*69\s*\|\s*神樹はじめ\s*\|\s*)はじめさん(\s*\|)', r'\g<1>神樹さん\g<2>', text)

# 19. CHAR_55:
text = re.sub(r'(\|\s*61\s*\|\s*鶴海ひまり\s*\|\s*)鶴海会長(\s*\|)', r'\g<1>鶴海さん\g<2>', text)
text = re.sub(r'(\|\s*69\s*\|\s*神樹はじめ\s*\|\s*)はじめさん(\s*\|)', r'\g<1>神樹さん\g<2>', text)
text = re.sub(r'(\|\s*45\s*\|\s*円城寺れいか\s*\|\s*)れいか様(\s*\|)', r'\g<1>陛下\g<2>', text)

# 20. CHAR_56:
text = re.sub(r'(\|\s*16\s*\|\s*大虎いさみ\s*\|\s*)いさみ(\s*\|)', r'\g<1>大虎\g<2>', text)
text = re.sub(r'(\|\s*12\s*\|\s*神樹いちか\s*\|\s*)いちか(\s*\|)', r'\g<1>神樹\g<2>', text)

# 21. CHAR_57:
text = re.sub(r'(\|\s*48\s*\|\s*四方みつる\s*\|\s*)みつる(\s*\|)', r'\g<1>みぃくん\g<2>', text)

# 22. CHAR_58:
# 魔人のひと, ゆんゆんのひと, 生き神のひと 削除
text = re.sub(r'\|\s*51\s*\|\s*御影かすみ\s*\|\s*魔人のひと\s*\|[^\n]*\n', '', text)
text = re.sub(r'\|\s*65\s*\|\s*時国そら\s*\|\s*ゆんゆんのひと\s*\|[^\n]*\n', '', text)
text = re.sub(r'\|\s*69\s*\|\s*神樹はじめ\s*\|\s*生き神のひと\s*\|[^\n]*\n', '', text)

# 23. CHAR_59:
text = re.sub(r'(\|\s*51\s*\|\s*御影かすみ\s*\|\s*)かすみん(\s*\|)', r'\g<1>かすみちゃん\g<2>', text)

# 24. CHAR_60:
text = re.sub(r'(\|\s*57\s*\|\s*岩戸サン\s*\|\s*)サン(\s*\|)', r'\g<1>岩戸さん\g<2>', text)

# 26. CHAR_63:
text = re.sub(r'(\|\s*62\s*\|\s*黒森すず\s*\|\s*)すず(\s*\|)', r'\g<1>黒森ちゃん\g<2>', text)
text = re.sub(r'(\|\s*6\s*\|\s*藍乃あいか\s*\|\s*)アイカ(\s*\|)', r'\g<1>藍乃さん\g<2>', text)

# 27. CHAR_65:
text = re.sub(r'(\|\s*0\s*\|\s*あなた\s*\|\s*)転校生さん(\s*\|)', r'\g<1>転校生くん\g<2>', text)
text = re.sub(r'(\|\s*69\s*\|\s*神樹はじめ\s*\|\s*)生き神さま(\s*\|)', r'\g<1>神樹さん\g<2>', text)

with open('tools/キャラ資料/呼称定義台帳_20261014.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated tools/キャラ資料/呼称定義台帳_20261014.md successfully!")
