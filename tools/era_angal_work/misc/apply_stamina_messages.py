def apply_stamina_exhaustion_messages():
    # 1. Update CSV/Tflag.csv
    with open('CSV/Tflag.csv', 'rb') as f:
        tflag_csv = f.read().decode('cp932')
    
    if "993,コマンド開始時耐力" not in tflag_csv:
        tflag_append = (
            "\r\n993,コマンド開始時耐力,;各コマンド・パートナー行動開始時点での主人公耐力\r\n"
            "995,調教中空撃ち回数,;調教中に耐力0で射精できず空撃ち絶頂になった回数\r\n"
        )
        tflag_csv += tflag_append
        with open('CSV/Tflag.csv', 'wb') as f:
            f.write(tflag_csv.encode('cp932'))
        print("SUCCESS: CSV/Tflag.csv updated.")

    # 2. Update ERB/EVENT_TRAIN_調教イベント処理.ERB
    fpath = 'ERB/EVENT_TRAIN_調教イベント処理.ERB'
    with open(fpath, 'rb') as f:
        content = f.read().decode('cp932')
    target = (
        "TFLAG:999 = 0\r\n"
        "TFLAG:301 = 0\r\n"
        "TFLAG:898 = 0\r\n"
        "TFLAG:899 = 0\r\n"
        "TFLAG:51 = 0\r\n"
    )
    replacement = (
        "TFLAG:999 = 0\r\n"
        "TFLAG:301 = 0\r\n"
        "TFLAG:898 = 0\r\n"
        "TFLAG:899 = 0\r\n"
        "TFLAG:51 = 0\r\n"
        "TFLAG:995 = 0\r\n"
    )
    if target in content and "TFLAG:995 = 0" not in content:
        content = content.replace(target, replacement)
        with open(fpath, 'wb') as f:
            f.write(content.encode('cp932'))
        print(f"SUCCESS: {fpath} updated.")

    # 3. Update ERB/SYSTEM_基本システム処理.ERB
    fpath = 'ERB/SYSTEM_基本システム処理.ERB'
    with open(fpath, 'rb') as f:
        content = f.read().decode('cp932')
    target = (
        "REPEAT 30\r\n"
        "\tTFLAG:COUNT = 0\r\n"
        "REND\r\n"
        "TFLAG:100 = 0\r\n"
        "TFLAG:540 = 0\r\n"
    )
    replacement = (
        "REPEAT 30\r\n"
        "\tTFLAG:COUNT = 0\r\n"
        "REND\r\n"
        "TFLAG:100 = 0\r\n"
        "TFLAG:540 = 0\r\n"
        ";コマンド開始時の耐力を記録（今回出し切ったか判定用）\r\n"
        "TFLAG:993 = BASE:MASTER:4\r\n"
    )
    if target in content and "TFLAG:993 = BASE:MASTER:4" not in content:
        content = content.replace(target, replacement)
        with open(fpath, 'wb') as f:
            f.write(content.encode('cp932'))
        print(f"SUCCESS: {fpath} updated.")

    # 4. Update ERB/PARTNER_TURN_パートナーターン.ERB
    fpath = 'ERB/PARTNER_TURN_パートナーターン.ERB'
    with open(fpath, 'rb') as f:
        content = f.read().decode('cp932')
    target = (
        "DOWNBASE:MASTER:0 = 0\r\n"
        "DOWNBASE:MASTER:4 = 0\r\n"
    )
    replacement = (
        "DOWNBASE:MASTER:0 = 0\r\n"
        "DOWNBASE:MASTER:4 = 0\r\n"
        ";パートナーターン開始時の耐力を記録\r\n"
        "TFLAG:993 = BASE:MASTER:4\r\n"
    )
    if target in content and "TFLAG:993 = BASE:MASTER:4" not in content:
        content = content.replace(target, replacement)
        with open(fpath, 'wb') as f:
            f.write(content.encode('cp932'))
        print(f"SUCCESS: {fpath} updated.")

    # 5. Update ERB/EVENT_SHOOT_射精処理.ERB
    fpath = 'ERB/EVENT_SHOOT_射精処理.ERB'
    with open(fpath, 'rb') as f:
        content = f.read().decode('cp932')
    
    idx_start = content.find("SELECTCASE RAND(4)\r\n\tCASE 0\r\n\t\tPRINTFORML もう何も出せないのに")
    idx_end = content.find("ENDSELECT\r\n\tRETURN 0", idx_start) + len("ENDSELECT\r\n\tRETURN 0")

    if idx_start == -1:
        print("ERROR: shoot message slice not found in EVENT_SHOOT")
        return False

    new_branch = (
        ";今回のコマンド開始時にはまだ耐力があった（今回出し切った）か、調教中初めて出なくなった場合\r\n"
        "\tIF TFLAG:993 > 0 || TFLAG:995 == 0\r\n"
        "\t\tTFLAG:995 = 1\r\n"
        "\t\t;今回のコマンドで出し切ったときのメッセージ\r\n"
        "\t\tSELECTCASE RAND(4)\r\n"
        "\t\tCASE 0\r\n"
        "\t\t\tPRINTFORML 今回の絶頂で最後の一滴まで出し尽くし、%CALLNAME:(TFLAG:996)%の耐力は完全に底を突いた……\r\n"
        "\t\tCASE 1\r\n"
        "\t\t\tPRINTFORML 全てを搾り取られた%CALLNAME:(TFLAG:996)%は、激しい快感の余韻の中で力なく身体を脱力させた……\r\n"
        "\t\tCASE 2\r\n"
        "\t\t\tPRINTFORML %CALLNAME:LOCAL%の激しい責めに限界まで絞り出され、%CALLNAME:(TFLAG:996)%は出し切った快感に震えながら果てた……\r\n"
        "\t\tCASEELSE\r\n"
        "\t\t\tPRINTFORML これで完全に空っぽだ。%CALLNAME:(TFLAG:996)%は最後の一滴まで搾り取られ、熱いため息を漏らした……\r\n"
        "\t\tENDSELECT\r\n"
        "\tELSE\r\n"
        "\t\tTFLAG:995 += 1\r\n"
        "\t\t;既に出し切っててもう出せない状態でまた出す状況になったときのメッセージ\r\n"
        "\t\tSELECTCASE RAND(4)\r\n"
        "\t\tCASE 0\r\n"
        "\t\t\tPRINTFORML もう何も出せないはずなのに、%CALLNAME:LOCAL%の執拗な責めが%CALLNAME:(TFLAG:996)%の身体を何度も震わせる……\r\n"
        "\t\tCASE 1\r\n"
        "\t\t\tPRINTFORML とっくに空になったはずの奥をなお弄ばれ、%CALLNAME:(TFLAG:996)%は一滴も出ないまま声のない絶頂を繰り返した……\r\n"
        "\t\tCASE 2\r\n"
        "\t\t\tPRINTFORML %CALLNAME:LOCAL%は限界を超えても容赦なく快感を重ね、出ない%CALLNAME:(TFLAG:996)%から残り香まで搾り取っていく……\r\n"
        "\t\tCASEELSE\r\n"
        "\t\t\tPRINTFORML もうこれ以上は何も出ない。それなのに容赦なく続く刺激に、%CALLNAME:(TFLAG:996)%は力なく身悶えさせられている……\r\n"
        "\t\tENDSELECT\r\n"
        "\tENDIF\r\n"
        "\t;次回以降の空撃ち判定用にコマンド開始時耐力を0に更新\r\n"
        "\tTFLAG:993 = 0\r\n"
        "\tRETURN 0"
    )

    content = content[:idx_start] + new_branch + content[idx_end:]
    with open(fpath, 'wb') as f:
        f.write(content.encode('cp932'))
    print("SUCCESS: EVENT_SHOOT_射精処理.ERB updated.")
    return True

if __name__ == '__main__':
    apply_stamina_exhaustion_messages()
