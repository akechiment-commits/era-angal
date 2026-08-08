from pathlib import Path


COMMANDS = (60, 62, 76, 78, 79, 84, 86, 202, 258, 318)
WITH_ASSISTANT = {62, 76, 202, 258}


def find_target(cno: int) -> Path:
    matches = list(Path("ERB/CHAR").glob(f"CHAR_{cno}_*_COM.ERB"))
    if len(matches) != 1:
        raise RuntimeError(f"expected one target for CHAR_{cno}, found {matches}")
    return matches[0]


def build_block(cno: int, tag: str, lines: dict[int, tuple[list[str], list[str]]]) -> str:
    if set(lines) != set(COMMANDS):
        raise RuntimeError(f"command set mismatch: {sorted(lines)}")
    out = [
        f";=== {tag} MISSING COMMAND TRIAL START ===",
        "; 未実装10コマンド（恋慕TALENT:85／非恋慕を各3種）",
        "",
    ]
    for com in COMMANDS:
        lover, normal = lines[com]
        if len(lover) != 3 or len(normal) != 3:
            raise RuntimeError(f"COM{com} must have three lover and three normal lines")
        out.append(f";--- COM{com} ---")
        if com in (76, 202):
            out.append("; 助手調教専用：対象と女性助手の二人だけ")
        elif com == 258:
            out.append("; 視点：対象はPLAYERとの騎乗位を続け、助手がPLAYERの顔へ跨る")
        elif com == 318:
            out.append("; 視点：対象がPLAYERの頭を撫でる側")
        out.append(f"IF SELECTCOM == {com}")
        if com in WITH_ASSISTANT:
            out.append(f"\tCALL AITE_YOBI, {cno}, ASSI")
            out.append("\tLOCALS '= @\"%RESULTS%\"")
        out.extend(("\tA = RAND:3", "\tIF TALENT:TARGET:85"))
        for i, speech in enumerate(lover):
            out.append("\t\tIF A == 0" if i == 0 else ("\t\tELSEIF A == 1" if i == 1 else "\t\tELSE"))
            out.append(f"\t\t\tPRINTFORMW 「{speech}」")
        out.extend(("\t\tENDIF", "\tELSE"))
        for i, speech in enumerate(normal):
            out.append("\t\tIF A == 0" if i == 0 else ("\t\tELSEIF A == 1" if i == 1 else "\t\tELSE"))
            out.append(f"\t\t\tPRINTFORMW 「{speech}」")
        out.extend(("\t\tENDIF", "\tENDIF", "ENDIF", ""))
    out.append(f";=== {tag} MISSING COMMAND TRIAL END ===")
    return "\r\n".join(out)


def install(cno: int, tag: str, lines: dict[int, tuple[list[str], list[str]]]) -> None:
    target = find_target(cno)
    text = target.read_bytes().decode("cp932")
    start_marker = f";=== {tag} MISSING COMMAND TRIAL START ==="
    end_marker = f";=== {tag} MISSING COMMAND TRIAL END ==="
    block = build_block(cno, tag, lines)
    if start_marker in text:
        start = text.index(start_marker)
        end = text.index(end_marker, start) + len(end_marker)
        text = text[:start] + block + text[end:]
    else:
        virgin = text.index(f"@CHAR_VIRGIN_{cno}")
        anchor = text.rfind(";==============================================================", 0, virgin)
        if anchor < 0:
            raise RuntimeError(f"insertion anchor not found: {target}")
        text = text[:anchor] + block + "\r\n\r\n" + text[anchor:]
    target.write_bytes(text.encode("cp932"))
