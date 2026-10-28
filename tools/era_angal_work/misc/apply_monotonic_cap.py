import sys

def apply_monotonic_cap_rebalance():
    filepath = 'ERB/SHOP_ショップ.ERB'
    with open(filepath, 'rb') as f:
        content = f.read().decode('cp932')

    # Solo money-making
    start_solo = content.find(";基礎能力（技巧）\r\n\tLOCAL:2 = ABL:MASTER:2")
    end_solo = content.find("MONEY += P", start_solo)
    if start_solo == -1 or end_solo == -1:
        print("ERROR: solo section not found")
        return False

    new_solo = (
        ";基礎能力（技巧）\r\n"
        "\tLOCAL:2 = ABL:MASTER:2\r\n"
        "\tSIF LOCAL:2 > 5\r\n"
        "\t\tLOCAL:2 = 5 + SQRT((LOCAL:2 - 5) * 10)\r\n"
        "\tP = (LOCAL:2 + 10) * 20\r\n"
        "\tPRINTFORM %CALLNAME:MASTER%は\r\n"
        "\tIF TFLAG:17 == 1\t; 【[コマンド内容]==1】\r\n"
        "\t\tP *= 50\r\n"
        "\t\tPRINT 配達、\r\n"
        "\tELSEIF TFLAG:17 == 2\t; 【[コマンド内容]==2】\r\n"
        "\t\tP *= 85\r\n"
        "\t\tPRINT コンビニでアルバイト、\r\n"
        "\tELSEIF TFLAG:17 == 3\t; 【[コマンド内容]==3】\r\n"
        "\t\tP *= 100\r\n"
        "\t\tSIF TALENT:MASTER:209\t; 【MASTER:[野菜を育てる程度の能力]】\r\n"
        "\t\t\tP *= 3\r\n"
        "\t\tPRINT イベントスタッフ、\r\n"
        "\tELSEIF TFLAG:17 == 4\t; 【[コマンド内容]==4】\r\n"
        "\t\tP *= 120\r\n"
        "\t\tPRINT フリマアプリで稼ぎ、\r\n"
        "\tELSE\r\n"
        "\t\tP *= 250\r\n"
        "\t\tPRINT 懸賞に当たり、\r\n"
        "\tENDIF\r\n"
        "\r\n"
        "\t;買物ボーナス（獲得資金増加）\r\n"
        "\tIF ABL:MASTER:86 == 1\t; 【MASTER:[獲得資金増加]Lv==1】\r\n"
        "\t\tTIMES P , 1.50\r\n"
        "\tELSEIF ABL:MASTER:86 > 1\t; 【MASTER:[獲得資金増加]Lv>1】\r\n"
        "\t\tLOCAL:86 = ABL:MASTER:86\r\n"
        "\t\tSIF LOCAL:86 > 5\r\n"
        "\t\t\tLOCAL:86 = 5 + SQRT((LOCAL:86 - 5) * 8)\r\n"
        "\t\tP *= LOCAL:86\r\n"
        "\tENDIF\r\n"
        "\r\n"
        "\t;高額所得補正（異常インフレ防止）\r\n"
        "\tIF P > 1000000\r\n"
        "\t\tLOCAL:10 = MIN(P, 5000000) - 1000000\r\n"
        "\t\tLOCAL:11 = 0\r\n"
        "\t\tSIF P > 5000000\r\n"
        "\t\t\tLOCAL:11 = MIN(P, 20000000) - 5000000\r\n"
        "\t\tLOCAL:12 = 0\r\n"
        "\t\tSIF P > 20000000\r\n"
        "\t\t\tLOCAL:12 = P - 20000000\r\n"
        "\t\tP = 1000000 + LOCAL:10 / 2 + LOCAL:11 / 4 + LOCAL:12 / 10\r\n"
        "\tENDIF\r\n"
        "\tP = LIMIT(P, 0, 50000000)\r\n"
        "\r\n"
        "\t;成果・出来栄えによる振れ幅（80%〜100%＋端数）\r\n"
        "\t;高額補正・上限キャップ後に掛けることで、能力向上時の逆転を防ぎつつキャップ時も毎回変動\r\n"
        "\tP = P * (8000 + RAND:2001) / 10000\r\n"
        "\tSIF P > 1000\r\n"
        "\t\tP += RAND:1000 - 500\r\n"
        "\tP = LIMIT(P, 0, 50000000)\r\n"
        "\t\r\n"
        "\tPRINTFORMW ${P}の収入を得た。\r\n\t"
    )

    content = content[:start_solo] + new_solo + content[end_solo:]

    # Duo money-making
    start_duo = content.find(";基礎能力（技巧・奉仕精神）\r\n\tLOCAL:1 = ABL:MASTER:2 * 2 + ABL:TARGET:2")
    end_duo = content.find("MONEY += P", start_duo)
    if start_duo == -1 or end_duo == -1:
        print("ERROR: duo section not found")
        return False

    new_duo = (
        ";基礎能力（技巧・奉仕精神）\r\n"
        "\tLOCAL:1 = ABL:MASTER:2 * 2 + ABL:TARGET:2 + ABL:TARGET:6 * 2\r\n"
        "\tSIF LOCAL:1 > 25\r\n"
        "\t\tLOCAL:1 = 25 + SQRT((LOCAL:1 - 25) * 20)\r\n"
        "\tP = (LOCAL:1 + B + 15) * 10\r\n"
        "\tPRINTFORM %CALLNAME:MASTER%と%CALLNAME:TARGET%は２人で\r\n"
        "\tIF TFLAG:17 == 1\t; 【[コマンド内容]==1】\r\n"
        "\t\tP *= 60\r\n"
        "\t\tPRINT カフェでアルバイト、\r\n"
        "\tELSEIF TFLAG:17 == 2\t; 【[コマンド内容]==2】\r\n"
        "\t\tP *= 90\r\n"
        "\t\tPRINT 配達、\r\n"
        "\tELSEIF TFLAG:17 == 3\t; 【[コマンド内容]==3】\r\n"
        "\t\tP *= 110\r\n"
        "\t\tPRINT コンビニでアルバイト、\r\n"
        "\tELSEIF TFLAG:17 == 4\t; 【[コマンド内容]==4】\r\n"
        "\t\tP *= 140\r\n"
        "\t\tPRINT イベントスタッフ、\r\n"
        "\t\tSIF TALENT:MASTER:209\t; 【MASTER:[野菜を育てる程度の能力]】\r\n"
        "\t\t\tP *= 3\r\n"
        "\tELSE\r\n"
        "\t\tP *= 400\r\n"
        "\t\tPRINT 懸賞に当たり、\r\n"
        "\tENDIF\r\n"
        "\r\n"
        "\t;買物ボーナス（獲得資金増加）\r\n"
        "\tIF ABL:MASTER:86 == 1\t; 【MASTER:[獲得資金増加]Lv==1】\r\n"
        "\t\tTIMES P , 1.50\r\n"
        "\tELSEIF ABL:MASTER:86 > 1\t; 【MASTER:[獲得資金増加]Lv>1】\r\n"
        "\t\tLOCAL:86 = ABL:MASTER:86\r\n"
        "\t\tSIF LOCAL:86 > 5\r\n"
        "\t\t\tLOCAL:86 = 5 + SQRT((LOCAL:86 - 5) * 8)\r\n"
        "\t\tP *= LOCAL:86\r\n"
        "\tENDIF\r\n"
        "\r\n"
        "\t;金銭感覚ボーナス（MASTER＋TARGETの合算）\r\n"
        "\tIF ABL:MASTER:89 + ABL:TARGET:89 > 0\t; 【MASTER:[金銭感覚] / TARGET:[金銭感覚]Lv>0】\r\n"
        "\t\tLOCAL:89 = ABL:MASTER:89 + ABL:TARGET:89\r\n"
        "\t\tSIF LOCAL:89 > 10\r\n"
        "\t\t\tLOCAL:89 = 10 + SQRT((LOCAL:89 - 10) * 10)\r\n"
        "\t\tP += P * LOCAL:89 * 3 / 100\r\n"
        "\tENDIF\r\n"
        "\r\n"
        "\t;高額所得補正（異常インフレ防止）\r\n"
        "\tIF P > 1000000\r\n"
        "\t\tLOCAL:10 = MIN(P, 5000000) - 1000000\r\n"
        "\t\tLOCAL:11 = 0\r\n"
        "\t\tSIF P > 5000000\r\n"
        "\t\t\tLOCAL:11 = MIN(P, 20000000) - 5000000\r\n"
        "\t\tLOCAL:12 = 0\r\n"
        "\t\tSIF P > 20000000\r\n"
        "\t\t\tLOCAL:12 = P - 20000000\r\n"
        "\t\tP = 1000000 + LOCAL:10 / 2 + LOCAL:11 / 4 + LOCAL:12 / 10\r\n"
        "\tENDIF\r\n"
        "\tP = LIMIT(P, 0, 50000000)\r\n"
        "\r\n"
        "\t;成果・出来栄えによる振れ幅（80%〜100%＋端数）\r\n"
        "\t;高額補正・上限キャップ後に掛けることで、能力向上時の逆転を防ぎつつキャップ時も毎回変動\r\n"
        "\tP = P * (8000 + RAND:2001) / 10000\r\n"
        "\tSIF P > 1000\r\n"
        "\t\tP += RAND:1000 - 500\r\n"
        "\tP = LIMIT(P, 0, 50000000)\r\n"
        "\t\r\n"
        "\tPRINTFORML ${P}の収入を得た。\r\n\t"
    )

    content = content[:start_duo] + new_duo + content[end_duo:]

    with open(filepath, 'wb') as f:
        f.write(content.encode('cp932'))
    print("SUCCESS: SHOP_ショップ.ERB updated.")
    return True

if __name__ == '__main__':
    apply_monotonic_cap_rebalance()
