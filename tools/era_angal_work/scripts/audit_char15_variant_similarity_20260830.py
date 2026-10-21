"""CHAR15の同一RAND3内で、ほぼ同じ台詞が並ぶ箇所を洗い出す。"""

from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_15_長町やえ_COM.ERB"


def command_blocks(lines: list[str]):
    starts = [
        i for i, line in enumerate(lines)
        if line.strip().startswith(("IF SELECTCOM ==", "ELSEIF SELECTCOM =="))
    ]
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        match = re.search(r"SELECTCOM == (\d+)", lines[start])
        if match:
            yield int(match.group(1)), lines[start:end]


def rand_variants(block: list[str]):
    relation = None
    branch = None
    current: list[str] = []
    found = []

    def flush() -> None:
        nonlocal current
        text = "".join(current).strip()
        if relation and branch is not None and text:
            found.append((relation, branch, text))
        current = []

    for line in block:
        stripped = line.strip()
        indent = len(line) - len(line.lstrip("\t"))
        if stripped.startswith("IF TALENT:TARGET:153") and indent <= 1:
            flush()
            relation = "恋人"
            branch = None
            continue
        if stripped == "ELSE" and indent <= 1 and relation == "恋人":
            flush()
            relation = "通常"
            branch = None
            continue
        if stripped == "IF A == 0" and indent >= 2:
            flush()
            branch = 0
            continue
        if stripped == "ELSEIF A == 1" and indent >= 2:
            flush()
            branch = 1
            continue
        if stripped == "ELSE" and indent >= 2 and relation and branch is not None:
            flush()
            branch = 2
            continue
        if branch is not None and "PRINTFORM" in line:
            current.append(line.strip())
    flush()
    return found


def normalize(text: str) -> str:
    text = re.sub(r"PRINTFORM\w*", "", text)
    text = re.sub(r"%[^%]+%", "", text)
    text = text.replace("おに～さん", "").replace("あたし", "")
    text = re.sub(r"[「」♪☆。、！？…・ー～\s]", "", text)
    return re.sub(r"\s+", "", text)


def main() -> None:
    lines = TARGET.read_bytes().decode("cp932").splitlines()
    results = []
    for command, block in command_blocks(lines):
        variants = rand_variants(block)
        # COM318等の絶頂・複数条件ブロックはA分岐が多数あるため、
        # 恋人3種＋通常3種の単純RAND3ブロックだけを比較する。
        if len(variants) != 6:
            continue
        if sorted((relation, branch) for relation, branch, _ in variants) != sorted(
            [("恋人", 0), ("恋人", 1), ("恋人", 2), ("通常", 0), ("通常", 1), ("通常", 2)]
        ):
            continue
        for i, (relation, branch, left) in enumerate(variants):
            for relation2, branch2, right in variants[i + 1:]:
                if relation != relation2:
                    continue
                ratio = SequenceMatcher(None, normalize(left), normalize(right)).ratio()
                # 「単語を少し替えただけ」を拾うため、前回より厳しく見る。
                if ratio >= 0.45:
                    results.append((ratio, command, relation, branch, branch2, left, right))
    results.sort(reverse=True)
    print(f"近似候補: {len(results)}件")
    for ratio, command, relation, branch, branch2, left, right in results[:200]:
        print(f"COM{command} {relation} A{branch}/A{branch2} similarity={ratio:.3f}")
        print(f"  A{branch}: {left}")
        print(f"  A{branch2}: {right}")


if __name__ == "__main__":
    main()
