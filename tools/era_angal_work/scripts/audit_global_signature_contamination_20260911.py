"""原作で特定キャラに偏る語が、別CHARの現行COMへ混入していないか調べる。"""

from collections import Counter, defaultdict
from pathlib import Path
import re
import sys


sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3]
CHAR_DIR = ROOT / "ERB" / "CHAR"
SOURCE_DIR = ROOT / "tools" / "output"


def load_source_map() -> dict[str, Path]:
    sources: dict[str, Path] = {}
    for path in SOURCE_DIR.glob("*.txt"):
        if "_" in path.stem or "・" in path.stem or "＆" in path.stem:
            continue
        try:
            first = path.read_text(encoding="utf-8").splitlines()[0]
        except (UnicodeDecodeError, IndexError):
            continue
        if first.startswith("# "):
            sources[path.stem] = path
    return sources


def char_source(path: Path, sources: dict[str, Path]) -> Path | None:
    stem = path.stem.removesuffix("_COM")
    name = re.sub(r"^CHAR_\d+_", "", stem)
    candidates = [source for source_name, source in sources.items() if source_name in name]
    return max(candidates, key=lambda source: len(source.stem), default=None)


def source_dialogues(path: Path) -> list[str]:
    rows: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\[\d+\]\s*(?:「(.+)」|(.+))$", line)
        if match:
            rows.append(match.group(1) or match.group(2))
    return rows


def current_dialogues(path: Path) -> list[str]:
    text = path.read_bytes().decode("cp932")
    return re.findall(r"PRINTFORM(?:L|W)?\s+「([^」]+)」", text)


def signature_counts(rows: list[str], n: int) -> Counter[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        clean = re.sub(r"[%\dA-Za-z_\-]", "", row)
        clean = re.sub(r"[\s、。，．！？!?♪☆…～〜ー・（）()「」『』【】]", "", clean)
        seen = {clean[offset : offset + n] for offset in range(len(clean) - n + 1)}
        counts.update(piece for piece in seen if re.fullmatch(r"[ぁ-んァ-ヶ一-龠々ー]+", piece))
    return counts


def main() -> None:
    sources = load_source_map()
    source_rows: dict[str, list[str]] = {}
    current_rows: dict[str, list[str]] = {}
    source_paths: dict[str, Path] = {}
    for current in sorted(CHAR_DIR.glob("CHAR_*_COM.ERB")):
        source = char_source(current, sources)
        if source is None:
            continue
        key = current.name
        source_paths[key] = source
        source_rows[key] = source_dialogues(source)
        current_rows[key] = current_dialogues(current)

    # 原作で「そのキャラに偏る」4〜6文字の連続語を署名語とする。
    by_length: dict[int, dict[str, Counter[str]]] = {}
    for n in (4, 5, 6):
        by_length[n] = {key: signature_counts(rows, n) for key, rows in source_rows.items()}

    signatures: list[tuple[str, str, int, int, str]] = []
    for n, per_char in by_length.items():
        for owner, counts in per_char.items():
            for phrase, owner_count in counts.items():
                if owner_count < 3:
                    continue
                other_source_chars = sum(
                    1 for other, other_counts in per_char.items() if other != owner and other_counts[phrase] >= 2
                )
                if other_source_chars > 1:
                    continue
                signatures.append((phrase, owner, owner_count, n, source_paths[owner].stem))

    # 長い語を先に出す。同じ語の部分文字列も別の尺度として残す。
    selected = sorted(signatures, key=lambda item: (-item[3], -item[2], item[0], item[1]))

    current_counts_by_length = {
        n: {key: signature_counts(rows, n) for key, rows in current_rows.items()}
        for n in (4, 5, 6)
    }
    if "--own-absent" in sys.argv:
        only = set()
        if "--only" in sys.argv:
            position = sys.argv.index("--only")
            if position + 1 < len(sys.argv):
                only = set(sys.argv[position + 1].split(","))
        for current in sorted(current_rows):
            if only and current[5:7] not in only:
                continue
            absent = [
                (count, phrase)
                for phrase, count in current_counts_by_length[4][current].items()
                if count >= 10 and by_length[4][current][phrase] == 0
            ]
            print(f"=== {current} ===")
            for count, phrase in sorted(absent, reverse=True)[:20]:
                print(f"{phrase}: current={count}")
        return
    if "--core" in sys.argv:
        terms = [
            "きみ", "あなた", "転校生くん", "転校生さん", "お兄ちゃん先輩", "おに～さん",
            "ですぅ", "ますぅ", "ですよぉ", "ですねぇ", "よぉ", "ふむ", "実験", "園芸",
            "採点", "興味深い", "はうう", "わさ", "にゃはは", "るるる", "っす", "ですのぉ",
        ]
        for current in sorted(current_rows):
            source_text = "\n".join(source_rows[current])
            current_text = "\n".join(current_rows[current])
            findings = []
            for term in terms:
                source_count = source_text.count(term)
                current_count = current_text.count(term)
                if current_count >= 10 and (source_count == 0 or current_count >= source_count * 3):
                    findings.append((current_count, source_count, term))
            if findings:
                print(f"=== {current} ===")
                for current_count, source_count, term in sorted(findings, reverse=True):
                    print(f"{term}: current={current_count} source={source_count}")
        return
    findings: list[tuple[int, float, str, str, int, int, str]] = []
    for phrase, owner, owner_source_count, n, owner_name in selected:
        for current, rows in current_rows.items():
            if current == owner:
                continue
            current_count = current_counts_by_length[n][current][phrase]
            if current_count < 5:
                continue
            own_source_count = by_length[n][current][phrase]
            ratio = current_count / max(1, len(rows))
            findings.append((current_count, ratio, current, phrase, owner_source_count, own_source_count, owner_name))

    findings.sort(key=lambda item: (-item[0], -item[1], item[2], item[3]))
    print("CHAR_FILES", len(current_rows))
    print("SIGNATURES", len(selected))
    print("CROSS_FINDINGS", len(findings))
    for count, ratio, current, phrase, owner_source_count, own_source_count, owner_name in findings[:200]:
        print(
            f"{current} <- {owner_name}: {phrase} current={count} "
            f"source_owner={owner_source_count} source_self={own_source_count} "
            f"current_ratio={ratio:.4%}"
        )


if __name__ == "__main__":
    main()
