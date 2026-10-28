import re

def update_event_shoot():
    filepath = 'ERB/EVENT_SHOOT_射精処理.ERB'
    with open(filepath, 'rb') as f:
        content = f.read().decode('cp932')

    old_block = (
        "IF TFLAG:302 == 4\t; 【[絶頂]==4】\r\n"
        "\tIF TFLAG:714 > 10\r\n"
        "\t\tPRINTFORML 超量射精（{TFLAG:719}ml）\r\n"
        "\tELSE\r\n"
        "\t\tPRINTFORML 超量射精×{TFLAG:714}（{TFLAG:719}ml）\r\n"
        "\tENDIF\r\n"
        "ELSEIF TFLAG:302 == 2\t; 【[絶頂]==2】\r\n"
        "\tIF TFLAG:714 > 10\r\n"
        "\t\tPRINTFORML 大量射精（{TFLAG:719}ml）\r\n"
        "\tELSE\r\n"
        "\t\tPRINTFORML 大量射精×{TFLAG:714}（{TFLAG:719}ml）\r\n"
        "\tENDIF\r\n"
        "ELSEIF TFLAG:302 == 1\t; 【[絶頂]==1】\r\n"
        "\tIF TFLAG:714 > 10\r\n"
        "\t\tPRINTFORML 射精（{TFLAG:719}ml）\r\n"
        "\tELSE\r\n"
        "\t\tPRINTFORML 射精×{TFLAG:714}（{TFLAG:719}ml）\r\n"
        "\tENDIF\r\n"
        "ENDIF"
    )

    new_block = (
        "IF TFLAG:302 == 4\t; 【[絶頂]==4】\r\n"
        "\tPRINTFORML 超量射精×{TFLAG:714}（{TFLAG:719}ml）\r\n"
        "ELSEIF TFLAG:302 == 2\t; 【[絶頂]==2】\r\n"
        "\tPRINTFORML 大量射精×{TFLAG:714}（{TFLAG:719}ml）\r\n"
        "ELSEIF TFLAG:302 == 1\t; 【[絶頂]==1】\r\n"
        "\tPRINTFORML 射精×{TFLAG:714}（{TFLAG:719}ml）\r\n"
        "ENDIF"
    )

    if old_block not in content:
        print("ERROR: old_block not found in EVENT_SHOOT")
        return False

    content = content.replace(old_block, new_block)
    with open(filepath, 'wb') as f:
        f.write(content.encode('cp932'))
    print("SUCCESS: EVENT_SHOOT_射精処理.ERB updated.")
    return True

def update_shop_cap():
    filepath = 'ERB/SHOP_ショップ.ERB'
    with open(filepath, 'rb') as f:
        content = f.read().decode('cp932')

    old_cap = (
        "\t\tP = 1000000 + LOCAL:10 / 2 + LOCAL:11 / 4 + LOCAL:12 / 10\r\n"
        "\tENDIF\r\n"
        "\tP = LIMIT(P, 0, 50000000)"
    )

    new_cap = (
        "\t\tP = 1000000 + LOCAL:10 / 2 + LOCAL:11 / 4 + LOCAL:12 / 10\r\n"
        "\tENDIF\r\n"
        "\t;上限5000万キャップと到達時の振れ幅（毎回同じ金額になるのを防止）\r\n"
        "\tIF P >= 50000000\r\n"
        "\t\t;キャップ到達時でも75%〜100%（3750万〜5000万円）の振れ幅＋リアルな端数\r\n"
        "\t\tP = 37500000 + RAND:12500000 + RAND:1000 * 1000 + RAND:1000\r\n"
        "\t\tP = LIMIT(P, 37500000, 50000000)\r\n"
        "\tENDIF"
    )

    count = content.count(old_cap)
    if count == 0:
        print("ERROR: old_cap not found in SHOP_ショップ.ERB")
        return False
    print(f"Found {count} occurrences of old_cap in SHOP_ショップ.ERB")

    content = content.replace(old_cap, new_cap)
    with open(filepath, 'wb') as f:
        f.write(content.encode('cp932'))
    print("SUCCESS: SHOP_ショップ.ERB updated.")
    return True

if __name__ == '__main__':
    ok1 = update_event_shoot()
    ok2 = update_shop_cap()
    if ok1 and ok2:
        print("ALL UPDATES COMPLETED SUCCESSFULLY.")
