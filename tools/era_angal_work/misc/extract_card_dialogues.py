#!/usr/bin/env python3
"""Extract card-specific comments and memos from the local kmskwiki mirror.

The mirror contains both the normal card pages (e.g. ``972.html``) and
duplicated backlink pages (e.g. ``9722271.html`` / ``972decf.html``).  This
script keeps only the page whose filename matches the ``No.`` in its title.
"""

from __future__ import annotations

import argparse
import html
import re
from collections import OrderedDict
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


WIKI_TITLE_RE = re.compile(
    r"<title>\s*No\.(\d+)\s*(.*?)\s*\[あんガルDB補完Wiki\]",
    re.IGNORECASE | re.DOTALL,
)


@dataclass
class Card:
    number: int
    display_name: str
    character: str
    skill_name: str
    skill_effect: str
    attribute: str
    memo: str
    comments: OrderedDict[str, str]


class TableParser(HTMLParser):
    """Collect table rows while retaining enough structure for the comment table."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self._table: list[list[str]] | None = None
        self._row: list[str] | None = None
        self._cell: list[str] | None = None
        self._cell_tag: str | None = None

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        tag = tag.lower()
        if tag == "table":
            if self._table is None:
                self._table = []
            return
        if self._table is not None and tag == "tr":
            self._row = []
            return
        if self._row is not None and tag in {"th", "td"}:
            self._cell = []
            self._cell_tag = tag
            return
        if self._cell is not None and tag == "br":
            self._cell.append("\n")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if self._cell is not None and tag == self._cell_tag:
            assert self._row is not None
            self._row.append("".join(self._cell))
            self._cell = None
            self._cell_tag = None
            return
        if self._row is not None and tag == "tr":
            assert self._table is not None
            self._table.append(self._row)
            self._row = None
            return
        if self._table is not None and tag == "table":
            self.tables.append(self._table)
            self._table = None

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)


def clean(value: str) -> str:
    value = html.unescape(value).replace("\xa0", " ")
    # HTML indentation is not part of the dialogue; preserve explicit BRs.
    lines = [re.sub(r"[ \t\r\f\v]+", " ", line).strip() for line in value.split("\n")]
    lines = [line for line in lines if line]
    return "\n".join(lines)


def parse_page(path: Path) -> Card | None:
    source = path.read_text(encoding="utf-8", errors="replace")
    match = WIKI_TITLE_RE.search(source)
    if not match:
        return None

    number = int(match.group(1))
    if path.stem != str(number):
        return None

    display_name = clean(match.group(2))
    character = display_name
    if display_name.startswith("[") and "]" in display_name:
        character = display_name.split("]", 1)[1].strip()

    parser = TableParser()
    parser.feed(source)
    skill_name = ""
    skill_effect = ""
    attribute = ""
    memo = ""
    comment_table: list[list[str]] | None = None
    for table in parser.tables:
        for row in table:
            cells = [clean(cell) for cell in row]
            for index in range(0, len(cells) - 1, 2):
                label, value = cells[index], cells[index + 1]
                if label == "スキル":
                    skill_lines = [line for line in value.split("\n") if line]
                    skill_name = skill_lines[0] if skill_lines else ""
                    skill_effect = "\n".join(skill_lines[1:])
                elif label == "属性":
                    attribute = value
                elif label == "メモ":
                    memo = value
        if any("コメント" in clean(cell) for row in table for cell in row):
            comment_table = table
            break
    if comment_table is None:
        return Card(
            number, display_name, character, skill_name, skill_effect,
            attribute, memo, OrderedDict()
        )

    comments: OrderedDict[str, str] = OrderedDict()
    wanted = {"通常", "開花", "熟練度最大"}
    for row in comment_table:
        cells = [clean(cell) for cell in row]
        if len(cells) >= 2 and cells[0] in wanted:
            comments[cells[0]] = cells[1]
    return Card(
        number, display_name, character, skill_name, skill_effect,
        attribute, memo, comments
    )


def extract(wiki_card_dir: Path) -> list[Card]:
    cards: list[Card] = []
    for path in wiki_card_dir.glob("*.html"):
        if not path.stem.isdigit():
            continue
        card = parse_page(path)
        if card is not None:
            cards.append(card)
    return sorted(cards, key=lambda card: card.number)


def load_character_names() -> OrderedDict[str, int]:
    """Load the project's canonical character names, if the repo is available."""
    names: OrderedDict[str, int] = OrderedDict()
    csv_dir = Path(__file__).resolve().parents[1] / "CSV"
    for path in csv_dir.glob("Chara*_*.csv"):
        match = re.match(r"Chara(\d+)_(.+)\.csv$", path.name)
        if match:
            names[match.group(2)] = int(match.group(1))
    return names


def character_group(card: Card, known_names: OrderedDict[str, int]) -> str | None:
    """Return an individual owner, or None for a shared/group card."""
    if card.character in known_names:
        return card.character
    match = re.search(r"\(([^()]+)\)$", card.character)
    if match and match.group(1) in known_names:
        return match.group(1)
    return None


def format_ranges(numbers: list[int]) -> str:
    """Format sorted integers as compact ranges."""
    if not numbers:
        return "なし"
    ranges: list[str] = []
    start = previous = numbers[0]
    for number in numbers[1:]:
        if number == previous + 1:
            previous = number
            continue
        ranges.append(str(start) if start == previous else f"{start}〜{previous}")
        start = previous = number
    ranges.append(str(start) if start == previous else f"{start}〜{previous}")
    return ", ".join(ranges)


def render(cards: list[Card], source_dir: Path) -> str:
    known_names = load_character_names()
    groups: OrderedDict[str, list[Card]] = OrderedDict()
    shared: list[Card] = []
    for card in cards:
        group = character_group(card, known_names)
        if group is None:
            shared.append(card)
        else:
            groups.setdefault(group, []).append(card)

    groups = OrderedDict(
        sorted(groups.items(), key=lambda item: known_names.get(item[0], 10**9))
    )
    labels = ("通常", "開花", "熟練度最大")
    populated = sum(1 for card in cards for label in labels if card.comments.get(label))
    empty_cards = sum(not any(card.comments.get(label) for label in labels) for card in cards)
    populated_skills = sum(bool(card.skill_name) for card in cards)
    populated_attributes = sum(bool(card.attribute) for card in cards)
    populated_memos = sum(bool(card.memo) for card in cards)
    card_numbers = [card.number for card in cards]
    missing_numbers = [number for number in range(1, max(card_numbers) + 1)
                       if number not in set(card_numbers)]

    lines = [
        "# カード付属台詞（Wiki抽出）",
        "",
        f"- 対象: `{source_dir}`",
        f"- 対象カードページ: {len(cards)}件",
        f"- 番号範囲: No.1〜No.{max(card_numbers)}（欠番 {len(missing_numbers)}件: {format_ranges(missing_numbers)}）",
        f"- 台詞欄: {len(cards) * len(labels)}枠（非空 {populated}枠、全枠空欄 {empty_cards}件）",
        f"- スキル名欄: {len(cards)}件（非空 {populated_skills}件）",
        f"- 属性欄: {len(cards)}件（非空 {populated_attributes}件）",
        f"- メモ欄: {len(cards)}件（非空 {populated_memos}件）",
        "- 抽出対象: 各個別ページの「コメント」欄（通常／開花／熟練度最大）",
        "- 各個別ページの「スキル」欄からスキル名・効果を分離して併記",
        "- 各個別ページの「属性」欄もカードごとに併記",
        "- 各個別ページの「メモ」欄もカードごとに併記",
        "- `*2271.html`、`*decf.html` などの重複・バックリンクHTMLは除外",
        "- 括弧内に個人名がある合同カードは、その個人名のキャラ欄へ分類",
        "- 個人名を特定できない部活・合同カードは「共通・複数キャラ」へ分類",
        "- 空欄はWiki上で未登録のため `（空欄）` と表記",
        "",
    ]

    for character, character_cards in groups.items():
        lines.extend([f"## {character}", ""])
        for card in character_cards:
            lines.extend([f"### No.{card.number} {card.display_name}", ""])
            skill_name = card.skill_name or "（空欄）"
            skill_effect = card.skill_effect.replace("\n", "<br>") if card.skill_effect else "（空欄）"
            attribute = card.attribute or "（空欄）"
            lines.append(f"- スキル名: {skill_name}")
            lines.append(f"- スキル効果: {skill_effect}")
            lines.append(f"- 属性: {attribute}")
            memo = card.memo.replace("\n", "<br>") if card.memo else "（空欄）"
            lines.append(f"- メモ: {memo}")
            for label in ("通常", "開花", "熟練度最大"):
                value = card.comments.get(label, "") or "（空欄）"
                value = value.replace("\n", "<br>")
                lines.append(f"- {label}: {value}")
            lines.append("")

    if shared:
        lines.extend(["## 共通・複数キャラ", ""])
        for card in shared:
            lines.extend([f"### No.{card.number} {card.display_name}", ""])
            skill_name = card.skill_name or "（空欄）"
            skill_effect = card.skill_effect.replace("\n", "<br>") if card.skill_effect else "（空欄）"
            attribute = card.attribute or "（空欄）"
            lines.append(f"- スキル名: {skill_name}")
            lines.append(f"- スキル効果: {skill_effect}")
            lines.append(f"- 属性: {attribute}")
            memo = card.memo.replace("\n", "<br>") if card.memo else "（空欄）"
            lines.append(f"- メモ: {memo}")
            for label in ("通常", "開花", "熟練度最大"):
                value = card.comments.get(label, "") or "（空欄）"
                value = value.replace("\n", "<br>")
                lines.append(f"- {label}: {value}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("wiki_card_dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    cards = extract(args.wiki_card_dir)
    text = render(cards, args.wiki_card_dir)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")

    known_names = load_character_names()
    groups = {character_group(card, known_names) for card in cards}
    groups.discard(None)
    shared = sum(character_group(card, known_names) is None for card in cards)
    populated_skills = sum(bool(card.skill_name) for card in cards)
    populated_attributes = sum(bool(card.attribute) for card in cards)
    populated_memos = sum(bool(card.memo) for card in cards)
    card_numbers = [card.number for card in cards]
    missing_numbers = [number for number in range(1, max(card_numbers) + 1)
                       if number not in set(card_numbers)]
    populated = sum(
        1 for card in cards for label in ("通常", "開花", "熟練度最大")
        if card.comments.get(label)
    )
    print(
        f"\n[summary] cards={len(cards)} groups={len(groups)} "
        f"shared_cards={shared} populated_comments={populated} "
        f"populated_skills={populated_skills} "
        f"populated_attributes={populated_attributes} populated_memos={populated_memos} "
        f"missing_numbers={format_ranges(missing_numbers)}",
        file=__import__("sys").stderr,
    )


if __name__ == "__main__":
    main()
