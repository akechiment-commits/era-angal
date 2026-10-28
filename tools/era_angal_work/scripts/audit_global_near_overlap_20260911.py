"""全CHARの同一COM間で、完全一致以外の高類似口上を抽出する。"""

from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
import re
import sys


sys.stdout.reconfigure(encoding="utf-8")


ROOT = Path(__file__).resolve().parents[3]
CHAR_DIR = ROOT / "ERB" / "CHAR"


def normalize(value: str) -> str:
    value = re.sub(r"%[^%]+%", "%X%", value)
    return re.sub(r"[「」。、，．！？!?♪☆…～〜ー・（）()\s]", "", value)


def difference_size(left: str, right: str) -> int:
    matcher = SequenceMatcher(None, left, right, autojunk=False)
    return sum(
        max(i2 - i1, j2 - j1)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes()
        if tag != "equal"
    )


def collect() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(CHAR_DIR.glob("CHAR_*_COM.ERB")):
        text = path.read_bytes().decode("cp932")
        com = "?"
        for line_no, line in enumerate(text.splitlines(), 1):
            match = re.match(r"IF SELECTCOM == (\d+)", line)
            if match:
                com = match.group(1)
            for dialogue in re.findall(r"PRINTFORM(?:L|W)?\s+「([^」]{16,})」", line):
                rows.append(
                    {
                        "file": path.name,
                        "com": com,
                        "line": line_no,
                        "text": dialogue,
                        "norm": normalize(dialogue),
                    }
                )
    return rows


def main() -> None:
    rows = collect()
    by_com: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_com.setdefault(str(row["com"]), []).append(row)

    candidates: list[tuple[float, dict[str, object], dict[str, object]]] = []
    for com, group in by_com.items():
        shingles: dict[str, list[int]] = defaultdict(list)
        for index, row in enumerate(group):
            norm = str(row["norm"])
            if len(norm) < 18:
                continue
            for shingle in {norm[offset : offset + 4] for offset in range(len(norm) - 3)}:
                shingles[shingle].append(index)

        pair_overlap: Counter[tuple[int, int]] = Counter()
        for indexes in shingles.values():
            for left_pos, left_index in enumerate(indexes):
                for right_index in indexes[left_pos + 1 :]:
                    if group[left_index]["file"] == group[right_index]["file"]:
                        continue
                    pair = tuple(sorted((left_index, right_index)))
                    pair_overlap[pair] += 1

        for (left_index, right_index), shared in pair_overlap.items():
            if shared < 4:
                continue
            left = group[left_index]
            right = group[right_index]
            left_norm = str(left["norm"])
            right_norm = str(right["norm"])
            if left_norm == right_norm:
                continue
            ratio = SequenceMatcher(None, left_norm, right_norm, autojunk=False).ratio()
            if ratio >= 0.85:
                candidates.append((ratio, left, right))

    candidates.sort(key=lambda item: (-item[0], str(item[1]["file"]), int(item[1]["line"])))
    print("FILES", len({row["file"] for row in rows}))
    print("DIALOGUE_ROWS", len(rows))
    significant = [
        item
        for item in candidates
        if item[0] >= 0.88 and difference_size(str(item[1]["norm"]), str(item[2]["norm"])) >= 5
    ]
    requested_pairs = None
    if len(sys.argv) > 1 and (len(sys.argv) - 1) % 2 == 0:
        requested_pairs = {
            tuple(sorted(sys.argv[offset : offset + 2]))
            for offset in range(1, len(sys.argv), 2)
        }
        significant = [
            item
            for item in significant
            if tuple(sorted((str(item[1]["file"])[5:7], str(item[2]["file"])[5:7])))
            in requested_pairs
        ]
    pair_summary: dict[tuple[str, str], list[float]] = defaultdict(list)
    for ratio, left, right in significant:
        pair = tuple(sorted((str(left["file"]), str(right["file"]))))
        pair_summary[pair].append(ratio)
    print("CANDIDATES_GE_085", len(candidates))
    print("SIGNIFICANT_GE_088_DIFF_GE_5", len(significant))
    print("SIGNIFICANT_PAIR_SUMMARY")
    for pair, ratios in sorted(pair_summary.items(), key=lambda item: (-len(item[1]), -max(item[1]), item[0])):
        print(f"  {len(ratios)} MAX {max(ratios):.4f} {pair[0]} || {pair[1]}")
    for ratio, left, right in significant[:200]:
        print(
            f"RATIO {ratio:.4f} COM {left['com']} "
            f"{left['file']}:{left['line']} || {right['file']}:{right['line']}"
        )
        print(f"  A {left['text']}")
        print(f"  B {right['text']}")


if __name__ == "__main__":
    main()
