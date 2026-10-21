# -*- coding: utf-8 -*-
"""
Apply fixes for:
1. Bug Audit #12: Club activity (CLUB_ACTIVITY_部活動システム.ERB) overwriting skills > 100 down to 100, and INIT_CLUB_FLAGS SIF/BREAK bug.
2. Bug Audit #13A: @AITE_YOBI (AITE_YOBI_相手呼称.ERB) using party slot index instead of NO:AI for grade/special nickname lookup, and out-of-bounds guard when ASSI < 0.
3. Bug Audit #13B: Assistant COM blocks in CHAR_*_COM.ERB missing CALL AITE_YOBI, N, ASSI (or having stray unused AITE_YOBI ASSI calls).
4. Kojo syntax/branch bugs in CHAR_01, CHAR_14, CHAR_15, CHAR_34, CHAR_65.
"""
import glob
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")


def read_cp932(path: str) -> str:
    with open(path, "rb") as f:
        return f.read().decode("cp932").replace("\r\n", "\n")


def write_cp932(path: str, text: str) -> None:
    raw = text.replace("\r\n", "\n").replace("\n", "\r\n").encode("cp932")
    with open(path, "wb") as f:
        f.write(raw)


def fix_club_activity() -> None:
    path = "ERB/CLUB_ACTIVITY_部活動システム.ERB"
    text = read_cp932(path)

    # Replace all patterns of:
    # <indent>ABL:<WHO>:<IDX> += <DELTA>
    # <indent>SIF ABL:<WHO>:<IDX> > 100<comment>
    # <indent>\tABL:<WHO>:<IDX> = 100
    pattern = re.compile(
        r"^([ \t]*)ABL:(MASTER|TARGET):(\d+) \+= ([A-Z0-9]+)\n"
        r"\1SIF ABL:\2:\3 > 100([ \t]*;[^\n]*)?\n"
        r"\1[ \t]+ABL:\2:\3 = 100$",
        re.MULTILINE,
    )

    def repl(m: re.Match) -> str:
        indent, who, idx, delta, comment = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5) or ""
        comment = comment.replace(">100", "<100")
        return f"{indent}SIF ABL:{who}:{idx} < 100{comment}\n{indent}\tABL:{who}:{idx} = MIN(ABL:{who}:{idx} + {delta}, 100)"

    new_text, count = pattern.subn(repl, text)
    print(f"[CLUB_ACTIVITY] Updated {count} capped skill/talent increments")

    # Fix @INIT_CLUB_FLAGS SIF + BREAK bug
    old_init = (
        "REPEAT CHARANUM\n"
        "\tSIF CFLAG:COUNT:25 > 0\t; 【COUNT:[初期噴乳経験]>0】\n"
        "\t\tA = 1\n"
        "\t\tBREAK\n"
        "REND"
    )
    new_init = (
        "REPEAT CHARANUM\n"
        "\tIF CFLAG:COUNT:25 > 0\t; 【COUNT:[初期噴乳経験]>0】\n"
        "\t\tA = 1\n"
        "\t\tBREAK\n"
        "\tENDIF\n"
        "REND"
    )
    if old_init in new_text:
        new_text = new_text.replace(old_init, new_init, 1)
        print("[CLUB_ACTIVITY] Fixed @INIT_CLUB_FLAGS IF/BREAK block")

    if new_text != text:
        write_cp932(path, new_text)


def fix_aite_yobi() -> None:
    path = "ERB/AITE_YOBI_相手呼称.ERB"
    text = read_cp932(path)

    old_head = (
        "@AITE_YOBI, ARG, ARG:1\n"
        "#DIM SP\n"
        "#DIM AI\n"
        "#DIMS SUR\n"
        "\tSP = ARG\n"
        "\tAI = ARG:1\n"
        "\t;苗字（フルネームから呼び名を除去）\n"
        "\tSUR '= REPLACE(NAME:AI, CALLNAME:AI, \"\")\n"
        "\tSUR '= REPLACE(SUR, \"・\", \"\")\n"
        "\tSIF SUR == \"\"\n"
        "\t\tSUR '= CALLNAME:AI\n"
    )
    new_head = (
        "@AITE_YOBI, ARG, ARG:1\n"
        "#DIM SP\n"
        "#DIM AI\n"
        "#DIM AI_SLOT\n"
        "#DIMS SUR\n"
        "\tSP = ARG\n"
        "\tAI_SLOT = ARG:1\n"
        "\tSIF AI_SLOT < 0 || AI_SLOT >= CHARANUM\n"
        "\t\tAI_SLOT = PLAYER\n"
        "\tSIF AI_SLOT < 0 || AI_SLOT >= CHARANUM\n"
        "\t\tAI_SLOT = 0\n"
        "\tIF AI_SLOT == 0\n"
        "\t\tAI = NO:0\n"
        "\tELSEIF NO:AI_SLOT > 0\n"
        "\t\tAI = NO:AI_SLOT\n"
        "\tELSE\n"
        "\t\tAI = AI_SLOT\n"
        "\tENDIF\n"
        "\t;苗字（フルネームから呼び名を除去）\n"
        "\tSUR '= REPLACE(NAME:AI_SLOT, CALLNAME:AI_SLOT, \"\")\n"
        "\tSUR '= REPLACE(SUR, \"・\", \"\")\n"
        "\tSIF SUR == \"\"\n"
        "\t\tSUR '= CALLNAME:AI_SLOT\n"
    )
    if old_head in text:
        text = text.replace(old_head, new_head, 1)
        print("[AITE_YOBI] Updated header to resolve AI_SLOT and AI (NO:AI_SLOT) with bounds guard")

    # Replace %CALLNAME:AI% with %CALLNAME:AI_SLOT% in section (1)
    text, n_call = re.subn(r"%CALLNAME:AI%", "%CALLNAME:AI_SLOT%", text)
    print(f"[AITE_YOBI] Replaced {n_call} occurrences of %CALLNAME:AI% with %CALLNAME:AI_SLOT%")

    write_cp932(path, text)


def fix_kojo_files() -> None:
    # 1. CHAR_01 COM69 L3431-3435 PRINTFORML -> PRINTFORMW
    p01 = "ERB/CHAR/CHAR_01_三善かなえ_COM.ERB"
    t01 = read_cp932(p01)
    old_01 = (
        "\t\tIF A == 0\n"
        "\t\t\tPRINTFORML 「ん……っ、んむ……。転校生さんのを咥えながら、私のほうも舐められて……っ。ふぁ、忙しいですね♪」\n"
        "\t\tELSEIF A == 1\n"
        "\t\t\tPRINTFORML 「ちゅ……っ、奥まで頑張ります。あっ、そこを舐められると……口に力が入りません……♪」\n"
        "\t\tELSE\n"
        "\t\t\tPRINTFORML 「んっ……お互いに気持ちよくなるのですから、合理的ではありますね。……でも、頭が追いつきません♪」\n"
        "\t\tENDIF"
    )
    new_01 = old_01.replace("PRINTFORML", "PRINTFORMW")
    if old_01 in t01:
        t01 = t01.replace(old_01, new_01, 1)
        write_cp932(p01, t01)
        print("[KOJO] Fixed CHAR_01 COM69 PRINTFORML -> PRINTFORMW")

    # 2. CHAR_14 COM203 (L4121) and COM390 (L4370)
    p14 = "ERB/CHAR/CHAR_14_花音ことり_COM.ERB"
    t14 = read_cp932(p14)
    old_14_a = (
        "\tIF TALENT:TARGET:153\t; 【TARGET:[恋人]】\n"
        "\t\t;恋人\n"
        "\t\tPRINTFORML 「え、おらが%LOCALS%に、これを……？　あぅ、戸惑うげど……ほら、%LOCALS%の中、\n"
        "\t\tIF A == 0\n"
        "\t\t\tPRINTFORMW ぜんぶ見えちまうなぁ……恥ずかしいだろ……？♪」"
    )
    new_14_a = (
        "\tIF TALENT:TARGET:153\t; 【TARGET:[恋人]】\n"
        "\t\t;恋人\n"
        "\t\tIF A == 0\n"
        "\t\t\tPRINTFORML 「え、おらが%LOCALS%に、これを……？　あぅ、戸惑うげど……ほら、%LOCALS%の中、\n"
        "\t\t\tPRINTFORMW ぜんぶ見えちまうなぁ……恥ずかしいだろ……？♪」"
    )
    old_14_b = (
        "\tELSE\n"
        "\t\t;通常\n"
        "\t\tPRINTFORML 「うはぁ、ゲームセンターは賑やかだなぁ！　えへ、故郷の島にはなかっだがら、新鮮だよ。\n"
        "\t\tIF A == 0\n"
        "\t\t\tPRINTFORMW 転校生しゃん、付きあってぐれてあんがど♪」"
    )
    new_14_b = (
        "\tELSE\n"
        "\t\t;通常\n"
        "\t\tIF A == 0\n"
        "\t\t\tPRINTFORML 「うはぁ、ゲームセンターは賑やかだなぁ！　えへ、故郷の島にはなかっだがら、新鮮だよ。\n"
        "\t\t\tPRINTFORMW 転校生しゃん、付きあってぐれてあんがど♪」"
    )
    changed_14 = False
    if old_14_a in t14:
        t14 = t14.replace(old_14_a, new_14_a, 1)
        changed_14 = True
    if old_14_b in t14:
        t14 = t14.replace(old_14_b, new_14_b, 1)
        changed_14 = True
    if changed_14:
        write_cp932(p14, t14)
        print("[KOJO] Fixed CHAR_14 COM203 and COM390 leaked PRINTFORML")

    # 3. CHAR_15 COM196 (L3916, L3925)
    p15 = "ERB/CHAR/CHAR_15_長町やえ_COM.ERB"
    t15 = read_cp932(p15)
    old_15 = (
        "\tIF TALENT:TARGET:153\t; 【TARGET:[恋人]】\n"
        "\t\t;恋人\n"
        "\t\tIF A == 0\n"
        "\t\t\tPRINTFORML 「ひゃっ、こ、これ挿れるのっ……！？　あぅ、%LOCALS%の張形、本物じゃないのにっ、\n"
        "\t\tELSEIF A == 1\n"
        "\t\t\tPRINTFORMW 「うひゃあ、張形が奥で止まらないっ……！　お尻から胸まで、ずずっと響いてくるよぉっ♪」\n"
        "\t\tELSE\n"
        "\t\t\tPRINTFORMW 「%LOCALS%に抱きつくと、動きのたびに息が重なるっ……。身体を預けてる感じ、忘れられないよっ♪」\n"
        "\t\tENDIF\n"
        "\tELSE\n"
        "\t\t;通常\n"
        "\t\tIF A == 0\n"
        "\t\t\tPRINTFORML 「やっ、おもちゃっ……！？　あぅ、%LOCALS%にぐいって入れられてっ、変な感じっ……あたし、\n"
        "\t\tELSEIF A == 1"
    )
    new_15 = (
        "\tIF TALENT:TARGET:153\t; 【TARGET:[恋人]】\n"
        "\t\t;恋人\n"
        "\t\tIF A == 0\n"
        "\t\t\tPRINTFORML 「ひゃっ、こ、これ挿れるのっ……！？　あぅ、%LOCALS%の張形、本物じゃないのにっ、\n"
        "\t\t\tPRINTFORMW 奥まで来ちゃうっ……おに～さんが見てるのにっ……♪」\n"
        "\t\tELSEIF A == 1\n"
        "\t\t\tPRINTFORMW 「うひゃあ、張形が奥で止まらないっ……！　お尻から胸まで、ずずっと響いてくるよぉっ♪」\n"
        "\t\tELSE\n"
        "\t\t\tPRINTFORMW 「%LOCALS%に抱きつくと、動きのたびに息が重なるっ……。身体を預けてる感じ、忘れられないよっ♪」\n"
        "\t\tENDIF\n"
        "\tELSE\n"
        "\t\t;通常\n"
        "\t\tIF A == 0\n"
        "\t\t\tPRINTFORML 「やっ、おもちゃっ……！？　あぅ、%LOCALS%にぐいって入れられてっ、変な感じっ……あたし、\n"
        "\t\t\tPRINTFORMW これでも感じちゃうのっ……恥ずかしいよぉ……っ！」\n"
        "\t\tELSEIF A == 1"
    )
    if old_15 in t15:
        t15 = t15.replace(old_15, new_15, 1)
        write_cp932(p15, t15)
        print("[KOJO] Restored missing second lines in CHAR_15 COM196")

    # 4. CHAR_34 L4820 double closing bracket
    p34 = "ERB/CHAR/CHAR_34_桐島かいり_COM.ERB"
    t34 = read_cp932(p34)
    old_34 = 'PRINTFORMW 「ん、ふぁ、あつ、熱いっ……！　──こ、こんなに出るの、はじめてで、かいり、びっくりしてますのっ……」」'
    new_34 = 'PRINTFORMW 「ん、ふぁ、あつ、熱いっ……！　──こ、こんなに出るの、はじめてで、かいり、びっくりしてますのっ……」'
    if old_34 in t34:
        t34 = t34.replace(old_34, new_34, 1)
        write_cp932(p34, t34)
        print("[KOJO] Fixed double closing bracket in CHAR_34 L4820")

    # 5. CHAR_65 COM56 (L3487)
    p65 = "ERB/CHAR/CHAR_65_時国そら_COM.ERB"
    t65 = read_cp932(p65)
    old_65 = (
        "\tELSE\n"
        "\t\t;通常\n"
        "\t\tPRINTFORML 「あ……あなたが、%LOCALS%を……。ん、激しい……。（わたしの心臓まで、はやくなってる）……\n"
        "\t\tA = RAND:3\n"
        "\t\tIF A == 0\n"
        "\t\t\tPRINTFORMW ふふ、つづけて？　わたしも、見ていてあげる」"
    )
    new_65 = (
        "\tELSE\n"
        "\t\t;通常\n"
        "\t\tA = RAND:3\n"
        "\t\tIF A == 0\n"
        "\t\t\tPRINTFORML 「あ……あなたが、%LOCALS%を……。ん、激しい……。（わたしの心臓まで、はやくなってる）……\n"
        "\t\t\tPRINTFORMW ふふ、つづけて？　わたしも、見ていてあげる」"
    )
    if old_65 in t65:
        t65 = t65.replace(old_65, new_65, 1)
        write_cp932(p65, t65)
        print("[KOJO] Fixed CHAR_65 COM56 leaked PRINTFORML")

    # 6. Normalize @KOJO_MESSAGE_COM_<cid> top-level RETURN 0 and AITE_YOBI PLAYER placement,
    #    then ensure every SELECTCOM block using %LOCALS% has CALL AITE_YOBI, <cid>, ASSI.
    added_assi_calls = 0
    removed_stray_calls = 0
    fixed_return_files = 0
    modified_files = 0

    for fpath in sorted(glob.glob("ERB/CHAR/CHAR_[0-9]*_COM.ERB")):
        m_cid = re.search(r"CHAR_(\d+)_", os.path.basename(fpath))
        if not m_cid:
            continue
        cid = int(m_cid.group(1))
        text = read_cp932(fpath)
        orig_text = text

        # If any IF SELECTCOM == ... blocks were accidentally placed after @CHAR_ORGASM_<cid>'s RETURN 0
        # (before @TRAIN_MESSAGE_B280_<cid>), move them back into @KOJO_MESSAGE_COM_<cid>.
        m_orgasm = re.search(rf"^@CHAR_ORGASM_{cid}\b", text, re.MULTILINE)
        m_b280 = re.search(rf"^@TRAIN_MESSAGE_B280_{cid}\b", text, re.MULTILINE)
        m_virgin_pre = re.search(rf"^@CHAR_VIRGIN_{cid}\b", text, re.MULTILINE)
        if m_orgasm and m_b280 and m_virgin_pre:
            orgasm_chunk = text[m_orgasm.start() : m_b280.start()]
            m_ret_sel = re.search(
                r"(^RETURN 0\n+)((?:[ \t]*;[^\n]*\n|\n)*IF SELECTCOM == 60\b.*)",
                orgasm_chunk,
                re.MULTILINE | re.DOTALL,
            )
            if m_ret_sel:
                misplaced_selectcoms = m_ret_sel.group(2).rstrip() + "\n\n"
                cleaned_orgasm_chunk = orgasm_chunk[: m_ret_sel.start()] + "RETURN 0\n\n"
                text = (
                    text[: m_virgin_pre.start()]
                    + "\n"
                    + misplaced_selectcoms
                    + text[m_virgin_pre.start() : m_orgasm.start()]
                    + cleaned_orgasm_chunk
                    + text[m_b280.start() :]
                )

        # Split at @CHAR_VIRGIN_<cid> so we can clean up @KOJO_MESSAGE_COM_<cid>
        m_virgin = re.search(rf"^@CHAR_VIRGIN_{cid}\b", text, re.MULTILINE)
        if m_virgin:
            kojo_com_part = text[: m_virgin.start()]
            rest_part = text[m_virgin.start() :]

            lines = kojo_com_part.split("\n")
            new_lines = []
            depth = 0
            prev_sif = False
            seen_tequip_return = False
            removed_player_yobi = False

            i = 0
            while i < len(lines):
                line = lines[i]
                s = line.split(";", 1)[0].strip()

                if not seen_tequip_return:
                    new_lines.append(line)
                    if prev_sif and s == "RETURN 0":
                        seen_tequip_return = True
                        prev_sif = False
                        # Ensure AITE_YOBI PLAYER is right after TEQUIP:45 RETURN 0
                        new_lines.append(
                            "; ▼ 相手呼称システム（女性同士COMで相手を原作準拠の呼び方に。%LOCALS%で展開・アンカー1回方式）"
                        )
                        new_lines.append(f"CALL AITE_YOBI, {cid}, PLAYER")
                        new_lines.append('LOCALS \'= @"%RESULTS%"')
                    elif s.startswith("SIF "):
                        prev_sif = True
                    elif s:
                        prev_sif = False
                    i += 1
                    continue

                # Skip existing top-level AITE_YOBI PLAYER header (since we placed it right after TEQUIP:45 RETURN 0)
                if depth == 0 and (
                    line.strip().startswith("; ▼ 相手呼称システム")
                    or re.match(rf"^[ \t]*CALL\s+AITE_YOBI\s*,\s*{cid}\s*,\s*PLAYER\b", line)
                ):
                    if (
                        re.match(rf"^[ \t]*CALL\s+AITE_YOBI\s*,\s*{cid}\s*,\s*PLAYER\b", line)
                        and i + 1 < len(lines)
                        and 'LOCALS \'= @"%RESULTS%"' in lines[i + 1]
                    ):
                        i += 2
                        continue
                    i += 1
                    continue

                if prev_sif:
                    prev_sif = False
                    new_lines.append(line)
                    i += 1
                    continue

                if s.startswith("SIF "):
                    prev_sif = True
                    new_lines.append(line)
                    i += 1
                    continue

                if re.match(r"^IF\b", s):
                    depth += 1
                elif re.match(r"^ENDIF\b", s):
                    depth = max(0, depth - 1)
                elif re.match(r"^RETURN\s+0\b", s) and depth == 0:
                    # Drop mid-function or duplicate top-level RETURN 0; we will append a single RETURN 0 at the end
                    i += 1
                    continue

                new_lines.append(line)
                i += 1

            # Strip trailing blank lines and append single RETURN 0 + blank line before @CHAR_VIRGIN_<cid>
            while new_lines and new_lines[-1].strip() == "":
                new_lines.pop()
            new_lines.append("RETURN 0")
            new_lines.append("")
            new_lines.append("")
            rebuilt_kojo_com = "\n".join(new_lines)
            if rebuilt_kojo_com != kojo_com_part:
                fixed_return_files += 1
            text = rebuilt_kojo_com + rest_part

        # Process each IF SELECTCOM == <num> block up to next ;--- or IF SELECTCOM or RETURN 0 or @
        pattern_block = re.compile(
            r"(^IF SELECTCOM == (\d+)[^\n]*\n)(.*?)(?=^;---|^IF SELECTCOM ==|^RETURN 0\b|^@|\Z)",
            re.MULTILINE | re.DOTALL,
        )

        def process_block(m: re.Match) -> str:
            nonlocal added_assi_calls, removed_stray_calls
            header = m.group(1)
            body = m.group(3)
            code_only = "\n".join(
                l.split(";", 1)[0] for l in body.splitlines() if not l.lstrip().startswith(";")
            )
            has_locals = "%LOCALS%" in code_only
            has_assi_yobi = bool(re.search(rf"CALL AITE_YOBI,\s*{cid},\s*ASSI\b", code_only))

            if has_locals and not has_assi_yobi:
                inject = f"\tCALL AITE_YOBI, {cid}, ASSI\n\tLOCALS '= @\"%RESULTS%\"\n"
                added_assi_calls += 1
                return header + inject + body
            elif not has_locals and has_assi_yobi:
                new_body, n_rem = re.subn(
                    rf"[ \t]*CALL AITE_YOBI,\s*{cid},\s*ASSI\n[ \t]*LOCALS '= @\"%RESULTS%\"\n?",
                    "",
                    body,
                )
                if n_rem > 0:
                    removed_stray_calls += n_rem
                    return header + new_body
            return m.group(0)

        new_text = pattern_block.sub(process_block, text)
        if new_text != orig_text:
            write_cp932(fpath, new_text)
            modified_files += 1

    print(
        f"[KOJO AITE_YOBI & RETURN] Normalized top-level RETURN/header in {fixed_return_files} files; "
        f"added {added_assi_calls} missing AITE_YOBI ASSI calls, "
        f"removed {removed_stray_calls} stray calls across {modified_files} files."
    )


if __name__ == "__main__":
    fix_club_activity()
    fix_aite_yobi()
    fix_kojo_files()
