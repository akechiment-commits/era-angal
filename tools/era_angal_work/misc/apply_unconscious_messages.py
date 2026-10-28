def apply_unconscious_stamina_messages():
    fpath = 'ERB/EVENT_SHOOT_射精処理.ERB'
    with open(fpath, 'rb') as f:
        content = f.read().decode('cp932')

    idx_start = content.find("LOCAL = T\r\n\tIF LOCAL == TFLAG:996 || LOCAL < 0")
    idx_end = content.find("TFLAG:993 = 0\r\n\tRETURN 0", idx_start) + len("TFLAG:993 = 0\r\n\tRETURN 0")

    if idx_start == -1 or idx_end == -1:
        print("ERROR: block not found in EVENT_SHOOT")
        return False

    new_block = (
        "LOCAL = T\r\n"
        "\tIF LOCAL == TFLAG:996 || LOCAL < 0\r\n"
        "\t\tIF ASSI > 0 && ASSI != TFLAG:996\r\n"
        "\t\t\tLOCAL = ASSI\r\n"
        "\t\tELSE\r\n"
        "\t\t\tLOCAL = PLAYER\r\n"
        "\t\tENDIF\r\n"
        "\tENDIF\r\n"
        "\t;相手の意識があるか判定（0=意識あり、1=気絶・意識なし）\r\n"
        "\tLOCAL:1 = 0\r\n"
        "\tSIF LOCAL >= 0 && LOCAL < CHARANUM && (TFLAG:899 || BASE:LOCAL:0 <= 0)\r\n"
        "\t\tLOCAL:1 = 1\r\n"
        "\r\n"
        "\t;今回のコマンド開始時にはまだ耐力があった（今回出し切った）か、調教中初めて出なくなった場合\r\n"
        "\tIF TFLAG:993 > 0 || TFLAG:995 == 0\r\n"
        "\t\tTFLAG:995 = 1\r\n"
        "\t\tIF LOCAL:1\r\n"
        "\t\t\t;相手の意識が無い場合のメッセージ（出し切った瞬間）\r\n"
        "\t\t\tSELECTCASE RAND(4)\r\n"
        "\t\t\tCASE 0\r\n"
        "\t\t\t\tPRINTFORML 意識を失いぐったりと横たわる%CALLNAME:LOCAL%の中で、%CALLNAME:(TFLAG:996)%は最後の一滴まで出し尽くし、完全に耐力を使い果たした……\r\n"
        "\t\t\tCASE 1\r\n"
        "\t\t\t\tPRINTFORML 気を失った%CALLNAME:LOCAL%の生ぬるい肉体に全てを搾り取られ、%CALLNAME:(TFLAG:996)%は力なくその上に倒れ込んだ……\r\n"
        "\t\t\tCASE 2\r\n"
        "\t\t\t\tPRINTFORML 眠るように静まり返った%CALLNAME:LOCAL%を相手に限界まで絞り出され、%CALLNAME:(TFLAG:996)%は出し切った快感に震えながら果てた……\r\n"
        "\t\t\tCASEELSE\r\n"
        "\t\t\t\tPRINTFORML これで完全に空っぽだ。反応のない%CALLNAME:LOCAL%の身体に最後の一滴まで吸い取られ、%CALLNAME:(TFLAG:996)%は虚脱感に沈んだ……\r\n"
        "\t\t\tENDSELECT\r\n"
        "\t\tELSE\r\n"
        "\t\t\t;相手の意識がある場合のメッセージ（出し切った瞬間）\r\n"
        "\t\t\tSELECTCASE RAND(4)\r\n"
        "\t\t\tCASE 0\r\n"
        "\t\t\t\tPRINTFORML 今回の絶頂で最後の一滴まで出し尽くし、%CALLNAME:(TFLAG:996)%の耐力は完全に底を突いた……\r\n"
        "\t\t\tCASE 1\r\n"
        "\t\t\t\tPRINTFORML 全てを搾り取られた%CALLNAME:(TFLAG:996)%は、激しい快感の余韻の中で力なく身体を脱力させた……\r\n"
        "\t\t\tCASE 2\r\n"
        "\t\t\t\tPRINTFORML %CALLNAME:LOCAL%の激しい責めに限界まで絞り出され、%CALLNAME:(TFLAG:996)%は出し切った快感に震えながら果てた……\r\n"
        "\t\t\tCASEELSE\r\n"
        "\t\t\t\tPRINTFORML これで完全に空っぽだ。%CALLNAME:(TFLAG:996)%は最後の一滴まで搾り取られ、熱いため息を漏らした……\r\n"
        "\t\t\tENDSELECT\r\n"
        "\t\tENDIF\r\n"
        "\tELSE\r\n"
        "\t\tTFLAG:995 += 1\r\n"
        "\t\tIF LOCAL:1\r\n"
        "\t\t\t;相手の意識が無い場合のメッセージ（既に出し切っている状態での空撃ち）\r\n"
        "\t\t\tSELECTCASE RAND(4)\r\n"
        "\t\t\tCASE 0\r\n"
        "\t\t\t\tPRINTFORML とっくに耐力は尽き果て、何も出せないはずなのに……意識のない%CALLNAME:LOCAL%の体温に刺激され、%CALLNAME:(TFLAG:996)%は空撃ちの絶頂に震えた……\r\n"
        "\t\t\tCASE 1\r\n"
        "\t\t\t\tPRINTFORML 気を失った%CALLNAME:LOCAL%の肉体が無意識に締め付け、空っぽの%CALLNAME:(TFLAG:996)%は一滴も出ないまま乾いたオーガズムを強いられた……\r\n"
        "\t\t\tCASE 2\r\n"
        "\t\t\t\tPRINTFORML もうこれ以上は何も出ない。ぐったりと動かない%CALLNAME:LOCAL%の上で、%CALLNAME:(TFLAG:996)%は声もなくただ身体を跳ねさせる……\r\n"
        "\t\t\tCASEELSE\r\n"
        "\t\t\t\tPRINTFORML 意識のない%CALLNAME:LOCAL%の温もりになお弄ばれ、出し尽くしたはずの身体は出ない快感に何度も引き攣っている……\r\n"
        "\t\t\tENDSELECT\r\n"
        "\t\tELSE\r\n"
        "\t\t\t;相手の意識がある場合のメッセージ（既に出し切っている状態での空撃ち）\r\n"
        "\t\t\tSELECTCASE RAND(4)\r\n"
        "\t\t\tCASE 0\r\n"
        "\t\t\t\tPRINTFORML もう何も出せないはずなのに、%CALLNAME:LOCAL%の執拗な責めが%CALLNAME:(TFLAG:996)%の身体を何度も震わせる……\r\n"
        "\t\t\tCASE 1\r\n"
        "\t\t\t\tPRINTFORML とっくに空になったはずの奥をなお弄ばれ、%CALLNAME:(TFLAG:996)%は一滴も出ないまま声のない絶頂を繰り返した……\r\n"
        "\t\t\tCASE 2\r\n"
        "\t\t\t\tPRINTFORML %CALLNAME:LOCAL%は限界を超えても容赦なく快感を重ね、出ない%CALLNAME:(TFLAG:996)%から残り香まで搾り取っていく……\r\n"
        "\t\t\tCASEELSE\r\n"
        "\t\t\t\tPRINTFORML もうこれ以上は何も出ない。それなのに容赦なく続く刺激に、%CALLNAME:(TFLAG:996)%は力なく身悶えさせられている……\r\n"
        "\t\t\tENDSELECT\r\n"
        "\t\tENDIF\r\n"
        "\tENDIF\r\n"
        "\t;次回以降の空撃ち判定用にコマンド開始時耐力を0に更新\r\n"
        "\tTFLAG:993 = 0\r\n"
        "\tRETURN 0"
    )

    content = content[:idx_start] + new_block + content[idx_end:]
    with open(fpath, 'wb') as f:
        f.write(content.encode('cp932'))
    print("SUCCESS: EVENT_SHOOT_射精処理.ERB updated.")
    return True

if __name__ == '__main__':
    apply_unconscious_stamina_messages()
