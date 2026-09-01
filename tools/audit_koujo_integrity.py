#!/usr/bin/env python3
"""口上編集の構造・視点契約・注釈を横断監査する。

目的は、会話のコンテキストが圧縮されても再発しやすい次の事故を機械的に止めること。

* RAND:3 の分岐欠落・同一分岐の重複
* 追加10コマンド／独自10コマンドの枠欠落
* 双頭バイブ等、助手参加が必要な枠の %LOCALS% 欠落
* コマンド注釈の削除・改名、既存枠の消失
* 空台詞・CP932以外・LF混入・同一台詞の重複

使い方:
  python tools/audit_koujo_integrity.py
  python tools/audit_koujo_integrity.py --char 61 --require-spec --strict
  python tools/audit_koujo_integrity.py --write-manifest
  python tools/audit_koujo_integrity.py --duplicates
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parent.parent
CHAR_DIR = ROOT / "ERB" / "CHAR"
CONTRACTS_PATH = ROOT / "tools" / "koujo_integrity_contracts.json"
DEFAULT_MANIFEST = ROOT / "tools" / "koujo_manifest.json"
SPEC_DIR = ROOT / "tools" / "koujo_specs"

SELECTOR_RE = re.compile(r"^\s*IF\s+SELECTCOM\s*==\s*(\d+)", re.I)
SELECTOR_ELSEIF_RE = re.compile(r"^\s*ELSEIF\s+SELECTCOM\s*==\s*(\d+)", re.I)
RANGE_RE = re.compile(
    r"^\s*IF\s+SELECTCOM\s*>=\s*(\d+)\s*&&\s*SELECTCOM\s*<=\s*(\d+)", re.I
)
RAND_RE = re.compile(r"\bRAND\s*:\s*(\d+)", re.I)
PRINT_RE = re.compile(r"^\s*PRINTFORM(?:L|W)?\b", re.I)
ANNOTATION_RE = re.compile(r"\bCOM\s*(\d+)(?:\s*-\s*(\d+))?\b", re.I)


@dataclass(frozen=True)
class CommandBlock:
    number: int
    start: int
    end: int
    lines: tuple[str, ...]
    annotation: str | None

    @property
    def body(self) -> str:
        return "\n".join(self.lines)

    @property
    def prints(self) -> tuple[str, ...]:
        return tuple(
            line.strip()
            for line in self.lines
            if PRINT_RE.match(code_part(line)) and not line.lstrip().startswith(";")
        )


@dataclass
class AuditReport:
    errors: list[str]
    warnings: list[str]
    notes: list[str]

    def __init__(self) -> None:
        self.errors = []
        self.warnings = []
        self.notes = []


def code_part(line: str) -> str:
    if line.lstrip().startswith(";"):
        return ""
    return line.split(";", 1)[0]


def read_cp932(path: Path) -> str:
    return path.read_bytes().decode("cp932")


def char_files() -> list[Path]:
    return sorted(
        path
        for path in CHAR_DIR.glob("CHAR_*_COM.ERB")
        if "TEMPLATE" not in path.name
    )


def char_number(path: Path) -> int:
    match = re.match(r"CHAR_(\d+)_", path.name)
    if not match:
        raise ValueError(f"キャラ番号を読めません: {path.name}")
    return int(match.group(1))


def line_opens_if(line: str) -> bool:
    code = code_part(line).strip()
    return bool(re.match(r"^IF(?:\s|\()", code, re.I))


def line_closes_if(line: str) -> bool:
    return bool(re.match(r"^\s*ENDIF\b", code_part(line), re.I))


def matching_end(lines: list[str], start: int) -> int:
    depth = 0
    for index in range(start, len(lines)):
        if line_opens_if(lines[index]):
            depth += 1
        if line_closes_if(lines[index]):
            depth -= 1
            if depth == 0:
                return index
    return len(lines) - 1


def annotation_before(lines: list[str], start: int, number: int) -> str | None:
    for line in reversed(lines[max(0, start - 40) : start]):
        stripped = line.strip()
        if not stripped.startswith(";"):
            continue
        for match in ANNOTATION_RE.finditer(stripped):
            first = int(match.group(1))
            last = int(match.group(2) or first)
            if first <= number <= last:
                return stripped
    return None


def extract_blocks(text: str) -> dict[int, CommandBlock]:
    lines = text.replace("\r\n", "\n").split("\n")
    exact: dict[int, CommandBlock] = {}
    stack: list[int] = []
    spans: dict[int, int] = {}
    selectors: list[tuple[int, int, int]] = []
    ranges: list[tuple[int, int, int]] = []

    # ELSEIF SELECTCOM branches (notably COM280-284 and COM410-414) belong to
    # the opening IF's block. Keep the owner IF while walking the nesting stack.
    for index, line in enumerate(lines):
        code = code_part(line)
        exact_match = SELECTOR_RE.match(code)
        elseif_match = SELECTOR_ELSEIF_RE.match(code)
        range_match = RANGE_RE.match(code)
        if exact_match:
            selectors.append((int(exact_match.group(1)), index, index))
        elif elseif_match:
            owner = stack[-1] if stack else index
            selectors.append((int(elseif_match.group(1)), owner, index))
        if range_match:
            ranges.append((int(range_match.group(1)), int(range_match.group(2)), index))

        if line_opens_if(line):
            stack.append(index)
        elif line_closes_if(line) and stack:
            spans[stack.pop()] = index

    for number, owner, selector_line in selectors:
        end = spans.get(owner)
        if end is None:
            end = matching_end(lines, owner)
        exact.setdefault(
            number,
            CommandBlock(
                number,
                owner,
                end,
                tuple(lines[owner : end + 1]),
                annotation_before(lines, owner, number),
            ),
        )

    # Some legacy files have only a range guard and no nested exact selector.
    # Use the range as a fallback, but prefer a precise selector when present.
    for first, last, owner in ranges:
        end = spans.get(owner, matching_end(lines, owner))
        for number in range(first, last + 1):
            if number in exact:
                continue
            exact[number] = CommandBlock(
                number,
                owner,
                end,
                tuple(lines[owner : end + 1]),
                annotation_before(lines, owner, number),
            )
    return exact


def load_contracts() -> dict:
    return json.loads(CONTRACTS_PATH.read_text(encoding="utf-8"))


def command_ids(contract: dict, key: str) -> list[int]:
    values: list[int] = []
    for raw in contract.get(key, {}):
        if "-" in raw:
            first, last = (int(part) for part in raw.split("-", 1))
            values.extend(range(first, last + 1))
        else:
            values.append(int(raw))
    return sorted(set(values))


def normalize_print(line: str) -> str:
    value = re.sub(r"^\s*PRINTFORM(?:L|W)?\s*", "", line, flags=re.I)
    value = value.replace("「", "").replace("」", "")
    value = re.sub(r"\s+", "", value)
    return value


def rand3_problems(block: CommandBlock) -> list[str]:
    problems: list[str] = []
    lines = list(block.lines)
    positions = [index for index, line in enumerate(lines) if re.search(r"\bRAND\s*:\s*3\b", code_part(line), re.I)]
    for position in positions:
        next_position = next((candidate for candidate in positions if candidate > position), len(lines))
        segment = "\n".join(lines[position:next_position])
        if not re.search(r"^\s*IF\s+A\s*==\s*0", segment, re.I | re.M):
            problems.append("A==0分岐なし")
        if not re.search(r"^\s*ELSEIF\s+A\s*==\s*1", segment, re.I | re.M):
            problems.append("A==1分岐なし")
        if not re.search(r"^\s*ELSE(?:IF\s+A\s*==\s*2)?\b", segment, re.I | re.M):
            problems.append("A==2またはELSE分岐なし")
    return problems


def build_manifest(files: list[Path]) -> dict:
    entries: dict[str, dict] = {}
    for path in files:
        blocks = extract_blocks(read_cp932(path))
        entries[path.name] = {
            "commands": {
                str(number): block.annotation for number, block in sorted(blocks.items())
            }
        }
    return {"version": 1, "files": entries}


def compare_manifest(current: dict, baseline: dict, report: AuditReport) -> None:
    for filename, old_entry in baseline.get("files", {}).items():
        current_entry = current.get("files", {}).get(filename)
        if current_entry is None:
            report.errors.append(f"マニフェスト基準ファイルが消失: {filename}")
            continue
        old_commands = old_entry.get("commands", {})
        new_commands = current_entry.get("commands", {})
        for number, old_annotation in old_commands.items():
            if number not in new_commands:
                report.errors.append(f"{filename}: 既存COM{number}枠が消失")
            elif new_commands[number] != old_annotation:
                report.errors.append(f"{filename}: COM{number}の注釈が変更・消失")


def spec_for(number: int) -> Path | None:
    matches = sorted(SPEC_DIR.glob(f"CHAR_{number:02d}_*.json"))
    return matches[0] if matches else None


def load_spec(path: Path | None) -> dict | None:
    if path is None:
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"仕様表を読めません: {path}: {exc}") from exc


def audit_file(
    path: Path,
    contract: dict,
    report: AuditReport,
    detail: bool,
    enforce_contract: bool,
    audit_rand_missing: bool,
    spec: dict | None,
) -> None:
    filename = path.name
    try:
        raw = path.read_bytes()
        text = raw.decode("cp932")
    except UnicodeDecodeError as exc:
        report.errors.append(f"{filename}: CP932で読めない: {exc}")
        return

    if b"\n" in raw.replace(b"\r\n", b""):
        report.errors.append(f"{filename}: lone LF改行")

    blocks = extract_blocks(text)
    if not blocks:
        report.errors.append(f"{filename}: SELECTCOMブロックなし")
        return

    expected_additional = command_ids(contract, "additional_commands")
    expected_custom = command_ids(contract, "custom_commands")

    for number in expected_additional + expected_custom:
        if number not in blocks:
            target = report.errors if enforce_contract else report.warnings
            target.append(f"{filename}: 必須COM{number}枠がない")

    for number, block in sorted(blocks.items()):
        if block.annotation is None:
            report.errors.append(f"{filename}: COM{number}の注釈がない")

        if any("「」" in line for line in block.prints):
            report.errors.append(f"{filename}: COM{number}に空台詞がある")

        rand_values = sorted(set(int(value) for value in RAND_RE.findall(block.body)))
        if 3 in rand_values:
            for problem in rand3_problems(block):
                report.errors.append(f"{filename}: COM{number} RAND:3 {problem}")
        elif not rand_values and block.prints and (audit_rand_missing or number in expected_additional + expected_custom):
            report.warnings.append(f"{filename}: COM{number} RANDなし（必要性を確認）")

        normalized = [normalize_print(line) for line in block.prints]
        duplicates = sorted({line for line in normalized if line and normalized.count(line) > 1})
        if duplicates:
            report.errors.append(f"{filename}: COM{number}内に同一台詞重複 {len(duplicates)}件")

        if spec:
            forbidden = spec.get("voice", {}).get("forbidden_patterns", [])
            for pattern in forbidden:
                if pattern and pattern in block.body:
                    target = report.errors if enforce_contract else report.warnings
                    target.append(f"{filename}: COM{number}に仕様表の禁止表現が残る: {pattern}")

        contract_entry = contract.get("additional_commands", {}).get(str(number))
        if contract_entry:
            for required in contract_entry.get("required_tokens", []):
                if required not in block.body:
                    target = report.errors if enforce_contract else report.warnings
                    target.append(
                        f"{filename}: COM{number} {contract_entry['name']} に必須呼称 {required} がない"
                    )
            if detail:
                report.notes.append(
                    f"{filename}: COM{number} {contract_entry['name']} - {contract_entry['viewpoint']}"
                )

        viewpoint_entry = contract.get("viewpoint_commands", {}).get(str(number))
        if viewpoint_entry:
            for suspicious in viewpoint_entry.get("suspicious_patterns", []):
                if suspicious in block.body:
                    report.warnings.append(
                        f"{filename}: COM{number} 視点要確認（疑わしい受動表現: {suspicious}）"
                    )
            if detail:
                report.notes.append(
                    f"{filename}: COM{number} {viewpoint_entry['name']} - {viewpoint_entry['viewpoint']}"
                )

    if detail:
        for number in sorted(set(expected_additional + expected_custom)):
            block = blocks.get(number)
            if block:
                report.notes.append(
                    f"{filename}: COM{number} lines={block.start + 1}-{block.end + 1} prints={len(block.prints)}"
                )


def cross_file_duplicates(files: list[Path], report: AuditReport) -> None:
    seen: dict[str, tuple[str, int]] = {}
    for path in files:
        blocks = extract_blocks(read_cp932(path))
        for block in blocks.values():
            for line in block.prints:
                normalized = normalize_print(line)
                if len(normalized) < 12:
                    continue
                previous = seen.get(normalized)
                if previous and previous[0] != path.name:
                    report.warnings.append(
                        f"台詞重複候補: {previous[0]}:{previous[1]} と {path.name}:COM{block.number}"
                    )
                else:
                    seen[normalized] = (path.name, block.number)


def same_file_duplicates(path: Path, report: AuditReport) -> None:
    """同一キャラの別COM間にある完全一致台詞を、要目視の警告にする。

    COM280-284/410-414のようなレンジ式はextract_blocks上で同じ開始位置を
    共有するため、開始位置が異なるブロックだけを重複として扱う。
    """
    blocks = extract_blocks(read_cp932(path))
    seen: dict[str, list[tuple[int, int]]] = {}
    for number, block in sorted(blocks.items()):
        for line in block.prints:
            normalized = normalize_print(line)
            if len(normalized) < 12:
                continue
            seen.setdefault(normalized, []).append((number, block.start + 1))

    for normalized, references in sorted(seen.items()):
        starts = sorted({start for _, start in references})
        if len(starts) < 2:
            continue
        by_start: dict[int, list[int]] = {}
        for number, start in references:
            by_start.setdefault(start, []).append(number)
        locations = "/".join(
            f"COM{','.join(str(number) for number in sorted(numbers))}(L{start})"
            for start, numbers in sorted(by_start.items())
        )
        preview = normalized[:48] + ("…" if len(normalized) > 48 else "")
        report.warnings.append(
            f"{path.name}: COM間に同一台詞（要目視） {locations}: 「{preview}」"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--char", type=int, help="指定キャラだけ監査")
    parser.add_argument("--strict", action="store_true", help="警告も失敗扱いにする")
    parser.add_argument("--require-spec", action="store_true", help="指定キャラの仕様JSONを必須にする")
    parser.add_argument("--rand-audit", action="store_true", help="全COMのRANDなしを警告する")
    parser.add_argument(
        "--duplicates",
        action="store_true",
        help="キャラ間・キャラ内COM間の完全一致台詞も警告する",
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--write-manifest", action="store_true", help="現在の注釈・枠をマニフェストへ保存")
    parser.add_argument("--no-manifest", action="store_true", help="既存マニフェストを比較しない")
    return parser.parse_args()


def run_audit(
    char: int | None = None,
    strict: bool = False,
    require_spec: bool = False,
    duplicates: bool = False,
    rand_audit: bool = False,
    manifest_path: Path = DEFAULT_MANIFEST,
    write_manifest: bool = False,
    compare_existing_manifest: bool = True,
) -> AuditReport:
    contract = load_contracts()
    files = char_files()
    if char is not None:
        files = [path for path in files if char_number(path) == char]
        if not files:
            report = AuditReport()
            report.errors.append(f"CHAR_{char:02d} のCOMファイルがない")
            return report

    report = AuditReport()
    enforce_contract = char is not None or strict
    selected_spec = None
    if char is not None:
        try:
            selected_spec = load_spec(spec_for(char))
        except ValueError as exc:
            report.errors.append(str(exc))
    for path in files:
        audit_file(
            path,
            contract,
            report,
            detail=char is not None,
            enforce_contract=enforce_contract,
            audit_rand_missing=rand_audit or char is not None,
            spec=selected_spec,
        )

    if char is not None and require_spec and spec_for(char) is None:
        report.errors.append(
            f"CHAR_{char:02d}: 仕様表がない（tools/koujo_specs/CHAR_TEMPLATE.jsonをコピーして作成）"
        )
    if char is not None and require_spec and selected_spec:
        checklist = selected_spec.get("review_checklist", {})
        incomplete = sorted(key for key, value in checklist.items() if value is not True)
        if incomplete:
            target = report.errors if strict else report.warnings
            target.append(f"CHAR_{char:02d}: 仕様表チェックリスト未完了: {', '.join(incomplete)}")

    if char is not None or duplicates:
        for path in files:
            same_file_duplicates(path, report)

    if duplicates:
        cross_file_duplicates(files, report)

    if char is None:
        current_manifest = build_manifest(files)
        if write_manifest:
            manifest_path.parent.mkdir(parents=True, exist_ok=True)
            manifest_path.write_text(
                json.dumps(current_manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            report.notes.append(f"マニフェストを書き出しました: {manifest_path}")
        elif compare_existing_manifest and manifest_path.exists():
            try:
                baseline = json.loads(manifest_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                report.errors.append(f"マニフェストJSONが壊れている: {manifest_path}: {exc}")
            else:
                compare_manifest(current_manifest, baseline, report)
        elif compare_existing_manifest:
            report.notes.append("マニフェストなし（--write-manifestで初回作成できます）")

    if strict and report.warnings:
        report.errors.extend(f"警告をstrictで昇格: {warning}" for warning in report.warnings)
    return report


def main() -> int:
    args = parse_args()
    report = run_audit(
        char=args.char,
        strict=args.strict,
        require_spec=args.require_spec,
        duplicates=args.duplicates,
        rand_audit=args.rand_audit,
        manifest_path=(ROOT / args.manifest if not args.manifest.is_absolute() else args.manifest),
        write_manifest=args.write_manifest,
        compare_existing_manifest=not args.no_manifest,
    )
    for message in report.errors:
        print(f"[NG] {message}")
    for message in report.warnings:
        print(f"[WARN] {message}")
    for message in report.notes:
        print(f"[NOTE] {message}")
    print(
        f"口上整合監査: {'NG' if report.errors else 'OK'} "
        f"（errors={len(report.errors)} warnings={len(report.warnings)}）"
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
