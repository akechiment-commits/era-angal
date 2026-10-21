# -*- coding: utf-8 -*-
"""
Apply Audit #13 comprehensive fixes across Kojo and System/COMF files:
1. Unquoted single-line PRINTFORMW dialogue lines across 8 CHAR_*_COM.ERB files (530 lines).
2. Duplicate / contradictory SELECTCOM blocks in CHAR_01_三善かなえ_COM.ERB and CHAR_27_夏野ゆり_COM.ERB.
3. Female-only / Assistant-partner COM viewpoint & partner gender fixes in CHAR_27, CHAR_66, CHAR_67.
4. COMF203.ERB (クスコされる) execution gate, actor reference, and @COM_ORDER_203 fixes.
5. ABL ladder variable index mismatches across 14 System/COMF files.
6. @COM_ORDER_* display mismatches across 5 COMF files (COMF68, 360, 361, 367, 370).

All ERB files are read and written strictly as cp932 with CRLF line endings.
"""

import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]


def read_erb(path: pathlib.Path) -> str:
    return path.read_bytes().decode("cp932")


def write_erb(path: pathlib.Path, text: str) -> bool:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", "\r\n")
    raw = normalized.encode("cp932")
    if path.read_bytes() == raw:
        return False
    path.write_bytes(raw)
    return True


def fix_category1_unquoted_printformw() -> tuple[int, int]:
    """Wrap unquoted single-line PRINTFORMW spoken dialogue lines in 「...」."""
    char_dir = ROOT / "ERB" / "CHAR"
    files_changed = 0
    lines_changed = 0

    for p in sorted(char_dir.glob("CHAR_*.ERB")):
        text = read_erb(p)
        lines = text.splitlines()
        new_lines = []
        in_train_msg = False
        changed_here = 0

        for line in lines:
            s = line.strip()
            if s.startswith("@"):
                in_train_msg = s.startswith("@TRAIN_MESSAGE")
            if not in_train_msg and s.startswith("PRINTFORMW "):
                m = re.match(r"^(\s*PRINTFORMW )(.+)$", line)
                if m:
                    prefix, content = m.group(1), m.group(2)
                    if (
                        not content.startswith("「")
                        and not content.endswith("」")
                        and not content.startswith("（")
                        and not content.endswith("）")
                        and not content.startswith("◆")
                        and not content.startswith("%CALLNAME:PLAYER%")
                        and not content.startswith("%CALLNAME:TARGET%")
                    ):
                        line = f"{prefix}「{content}」"
                        changed_here += 1
            new_lines.append(line)

        if changed_here > 0:
            if write_erb(p, "\r\n".join(new_lines) + "\r\n"):
                files_changed += 1
                lines_changed += changed_here

    return files_changed, lines_changed


def fix_category2_char01_and_char27() -> int:
    """Deduplicate COM280-284/410-414 in CHAR_01 and fix Tsuyuri blocks in CHAR_27."""
    changed = 0

    # 2A: CHAR_01_三善かなえ_COM.ERB - remove old duplicate non-RAND:3 COM280-284 & COM410-414 block
    p01 = ROOT / "ERB" / "CHAR" / "CHAR_01_三善かなえ_COM.ERB"
    t01 = read_erb(p01)
    old_dup_01 = re.compile(
        r";==============================================================\r\n"
        r"; 口上独自ウフフ（COM280-284）/ 口上独自純愛（COM410-414）\r\n"
        r";==============================================================\r\n"
        r";--- COM280-284 独自ウフフ ---\r\n"
        r";  ※ウフフ中の独自カスタムコマンド（各キャラ固有の性的シチュエーション）\r\n"
        r"IF SELECTCOM == 280\t; 【コマンド:\[口上独自ウフフ1\]】\r\n"
        r"\t;◆地の文（場面: 楽器庫の秘密）\r\n"
        r"\tIF TALENT:TARGET:153.*?"
        r"ELSEIF SELECTCOM == 414\t; 【コマンド:\[口上独自純愛5\]】\r\n"
        r".*?"
        r"\tENDIF\r\n"
        r"ENDIF\r\n\r\n",
        re.S,
    )
    t01_new, n01 = old_dup_01.subn("", t01, count=1)
    if n01 > 0 and write_erb(p01, t01_new):
        changed += 1

    # 2B: CHAR_27_夏野ゆり_COM.ERB - unify Tsuyuri section, merge duplicate RAND:3 blocks into RAND:6,
    # remove contradictory && ASSIPLAY == 0 inside Tsuyuri block, and allow assistant-partner COMs
    # when (NO:PLAYER == 25) || (ASSI > 0 && NO:ASSI == 25).
    p27 = ROOT / "ERB" / "CHAR" / "CHAR_27_夏野ゆり_COM.ERB"
    t27 = read_erb(p27)

    m_start = re.search(r";=== NATSUNO YURI TSUYURI ASSISTANT NON-EROTIC START ===", t27)
    m_end = re.search(r";=== NATSUNO YURI TSUYURI ALL COMMANDS END ===\r\n", t27)
    if m_start and m_end:
        tsuyuri_sec = t27[m_start.start() : m_end.end()]
        block_re = re.compile(
            r"(;--- COM\d+[^\r\n]*\r\n)?"
            r"    (?:IF|ELSEIF) SELECTCOM == (\d+)(?: && ASSIPLAY == 0)?([^\r\n]*)\r\n"
            r"        A = RAND:\d+\r\n"
            r"(.*?)"
            r"        ENDIF\r\n"
            r"        RETURN 0\r\n",
            re.S,
        )
        blocks_by_com: dict[int, list[tuple[str, str, list[str]]]] = {}
        com_order: list[int] = []
        for bm in block_re.finditer(tsuyuri_sec):
            hdr = bm.group(1) or f";--- COM{bm.group(2)} ---\r\n"
            com_no = int(bm.group(2))
            comment_tail = bm.group(3)
            comment_tail = comment_tail.replace(" / 調教者:[主人]", "")
            if comment_tail.strip() == "; 【調教者:[主人]】":
                comment_tail = "\t; 【コマンド:[縁側で寛ぐ]】"
            body = bm.group(4)
            prints = [
                pm.group(1)
                for pm in re.finditer(r"^\s*(PRINTFORMW .+)$", body, re.M)
            ]
            if com_no not in blocks_by_com:
                blocks_by_com[com_no] = []
                com_order.append(com_no)
            blocks_by_com[com_no].append((hdr, comment_tail, prints))

        assi_partner_coms = {56, 62, 65, 66, 68, 258}

        out_lines = [
            ";=== NATSUNO YURI TSUYURI ASSISTANT & TRAINER SPECIAL START ===",
            "; つゆりが調教者（NO:PLAYER == 25）または助手参加時の専用口上",
            "IF (NO:PLAYER == 25) || (ASSI > 0 && NO:ASSI == 25)",
        ]
        first_assi = True
        for com_no in sorted(c for c in com_order if c in assi_partner_coms):
            entries = blocks_by_com[com_no]
            hdr, comment_tail, _ = entries[0]
            all_prints: list[str] = []
            for _, _, pr in entries:
                for p_line in pr:
                    if p_line not in all_prints:
                        all_prints.append(p_line)
            out_lines.append(hdr.rstrip("\r\n"))
            kw = "IF" if first_assi else "ELSEIF"
            first_assi = False
            out_lines.append(f"    {kw} SELECTCOM == {com_no}{comment_tail}")
            out_lines.append(f"        A = RAND:{len(all_prints)}")
            for idx, p_line in enumerate(all_prints):
                if idx == 0:
                    out_lines.append("        IF A == 0")
                elif idx < len(all_prints) - 1:
                    out_lines.append(f"        ELSEIF A == {idx}")
                else:
                    out_lines.append("        ELSE")
                out_lines.append(f"            {p_line}")
            out_lines.append("        ENDIF")
            out_lines.append("        RETURN 0")
        out_lines.append("    ENDIF")
        out_lines.append("ENDIF")
        out_lines.append(";=== NATSUNO YURI TSUYURI ALL COMMANDS START ===")
        out_lines.append("IF NO:PLAYER == 25")

        first_trainer = True
        for com_no in sorted(c for c in com_order if c not in assi_partner_coms):
            entries = blocks_by_com[com_no]
            hdr, comment_tail, _ = entries[0]
            all_prints = []
            for _, _, pr in entries:
                for p_line in pr:
                    if p_line not in all_prints:
                        all_prints.append(p_line)
            out_lines.append(hdr.rstrip("\r\n"))
            kw = "IF" if first_trainer else "ELSEIF"
            first_trainer = False
            out_lines.append(f"    {kw} SELECTCOM == {com_no}{comment_tail}")
            out_lines.append(f"        A = RAND:{len(all_prints)}")
            for idx, p_line in enumerate(all_prints):
                if idx == 0:
                    out_lines.append("        IF A == 0")
                elif idx < len(all_prints) - 1:
                    out_lines.append(f"        ELSEIF A == {idx}")
                else:
                    out_lines.append("        ELSE")
                out_lines.append(f"            {p_line}")
            out_lines.append("        ENDIF")
            out_lines.append("        RETURN 0")
        out_lines.append("    ENDIF")
        out_lines.append("ENDIF")
        out_lines.append(";=== NATSUNO YURI TSUYURI ALL COMMANDS END ===")

        new_tsuyuri_sec = "\r\n".join(out_lines) + "\r\n"
        t27_new = t27[: m_start.start()] + new_tsuyuri_sec + t27[m_end.end() :]
        if write_erb(p27, t27_new):
            changed += 1

    return changed


def fix_category3_female_partner_kojo() -> int:
    """Fix female-only / assistant-partner COM viewpoint & partner gender issues in CHAR_27, 66, 67."""
    changed = 0

    # 3A: CHAR_27_夏野ゆり_COM.ERB COM60 (助手にキスさせる)
    p27 = ROOT / "ERB" / "CHAR" / "CHAR_27_夏野ゆり_COM.ERB"
    t27 = read_erb(p27)
    old_27_com60 = (
        ";--- COM60 助手にキスさせる ---\r\n"
        "IF SELECTCOM == 60\t; 【コマンド:[助手にキスさせる]】\r\n"
        "\tA = RAND:3\r\n"
        "\tIF TALENT:TARGET:85\t; 【TARGET:[恋慕]】\r\n"
        "\t\tIF A == 0\r\n"
        "\t\t\tPRINTFORMW 「……ちゅ。……これは、つゆりちゃんには内緒。……もう一度くらいなら」\r\n"
        "\t\tELSEIF A == 1\r\n"
        "\t\t\tPRINTFORMW 「……嫌とは言ってない。……その顔、少しだけなら許す」\r\n"
        "\t\tELSE\r\n"
        "\t\t\tPRINTFORMW 「……転校生、近い。男は嫌いなのに、離れるのも惜しい」\r\n"
        "\t\tENDIF\r\n"
        "\tELSE\r\n"
        "\t\tIF A == 0\r\n"
        "\t\t\tPRINTFORMW 「……ちょっと。何をしてる。離れろ」\r\n"
        "\t\tELSEIF A == 1\r\n"
        "\t\t\tPRINTFORMW 「……今のは忘れろ。忘れたと言え、転校生」\r\n"
        "\t\tELSE\r\n"
        "\t\t\tPRINTFORMW 「……急に触るな。わたしは、まだあんたを許してない」\r\n"
        "\t\tENDIF\r\n"
        "\tENDIF\r\n"
        "ENDIF"
    )
    new_27_com60 = (
        ";--- COM60 助手にキスさせる ---\r\n"
        "IF SELECTCOM == 60\t; 【コマンド:[助手にキスさせる]】\r\n"
        "\tCALL AITE_YOBI, 27, ASSI\r\n"
        "\tLOCALS '= @\"%RESULTS%\"\r\n"
        "\tA = RAND:3\r\n"
        "\tIF TALENT:TARGET:85\t; 【TARGET:[恋慕]】\r\n"
        "\t\tIF A == 0\r\n"
        "\t\t\tPRINTFORMW 「……ちゅ。……これは、つゆりちゃんには内緒。……もう一度くらいなら」\r\n"
        "\t\tELSEIF A == 1\r\n"
        "\t\t\tPRINTFORMW 「……%LOCALS%、近い。嫌とは言ってないから、少しだけなら許す」\r\n"
        "\t\tELSE\r\n"
        "\t\t\tPRINTFORMW 「……んっ。女の子同士だから平気と思ったのに、息が乱れる……」\r\n"
        "\t\tENDIF\r\n"
        "\tELSE\r\n"
        "\t\tIF A == 0\r\n"
        "\t\t\tPRINTFORMW 「……ちょっと、%LOCALS%。何をしてる。離れて」\r\n"
        "\t\tELSEIF A == 1\r\n"
        "\t\t\tPRINTFORMW 「……今のは忘れて。命令でも、唇は安くない」\r\n"
        "\t\tELSE\r\n"
        "\t\t\tPRINTFORMW 「……急に触らないで。わたしは、まだ許してない」\r\n"
        "\t\tENDIF\r\n"
        "\tENDIF\r\n"
        "ENDIF"
    )
    if old_27_com60 in t27:
        t27 = t27.replace(old_27_com60, new_27_com60, 1)
        if write_erb(p27, t27):
            changed += 1

    # 3B: CHAR_66_曽根セイラ_COM.ERB COM61 (クンニ強制) & COM63 (貝あわせ)
    p66 = ROOT / "ERB" / "CHAR" / "CHAR_66_曽根セイラ_COM.ERB"
    t66 = read_erb(p66)
    old_66_com61 = (
        "IF SELECTCOM == 61\t; 【コマンド:[クンニ強制]】\r\n"
        "\tIF TALENT:TARGET:153\t; 【TARGET:[恋人]】\r\n"
        "\t\t;恋人\r\n"
        "\t\tA = RAND:3\r\n"
        "\t\tIF A == 0\r\n"
        "\t\tPRINTFORMW 「ちゅっ……ん、ふふ、舌を重ねると、音まで近くなるけれど♪」\r\n"
        "\t\tELSEIF A == 1\r\n"
        "\t\tPRINTFORMW 「んん、れろ……転校生くんの味、もう少し知りたいかなって☆」\r\n"
        "\t\tELSE\r\n"
        "\t\tPRINTFORMW 「ふぁ……唇を離すと寒いわね。もう一度、今度はゆっくりして？」\r\n"
        "\t\tENDIF\r\n"
        "\tELSE\r\n"
        "\t\t;通常\r\n"
        "\t\tA = RAND:3\r\n"
        "\t\tIF A == 0\r\n"
        "\t\tPRINTFORMW 「ひゃ、れろ……お、女の子の味って、こんなのなのね……っ」\r\n"
        "\t\tELSEIF A == 1\r\n"
        "\t\tPRINTFORMW 「んっ、ちゅ……夢中になってしまうけれど、あたし、変じゃないかしら」\r\n"
        "\t\tELSE\r\n"
        "\t\tPRINTFORMW 「ふぁ……顔が近いまま止まらないのね。知らないふりをするには、気持ちよすぎるわ」\r\n"
        "\t\tENDIF\r\n"
        "\tENDIF\r\n"
        "ENDIF"
    )
    new_66_com61 = (
        "IF SELECTCOM == 61\t; 【コマンド:[クンニ強制]】\r\n"
        "\tCALL AITE_YOBI, 66, ASSI\r\n"
        "\tLOCALS '= @\"%RESULTS%\"\r\n"
        "\tIF TALENT:TARGET:153\t; 【TARGET:[恋人]】\r\n"
        "\t\t;恋人\r\n"
        "\t\tA = RAND:3\r\n"
        "\t\tIF A == 0\r\n"
        "\t\tPRINTFORMW 「ちゅっ……ん、ふふ、舌で撫でるたび、%LOCALS%の可愛い声が近くなるけれど♪」\r\n"
        "\t\tELSEIF A == 1\r\n"
        "\t\tPRINTFORMW 「んん、れろ……%LOCALS%のここ、すっかり甘くて熱くなっているわね☆」\r\n"
        "\t\tELSE\r\n"
        "\t\tPRINTFORMW 「ふぁ……震えているのが舌に伝わるわ。もう一度、ゆっくり舐めてあげる♪」\r\n"
        "\t\tENDIF\r\n"
        "\tELSE\r\n"
        "\t\t;通常\r\n"
        "\t\tA = RAND:3\r\n"
        "\t\tIF A == 0\r\n"
        "\t\tPRINTFORMW 「ひゃ、れろ……お、女の子の味って、こんなのなのね……っ」\r\n"
        "\t\tELSEIF A == 1\r\n"
        "\t\tPRINTFORMW 「んっ、ちゅ……夢中になってしまうけれど、あたし、変じゃないかしら」\r\n"
        "\t\tELSE\r\n"
        "\t\tPRINTFORMW 「ふぁ……%LOCALS%の息が乱れていくわね。舌を動かすたび、こっちまで熱くなるわ」\r\n"
        "\t\tENDIF\r\n"
        "\tENDIF\r\n"
        "ENDIF"
    )
    old_66_com63 = (
        "IF SELECTCOM == 63\t; 【コマンド:[貝あわせ]】\r\n"
        "\tIF TALENT:TARGET:153\t; 【TARGET:[恋人]】\r\n"
        "\t\t;恋人\r\n"
        "\t\tA = RAND:3\r\n"
        "\t\tIF A == 0\r\n"
        "\t\tPRINTFORMW 「んっ、擦れるたびに、転校生くんの息が変わるけれど～♪」"
    )
    new_66_com63 = (
        "IF SELECTCOM == 63\t; 【コマンド:[貝あわせ]】\r\n"
        "\tCALL AITE_YOBI, 66, ASSI\r\n"
        "\tLOCALS '= @\"%RESULTS%\"\r\n"
        "\tIF TALENT:TARGET:153\t; 【TARGET:[恋人]】\r\n"
        "\t\t;恋人\r\n"
        "\t\tA = RAND:3\r\n"
        "\t\tIF A == 0\r\n"
        "\t\tPRINTFORMW 「んっ、擦れるたびに、%LOCALS%の息が変わるけれど～♪」"
    )
    t66_new = t66.replace(old_66_com61, new_66_com61, 1).replace(old_66_com63, new_66_com63, 1)
    if t66_new != t66 and write_erb(p66, t66_new):
        changed += 1

    # 3C: CHAR_67_日滝ましろ_COM.ERB COM61 (クンニ強制)
    p67 = ROOT / "ERB" / "CHAR" / "CHAR_67_日滝ましろ_COM.ERB"
    t67 = read_erb(p67)
    old_67_com61 = (
        "IF SELECTCOM == 61\t; 【コマンド:[クンニ強制]】\r\n"
        "\tIF TALENT:TARGET:153\t; 【TARGET:[恋人]】\r\n"
        "\t\t;恋人\r\n"
        "\t\tA = RAND:3\r\n"
        "\t\tIF A == 0\r\n"
        "\t\t\tPRINTFORMW 「れろ、ちゅっ☆　ふふ、もうこんなにトロトロだぞ♪　ぴちゃ、ん……私の舌で、もっと感じさせてやるっ☆　れろれろ♪」\r\n"
        "\t\tELSEIF A == 1\r\n"
        "\t\t\tPRINTFORMW 「ちゅっ……舌を重ねると、声より先に気持ちが伝わるな。もう一度、ゆっくりだ♪」\r\n"
        "\t\tELSE\r\n"
        "\t\t\tPRINTFORMW 「んっ、唇を離すと寒い。恋人くん、私の元気を口から分けてやろうか☆」\r\n"
        "\t\tENDIF\r\n"
        "\tELSE\r\n"
        "\t\t;通常\r\n"
        "\t\tA = RAND:3\r\n"
        "\t\tIF A == 0\r\n"
        "\t\t\tPRINTFORMW 「ん、れろ……ほう、女の子のここはこんな味か☆　ちゅ、ぷ……む、不慣れだが……これは悪くないぞ……れろっ」\r\n"
        "\t\tELSEIF A == 1\r\n"
        "\t\t\tPRINTFORMW 「わっ、舌まで！？　うう、夢中になると息を忘れるぞ……でも、離れるな！」\r\n"
        "\t\tELSE\r\n"
        "\t\t\tPRINTFORMW 「んっ、近すぎて何を言えばいいか分からないな。キスだけで、こんなに熱くなるのか……」\r\n"
        "\t\tENDIF\r\n"
        "\tENDIF\r\n"
        "ENDIF"
    )
    new_67_com61 = (
        "IF SELECTCOM == 61\t; 【コマンド:[クンニ強制]】\r\n"
        "\tCALL AITE_YOBI, 67, ASSI\r\n"
        "\tLOCALS '= @\"%RESULTS%\"\r\n"
        "\tIF TALENT:TARGET:153\t; 【TARGET:[恋人]】\r\n"
        "\t\t;恋人\r\n"
        "\t\tA = RAND:3\r\n"
        "\t\tIF A == 0\r\n"
        "\t\t\tPRINTFORMW 「れろ、ちゅっ☆　ふふ、もうこんなにトロトロだぞ♪　ぴちゃ、ん……私の舌で、もっと感じさせてやるっ☆　れろれろ♪」\r\n"
        "\t\tELSEIF A == 1\r\n"
        "\t\t\tPRINTFORMW 「ちゅっ……舌で撫でると、%LOCALS%の震えがすぐ伝わるな。もう一度、ゆっくり舐めるぞ♪」\r\n"
        "\t\tELSE\r\n"
        "\t\t\tPRINTFORMW 「んっ、れろ……%LOCALS%が気持ちよさそうだと、団長まで嬉しくなるぞ。恋人くんもちゃんと見ていてくれ☆」\r\n"
        "\t\tENDIF\r\n"
        "\tELSE\r\n"
        "\t\t;通常\r\n"
        "\t\tA = RAND:3\r\n"
        "\t\tIF A == 0\r\n"
        "\t\t\tPRINTFORMW 「ん、れろ……ほう、女の子のここはこんな味か☆　ちゅ、ぷ……む、不慣れだが……これは悪くないぞ……れろっ」\r\n"
        "\t\tELSEIF A == 1\r\n"
        "\t\t\tPRINTFORMW 「んっ、ちゅ……夢中で舐めていると息を忘れるぞ……%LOCALS%、苦しかったら言えよ！」\r\n"
        "\t\tELSE\r\n"
        "\t\t\tPRINTFORMW 「れろ……っ、近すぎてどこを見ればいいか分からないな。奉仕してるだけなのに、私まで熱くなるぞ……」\r\n"
        "\t\tENDIF\r\n"
        "\tENDIF\r\n"
        "ENDIF"
    )
    if old_67_com61 in t67:
        t67 = t67.replace(old_67_com61, new_67_com61, 1)
        if write_erb(p67, t67):
            changed += 1

    return changed


def fix_category4_comf203() -> int:
    """Fix COMF203.ERB (クスコされる) execution gate, actor references, and @COM_ORDER_203."""
    p = ROOT / "ERB" / "COMF" / "COMF203.ERB"
    text = read_erb(p)
    orig = text

    # 4A: @COM_ABLE203 - check PLAYER instead of MASTER for male/virgin
    text = text.replace(
        ";マスターがオトコだとダメ\r\n"
        "SIF TALENT:MASTER:122\t; 【MASTER:[オトコ]】\r\n"
        "\tRETURN 0\r\n"
        ";アイテムを持っているか、アイテムなし設定でないとダメ\r\n"
        "SIF ITEM:40 == 0 && NOITEM == 0\t; 【アイテム:[クスコ]==0】\r\n"
        "\tRETURN 0\r\n"
        ";マスターが処女だとダメ\r\n"
        "SIF TALENT:MASTER:0 == 1\t; 【MASTER:[処女]】\r\n"
        "\tRETURN 0",
        ";調教者がオトコだとダメ\r\n"
        "SIF TALENT:PLAYER:122\t; 【PLAYER:[オトコ]】\r\n"
        "\tRETURN 0\r\n"
        ";アイテムを持っているか、アイテムなし設定でないとダメ\r\n"
        "SIF ITEM:40 == 0 && NOITEM == 0\t; 【アイテム:[クスコ]==0】\r\n"
        "\tRETURN 0\r\n"
        ";調教者が処女だとダメ\r\n"
        "SIF TALENT:PLAYER:0 == 1\t; 【PLAYER:[処女]】\r\n"
        "\tRETURN 0",
        1,
    )

    # 4B: @COM203 - TEQUIP:PLAYER:86, ABL:1 in SOURCE:11, EXP:PLAYER:40
    text = text.replace(
        "SIF TEQUIP:MASTER:86\t; 【[排卵誘発剤効果発揮中]使用中】\r\n\tSOURCE:11 += 500",
        "SIF TEQUIP:PLAYER:86\t; 【[排卵誘発剤効果発揮中]使用中】\r\n\tSOURCE:11 += 500",
        1,
    )
    text = text.replace(
        "\t;ここは放尿から\r\n\tSOURCE:11 += SOURCE:11 + (ABL:11 * 350)",
        "\t;ここは放尿から\r\n\tSOURCE:11 += SOURCE:11 + (ABL:1 * 350)",
        1,
    )
    text = text.replace(
        ";女同士ならレズ経験が増える\r\n"
        "IF TALENT:122 == 0 && TALENT:PLAYER:122 == 0\t; 【[オトコ]なし / PLAYER:[オトコ]なし】\r\n"
        "\tPRINTFORML %EXPNAME:40%＋4\r\n"
        "\tEXP:40 += 4\r\n"
        "ENDIF",
        ";女同士ならレズ経験が増える\r\n"
        "IF TALENT:122 == 0 && TALENT:PLAYER:122 == 0\t; 【[オトコ]なし / PLAYER:[オトコ]なし】\r\n"
        "\tPRINTFORML %EXPNAME:40%＋4\r\n"
        "\tEXP:40 += 4\r\n"
        "\tEXP:PLAYER:40 += 4\r\n"
        "ENDIF",
        1,
    )

    # 4C: @TRAIN_MESSAGE_COM203 - PLAYER instead of MASTER/TARGET for the opened vagina owner, TFLAG:37
    old_train_203 = (
        "@TRAIN_MESSAGE_COM203\r\n"
        ";クスコの着脱どうしよう\r\n"
        "SIF TEQUIP:53\t; 【[撮影中]使用中】\r\n"
        "\tPRINT ビデオカメラの前で\r\n"
        "SIF TEQUIP:57\t; 【[羞恥（大鏡）プレイ中]使用中】\r\n"
        "\tPRINT 鏡に映りこむように、\r\n"
        "IF TFLAG:45\t; 【[主導権]】\r\n"
        "\tPRINTFORM %CALLNAME:TARGET%は%CALLNAME:MASTER%に\r\n"
        "ELSE\r\n"
        "\tPRINTFORM %CALLNAME:MASTER%は%CALLNAME:TARGET%に\r\n"
        "ENDIF\r\n"
        ";暫定的にムードを使用\r\n"
        "IF TFLAG:37 > 30\t; 【[ムード]>30】\r\n"
        "\tPRINT 淫らにヒクつく膣\r\n"
        "ELSEIF TFLAG:50 > 10\t; 【[調教者切替]>10】\r\n"
        "\tPRINT 濡れそぼった膣\r\n"
        "ELSEIF (TALENT:100 || TALENT:149) && TALENT:109\t; 【[小柄体型] / [子供体型] / [貧乳]】\r\n"
        "\tPRINT 幼いワレメ\r\n"
        "ELSEIF TALENT:149\t; 【[子供体型]】\r\n"
        "\tPRINT いたいけな膣\r\n"
        "ELSEIF TALENT:100\t; 【[小柄体型]】\r\n"
        "\tPRINT 小さな膣\r\n"
        "ELSE\r\n"
        "\tPRINT 陰唇\r\n"
        "ENDIF\r\n"
        "PRINT の奥まで膣鏡を挿入\r\n"
        "IF TFLAG:45\t; 【[主導権]】\r\n"
        "\tPRINT し、割り開いた\r\n"
        "ELSE\r\n"
        "\tPRINT させ、割り開いた\r\n"
        "ENDIF\r\n"
        "PRINTL 　\r\n"
        ";クスコで開かれた中を観察。小柄以下は幼く狭い内部を強調\r\n"
        "IF TALENT:149\t; 【[子供体型]】\r\n"
        "\tSELECTCASE RAND:3\r\n"
        "\tCASE 0\r\n"
        "\t\tPRINTFORML 膣鏡に押し広げられた幼い内部は、まだ誰の形にも馴染んでいない狭い隘路がぴたりと閉じ合わさり、淡い桜色の襞が奥でほつほつと震えている\r\n"
        "\tCASE 1\r\n"
        "\t\tPRINTFORML 限界まで開かれてもなお慎ましいその中は、子供のように小さな子宮口がひっそりと顔を覗かせ、無垢な粘膜が露わにされた羞恥にきゅうと収縮した\r\n"
        "\tCASEELSE\r\n"
        "\t\tPRINTFORML 大人のものとは比べものにならないほど狭く浅い膣道が余すところなく晒され、未熟な薄桃色の襞が、覗き込む視線に怯えるように小刻みにひくついている\r\n"
        "\tENDSELECT\r\n"
        "ELSEIF TALENT:100\t; 【[小柄体型]】\r\n"
        "\tSELECTCASE RAND:3\r\n"
        "\tCASE 0\r\n"
        "\t\tPRINTFORML 膣鏡に押し広げられた小ぶりな内部は、狭い膣道がきゅっと締まり、桜色の襞が奥で控えめに震えている\r\n"
        "\tCASE 1\r\n"
        "\t\tPRINTFORML 小柄な身体に見合った浅い膣道の奥で、小さな子宮口がつつましく顔を覗かせ、晒された羞恥に収縮した\r\n"
        "\tCASEELSE\r\n"
        "\t\tPRINTFORML こぢんまりとした膣内が隅々まで露わにされ、薄紅の襞が視線を浴びてひくりと縮こまった\r\n"
        "\tENDSELECT\r\n"
        "ENDIF\r\n"
        "PRINTFORM %CALLNAME:TARGET%は\r\n"
        "IF CFLAG:PLAYER:103 > 0\t; 【PLAYER:[奴隷中出し]>0】\r\n"
        "\tSIF CFLAG:PLAYER:103 >= 10\t; 【PLAYER:[奴隷中出し]>=10】\r\n"
        "\t\tPRINT たっぷりと\r\n"
        "\tPRINT 子種\r\n"
        "\tIF RAND:2\r\n"
        "\t\tPRINT で満たされている様を\r\n"
        "\tELSE\r\n"
        "\t\tPRINT が溜まっている様を\r\n"
        "\tENDIF\r\n"
        ";暫定的にムード値or排卵誘発剤\r\n"
        "ELSEIF TFLAG:37 > 30 || TEQUIP:MASTER:86\t; 【[排卵誘発剤効果発揮中]使用中 / [ムード]>30】\r\n"
        "\tIF TEQUIP:MASTER:86\t; 【[排卵誘発剤効果発揮中]使用中】\r\n"
        "\t\tPRINT 広げられた秘肉から大量の白濁した愛液が流れている様を\r\n"
        "\tELSEIF TALENT:37 > 30\t; 【[弱味]>30】\r\n"
        "\t\tPRINT 子宮口が降りてきている様を\r\n"
        "\tELSE\r\n"
        "\t\tPRINT ぷっくりと膨れたＧスポットの様子を\r\n"
        "\tENDIF\r\n"
        "ELSE\r\n"
        "\tIF RAND:2\r\n"
        "\t\tPRINT 膣壁が妖しく蠢いている様を\r\n"
        "\tELSE\r\n"
        "\t\tPRINT 洪水のように愛液を垂れ流している様を\r\n"
        "\tENDIF\r\n"
        "ENDIF\r\n"
        "PRINT 口に出して\r\n"
        ";さどっけが高い\r\n"
        "IF ABL:15 >= 5\t; 【[サドっ気]Lv>=5】\r\n"
        "\tPRINT 冷やかし\r\n"
        "ELSE\r\n"
        "\tPRINTFORM %CALLNAME:MASTER%に伝え\r\n"
        "ENDIF\r\n"
        ";倒錯的\r\n"
        "IF TALENT:80\t; 【[倒錯的]】\r\n"
        "\tPRINT 、その中\r\n"
        "\t;サドで女でふたなりでない\r\n"
        "\tIF TALENT:83 && TALENT:MASTER:122 == 0 && TALENT:121 == 0\t; 【[サド] / MASTER:[オトコ]なし / [ふたなり]なし】\r\n"
        "\t\tPRINT に自らの唾液を垂らし\r\n"
        "\t;サドで男かふたなり\r\n"
        "\t;ELSEIF TALENT:83 && (TALENT:121 || TALENT:122)\r\n"
        "\t;\tPRINT へ向けて自分の精を放っ\r\n"
        "\t;サドのみ\r\n"
        "\tELSE\r\n"
        "\t\tPRINT を指でつつい\r\n"
        "\tENDIF\r\n"
        "\tPRINT てかき混ぜ\r\n"
        "ENDIF\r\n"
        "PRINT ている\r\n"
        "\r\n"
        "IF TALENT:88\t; 【[親愛]】\r\n"
        "\tPRINTFORM %CALLNAME:MASTER%は愛する人\r\n"
        "\tIF TALENT:80 && TALENT:MASTER:122 == 0 && TALENT:121 == 0\t; 【[倒錯的] / MASTER:[オトコ]なし / [ふたなり]なし】\r\n"
        "\t\tPRINT に体の奥まで\r\n"
        "\t\tIF ABL:15 >= 5\t; 【[サドっ気]Lv>=5】\r\n"
        "\t\t\tPRINT 犯される\r\n"
        "\t\tELSE\r\n"
        "\t\t\tPRINT 見せつける\r\n"
        "\t\tENDIF\r\n"
        "\t\tPRINT 快楽に溺れ\r\n"
        "\t\tSIF TALENT:72\t; 【[中毒しやすい]】\r\n"
        "\t\t\tPRINTFORM 、涎を垂らし\r\n"
        "\t\tSIF TALENT:70 || TALENT:80 || TALENT:79\t; 【[快感に素直] / [倒錯的] / [マゾ]】\r\n"
        "\t\t\tPRINT ながら自ら腰を突き上げ\r\n"
        "\t\tPRINTL ている…\r\n"
        "\tELSEIF TEQUIP:MASTER:86\t; 【[排卵誘発剤効果発揮中]使用中】\r\n"
        "\t\tPRINTFORML の見ている前で、%CALLNAME:MASTER%は白濁した蜜をとろとろと床へこぼした…\r\n"
        "\tELSE\r\n"
        "\t\tPRINTL に割り開かれた場所を見られ、興奮のあまり涎と涙と愛液を溢れさせている…\r\n"
        "\tENDIF\r\n"
        "ELSEIF TALENT:85 && TALENT:153\t; 【[恋慕] / [恋人]】\r\n"
        "\tPRINTFORML %CALLNAME:MASTER%は秘洞の奥まで見られていることに倒錯的な興奮を覚えている…\r\n"
        "ENDIF"
    )
    new_train_203 = (
        "@TRAIN_MESSAGE_COM203\r\n"
        ";クスコの着脱どうしよう\r\n"
        "SIF TEQUIP:53\t; 【[撮影中]使用中】\r\n"
        "\tPRINT ビデオカメラの前で\r\n"
        "SIF TEQUIP:57\t; 【[羞恥（大鏡）プレイ中]使用中】\r\n"
        "\tPRINT 鏡に映りこむように、\r\n"
        "IF TFLAG:45\t; 【[主導権]】\r\n"
        "\tPRINTFORM %CALLNAME:TARGET%は%CALLNAME:PLAYER%に\r\n"
        "ELSE\r\n"
        "\tPRINTFORM %CALLNAME:PLAYER%は%CALLNAME:TARGET%に\r\n"
        "ENDIF\r\n"
        ";暫定的にムードを使用\r\n"
        "IF TFLAG:37 > 30\t; 【[ムード]>30】\r\n"
        "\tPRINT 淫らにヒクつく膣\r\n"
        "ELSEIF TFLAG:50 > 10\t; 【[調教者切替]>10】\r\n"
        "\tPRINT 濡れそぼった膣\r\n"
        "ELSEIF (TALENT:PLAYER:100 || TALENT:PLAYER:149) && TALENT:PLAYER:109\t; 【PLAYER:[小柄体型] / PLAYER:[子供体型] / PLAYER:[貧乳]】\r\n"
        "\tPRINT 幼いワレメ\r\n"
        "ELSEIF TALENT:PLAYER:149\t; 【PLAYER:[子供体型]】\r\n"
        "\tPRINT いたいけな膣\r\n"
        "ELSEIF TALENT:PLAYER:100\t; 【PLAYER:[小柄体型]】\r\n"
        "\tPRINT 小さな膣\r\n"
        "ELSE\r\n"
        "\tPRINT 陰唇\r\n"
        "ENDIF\r\n"
        "PRINT の奥まで膣鏡を挿入\r\n"
        "IF TFLAG:45\t; 【[主導権]】\r\n"
        "\tPRINT し、割り開いた\r\n"
        "ELSE\r\n"
        "\tPRINT させ、割り開いた\r\n"
        "ENDIF\r\n"
        "PRINTL 　\r\n"
        ";クスコで開かれた中を観察。小柄以下は幼く狭い内部を強調\r\n"
        "IF TALENT:PLAYER:149\t; 【PLAYER:[子供体型]】\r\n"
        "\tSELECTCASE RAND:3\r\n"
        "\tCASE 0\r\n"
        "\t\tPRINTFORML 膣鏡に押し広げられた幼い内部は、まだ誰の形にも馴染んでいない狭い隘路がぴたりと閉じ合わさり、淡い桜色の襞が奥でほつほつと震えている\r\n"
        "\tCASE 1\r\n"
        "\t\tPRINTFORML 限界まで開かれてもなお慎ましいその中は、子供のように小さな子宮口がひっそりと顔を覗かせ、無垢な粘膜が露わにされた羞恥にきゅうと収縮した\r\n"
        "\tCASEELSE\r\n"
        "\t\tPRINTFORML 大人のものとは比べものにならないほど狭く浅い膣道が余すところなく晒され、未熟な薄桃色の襞が、覗き込む視線に怯えるように小刻みにひくついている\r\n"
        "\tENDSELECT\r\n"
        "ELSEIF TALENT:PLAYER:100\t; 【PLAYER:[小柄体型]】\r\n"
        "\tSELECTCASE RAND:3\r\n"
        "\tCASE 0\r\n"
        "\t\tPRINTFORML 膣鏡に押し広げられた小ぶりな内部は、狭い膣道がきゅっと締まり、桜色の襞が奥で控えめに震えている\r\n"
        "\tCASE 1\r\n"
        "\t\tPRINTFORML 小柄な身体に見合った浅い膣道の奥で、小さな子宮口がつつましく顔を覗かせ、晒された羞恥に収縮した\r\n"
        "\tCASEELSE\r\n"
        "\t\tPRINTFORML こぢんまりとした膣内が隅々まで露わにされ、薄紅の襞が視線を浴びてひくりと縮こまった\r\n"
        "\tENDSELECT\r\n"
        "ENDIF\r\n"
        "PRINTFORM %CALLNAME:TARGET%は\r\n"
        "IF CFLAG:PLAYER:103 > 0\t; 【PLAYER:[奴隷中出し]>0】\r\n"
        "\tSIF CFLAG:PLAYER:103 >= 10\t; 【PLAYER:[奴隷中出し]>=10】\r\n"
        "\t\tPRINT たっぷりと\r\n"
        "\tPRINT 子種\r\n"
        "\tIF RAND:2\r\n"
        "\t\tPRINT で満たされている様を\r\n"
        "\tELSE\r\n"
        "\t\tPRINT が溜まっている様を\r\n"
        "\tENDIF\r\n"
        ";暫定的にムード値or排卵誘発剤\r\n"
        "ELSEIF TFLAG:37 > 30 || TEQUIP:PLAYER:86\t; 【[排卵誘発剤効果発揮中]使用中 / [ムード]>30】\r\n"
        "\tIF TEQUIP:PLAYER:86\t; 【[排卵誘発剤効果発揮中]使用中】\r\n"
        "\t\tPRINT 広げられた秘肉から大量の白濁した愛液が流れている様を\r\n"
        "\tELSEIF TFLAG:37 > 30\t; 【[ムード]>30】\r\n"
        "\t\tPRINT 子宮口が降りてきている様を\r\n"
        "\tELSE\r\n"
        "\t\tPRINT ぷっくりと膨れたＧスポットの様子を\r\n"
        "\tENDIF\r\n"
        "ELSE\r\n"
        "\tIF RAND:2\r\n"
        "\t\tPRINT 膣壁が妖しく蠢いている様を\r\n"
        "\tELSE\r\n"
        "\t\tPRINT 洪水のように愛液を垂れ流している様を\r\n"
        "\tENDIF\r\n"
        "ENDIF\r\n"
        "PRINT 口に出して\r\n"
        ";さどっけが高い\r\n"
        "IF ABL:15 >= 5\t; 【[サドっ気]Lv>=5】\r\n"
        "\tPRINT 冷やかし\r\n"
        "ELSE\r\n"
        "\tPRINTFORM %CALLNAME:PLAYER%に伝え\r\n"
        "ENDIF\r\n"
        ";倒錯的\r\n"
        "IF TALENT:80\t; 【[倒錯的]】\r\n"
        "\tPRINT 、その中\r\n"
        "\t;サドで女でふたなりでない\r\n"
        "\tIF TALENT:83 && TALENT:PLAYER:122 == 0 && TALENT:121 == 0\t; 【[サド] / PLAYER:[オトコ]なし / [ふたなり]なし】\r\n"
        "\t\tPRINT に自らの唾液を垂らし\r\n"
        "\t;サドで男かふたなり\r\n"
        "\t;ELSEIF TALENT:83 && (TALENT:121 || TALENT:122)\r\n"
        "\t;\tPRINT へ向けて自分の精を放っ\r\n"
        "\t;サドのみ\r\n"
        "\tELSE\r\n"
        "\t\tPRINT を指でつつい\r\n"
        "\tENDIF\r\n"
        "\tPRINT てかき混ぜ\r\n"
        "ENDIF\r\n"
        "PRINT ている\r\n"
        "\r\n"
        "IF TALENT:88\t; 【[親愛]】\r\n"
        "\tPRINTFORM %CALLNAME:PLAYER%は愛する人\r\n"
        "\tIF TALENT:80 && TALENT:PLAYER:122 == 0 && TALENT:121 == 0\t; 【[倒錯的] / PLAYER:[オトコ]なし / [ふたなり]なし】\r\n"
        "\t\tPRINT に体の奥まで\r\n"
        "\t\tIF ABL:15 >= 5\t; 【[サドっ気]Lv>=5】\r\n"
        "\t\t\tPRINT 犯される\r\n"
        "\t\tELSE\r\n"
        "\t\t\tPRINT 見せつける\r\n"
        "\t\tENDIF\r\n"
        "\t\tPRINT 快楽に溺れ\r\n"
        "\t\tSIF TALENT:72\t; 【[中毒しやすい]】\r\n"
        "\t\t\tPRINTFORM 、涎を垂らし\r\n"
        "\t\tSIF TALENT:70 || TALENT:80 || TALENT:79\t; 【[快感に素直] / [倒錯的] / [マゾ]】\r\n"
        "\t\t\tPRINT ながら自ら腰を突き上げ\r\n"
        "\t\tPRINTL ている…\r\n"
        "\tELSEIF TEQUIP:PLAYER:86\t; 【[排卵誘発剤効果発揮中]使用中】\r\n"
        "\t\tPRINTFORML の見ている前で、%CALLNAME:PLAYER%は白濁した蜜をとろとろと床へこぼした…\r\n"
        "\tELSE\r\n"
        "\t\tPRINTL に割り開かれた場所を見られ、興奮のあまり涎と涙と愛液を溢れさせている…\r\n"
        "\tENDIF\r\n"
        "ELSEIF TALENT:85 && TALENT:153\t; 【[恋慕] / [恋人]】\r\n"
        "\tPRINTFORML %CALLNAME:PLAYER%は秘洞の奥まで見られていることに倒錯的な興奮を覚えている…\r\n"
        "ENDIF"
    )
    text = text.replace(old_train_203, new_train_203, 1)

    # 4D: @COM_ORDER_203 - CFLAG:2 < 15000 -> 1500, and display fixes
    text = text.replace(
        "\tIF CFLAG:2 < 15000\t; 【[好感度]<15000】\r\n\t\tB = 50",
        "\tIF CFLAG:2 < 1500\t; 【[好感度]<1500】\r\n\t\tB = 50",
    )
    text = text.replace(
        "\t\tIF CFLAG:2 < 15000\t; 【[好感度]<15000】\r\n\t\t\tB = 50",
        "\t\tIF CFLAG:2 < 1500\t; 【[好感度]<1500】\r\n\t\t\tB = 50",
    )
    text = text.replace(
        "\t;貞操無頓着\r\n"
        "\tIF TALENT:31\t; 【[貞操無頓着]】\r\n"
        "\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:71\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF",
        "\t;貞操無頓着\r\n"
        "\tIF TALENT:31\t; 【[貞操無頓着]】\r\n"
        "\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:31\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF",
        1,
    )
    old_order_disp_203 = (
        "\t;快感に素直\r\n"
        "\tIF TALENT:10\t; 【[臆病]】\r\n"
        "\t\tPRINT  - \r\n"
        "\t\tPRINTS TALENTNAME:70\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;快感の否定\r\n"
        "\tIF TALENT:71\t; 【[快感の否定]】\r\n"
        "\t\tPRINT  - \r\n"
        "\t\tPRINTS TALENTNAME:71\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;淫乱\r\n"
        "\tIF TALENT:76\t; 【[淫乱]】\r\n"
        "\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:76\r\n"
        "\t\tPRINTV '(,10,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;恋慕\r\n"
        "\tIF TALENT:71 && ASSIPLAY == 0\t; 【[快感の否定] / 調教者:[主人]】\r\n"
        "\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:71\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;倒錯的\r\n"
        "\tIF TALENT:80\t; 【[倒錯的]】\r\n"
        "\t\tPRINT  - \r\n"
        "\t\tPRINTS TALENTNAME:80\r\n"
        "\t\tPRINTV '(,7,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;サド\r\n"
        "\tIF TALENT:83\t; 【[サド]】\r\n"
        "\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:83\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;小悪魔\r\n"
        "\tIF TALENT:87\t; 【[小悪魔]】\r\n"
        "\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:87\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF"
    )
    new_order_disp_203 = (
        "\t;快感に素直\r\n"
        "\tIF TALENT:70\t; 【[快感に素直]】\r\n"
        "\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:70\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;快感の否定\r\n"
        "\tIF TALENT:71\t; 【[快感の否定]】\r\n"
        "\t\tPRINT  - \r\n"
        "\t\tPRINTS TALENTNAME:71\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;淫乱\r\n"
        "\tIF TALENT:76\t; 【[淫乱]】\r\n"
        "\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:76\r\n"
        "\t\tPRINTV '(,10,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;恋慕\r\n"
        "\tIF TALENT:85 && ASSIPLAY == 0\t; 【[恋慕] / 調教者:[主人]】\r\n"
        "\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:85\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;倒錯的\r\n"
        "\tIF TALENT:80\t; 【[倒錯的]】\r\n"
        "\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:80\r\n"
        "\t\tPRINTV '(,7,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;サド\r\n"
        "\tIF TALENT:83\t; 【[サド]】\r\n"
        "\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:83\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;小悪魔\r\n"
        "\tIF TALENT:87\t; 【[小悪魔]】\r\n"
        "\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:87\r\n"
        "\t\tPRINTV '(,3,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF"
    )
    text = text.replace(old_order_disp_203, new_order_disp_203, 1)

    if text != orig and write_erb(p, text):
        return 1
    return 0


def fix_category5_abl_ladders() -> int:
    """Fix ABL ladder variable index mismatches across 14 files."""
    changed = 0

    # 5A: ERB/COMF/CALC_EJAC.ERB
    p_ejac = ROOT / "ERB" / "COMF" / "CALC_EJAC.ERB"
    t_ejac = read_erb(p_ejac)
    t_ejac_new = t_ejac.replace(
        "\t\tELSE\r\n"
        "\t\t\tB = EJAC_SCALE(B, (MIN(MAX(0, ABL:0), 1000000) * 5 + 125), 100)\r\n"
        "\t\tENDIF\r\n"
        "\r\n"
        "\t\t;PALAM:潤滑をみる",
        "\t\tELSE\r\n"
        "\t\t\tB = EJAC_SCALE(B, (MIN(MAX(0, ABL:1), 1000000) * 5 + 125), 100)\r\n"
        "\t\tENDIF\r\n"
        "\r\n"
        "\t\t;PALAM:潤滑をみる",
        1,
    ).replace(
        "\t\t;プレイヤーのABL:マゾっ気をみる\r\n"
        "\t\tIF ABL:PLAYER:8 == 0\t; 【PLAYER:[マゾっ気]Lv==0】\r\n"
        "\t\t\tB = EJAC_SCALE(B, 9, 10)\r\n"
        "\t\tELSEIF ABL:PLAYER:3 == 1\t; 【PLAYER:[Ｃ感覚]Lv==1】\r\n"
        "\t\t\tB = EJAC_SCALE(B, 1, 1)\r\n"
        "\t\tELSEIF ABL:PLAYER:3 == 2\t; 【PLAYER:[Ｃ感覚]Lv==2】\r\n"
        "\t\t\tB = EJAC_SCALE(B, 11, 10)\r\n"
        "\t\tELSEIF ABL:PLAYER:3 == 3\t; 【PLAYER:[Ｃ感覚]Lv==3】\r\n"
        "\t\t\tB = EJAC_SCALE(B, 6, 5)\r\n"
        "\t\tELSEIF ABL:PLAYER:3 == 4\t; 【PLAYER:[Ｃ感覚]Lv==4】\r\n"
        "\t\t\tB = EJAC_SCALE(B, 13, 10)\r\n"
        "\t\tELSE\r\n"
        "\t\t\tB = EJAC_SCALE(B, 7, 5)\r\n"
        "\t\tENDIF",
        "\t\t;プレイヤーのABL:マゾっ気をみる\r\n"
        "\t\tIF ABL:PLAYER:8 == 0\t; 【PLAYER:[マゾっ気]Lv==0】\r\n"
        "\t\t\tB = EJAC_SCALE(B, 9, 10)\r\n"
        "\t\tELSEIF ABL:PLAYER:8 == 1\t; 【PLAYER:[マゾっ気]Lv==1】\r\n"
        "\t\t\tB = EJAC_SCALE(B, 1, 1)\r\n"
        "\t\tELSEIF ABL:PLAYER:8 == 2\t; 【PLAYER:[マゾっ気]Lv==2】\r\n"
        "\t\t\tB = EJAC_SCALE(B, 11, 10)\r\n"
        "\t\tELSEIF ABL:PLAYER:8 == 3\t; 【PLAYER:[マゾっ気]Lv==3】\r\n"
        "\t\t\tB = EJAC_SCALE(B, 6, 5)\r\n"
        "\t\tELSEIF ABL:PLAYER:8 == 4\t; 【PLAYER:[マゾっ気]Lv==4】\r\n"
        "\t\t\tB = EJAC_SCALE(B, 13, 10)\r\n"
        "\t\tELSE\r\n"
        "\t\t\tB = EJAC_SCALE(B, 7, 5)\r\n"
        "\t\tENDIF",
        1,
    )
    if t_ejac_new != t_ejac and write_erb(p_ejac, t_ejac_new):
        changed += 1

    # 5B: ERB/CONCERT_コンサートイベント.ERB
    p_conc = ROOT / "ERB" / "CONCERT_コンサートイベント.ERB"
    t_conc = read_erb(p_conc)
    t_conc_new = t_conc.replace(
        ";ABL:露出癖\r\n"
        "IF ABL:94 < 1\t; 【[表現技能]Lv<1】\r\n"
        "\tL += 1\r\n"
        "ELSEIF ABL:7 < 9\t; 【[露出癖]Lv<9】",
        ";ABL:露出癖\r\n"
        "IF ABL:7 < 1\t; 【[露出癖]Lv<1】\r\n"
        "\tL += 1\r\n"
        "ELSEIF ABL:7 < 9\t; 【[露出癖]Lv<9】",
        1,
    )
    if t_conc_new != t_conc and write_erb(p_conc, t_conc_new):
        changed += 1

    # 5C: ERB/COMF/COMF391.ERB
    p_391 = ROOT / "ERB" / "COMF" / "COMF391.ERB"
    t_391 = read_erb(p_391)
    t_391_new = t_391.replace(
        "ELSEIF ABL:6 == 2\t; 【[奉仕精神]Lv==2】\r\n"
        "ELSEIF ABL:7 == 3\t; 【[露出癖]Lv==3】\r\n"
        "\tTIMES B, 0.80\r\n"
        "ELSEIF ABL:6 == 4\t; 【[奉仕精神]Lv==4】",
        "ELSEIF ABL:6 == 2\t; 【[奉仕精神]Lv==2】\r\n"
        "ELSEIF ABL:6 == 3\t; 【[奉仕精神]Lv==3】\r\n"
        "\tTIMES B, 0.80\r\n"
        "ELSEIF ABL:6 == 4\t; 【[奉仕精神]Lv==4】",
        1,
    )
    if t_391_new != t_391 and write_erb(p_391, t_391_new):
        changed += 1

    # 5D: ERB/COMF/COMF66.ERB & COMF68.ERB (ABL:11 精液中毒 ELSE)
    for fn in ["COMF66.ERB", "COMF68.ERB"]:
        p = ROOT / "ERB" / "COMF" / fn
        t = read_erb(p)
        t_new = t.replace(
            "\tELSE\r\n"
            "\t\tSOURCE:7 = (ABL:11 * 3000) - 3000\r\n"
            "\t\tSOURCE:5 = SOURCE:5 * (ABL:0 * 3)\r\n"
            "\t\tTIMES SOURCE:13, 1.00\r\n"
            "\tENDIF",
            "\tELSE\r\n"
            "\t\tSOURCE:7 = (ABL:11 * 3000) - 3000\r\n"
            "\t\tSOURCE:5 = SOURCE:5 * (ABL:11 * 3)\r\n"
            "\t\tTIMES SOURCE:13, 1.00\r\n"
            "\tENDIF",
            1,
        )
        if t_new != t and write_erb(p, t_new):
            changed += 1

    # 5E: ERB/COMF/COMF71.ERB (ABL:4 Ｖ感覚 & ABL:5 Ａ感覚 ELSE)
    p_71 = ROOT / "ERB" / "COMF" / "COMF71.ERB"
    t_71 = read_erb(p_71)
    t_71_new = t_71.replace(
        "\tELSEIF ABL:4 == 4\t; 【[Ｖ感覚]Lv==4】\r\n"
        "\t\tSOURCE:1 = 350\r\n"
        "\t\tSOURCE:13 += 1950\r\n"
        "\tELSE\r\n"
        "\t\tSOURCE:1 = 200 + (ABL:3 * 50)\r\n"
        "\t\tSOURCE:13 += 1050 + (ABL:3 * 300)\r\n"
        "\tENDIF",
        "\tELSEIF ABL:4 == 4\t; 【[Ｖ感覚]Lv==4】\r\n"
        "\t\tSOURCE:1 = 350\r\n"
        "\t\tSOURCE:13 += 1950\r\n"
        "\tELSE\r\n"
        "\t\tSOURCE:1 = 200 + (ABL:4 * 50)\r\n"
        "\t\tSOURCE:13 += 1050 + (ABL:4 * 300)\r\n"
        "\tENDIF",
        1,
    ).replace(
        "\tELSEIF ABL:5 == 4\t; 【[Ａ感覚]Lv==4】\r\n"
        "\t\tSOURCE:2 = 350\r\n"
        "\t\tSOURCE:13 += 2600\r\n"
        "\tELSE\r\n"
        "\t\tSOURCE:2 = 200 + (ABL:3 * 50)\r\n"
        "\t\tSOURCE:13 += 1400 + (ABL:3 * 400)\r\n"
        "\tENDIF",
        "\tELSEIF ABL:5 == 4\t; 【[Ａ感覚]Lv==4】\r\n"
        "\t\tSOURCE:2 = 350\r\n"
        "\t\tSOURCE:13 += 2600\r\n"
        "\tELSE\r\n"
        "\t\tSOURCE:2 = 200 + (ABL:5 * 50)\r\n"
        "\t\tSOURCE:13 += 1400 + (ABL:5 * 400)\r\n"
        "\tENDIF",
        1,
    )
    if t_71_new != t_71 and write_erb(p_71, t_71_new):
        changed += 1

    # 5F: ERB/COMF/COMF191..195, 380, 381 (ABL:PLAYER:6 奉仕精神 ELSE)
    for fn in [
        "COMF191.ERB",
        "COMF192.ERB",
        "COMF193.ERB",
        "COMF194.ERB",
        "COMF195.ERB",
        "COMF380.ERB",
        "COMF381.ERB",
    ]:
        p = ROOT / "ERB" / "COMF" / fn
        t = read_erb(p)
        t_new = re.sub(
            r"(;ABL:奉仕精神をみる\r\n"
            r"IF ABL:PLAYER:6 == 0.*?"
            r"ELSEIF ABL:PLAYER:6 == 4.*?\r\n"
            r"(?:\t[^\r\n]*\r\n|;\t[^\r\n]*\r\n)+"
            r"ELSE\r\n"
            r"\tSOURCE:3 = SOURCE:3 \* \()ABL:PLAYER:2( \* 75 \+ 25\))",
            r"\1ABL:PLAYER:6\2",
            t,
            count=1,
            flags=re.S,
        )
        if t_new != t and write_erb(p, t_new):
            changed += 1

    # 5G: ERB/COMF/COMF205.ERB (ABL:10 自慰中毒 ELSE)
    p_205 = ROOT / "ERB" / "COMF" / "COMF205.ERB"
    t_205 = read_erb(p_205)
    t_205_new = t_205.replace(
        "ELSEIF ABL:10 == 4\t; 【[自慰中毒]Lv==4】\r\n"
        "\tSOURCE:4 = 450\r\n"
        "\tSOURCE:13 = 50\r\n"
        "\tTIMES SOURCE:8 , 0.50\r\n"
        "ELSE\r\n"
        "\tSOURCE:4 = 375 + (ABL:6 * 25)\r\n"
        "\tSOURCE:13 = 0\r\n"
        "\tTIMES SOURCE:8 , 0.10\r\n"
        "ENDIF",
        "ELSEIF ABL:10 == 4\t; 【[自慰中毒]Lv==4】\r\n"
        "\tSOURCE:4 = 450\r\n"
        "\tSOURCE:13 = 50\r\n"
        "\tTIMES SOURCE:8 , 0.50\r\n"
        "ELSE\r\n"
        "\tSOURCE:4 = 375 + (ABL:10 * 25)\r\n"
        "\tSOURCE:13 = 0\r\n"
        "\tTIMES SOURCE:8 , 0.10\r\n"
        "ENDIF",
        1,
    )
    if t_205_new != t_205 and write_erb(p_205, t_205_new):
        changed += 1

    # 5H: ERB/COMF/COMF372.ERB (ABL:5 Ａ感覚 ELSE)
    p_372 = ROOT / "ERB" / "COMF" / "COMF372.ERB"
    t_372 = read_erb(p_372)
    t_372_new = t_372.replace(
        "ELSEIF ABL:5 == 4\t; 【[Ａ感覚]Lv==4】\r\n"
        "\tSOURCE:2 = 1100\r\n"
        "\tSOURCE:3 = 230\r\n"
        "\tSOURCE:13 = 250\r\n"
        "ELSE\r\n"
        "\tSOURCE:2 = 500 + (ABL:5 * 200)\r\n"
        "\tSOURCE:3 = 200 + (ABL:14 * 10)\r\n"
        "\tSOURCE:13 = 250 + (ABL:5 * 50)\r\n"
        "ENDIF",
        "ELSEIF ABL:5 == 4\t; 【[Ａ感覚]Lv==4】\r\n"
        "\tSOURCE:2 = 1100\r\n"
        "\tSOURCE:3 = 230\r\n"
        "\tSOURCE:13 = 250\r\n"
        "ELSE\r\n"
        "\tSOURCE:2 = 500 + (ABL:5 * 200)\r\n"
        "\tSOURCE:3 = 200 + (ABL:5 * 10)\r\n"
        "\tSOURCE:13 = 250 + (ABL:5 * 50)\r\n"
        "ENDIF",
        1,
    )
    if t_372_new != t_372 and write_erb(p_372, t_372_new):
        changed += 1

    return changed


def fix_category6_com_order_displays() -> int:
    """Fix @COM_ORDER_* display mismatches in COMF68, 360, 361, 367, 370."""
    changed = 0

    # 6A: COMF360, COMF361, COMF367, COMF370 - キス未経験 (20)->(30) matching A -= 30
    for fn in ["COMF360.ERB", "COMF361.ERB", "COMF367.ERB", "COMF370.ERB"]:
        p = ROOT / "ERB" / "COMF" / fn
        t = read_erb(p)
        t_new = t.replace(
            "\t;キス未経験\r\n"
            "\tIF TALENT:151\t; 【[キス未経験]】\r\n"
            "\t\tPRINT  - \r\n"
            "\t\tPRINTS TALENTNAME:151\r\n"
            "\t\tPRINTV '(,20,')\r\n"
            "\t\tS = 1\r\n"
            "\tENDIF",
            "\t;キス未経験\r\n"
            "\tIF TALENT:151\t; 【[キス未経験]】\r\n"
            "\t\tPRINT  - \r\n"
            "\t\tPRINTS TALENTNAME:151\r\n"
            "\t\tPRINTV '(,30,')\r\n"
            "\t\tS = 1\r\n"
            "\tENDIF",
            1,
        )
        if t_new != t and write_erb(p, t_new):
            changed += 1

    # 6B: COMF68.ERB - @COM_ORDER_68 display checks TALENT:ASSI:122 and TALENT:ASSI:121 instead of MASTER
    p68 = ROOT / "ERB" / "COMF" / "COMF68.ERB"
    t68 = read_erb(p68)
    t68_new = t68.replace(
        "\t;男嫌い\r\n"
        "\tIF TALENT:82 && TALENT:ASSI:122\t; 【[男嫌い] / ASSI:[オトコ]】\r\n"
        "\t\tPRINT  - \r\n"
        "\t\tPRINTS TALENTNAME:82\r\n"
        "\t\tPRINTV '(,12,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;恋慕\r\n"
        "\tIF TALENT:85 && ASSIPLAY == 0\t; 【[恋慕] / 調教者:[主人]】\r\n"
        "\t\tSIF S\r\n"
        "\t\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:85\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\r\n"
        "\t;調教者がふたなり\r\n"
        "\tIF TALENT:ASSI:121\t; 【ASSI:[ふたなり]】",
        "\t;男嫌い\r\n"
        "\tIF TALENT:82 && TALENT:MASTER:122\t; 【[男嫌い] / MASTER:[オトコ]】\r\n"
        "\t\tPRINT  - \r\n"
        "\t\tPRINTS TALENTNAME:82\r\n"
        "\t\tPRINTV '(,12,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\t;恋慕\r\n"
        "\tIF TALENT:85 && ASSIPLAY == 0\t; 【[恋慕] / 調教者:[主人]】\r\n"
        "\t\tSIF S\r\n"
        "\t\t\tPRINT  + \r\n"
        "\t\tPRINTS TALENTNAME:85\r\n"
        "\t\tPRINTV '(,5,')\r\n"
        "\t\tS = 1\r\n"
        "\tENDIF\r\n"
        "\r\n"
        "\t;調教者がふたなり\r\n"
        "\tIF TALENT:MASTER:121\t; 【MASTER:[ふたなり]】",
        1,
    )
    if t68_new != t68 and write_erb(p68, t68_new):
        changed += 1

    return changed


def main() -> None:
    c1_files, c1_lines = fix_category1_unquoted_printformw()
    c2 = fix_category2_char01_and_char27()
    c3 = fix_category3_female_partner_kojo()
    c4 = fix_category4_comf203()
    c5 = fix_category5_abl_ladders()
    c6 = fix_category6_com_order_displays()
    print(f"Category 1 (unquoted PRINTFORMW): {c1_files} files ({c1_lines} lines)")
    print(f"Category 2 (CHAR_01 & CHAR_27 duplicate/contradictory COMs): {c2} files")
    print(f"Category 3 (Female-only / Assistant-partner Kojo): {c3} files")
    print(f"Category 4 (COMF203.ERB): {c4} files")
    print(f"Category 5 (ABL ladder mismatches): {c5} files")
    print(f"Category 6 (@COM_ORDER display mismatches): {c6} files")


if __name__ == "__main__":
    main()
