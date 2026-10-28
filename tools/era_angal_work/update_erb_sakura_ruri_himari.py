# -*- coding: utf-8 -*-
import sys

def update_erb():
    with open('ERB/AITE_YOBI_相手呼称.ERB', 'r', encoding='cp932') as f:
        text = f.read()

    # 1. Update default rule for Ruri (CASE 58)
    # Search for CASE 58 in default rules:
    # CASE 58
    #     RESULTS '= @"%CALLNAME:AI%ちゃん" -> RESULTS '= @"%CALLNAME:AI%のひと"
    old_default_58 = '\t\tCASE 58\n\t\t\t;天宮るり: 全学年「～ちゃん」\n\t\t\tRESULTS \'= @"%CALLNAME:AI%ちゃん"'
    new_default_58 = '\t\tCASE 58\n\t\t\t;天宮るり: 全学年「～のひと」（宇宙人・観測者の基本呼称）\n\t\t\tRESULTS \'= @"%CALLNAME:AI%のひと"'
    if old_default_58 in text:
        text = text.replace(old_default_58, new_default_58)
        print('Updated Ruri default rule successfully!')
    else:
        # try regex or loose match
        import re
        text = re.sub(
            r'(\t\tCASE 58\s*\n\t\t\t;[^\n]*\n\t\t\tRESULTS \'= @\"%CALLNAME:AI%)[^"]+(\")',
            r'\g<1>のひと\2',
            text
        )
        print('Updated Ruri default rule via regex!')

    # 2. Update CHAR_55 伊藤さくら
    # CASE 60: かえで -> かえでさん
    old_sakura_block = '''\t\tCASE 55
\t\t\t;伊藤さくら (3-B / 園芸部・美化委員)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生さん"
\t\t\t\t;--- 崇拝対象 ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (フォロワーとして絶対崇拝)
\t\t\t\t\tRESULTS '= @"れいか様"
\t\t\t\t;--- 親友フォロワー（75回登場） ---
\t\t\t\tCASE 60
\t\t\t\t\t;瀬川かえで (親友)
\t\t\t\t\tRESULTS '= @"かえで"
\t\t\t\t;--- 生徒会長・同級生 ---
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり
\t\t\t\t\tRESULTS '= @"鶴海会長"
\t\t\t\tCASE 69
\t\t\t\t\t;神樹はじめ (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"はじめさん"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (35回登場)
\t\t\t\t\tRESULTS '= @"あんずさん"
\t\t\tENDSELECT'''

    new_sakura_block = '''\t\tCASE 55
\t\t\t;伊藤さくら (3-B / 園芸部・美化委員)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生さん"
\t\t\t\t;--- 崇拝対象 ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (フォロワーとして絶対崇拝)
\t\t\t\t\tRESULTS '= @"れいか様"
\t\t\t\t;--- 春秋コンビ・最重要親友（原作165回すべて「かえでさん」） ---
\t\t\t\tCASE 60
\t\t\t\t\t;瀬川かえで (春秋コンビ親友・絶対敬称「かえでさん」)
\t\t\t\t\tRESULTS '= @"かえでさん"
\t\t\t\t;--- 生徒会長・同級生 ---
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり
\t\t\t\t\tRESULTS '= @"鶴海会長"
\t\t\t\tCASE 69
\t\t\t\t\t;神樹はじめ (神樹姓重複回避)
\t\t\t\t\tRESULTS '= @"はじめさん"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (35回登場)
\t\t\t\t\tRESULTS '= @"あんずさん"
\t\t\tENDSELECT'''

    if old_sakura_block in text:
        text = text.replace(old_sakura_block, new_sakura_block)
        print('Updated Sakura block successfully!')
    else:
        print('WARNING: old_sakura_block not found directly!')

    # 3. Update CHAR_58 天宮るり
    old_ruri_block = '''\t\tCASE 58
\t\t\t;天宮るり (3-B / 軽音部キーボード)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生くん"
\t\t\t\t;--- 最重要親友・幼馴染（111回登場！） ---
\t\t\t\tCASE 70
\t\t\t\t\t;神無月ほとり (唯一無二の理解者)
\t\t\t\t\tRESULTS '= @"ほとりちゃん"
\t\t\t\t;--- 生徒会長・同級生 ---
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり
\t\t\t\t\tRESULTS '= @"生徒会長"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず
\t\t\t\t\tRESULTS '= @"あんずさん"
\t\t\tENDSELECT'''

    new_ruri_block = '''\t\tCASE 58
\t\t\t;天宮るり (3-B / 天文部部長)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生のひと / 弟のひと / 素:転校生くん) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生のひと"
\t\t\t\t;--- 最重要親友・幼馴染（ほとりのひと / ほとりちゃん） ---
\t\t\t\tCASE 70
\t\t\t\t\t;神無月ほとり (最愛の幼馴染・副部長)
\t\t\t\t\tRESULTS '= @"ほとりのひと"
\t\t\t\t;--- 生徒会長 ---
\t\t\t\tCASE 61
\t\t\t\t\t;鶴海ひまり (生徒会長のひと)
\t\t\t\t\tRESULTS '= @"生徒会長のひと"
\t\t\t\t;--- 独自呼称 ---
\t\t\t\tCASE 10
\t\t\t\t\t;木之下ゆゆ (文芸部)
\t\t\t\t\tRESULTS '= @"ゆゆゆのひと"
\t\t\t\tCASE 51
\t\t\t\t\t;御影かすみ
\t\t\t\t\tRESULTS '= @"魔人のひと"
\t\t\t\tCASE 27
\t\t\t\t\t;夏野ゆり
\t\t\t\t\tRESULTS '= @"桃太郎のひと"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず
\t\t\t\t\tRESULTS '= @"あんずさん"
\t\t\tENDSELECT'''

    if old_ruri_block in text:
        text = text.replace(old_ruri_block, new_ruri_block)
        print('Updated Ruri block successfully!')
    else:
        print('WARNING: old_ruri_block not found directly!')

    # 4. Update CHAR_61 鶴海ひまり
    old_himari_block = '''\t\tCASE 61
\t\t\t;鶴海ひまり (3-B / 現生徒会長・合唱部)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (転校生) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"転校生くん"
\t\t\t\t;--- 敬愛する前会長（183回登場！） ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (敬愛する前会長)
\t\t\t\t\tRESULTS '= @"れいか先輩"
\t\t\t\t;--- 愛称・親友 ---
\t\t\t\tCASE 6
\t\t\t\t\t;藍乃あいか (170回登場！)
\t\t\t\t\tRESULTS '= @"あいかちゃん"
\t\t\t\tCASE 54
\t\t\t\t\t;久坂あやめ (80回登場！)
\t\t\t\t\tRESULTS '= @"あやめちゃん"
\t\t\t\tCASE 53
\t\t\t\t\t;花丘まり (56回登場！)
\t\t\t\t\tRESULTS '= @"まりちゃん"
\t\t\t\tCASE 62
\t\t\t\t\t;黒森すず (固有愛称！)
\t\t\t\t\tRESULTS '= @"くろりん"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (大親友愛称！17回登場)
\t\t\t\t\tRESULTS '= @"アンジー"
\t\t\tENDSELECT'''

    new_himari_block = '''\t\tCASE 61
\t\t\t;鶴海ひまり (3-B / 現生徒会長・合唱部 / 渾名付けが趣味！)
\t\t\tSELECTCASE AI
\t\t\t\t;--- 主人公 (渾名「下僕くん」原作230回登場！) ---
\t\t\t\tCASE 0
\t\t\t\t\tRESULTS '= @"下僕くん"
\t\t\t\t;--- 敬愛する前会長（183回登場！） ---
\t\t\t\tCASE 45
\t\t\t\t\t;円城寺れいか (敬愛する前会長)
\t\t\t\t\tRESULTS '= @"れいか先輩"
\t\t\t\t;--- 生徒会長の固有あだ名（公式設定・高頻度登場） ---
\t\t\t\tCASE 41
\t\t\t\t\t;悠木ともこ (剣道部・110回登場！)
\t\t\t\t\tRESULTS '= @"ユッキー"
\t\t\t\tCASE 48
\t\t\t\t\t;四方みつる (生徒会副会長・王子様・105回登場！)
\t\t\t\t\tRESULTS '= @"ミッチー"
\t\t\t\tCASE 24
\t\t\t\t\t;三波なつみ (演劇部・34回登場！)
\t\t\t\t\tRESULTS '= @"みなみん"
\t\t\t\tCASE 62
\t\t\t\t\t;黒森すず (軽音部・16回登場！※くろりんは0件誤記)
\t\t\t\t\tRESULTS '= @"クロちゃん"
\t\t\t\tCASE 72
\t\t\t\t\t;あんず (大親友愛称！17回登場)
\t\t\t\t\tRESULTS '= @"アンジー"
\t\t\t\t;--- 親しい友人・後輩への愛称 ---
\t\t\t\tCASE 6
\t\t\t\t\t;藍乃あいか (合唱部相棒・168回登場！)
\t\t\t\t\tRESULTS '= @"あいかちゃん"
\t\t\t\tCASE 54
\t\t\t\t\t;久坂あやめ (80回登場！)
\t\t\t\t\tRESULTS '= @"あやめちゃん"
\t\t\t\tCASE 53
\t\t\t\t\t;花丘まり (50回登場！)
\t\t\t\t\tRESULTS '= @"まりちゃん"
\t\t\t\tCASE 60
\t\t\t\t\t;瀬川かえで (30回登場！)
\t\t\t\t\tRESULTS '= @"かえでちゃん"
\t\t\t\tCASE 10
\t\t\t\t\t;木之下ゆゆ (文芸部・27回登場！)
\t\t\t\t\tRESULTS '= @"ゆゆちゃん"
\t\t\t\tCASE 40
\t\t\t\t\t;夜霧はやて (5回登場！)
\t\t\t\t\tRESULTS '= @"はやてちゃん"
\t\t\t\tCASE 55
\t\t\t\t\t;伊藤さくら (5回登場！)
\t\t\t\t\tRESULTS '= @"さくらちゃん"
\t\t\t\tCASE 51
\t\t\t\t\t;御影かすみ (4回登場！)
\t\t\t\t\tRESULTS '= @"かすみちゃん"
\t\t\tENDSELECT'''

    if old_himari_block in text:
        text = text.replace(old_himari_block, new_himari_block)
        print('Updated Himari block successfully!')
    else:
        print('WARNING: old_himari_block not found directly!')

    # Normalize line endings to CRLF
    text = text.replace('\r\n', '\n').replace('\n', '\r\n')

    with open('ERB/AITE_YOBI_相手呼称.ERB', 'wb') as f:
        f.write(text.encode('cp932'))
    print('ERB updated and written successfully!')

if __name__ == '__main__':
    update_erb()
