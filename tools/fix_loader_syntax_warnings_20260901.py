from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAR_DIR = ROOT / "ERB/CHAR"
BACKUP_DIR = ROOT / "tools/backups/loader_syntax_warnings_20260901"

FILES = {
    12: CHAR_DIR / "CHAR_12_神樹いちか_COM.ERB",
    16: CHAR_DIR / "CHAR_16_大虎いさみ_COM.ERB",
    17: CHAR_DIR / "CHAR_17_小鳩あずさ_COM.ERB",
    18: CHAR_DIR / "CHAR_18_熊沢ひめの_COM.ERB",
}


def fix_locals_escapes(text: str, char_no: int) -> tuple[str, int]:
    valid = "LOCALS '= @\"%RESULTS%\""
    if char_no == 16:
        broken = "LOCALS '= @\\\"%RESULTS%\\\""
    else:
        broken = "LOCALS \\'= @\"%RESULTS%\""
    count = text.count(broken)
    if count:
        text = text.replace(broken, valid)
    return text, count


def fix_char12_chain(text: str) -> tuple[str, int]:
    added = 0
    # 280-284 は1本の IF/ELSEIF 連鎖、410-414も別の1本の連鎖。
    # 各 ELSEIF の直前には、前ブロック内の TALENT 分岐を閉じる ENDIF が必要。
    # 外側の SELECTCOM 用 ENDIF は、各連鎖の最後（284/414）にだけ残す。
    for command in [281, 282, 283, 284, 411, 412, 413, 414]:
        marker = f";--- COM{command} "
        count = text.count(marker)
        if count != 1:
            raise RuntimeError(f"CHAR12: COM{command}見出しが {count} 件です")
        location = text.index(marker)
        if not text[:location].endswith("ENDIF\n"):
            text = text[:location] + "ENDIF\n" + text[location:]
            added += 1
    annotation = ";--- COM410-414 独自純愛 ---"
    if annotation not in text:
        anchor = ";--- COM410 独自純愛：お祭りの屋台めぐり ---\nIF SELECTCOM == 410"
        if text.count(anchor) != 1:
            raise RuntimeError("CHAR12: COM410の注釈位置を確認できません")
        text = text.replace(anchor, annotation + "\n" + anchor, 1)
        added += 1
    return text, added


def main() -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    total_escape_fixes = 0
    total_chain_fixes = 0

    for char_no, path in FILES.items():
        raw = path.read_bytes()
        text = raw.decode("cp932").replace("\r\n", "\n")
        if not (BACKUP_DIR / path.name).exists():
            (BACKUP_DIR / path.name).write_bytes(raw)

        if char_no in [16, 17, 18]:
            text, count = fix_locals_escapes(text, char_no)
            total_escape_fixes += count
        if char_no == 12:
            text, count = fix_char12_chain(text)
            total_chain_fixes += count

        path.write_bytes(text.replace("\n", "\r\n").encode("cp932"))

    print(f"LOCALSエスケープ修正: {total_escape_fixes} 箇所")
    print(f"CHAR12のIF/ELSEIF連鎖修正: {total_chain_fixes} 箇所")


if __name__ == "__main__":
    main()
