# -*- coding: utf-8 -*-
"""
Apply unconscious favor penalty to:
1. ERB/EVENT_S_特殊イベント.ERB:
   - MASTER_FLAG_CHECK:
     If partner is unconscious and NOT very intimate (no 恋慕/妄信/親愛/相愛/恋人/服従, and ABL:親密 < 10 or CFLAG:好感度 < 3000):
     - Every command executed lowers favor (20-30 for soft, 50-70 for invasive/sexual/painful)
     - Virginity loss (TFLAG:3 == 1) severely lowers favor (+700-900, +400 with 貞操観念)
     - Vaginal ejaculation lowers favor (+350-500, +200 with 貞操観念)
     - Anal ejaculation lowers favor (+250-350, +150 with 貞操観念)
     - Displays penalty and updated favor total

2. ERB/EVENT_N_妊娠イベント.ERB:
   - PREGNANCY_FEEL_UNCONSCIOUS:
     When unconscious pregnancy is discovered by a non-intimate character:
     - A-0 (Unaware virginity loss + unconscious pregnancy): -2000 to -2500 (-3000 with 貞操観念)
     - A-3 / B-3 (Impregnated by non-lover while unconscious): -1000 to -1300 / -800 to -1000
     - A-4 / B-4 (Chastity trait unwanted unconscious pregnancy): -1500 to -2000 / -1200 to -1500
     - A-6 / B-6 (Standard non-intimate unconscious pregnancy): -1000 to -1300 / -800 to -1000
     - Displays penalty and updated favor total
"""

import os
import shutil

def update_event_s():
    filepath = 'ERB/EVENT_S_特殊イベント.ERB'
    with open(filepath, 'r', encoding='cp932') as f:
        content = f.read()

    target = """IF TFLAG:899 || BASE:TARGET:0 <= 0\t; 【[気絶継続中] / TARGET:[体力]<=0】
\tR = 0
\tTFLAG:30 = 0
\tRETURN 0
ENDIF"""

    replacement = """;気絶中はターン経過しても好感度は上昇しない（非親密時はコマンドを重ねるごとに好感度低下）
IF TFLAG:899 || BASE:TARGET:0 <= 0\t; 【[気絶継続中] / TARGET:[体力]<=0】
\t; 非常に親密かどうかの判定
\t; 恋慕(85), 妄信(86), 親愛(88), 相愛(89), 恋人(153), 服従(180)のいずれかを所持、
\t; または [親密]Lv10以上 かつ [好感度]3000以上
\tLOCAL:80 = 0
\tSIF TALENT:TARGET:85 || TALENT:TARGET:86 || TALENT:TARGET:88 || TALENT:TARGET:89 || TALENT:TARGET:153 || TALENT:TARGET:180
\t\tLOCAL:80 = 1
\tSIF ABL:TARGET:0 >= 10 && CFLAG:TARGET:2 >= 3000
\t\tLOCAL:80 = 1

\t; 非常に親密な場合は好感度低下なし（既存仕様通り0変動）
\tIF LOCAL:80 == 1
\t\tR = 0
\t\tTFLAG:30 = 0
\t\tRETURN 0
\tENDIF

\t; --- 非常に親密でない場合：意識のない相手への行為による好感度低下 ---
\tLOCAL:81 = 0

\t; 「何もしない(SELECTCOM == 7)」はペナルティなし
\tIF SELECTCOM != 7
\t\t; 1. 基礎コマンドペナルティ
\t\t; 性交・道具・苦痛・排泄・羞恥・ハード系コマンドは重いペナルティ
\t\tIF IS_V_INSERT_COM(SELECTCOM) || IS_A_INSERT_COM(SELECTCOM) || (SELECTCOM >= 60 && SELECTCOM <= 79) || (SELECTCOM >= 40 && SELECTCOM <= 59) || (SELECTCOM >= 80 && SELECTCOM <= 89) || (SELECTCOM >= 140 && SELECTCOM <= 159) || (SELECTCOM >= 280 && SELECTCOM <= 284)
\t\t\tLOCAL:81 = 50 + RAND:21
\t\tELSE
\t\t\tLOCAL:81 = 20 + RAND:11
\t\tENDIF

\t\t; 素質補正
\t\tSIF TALENT:TARGET:30\t; 貞操観念
\t\t\tTIMES LOCAL:81 , 1.50
\t\tSIF TALENT:TARGET:11\t; 反抗的
\t\t\tTIMES LOCAL:81 , 1.20
\t\tSIF TALENT:TARGET:15\t; プライド高い
\t\t\tTIMES LOCAL:81 , 1.20
\t\tSIF TALENT:TARGET:32\t; 抑圧
\t\t\tTIMES LOCAL:81 , 1.20
\t\tSIF TALENT:TARGET:34\t; 抵抗
\t\t\tTIMES LOCAL:81 , 1.20
\t\tSIF TALENT:TARGET:31\t; 貞操無頓着
\t\t\tTIMES LOCAL:81 , 0.60
\t\tSIF TALENT:TARGET:22\t; 感情乏しい
\t\t\tTIMES LOCAL:81 , 0.80
\t\tSIF TALENT:TARGET:76\t; 淫乱
\t\t\tTIMES LOCAL:81 , 0.50

\t\t; 2. 処女喪失ペナルティ（大幅低下）
\t\tIF TFLAG:3 == 1
\t\t\tLOCAL:82 = 700 + RAND:201
\t\t\tSIF TALENT:TARGET:30\t; 貞操観念
\t\t\t\tLOCAL:82 += 400
\t\t\tSIF TALENT:TARGET:31\t; 貞操無頓着
\t\t\t\tLOCAL:82 = LOCAL:82 * 6 / 10
\t\t\tLOCAL:81 += LOCAL:82
\t\tENDIF

\t\t; 3. 膣内射精ペナルティ（追加低下）
\t\tIF TFLAG:302 > 0 && (TFLAG:703 == 1 || TFLAG:703 == 9 || (TFLAG:703 == 12 && TFLAG:(40 + ASSIPLAY) == 1))
\t\t\tLOCAL:83 = 350 + RAND:151
\t\t\tSIF TALENT:TARGET:30\t; 貞操観念
\t\t\t\tLOCAL:83 += 200
\t\t\tSIF TALENT:TARGET:31\t; 貞操無頓着
\t\t\t\tLOCAL:83 = LOCAL:83 * 7 / 10
\t\t\tLOCAL:81 += LOCAL:83
\t\t; アナル射精ペナルティ
\t\tELSEIF TFLAG:302 > 0 && (TFLAG:703 == 2 || TFLAG:703 == 10 || (TFLAG:703 == 12 && TFLAG:(40 + ASSIPLAY) == 2))
\t\t\tLOCAL:83 = 250 + RAND:101
\t\t\tSIF TALENT:TARGET:30\t; 貞操観念
\t\t\t\tLOCAL:83 += 150
\t\t\tLOCAL:81 += LOCAL:83
\t\tENDIF

\t\t; 好感度を減少
\t\tIF LOCAL:81 > 0
\t\t\tCFLAG:TARGET:2 -= LOCAL:81
\t\t\tIF TFLAG:3 == 1
\t\t\t\tPRINTFORML 意識のないまま純潔を奪われた%CALLNAME:TARGET%の好感度が激しく低下した…！
\t\t\tELSEIF TFLAG:302 > 0 && (TFLAG:703 == 1 || TFLAG:703 == 9 || (TFLAG:703 == 12 && TFLAG:(40 + ASSIPLAY) == 1))
\t\t\t\tPRINTFORML 意識のない胎内に精液を注ぎ込まれた%CALLNAME:TARGET%の好感度が大きく低下した…！
\t\t\tELSEIF TFLAG:302 > 0 && (TFLAG:703 == 2 || TFLAG:703 == 10 || (TFLAG:703 == 12 && TFLAG:(40 + ASSIPLAY) == 2))
\t\t\t\tPRINTFORML 意識のない腸内に精液を注ぎ込まれた%CALLNAME:TARGET%の好感度が大きく低下した…！
\t\t\tELSE
\t\t\t\tPRINTFORML 意識を失った%CALLNAME:TARGET%への一方的な行為により、好感度が低下した…
\t\t\tENDIF
\t\t\tPRINTFORML 好感度低下:{LOCAL:81}
\t\t\tSIF ((FLAG:23 & 1p26) == 0) && FLAG:2 != 1
\t\t\t\tPRINTFORMW 好感度合計:{CFLAG:TARGET:2}
\t\tENDIF
\tENDIF

\tR = 0
\tTFLAG:30 = 0
\tRETURN 0
ENDIF"""

    if target not in content:
        raise ValueError(f"Target not found in {filepath}")

    new_content = content.replace(target, replacement, 1)
    with open(filepath, 'w', encoding='cp932', newline='\r\n') as f:
        f.write(new_content)
    print(f"Successfully updated {filepath}")

def update_event_n():
    filepath = 'ERB/EVENT_N_妊娠イベント.ERB'
    with open(filepath, 'r', encoding='cp932') as f:
        content = f.read()

    # 1. Update PREGNANCY_FEEL_UNCONSCIOUS signature & local vars
    target_sig = """@PREGNANCY_FEEL_UNCONSCIOUS, ARG, ARG:1, ARG:2
#DIM MOM
#DIM DAD
#DIM LOVED
MOM = ARG
DAD = ARG:1
LOVED = ARG:2"""

    repl_sig = """@PREGNANCY_FEEL_UNCONSCIOUS, ARG, ARG:1, ARG:2
#DIM MOM
#DIM DAD
#DIM LOVED
#DIM PENALTY
MOM = ARG
DAD = ARG:1
LOVED = ARG:2
PENALTY = 0"""

    if target_sig not in content:
        raise ValueError(f"target_sig not found in {filepath}")
    content = content.replace(target_sig, repl_sig, 1)

    # 2. Update A-0 branch
    target_a0 = """\t;--- A-0. 無自覚処女喪失(CFLAG:1245 == 1)が未発覚のまま妊娠まで発覚した場合 ---
\tIF CFLAG:MOM:1245 == 1
\t\tCFLAG:MOM:1245 = 2
\t\tIF LOVED && (TALENT:MOM:88 || TALENT:MOM:89 || TALENT:MOM:85 || TALENT:MOM:153)
\t\t\tPRINTFORML まだ純潔のはずだった%CALLNAME:MOM%は、交わった記憶がないまま胎内に新しい命が宿っている事実に目を丸くした…
\t\t\tPRINTFORML 気を失っている間に%CALLNAME:DAD%に初めてを奪われ、そのまま子種まで注ぎ込まれていたのだと悟り、%CALLNAME:MOM%は涙目になりながらも震える手で下腹を撫でた…
\t\tELSE
\t\t\tPRINTFORML 処女のはずの自分の胎内に見覚えのない命が宿っているというあり得ない現実に、%CALLNAME:MOM%は全身の血の気を引かせた…
\t\t\tPRINTFORML 意識を失っている間に純潔を散らされたばかりか、一方的に種付けされて身籠らされていたのだと気づき、%CALLNAME:MOM%は蒼白になって下腹を抱え込んだ…
\t\tENDIF
\t\tRETURN
\tENDIF"""

    repl_a0 = """\t;--- A-0. 無自覚処女喪失(CFLAG:1245 == 1)が未発覚のまま妊娠まで発覚した場合 ---
\tIF CFLAG:MOM:1245 == 1
\t\tCFLAG:MOM:1245 = 2
\t\tIF LOVED && (TALENT:MOM:88 || TALENT:MOM:89 || TALENT:MOM:85 || TALENT:MOM:153 || TALENT:MOM:180)
\t\t\tPRINTFORML まだ純潔のはずだった%CALLNAME:MOM%は、交わった記憶がないまま胎内に新しい命が宿っている事実に目を丸くした…
\t\t\tPRINTFORML 気を失っている間に%CALLNAME:DAD%に初めてを奪われ、そのまま子種まで注ぎ込まれていたのだと悟り、%CALLNAME:MOM%は涙目になりながらも震える手で下腹を撫でた…
\t\tELSE
\t\t\tPRINTFORML 処女のはずの自分の胎内に見覚えのない命が宿っているというあり得ない現実に、%CALLNAME:MOM%は全身の血の気を引かせた…
\t\t\tPRINTFORML 意識を失っている間に純潔を散らされたばかりか、一方的に種付けされて身籠らされていたのだと気づき、%CALLNAME:MOM%は蒼白になって下腹を抱え込んだ…
\t\t\tPENALTY = 2000 + RAND:501
\t\t\tSIF TALENT:MOM:30\t; 貞操観念
\t\t\t\tPENALTY += 500
\t\t\tCFLAG:MOM:2 -= PENALTY
\t\t\tPRINTFORML 意識のないまま純潔を奪われて身籠らされた絶望により、好感度が大幅に低下した…！
\t\t\tPRINTFORML 好感度大幅低下:{PENALTY}
\t\t\tPRINTFORMW 好感度合計:{CFLAG:MOM:2}
\t\tENDIF
\t\tRETURN
\tENDIF"""

    if target_a0 not in content:
        raise ValueError(f"target_a0 not found in {filepath}")
    content = content.replace(target_a0, repl_a0, 1)

    # 3. Update A-3 (恋慕あり想い人以外)
    target_a3 = """\t;--- A-3. 恋慕・恋人ありで想い人以外の子（背徳） ---
\tELSEIF (TALENT:MOM:85 || TALENT:MOM:153) && LOVED == 0"""

    repl_a3 = """\t;--- A-3. 恋慕・恋人ありで想い人以外の子（背徳） ---
\tELSEIF (TALENT:MOM:85 || TALENT:MOM:153) && LOVED == 0
\t\tPENALTY = 1000 + RAND:301"""

    if target_a3 not in content:
        raise ValueError(f"target_a3 not found in {filepath}")
    content = content.replace(target_a3, repl_a3, 1)

    # 4. Update A-4 (貞操観念)
    target_a4 = """\t;--- A-4. 貞操観念（望まぬ無自覚妊娠） ---
\tELSEIF TALENT:MOM:30"""

    repl_a4 = """\t;--- A-4. 貞操観念（望まぬ無自覚妊娠） ---
\tELSEIF TALENT:MOM:30
\t\tPENALTY = 1500 + RAND:501"""

    if target_a4 not in content:
        raise ValueError(f"target_a4 not found in {filepath}")
    content = content.replace(target_a4, repl_a4, 1)

    # 5. Update A-6 (標準)
    target_a6 = """\t;--- A-6. 標準 ---
\tELSE
\t\tSELECTCASE RAND:3
\t\tCASE 0
\t\t\tPRINTFORML 意識を失う前には最後までシていなかったはずなのに、なぜ自分が身籠っているのか理解が追いつかず、%CALLNAME:MOM%は呆然と下腹を見下ろした…
\t\tCASE 1
\t\t\tPRINTFORML 交わった記憶がないまま胎内に宿った命の気配に、%CALLNAME:MOM%は気を失っていた間に中出しされていたのだと気づいて息を呑んだ…
\t\tCASEELSE
\t\t\tPRINTFORML 自分の知らぬ間に身体を貫かれ、気づいた時にはすでに母になっていたという事実に、%CALLNAME:MOM%は強い困惑を隠せないでいる…
\t\tENDSELECT
\tENDIF"""

    repl_a6 = """\t;--- A-6. 標準 ---
\tELSE
\t\tSELECTCASE RAND:3
\t\tCASE 0
\t\t\tPRINTFORML 意識を失う前には最後までシていなかったはずなのに、なぜ自分が身籠っているのか理解が追いつかず、%CALLNAME:MOM%は呆然と下腹を見下ろした…
\t\tCASE 1
\t\t\tPRINTFORML 交わった記憶がないまま胎内に宿った命の気配に、%CALLNAME:MOM%は気を失っていた間に中出しされていたのだと気づいて息を呑んだ…
\t\tCASEELSE
\t\t\tPRINTFORML 自分の知らぬ間に身体を貫かれ、気づいた時にはすでに母になっていたという事実に、%CALLNAME:MOM%は強い困惑を隠せないでいる…
\t\tENDSELECT
\t\t; 非常に親密でない場合は好感度低下
\t\tIF TALENT:MOM:180 == 0 && (ABL:MOM:0 < 10 || CFLAG:MOM:2 < 3000)
\t\t\tPENALTY = 1000 + RAND:301
\t\t\tSIF TALENT:MOM:11 || TALENT:MOM:15 || TALENT:MOM:34
\t\t\t\tPENALTY = PENALTY * 12 / 10
\t\tENDIF
\tENDIF"""

    if target_a6 not in content:
        raise ValueError(f"target_a6 not found in {filepath}")
    content = content.replace(target_a6, repl_a6, 1)

    # 6. Update B-3 (背徳)
    target_b3 = """\t;--- B-3. 恋慕・恋人ありで想い人以外の子（背徳） ---
\tELSEIF (TALENT:MOM:85 || TALENT:MOM:153) && LOVED == 0"""

    repl_b3 = """\t;--- B-3. 恋慕・恋人ありで想い人以外の子（背徳） ---
\tELSEIF (TALENT:MOM:85 || TALENT:MOM:153) && LOVED == 0
\t\tPENALTY = 800 + RAND:201"""

    if target_b3 not in content:
        raise ValueError(f"target_b3 not found in {filepath}")
    content = content.replace(target_b3, repl_b3, 1)

    # 7. Update B-4 (貞操観念)
    target_b4 = """\t;--- B-4. 貞操観念（望まぬ妊娠） ---
\tELSEIF TALENT:MOM:30"""

    repl_b4 = """\t;--- B-4. 貞操観念（望まぬ妊娠） ---
\tELSEIF TALENT:MOM:30
\t\tPENALTY = 1200 + RAND:301"""

    if target_b4 not in content:
        raise ValueError(f"target_b4 not found in {filepath}")
    content = content.replace(target_b4, repl_b4, 1)

    # 8. Update B-6 (標準) & end of function
    target_b6 = """\t;--- B-6. 標準 ---
\tELSE
\t\tSELECTCASE RAND:3
\t\tCASE 0
\t\t\tPRINTFORML 意識を失う前に交わっていた記憶と、目を覚ました後に突きつけられた妊娠の事実に、%CALLNAME:MOM%は戸惑いがちに下腹へ手を当てた…
\t\tCASE 1
\t\t\tPRINTFORML 意識が途切れるほど激しい交わりの末に身籠ってしまったことを知り、%CALLNAME:MOM%は複雑な面持ちでそっと腹を撫でた…
\t\tCASEELSE
\t\t\tPRINTFORML 気を失っている間にまで中出しされて母になっていたという現実に、%CALLNAME:MOM%は呆然と腹を見下ろした…
\t\tENDSELECT
\tENDIF
ENDIF
RETURN"""

    repl_b6 = """\t;--- B-6. 標準 ---
\tELSE
\t\tSELECTCASE RAND:3
\t\tCASE 0
\t\t\tPRINTFORML 意識を失う前に交わっていた記憶と、目を覚ました後に突きつけられた妊娠の事実に、%CALLNAME:MOM%は戸惑いがちに下腹へ手を当てた…
\t\tCASE 1
\t\t\tPRINTFORML 意識が途切れるほど激しい交わりの末に身籠ってしまったことを知り、%CALLNAME:MOM%は複雑な面持ちでそっと腹を撫でた…
\t\tCASEELSE
\t\t\tPRINTFORML 気を失っている間にまで中出しされて母になっていたという現実に、%CALLNAME:MOM%は呆然と腹を見下ろした…
\t\tENDSELECT
\t\t; 非常に親密でない場合は好感度低下
\t\tIF TALENT:MOM:180 == 0 && (ABL:MOM:0 < 10 || CFLAG:MOM:2 < 3000)
\t\t\tPENALTY = 800 + RAND:201
\t\t\tSIF TALENT:MOM:11 || TALENT:MOM:15 || TALENT:MOM:34
\t\t\t\tPENALTY = PENALTY * 12 / 10
\t\tENDIF
\tENDIF
ENDIF

IF PENALTY > 0
\tCFLAG:MOM:2 -= PENALTY
\tPRINTFORML 意識のない間に身籠らされた不本意な妊娠により、好感度が大幅に低下した…！
\tPRINTFORML 好感度大幅低下:{PENALTY}
\tPRINTFORMW 好感度合計:{CFLAG:MOM:2}
ENDIF
RETURN"""

    if target_b6 not in content:
        raise ValueError(f"target_b6 not found in {filepath}")
    content = content.replace(target_b6, repl_b6, 1)

    with open(filepath, 'w', encoding='cp932', newline='\r\n') as f:
        f.write(content)
    print(f"Successfully updated {filepath}")

if __name__ == '__main__':
    update_event_s()
    update_event_n()
    print("All updates applied cleanly!")
