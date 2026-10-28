def fix_info_localsize():
    filepath = 'ERB/INFO_情報表示.ERB'
    with open(filepath, 'rb') as f:
        content = f.read().decode('cp932')

    old_text = (
        "\t; 1回の最高射精量(CFLAG:1240)または平均20mLから射精回数を適正値に再計算\r\n"
        "\tLOCAL:98 = MAX(20, CFLAG:ARG:1240)\r\n"
        "\t; 体位別合計回数があればそれを優先\r\n"
        "\tLOCAL:99 = CFLAG:ARG:1250 + CFLAG:ARG:1251 + CFLAG:ARG:1252 + CFLAG:ARG:1253 + CFLAG:ARG:1254\r\n"
        "\tIF LOCAL:99 > 0 && LOCAL:99 <= CFLAG:ARG:1221\r\n"
        "\t\tCFLAG:ARG:1220 = LOCAL:99\r\n"
        "\tELSE\r\n"
        "\t\tCFLAG:ARG:1220 = LIMIT(CFLAG:ARG:1221 / LOCAL:98, 1, CFLAG:ARG:1221)\r\n"
        "\tENDIF"
    )

    new_text = (
        "\t; 1回の最高射精量(CFLAG:1240)または平均20mLから射精回数を適正値に再計算\r\n"
        "\tLOCAL:2 = MAX(20, CFLAG:ARG:1240)\r\n"
        "\t; 体位別合計回数があればそれを優先\r\n"
        "\tLOCAL:3 = CFLAG:ARG:1250 + CFLAG:ARG:1251 + CFLAG:ARG:1252 + CFLAG:ARG:1253 + CFLAG:ARG:1254\r\n"
        "\tIF LOCAL:3 > 0 && LOCAL:3 <= CFLAG:ARG:1221\r\n"
        "\t\tCFLAG:ARG:1220 = LOCAL:3\r\n"
        "\tELSE\r\n"
        "\t\tCFLAG:ARG:1220 = LIMIT(CFLAG:ARG:1221 / LOCAL:2, 1, CFLAG:ARG:1221)\r\n"
        "\tENDIF"
    )

    if old_text not in content:
        print("ERROR: old_text not found in INFO_情報表示.ERB")
        return False

    content = content.replace(old_text, new_text)
    with open(filepath, 'wb') as f:
        f.write(content.encode('cp932'))
    print("SUCCESS: INFO_情報表示.ERB updated.")
    return True

if __name__ == '__main__':
    fix_info_localsize()
