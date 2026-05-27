# -*- coding: utf-8 -*-
# ちんちんサイズ機能（cm数値・大小2種アイテム・主人公+女の子）
# 保持: CFLAG:<char>:1100 (cm)  標準15 / 範囲5-30 / ±3
# 対象ファイルは全てLF改行（ヘッダのみ稀にCRLFだがアンカー位置はLF）

def edit(path, repls):
    t=open(path,'rb').read().decode('cp932')
    for old,new,cnt in repls:
        c=t.count(old)
        assert c==cnt, f'{path}: アンカー{c}!={cnt}\n>>>{old[:90]}'
        t=t.replace(old,new)
    data=t.encode('cp932')
    open(path,'wb').write(data)
    print('OK', path.split('/')[-1])

# 1. Item.csv: 88/89 追加（LF）
edit('CSV/Item.csv', [(
 "78,尿漏れ改善薬,5000,;お漏らし癖が直る。",
 "78,尿漏れ改善薬,5000,;お漏らし癖が直る。\n"
 "88,ちんちんを大きくする薬,8000,;ふたなりのちんちんを3cm大きくする(最大30cm)\n"
 "89,ちんちんを小さくする薬,8000,;ふたなりのちんちんを3cm小さくする(最小5cm)", 1)])

# 2. Cflag.csv: 1100 ラベル（LF）
edit('CSV/Cflag.csv', [(
 "1025,見つめあう",
 "1025,見つめあう\n1100,ちんちんサイズ(cm)", 1)])

# 3. SHOP_ITEM（LF）
S='ERB/SHOP_ITEM_ショップアイテム定義.ERB'
edit(S, [
 # (販売条件) サイズ薬88/89: ふたなりキャラがいれば販売。ITEMSALES:81=0群の直後に追加
 ("ITEMSALES:80 = 0\nITEMSALES:81 = 0\n",
  "ITEMSALES:80 = 0\nITEMSALES:81 = 0\nITEMSALES:88 = 0\nITEMSALES:89 = 0\n", 1),
 # ふたなりキャラ判定ループ内（ITEMSALES:81判定の直後）でサイズ薬を販売可に
 ("\t\tSIF CFLAG:COUNT:0 == 0 && ABLE_EX_CHANGES(COUNT)\n\t\t\tITEMSALES:81 = 1\n\tREND",
  "\t\tSIF CFLAG:COUNT:0 == 0 && ABLE_EX_CHANGES(COUNT)\n\t\t\tITEMSALES:81 = 1\n"
  "\t\t;88,89 ちんちんサイズ変更（ふたなりキャラがいれば販売）\n"
  "\t\tSIF TALENT:COUNT:121\n\t\t\tITEMSALES:88 = 1\n"
  "\t\tSIF TALENT:COUNT:121\n\t\t\tITEMSALES:89 = 1\n\tREND", 1),
 # (a) 対象選択ガード: 非ふたなりは非表示
 ("\tSIF BOUGHT == 98 && COUNT == 0\n\t\tCONTINUE\n",
  "\tSIF BOUGHT == 98 && COUNT == 0\n\t\tCONTINUE\n"
  "\tSIF (BOUGHT == 88 || BOUGHT == 89) && TALENT:COUNT:121 == 0\n\t\tCONTINUE\n", 1),
 # (b) 主人公を選択肢に追加（サイズ薬・主人公がふたなりのとき）
 ("IF CHARANUM <= 100\n\tPRINTL [100] 戻る\n",
  "IF (BOUGHT == 88 || BOUGHT == 89) && TALENT:MASTER:121\n"
  "\tPRINTFORML [101] %CALLNAME:MASTER%（主人公）\nENDIF\n"
  "IF CHARANUM <= 100\n\tPRINTL [100] 戻る\n", 1),
 # (c) 入力検証: 主人公センチネル101許可
 ("ELSE\n\tIF RESULT < 0 || RESULT >= CHARANUM\n\t\tPRINTFORML 正しい値を入力してください\n\t\tGOTO INPUT_LOOP\n\tELSEIF TFLAG:RESULT == 0",
  "ELSEIF (BOUGHT == 88 || BOUGHT == 89) && RESULT == 101 && TALENT:MASTER:121\n"
  "\t;主人公を対象（ちんちんサイズ薬のみ）\n"
  "ELSE\n\tIF RESULT < 0 || RESULT >= CHARANUM\n\t\tPRINTFORML 正しい値を入力してください\n\t\tGOTO INPUT_LOOP\n\tELSEIF TFLAG:RESULT == 0", 1),
 # (d) ふたなり化時にサイズ初期値15cm
 ("\tTALENT:RESULT:121 = 1\n\tTFLAG:600 = 51",
  "\tTALENT:RESULT:121 = 1\n\t;ちんちんサイズ初期値(cm)\n\tSIF CFLAG:RESULT:1100 == 0\n\t\tCFLAG:RESULT:1100 = 15\n\tTFLAG:600 = 51", 1),
 # (e) アイテム88/89効果（ふたなり消去ブロック直後）
 (";ふたなりを消去\nIF BOUGHT == 72\n\tPRINTFORMW ＜%NAME:RESULT%はふたなりではなくなった＞\n\tTALENT:RESULT:121 = 0\n\tTFLAG:600 = 52\nENDIF\n",
  ";ふたなりを消去\nIF BOUGHT == 72\n\tPRINTFORMW ＜%NAME:RESULT%はふたなりではなくなった＞\n\tTALENT:RESULT:121 = 0\n\tTFLAG:600 = 52\nENDIF\n"
  ";ちんちんを大きくする\nIF BOUGHT == 88\n"
  "\tIF RESULT == 101\n"
  "\t\tSIF CFLAG:MASTER:1100 == 0\n\t\t\tCFLAG:MASTER:1100 = 15\n"
  "\t\tCFLAG:MASTER:1100 += 3\n\t\tSIF CFLAG:MASTER:1100 > 30\n\t\t\tCFLAG:MASTER:1100 = 30\n"
  "\t\tPRINTFORMW ＜%CALLNAME:MASTER%のちんちんが大きくなった（{CFLAG:MASTER:1100}cm）＞\n"
  "\tELSE\n"
  "\t\tSIF CFLAG:RESULT:1100 == 0\n\t\t\tCFLAG:RESULT:1100 = 15\n"
  "\t\tCFLAG:RESULT:1100 += 3\n\t\tSIF CFLAG:RESULT:1100 > 30\n\t\t\tCFLAG:RESULT:1100 = 30\n"
  "\t\tPRINTFORMW ＜%NAME:RESULT%のちんちんが大きくなった（{CFLAG:RESULT:1100}cm）＞\n"
  "\tENDIF\nENDIF\n"
  ";ちんちんを小さくする\nIF BOUGHT == 89\n"
  "\tIF RESULT == 101\n"
  "\t\tSIF CFLAG:MASTER:1100 == 0\n\t\t\tCFLAG:MASTER:1100 = 15\n"
  "\t\tCFLAG:MASTER:1100 -= 3\n\t\tSIF CFLAG:MASTER:1100 < 5\n\t\t\tCFLAG:MASTER:1100 = 5\n"
  "\t\tPRINTFORMW ＜%CALLNAME:MASTER%のちんちんが小さくなった（{CFLAG:MASTER:1100}cm）＞\n"
  "\tELSE\n"
  "\t\tSIF CFLAG:RESULT:1100 == 0\n\t\t\tCFLAG:RESULT:1100 = 15\n"
  "\t\tCFLAG:RESULT:1100 -= 3\n\t\tSIF CFLAG:RESULT:1100 < 5\n\t\t\tCFLAG:RESULT:1100 = 5\n"
  "\t\tPRINTFORMW ＜%NAME:RESULT%のちんちんが小さくなった（{CFLAG:RESULT:1100}cm）＞\n"
  "\tENDIF\nENDIF\n", 1),
 # (f) 末尾の口上呼び出しを主人公センチネルから保護
 ("T = TARGET\nTARGET = RESULT\nCALL KOJO_JUN\nTARGET = T",
  "T = TARGET\nIF RESULT >= 0 && RESULT < CHARANUM\n\tTARGET = RESULT\n\tCALL KOJO_JUN\n\tTARGET = T\nENDIF", 1),
])

# 4. INFO能力表示（LF）: MASTER/ASSI/TARGET にサイズ表示
I='ERB/INFO_情報表示.ERB'
edit(I, [
 ("\tPRINTFORM  ({BASE:MASTER:2}/{MAXBASE:MASTER:2})\n\tIF TEQUIP:MASTER:85 == 1",
  "\tPRINTFORM  ({BASE:MASTER:2}/{MAXBASE:MASTER:2})\n"
  "\tSIF CFLAG:MASTER:1100 == 0\n\t\tCFLAG:MASTER:1100 = 15\n"
  "\tPRINTFORM 　ちんちん：{CFLAG:MASTER:1100}cm\n"
  "\tIF TEQUIP:MASTER:85 == 1", 1),
 ("\t\tPRINTFORM ({BASE:ASSI:2}/{MAXBASE:ASSI:2})\n\t\tIF TEQUIP:ASSI:85 == 1",
  "\t\tPRINTFORM ({BASE:ASSI:2}/{MAXBASE:ASSI:2})\n"
  "\t\tSIF CFLAG:ASSI:1100 == 0\n\t\t\tCFLAG:ASSI:1100 = 15\n"
  "\t\tPRINTFORM 　ちんちん：{CFLAG:ASSI:1100}cm\n"
  "\t\tIF TEQUIP:ASSI:85 == 1", 1),
 ("\tPRINTFORM ({BASE:2}/{MAXBASE:2})\n\tIF TEQUIP:85 == 1",
  "\tPRINTFORM ({BASE:2}/{MAXBASE:2})\n"
  "\tSIF CFLAG:1100 == 0\n\t\tCFLAG:1100 = 15\n"
  "\tPRINTFORM 　ちんちん：{CFLAG:1100}cm\n"
  "\tIF TEQUIP:85 == 1", 1),
])
print('全実装 完了')
