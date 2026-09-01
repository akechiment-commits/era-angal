from collections import Counter
from pathlib import Path
import re


TARGET = Path(r"ERB/CHAR/CHAR_49_小松ぼたん_COM.ERB")


def quote_lines(text: str) -> list[str]:
    pattern = re.compile(r"^\s*PRINTFORM[LW]?\s+「(.+?)」\s*$", re.MULTILINE)
    return [m.group(1) for m in pattern.finditer(text)]


def main() -> None:
    raw = TARGET.read_bytes()
    text = raw.decode("cp932")
    lines = text.splitlines()
    all_quotes = quote_lines(text)
    duplicate_counts = Counter(all_quotes)
    duplicates = [(q, n) for q, n in duplicate_counts.items() if n >= 2 and len(q) >= 8]

    add_start = text.index(";=== BOTAN RAND3 AND ADDITIONAL10 START ===")
    add_end = text.index("RETURN 0", add_start)
    added_quotes = quote_lines(text[add_start:add_end])
    added_dupes = [q for q, n in Counter(added_quotes).items() if n >= 2]
    starts = Counter(q[:4] for q in added_quotes)

    scene_checks = {
        280: "穴場シャワー室",
        281: "夜の旧校舎",
        282: "貸切露天の二人",
        283: "家庭科室の戯れ",
        284: "ケーキ屋の密会",
        410: "思い出の和菓子屋",
        411: "温泉饅頭デート",
        412: "海の思い出",
        413: "ケーキパーティ",
        414: "だらだら甘味三昧",
    }
    scene_ok = all(
        re.search(
            rf"^(?:IF|ELSEIF) SELECTCOM == {code}\s*$\n\s*;◆地の文（場面: {re.escape(scene)}）\s*$",
            text,
            re.MULTILINE,
        )
        for code, scene in scene_checks.items()
    )

    if_count = sum(line.lstrip().startswith("IF ") for line in lines)
    endif_count = sum(line.strip() == "ENDIF" for line in lines)
    empty_quotes = len(re.findall(r"PRINTFORM[LW]?\s+「」", text))
    print(f"CP932 roundtrip: {text.encode('cp932') == raw}")
    print(f"CRLF: {raw.count(bytes([13, 10]))} / LF: {raw.count(bytes([10]))}")
    print(f"IF: {if_count} / ENDIF: {endif_count}")
    print(f"halfwidth~: {text.count('~')} / empty quote: {empty_quotes}")
    print(f"all quote lines: {len(all_quotes)}")
    print(f"exact duplicates (len>=8): {len(duplicates)}")
    print(f"additional10 quote lines: {len(added_quotes)} / exact duplicates: {len(added_dupes)} / unique: {len(set(added_quotes))}")
    print(f"additional10 first-four-char counts: {starts.most_common(12)}")
    print(f"custom scene order: {scene_ok}")
    print(f"COM318 viewpoint correction present: {'撫でているうちに' in text and '撫でられているうちに' not in text}")
    if duplicates:
        for q, n in duplicates[:10]:
            print(f"DUP {n}: {q}")
    if added_dupes:
        for q in added_dupes:
            print(f"ADD_DUP: {q}")


if __name__ == "__main__":
    main()
