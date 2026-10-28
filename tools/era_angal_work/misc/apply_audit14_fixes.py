import pathlib

ROOT = pathlib.Path('.')

def patch_file(rel_path, old_text, new_text):
    path = pathlib.Path(rel_path)
    data = path.read_bytes().decode('cp932')
    data = data.replace('\r\n', '\n')
    old_norm = old_text.replace('\r\n', '\n')
    new_norm = new_text.replace('\r\n', '\n')
    if old_norm not in data:
        if new_norm in data:
            print(f"Already patched: {rel_path}")
            return
        raise ValueError(f"Target text not found in {rel_path}:\n{repr(old_norm[:60])}")
    count = data.count(old_norm)
    if count > 1:
        raise ValueError(f"Target text appears multiple ({count}) times in {rel_path}")
    data = data.replace(old_norm, new_norm)
    # Ensure CRLF
    data = data.replace('\n', '\r\n')
    path.write_bytes(data.encode('cp932'))
    print(f"Patched: {rel_path}")

# 1. COMF33
patch_file(
    'ERB/COMF/COMF33.ERB',
    '\t;媚薬\n\tIF TEQUIP:21\t; 【[媚薬効果発揮中]使用中】\n\t\tSIF S\n\t\t\tPRINT  + \n\t\tPRINTS ITEMNAME:21\n\t\tPRINTV \'(,6,\')\n\t\tS = 1\n\tENDIF',
    '\t;媚薬\n\tIF TEQUIP:21\t; 【[媚薬効果発揮中]使用中】\n\t\tSIF S\n\t\t\tPRINT  + \n\t\tPRINTS ITEMNAME:26\n\t\tPRINTV \'(,6,\')\n\t\tS = 1\n\tENDIF'
)

# 2. COMF38
patch_file(
    'ERB/COMF/COMF38.ERB',
    '\t;媚薬\n\tIF TEQUIP:21\t; 【[媚薬効果発揮中]使用中】\n\t\tSIF S\n\t\t\tPRINT  + \n\t\tPRINTS ITEMNAME:21\n\t\tPRINTV \'(,6,\')\n\t\tS = 1\n\tENDIF',
    '\t;媚薬\n\tIF TEQUIP:21\t; 【[媚薬効果発揮中]使用中】\n\t\tSIF S\n\t\t\tPRINT  + \n\t\tPRINTS ITEMNAME:26\n\t\tPRINTV \'(,6,\')\n\t\tS = 1\n\tENDIF'
)

# 3. COMF62
patch_file(
    'ERB/COMF/COMF62.ERB',
    '\t;媚薬\n\tIF TEQUIP:21\t; 【[媚薬効果発揮中]使用中】\n\t\tSIF S\n\t\t\tPRINT  + \n\t\tPRINTS ITEMNAME:21\n\t\tPRINTV \'(,6,\')\n\t\tS = 1\n\tENDIF',
    '\t;媚薬\n\tIF TEQUIP:21\t; 【[媚薬効果発揮中]使用中】\n\t\tSIF S\n\t\t\tPRINT  + \n\t\tPRINTS ITEMNAME:26\n\t\tPRINTV \'(,6,\')\n\t\tS = 1\n\tENDIF'
)

# 4. COMF63
patch_file(
    'ERB/COMF/COMF63.ERB',
    '\t;媚薬\n\tIF TEQUIP:21\t; 【[媚薬効果発揮中]使用中】\n\t\tSIF S\n\t\t\tPRINT  + \n\t\tPRINTS ITEMNAME:21\n\t\tPRINTV \'(,6,\')\n\t\tS = 1\n\tENDIF',
    '\t;媚薬\n\tIF TEQUIP:21\t; 【[媚薬効果発揮中]使用中】\n\t\tSIF S\n\t\t\tPRINT  + \n\t\tPRINTS ITEMNAME:26\n\t\tPRINTV \'(,6,\')\n\t\tS = 1\n\tENDIF'
)

# 5. DAILY_LIFE
daily_path = list(ROOT.glob('ERB/*DAILY_LIFE*.ERB'))[0]
patch_file(
    daily_path,
    '\t\t\t\tPRINTFORMW %CALLNAME:MASTER%と%CALLNAME:TOINT(LOCALS)%の分も一緒に洗濯しているようだ',
    '\t\t\t\tPRINTFORMW %CALLNAME:MASTER%と%CALLNAME:(TOINT(LOCALS))%の分も一緒に洗濯しているようだ'
)
patch_file(
    daily_path,
    '\t\t\tPRINTFORMW %CALLNAME:TOINT(LOCALS:0)%と%CALLNAME:TOINT(LOCALS:1)%もきているようだ',
    '\t\t\tPRINTFORMW %CALLNAME:(TOINT(LOCALS:0))%と%CALLNAME:(TOINT(LOCALS:1))%もきているようだ'
)
patch_file(
    daily_path,
    '\t\t\tPRINTFORMW %CALLNAME:TOINT(LOCALS)%もきているようだ',
    '\t\t\tPRINTFORMW %CALLNAME:(TOINT(LOCALS))%もきているようだ'
)

# 6. YU-SYS
yusys_path = list(ROOT.glob('ERB/*YU-SYS*.ERB'))[0]
patch_file(
    yusys_path,
    ';キャラ別\nCALLFORM KOJO_NEXT_PLAY_{NO:TARGET}',
    ';キャラ別\nTRYCALLFORM KOJO_NEXT_PLAY_{NO:TARGET}'
)

# 7. PASSIVE_パートナーターン.ERB
patch_file(
    'ERB/PASSIVE_パートナーターン.ERB',
    '@TRAIN_MESSAGE_PASSIVEMODE_PASSIVEPHASE(ARG:0, ARG:1)\nCALLFORM PASSIVE_MESSAGE_{ARG:1}\nWAIT',
    '@TRAIN_MESSAGE_PASSIVEMODE_PASSIVEPHASE(ARG:0, ARG:1)\nTRYCALLFORM PASSIVE_MESSAGE_{ARG:1}\nWAIT'
)

# 8. COMMON
common_path = list(ROOT.glob('ERB/*COMMON*.ERB'))[0]
patch_file(
    common_path,
    ';従者判定\nCALL ATTENDANT',
    ';従者判定\n;CALL ATTENDANT ; 廃止済み（旧東方従者処理）'
)

# 9. CSV/Talent.csv
patch_file(
    'CSV/Talent.csv',
    ';着痩せ以外は詰め合わせから移植\n;実装するかは未定\n;140,絶壁,',
    ';着痩せ以外は詰め合わせから移植\n;実装するかは未定（※140(絶壁), 181(烙印), 182(隷属) 等はあんガル仕様移行に伴い廃止済み）\n;140,絶壁,'
)

# 10. CSV/Mark.csv
patch_file(
    'CSV/Mark.csv',
    ';4,反発感情取得履歴\n;89,妊娠で胸が膨らんだ\n;90,臨月or育児中',
    ';4,反発感情取得履歴 ; 廃止済み\n;89,妊娠で胸が膨らんだ ; 廃止済み\n;90,臨月or育児中 ; 廃止済み'
)

# 11. CSV/Item.csv
patch_file(
    'CSV/Item.csv',
    ';22,拡張バルーン,30000,\n;23,電極プラグ,50000,\n25,ローション,200,',
    ';22,拡張バルーン,30000,\n;23,電極プラグ,50000,\n; ※30(食材), 31(空き瓶), 46, 59, 65, 79, 81, 86, 87 等は廃止済み\n25,ローション,200,'
)

print("All fixes applied successfully!")
