def update_comf84():
    filepath = 'ERB/COMF/COMF84.ERB'
    with open(filepath, 'rb') as f:
        content = f.read().decode('cp932')

    # 1. Add TFLAG:19 = 1 and TFLAG:20
    if "TFLAG:19 = 1" not in content:
        target_1 = (
            "CALL TRAIN_MESSAGE_B\r\n"
            "\r\n"
            "\r\n"
            "LOSEBASE:0 += 50"
        )
        replacement_1 = (
            "CALL TRAIN_MESSAGE_B\r\n"
            "\r\n"
            ";V経験を伴うコマンドのフラグ(処女膜再生対応)\r\n"
            "TFLAG:19 = 1\r\n"
            "SIF TALENT:85 && ASSIPLAY == 0 && EXP:0 == 0\t; 【[恋慕] / [Ｖ経験]==0 / 主調教】\r\n"
            "\tTFLAG:20 = 1\r\n"
            "\r\n"
            "LOSEBASE:0 += 50"
        )
        if target_1 not in content:
            print("ERROR: target_1 not found in COMF84.ERB")
            return False
        content = content.replace(target_1, replacement_1)

    # 2. Add pain for virgin in SOURCE:6
    if "処女膜破損による苦痛を追加" not in content:
        target_2 = (
            ";EXP:Ｖ経験をみる\r\n"
            "IF EXP:0 < EXPLV:1\t; 【[Ｖ経験]<EXPLV:1】\r\n"
            "\tTIMES SOURCE:1 , 0.20\r\n"
            "\tTIMES SOURCE:13, 0.20\r\n"
            "\tSOURCE:6 = 150"
        )
        replacement_2 = (
            ";EXP:Ｖ経験をみる\r\n"
            "IF EXP:0 < EXPLV:1\t; 【[Ｖ経験]<EXPLV:1】\r\n"
            "\tTIMES SOURCE:1 , 0.20\r\n"
            "\tTIMES SOURCE:13, 0.20\r\n"
            "\tSOURCE:6 = 150\r\n"
            "\t;処女の場合は処女膜破損による苦痛を追加\r\n"
            "\tSIF TALENT:0\r\n"
            "\t\tSOURCE:6 += 1000"
        )
        if target_2 not in content:
            print("ERROR: target_2 not found in COMF84.ERB")
            return False
        content = content.replace(target_2, replacement_2)

    # 3. Add virgin description in TRAIN_MESSAGE_COM84
    if "処女膜を押し破って" not in content:
        idx_prevcom196 = content.find("PREVCOM == 196")
        idx_target = content.find("ELSEIF PREVCOM == 8 && ABL:MASTER:2 >= 3", idx_prevcom196)
        idx_end = content.find("ENDSELECT", idx_target) + len("ENDSELECT")

        old_slice = content[idx_target:idx_end]
        new_slice = (
            "ELSEIF PREVCOM == 8 && ABL:MASTER:2 >= 3\t; 【MASTER:[技巧]Lv>=3 / 前コマンド:[指挿入れ]】\r\n"
            "\tIF TALENT:0\t; 【[処女]】\r\n"
            "\t\tPRINTFORMW %CALLNAME:PLAYER%は浅く挿し入れていた指をさらに深く潜り込ませ、処女膜を押し破って膣天井の蠢く膨らみを刺激した…\r\n"
            "\tELSE\r\n"
            "\t\tSELECTCASE RAND:2\r\n"
            "\t\tCASE 0\r\n"
            "\t\t\tPRINTFORMW %CALLNAME:PLAYER%は%CALLNAME:TARGET%の膣の中で指を曲げ、ザラついた天井を刺激した…\r\n"
            "\t\tCASE 1\r\n"
            "\t\t\tPRINTFORMW %CALLNAME:PLAYER%は鉤状に曲げた指で%CALLNAME:TARGET%の蠢く天井を撫で、ぐっと手前に引き上げた…\r\n"
            "\t\tCASEELSE\r\n"
            "\t\t\tPRINTFORMW %CALLNAME:PLAYER%は%CALLNAME:TARGET%の膣の中で指を曲げ、ザラついた天井を刺激した…\r\n"
            "\t\tENDSELECT\r\n"
            "\tENDIF"
        )
        content = content[:idx_target] + new_slice + content[idx_end:]

    with open(filepath, 'wb') as f:
        f.write(content.encode('cp932'))
    print("SUCCESS: COMF84.ERB updated.")
    return True

if __name__ == '__main__':
    update_comf84()
