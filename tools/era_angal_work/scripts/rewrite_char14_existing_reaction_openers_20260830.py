"""CHAR14既存台詞の過密な反応音を、原作寄りの自然な発声へ分散する。"""

from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "ERB/CHAR/CHAR_14_花音ことり_COM.ERB"
SOURCE = ROOT / "tools/backups/CHAR14_before_rand3_20260829/CHAR_14_花音ことり_COM.ERB"
BEFORE = ROOT / "tools/backups/CHAR14_before_existing_interjection_20260830/CHAR_14_花音ことり_COM.ERB"
BACKUP = ROOT / "tools/backups/CHAR14_before_existing_reaction_openers_20260830/CHAR_14_花音ことり_COM.ERB"


TOKENS = ("ふああっ", "ふあぁっ", "ふあぅ", "ん゛っ", "んむっ", "ん……っ", "ふあっ", "ひっ", "んむ", "ふあ")
CANDIDATES = {
    "ん゛っ": ("あっ", "んっ", "ひゃっ", "はぁ", "ふぅ", "あぁっ", "うぅ", "ひゃあっ"),
    "ふあ": ("あっ", "んっ", "ひゃっ", "あぁっ", "はぁ", "ふぅ", "うぅ", "ひゃあっ"),
    "ふあぅ": ("あっ", "んっ", "ひゃっ", "あぁっ", "はぁ", "ふぅ", "うぅ", "ひゃあっ"),
    "ふあっ": ("あっ", "んっ", "ひゃっ", "あぁっ", "はぁ", "ふぅ", "うぅ", "ひゃあっ"),
    "ふああっ": ("あっ", "んっ", "ひゃっ", "あぁっ", "はぁ", "ふぅ", "うぅ", "ひゃあっ"),
    "ふあぁっ": ("あっ", "んっ", "ひゃっ", "あぁっ", "はぁ", "ふぅ", "うぅ", "ひゃあっ"),
    "ひっ": ("あっ", "んっ", "ひゃっ", "あぁっ", "はぁ", "ふぅ", "うぅ", "ひゃあっ"),
    "んむ": ("んっ", "あっ", "ひゃっ", "はぁ", "ふぅ", "うぅ"),
    "んむっ": ("んっ", "あっ", "ひゃっ", "はぁ", "ふぅ", "うぅ"),
    "ん……っ": ("あっ", "んっ", "はぁ", "ふぅ"),
}


def read_lines(path: Path) -> list[str]:
    return path.read_bytes().decode("cp932").splitlines()


def write_lines(path: Path, lines: list[str]) -> None:
    path.write_bytes("\r\n".join(lines).encode("cp932") + b"\r\n")


def normalize(line: str) -> str:
    return line.lstrip().replace("%CALLNAME:ASSI%", "%LOCALS%")


def original_token(line: str) -> str | None:
    text = normalize(line)
    start = text.find("「")
    if start < 0:
        return None
    for token in TOKENS:
        if text.startswith("「" + token, start):
            return token
    return None


def align_original_to_before(original: list[str], before: list[str]) -> dict[int, int]:
    # 既存RAND3化で構造行が変わった箇所はあるため、対象台詞だけを順番に照合する。
    mapping: dict[int, int] = {}
    before_index = 0
    for original_index, original_line in enumerate(original):
        if original_token(original_line) is None:
            continue
        wanted = normalize(original_line)
        search_index = before_index
        while search_index < len(before) and normalize(before[search_index]) != wanted:
            search_index += 1
        if search_index == len(before):
            # 前回の助手参加枠の全台詞置換など、既に現行から消えた旧行は対象外。
            continue
        mapping[original_index] = search_index
        before_index = search_index + 1
    return mapping


def main() -> None:
    if not SOURCE.exists() or not BEFORE.exists():
        raise RuntimeError("既存部分の基準バックアップがありません")
    original = read_lines(SOURCE)
    before = read_lines(BEFORE)
    current = read_lines(TARGET)
    mapping = align_original_to_before(original, before)
    counters: dict[str, int] = {token: 0 for token in TOKENS}
    selected = [(i, original_token(line)) for i, line in enumerate(original)]
    selected = [(i, token) for i, token in selected if token is not None]
    missing = [i + 1 for i, _ in selected if i not in mapping]
    if missing:
        print(f"現行で既に置換済みの旧行は対象外: {missing}")
        selected = [(i, token) for i, token in selected if i in mapping]

    changed = 0
    for original_index, token in selected:
        current_index = mapping[original_index]
        current_line = current[current_index]
        current_text = normalize(current_line)
        start = current_text.find("「")
        if start < 0 or not current_text.startswith("「" + token, start):
            continue
        options = CANDIDATES[token]
        replacement = options[counters[token] % len(options)]
        counters[token] += 1
        indent = current_line[: len(current_line) - len(current_text)]
        current[current_index] = indent + current_text[:start] + "「" + replacement + current_text[start + 1 + len(token) :]
        changed += 1

    if changed:
        BACKUP.parent.mkdir(parents=True, exist_ok=True)
        if not BACKUP.exists():
            shutil.copy2(TARGET, BACKUP)
        write_lines(TARGET, current)
    print(f"既存台詞の反応音をリライト: {changed}件")


if __name__ == "__main__":
    main()
