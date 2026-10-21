"""前回のキャラ別口上修正について、修正前後のPRINTFORM行一覧を生成する。"""

from __future__ import annotations

from difflib import SequenceMatcher
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tools/前回修正前後一覧_20260909.md"

SPECS = [
    ("CHAR02 北川ゆき COM", "tools/backups/CHAR02_before_yuki_kanae_diff_20260907/CHAR_02_北川ゆき_COM.ERB", "ERB/CHAR/CHAR_02_北川ゆき_COM.ERB"),
    ("CHAR07 高原ちあき COM", "tools/backups/CHAR07_before_yuki_kanae_style_audit_20260908/CHAR_07_高原ちあき_COM.ERB", "ERB/CHAR/CHAR_07_高原ちあき_COM.ERB"),
    ("CHAR07 高原ちあき base", "tools/backups/CHAR07_before_yuki_kanae_style_audit_20260908/CHAR_07_高原ちあき.ERB", "ERB/CHAR/CHAR_07_高原ちあき.ERB"),
    ("CHAR11 氷野くるみ COM", "tools/backups/CHAR11_before_char12_diff_20260908/CHAR_11_氷野くるみ_COM.ERB", "ERB/CHAR/CHAR_11_氷野くるみ_COM.ERB"),
    ("CHAR11 氷野くるみ base", "tools/backups/CHAR11_before_char12_diff_20260908/CHAR_11_氷野くるみ.ERB", "ERB/CHAR/CHAR_11_氷野くるみ.ERB"),
    ("CHAR45 円城寺れいか COM", "tools/backups/CHAR45_before_orgasm_dedupe_20260908/CHAR_45_円城寺れいか_COM.ERB", "ERB/CHAR/CHAR_45_円城寺れいか_COM.ERB"),
    ("CHAR49 小松ぼたん COM", "tools/backups/CHAR49_before_char72_diff_20260908/CHAR_49_小松ぼたん_COM.ERB", "ERB/CHAR/CHAR_49_小松ぼたん_COM.ERB"),
    ("CHAR53 花丘まり COM", None, "ERB/CHAR/CHAR_53_花丘まり_COM.ERB"),
    ("CHAR63 八雲ちづる COM", "tools/backups/CHAR63_before_personality_overlap_audit_20260908/CHAR_63_八雲ちづる_COM.ERB", "ERB/CHAR/CHAR_63_八雲ちづる_COM.ERB"),
    ("CHAR67 日滝ましろ COM", "tools/backups/CHAR67_before_personality_overlap_audit_20260908/CHAR_67_日滝ましろ_COM.ERB", "ERB/CHAR/CHAR_67_日滝ましろ_COM.ERB"),
    ("CHAR26 堀田さあや COM", "tools/backups/CHAR26_before_personality_overlap_audit_20260908/CHAR_26_堀田さあや_COM.ERB", "ERB/CHAR/CHAR_26_堀田さあや_COM.ERB"),
    ("CHAR52 湖南やこ COM", "tools/backups/CHAR52_before_personality_overlap_audit_20260908/CHAR_52_湖南やこ_COM.ERB", "ERB/CHAR/CHAR_52_湖南やこ_COM.ERB"),
    ("CHAR68 深鳥ふみ COM", "tools/backups/CHAR68_before_personality_overlap_audit_20260908/CHAR_68_深鳥ふみ_COM.ERB", "ERB/CHAR/CHAR_68_深鳥ふみ_COM.ERB"),
]


def read_current(path: str) -> list[str]:
    return (ROOT / path).read_bytes().decode("cp932").splitlines()


def read_before(path: str) -> list[str]:
    return (ROOT / path).read_bytes().decode("cp932").splitlines()


def read_head(path: str) -> list[str]:
    raw = subprocess.check_output([
        "git", "-c", "safe.directory=C:/Users/guile/era-angal",
        "show", "HEAD:" + path,
    ])
    return raw.decode("cp932").splitlines()


def emit_pairs(before: list[str], after: list[str]) -> list[tuple[int, str, str]]:
    # ほとんどの対象は同じ行数なので行番号を保つ。行数が異なるCHAR53等は
    # SequenceMatcherで変更ブロックを対応づけ、台詞行だけを残す。
    if len(before) == len(after):
        return [
            (index + 1, old.strip(), new.strip())
            for index, (old, new) in enumerate(zip(before, after))
            if old != new and ("PRINTFORM" in old or "PRINTFORM" in new)
        ]
    pairs: list[tuple[int, str, str]] = []
    matcher = SequenceMatcher(None, before, after, autojunk=False)
    for tag, old_start, old_end, new_start, new_end in matcher.get_opcodes():
        if tag == "equal":
            continue
        old_lines = [line.strip() for line in before[old_start:old_end] if "PRINTFORM" in line]
        new_lines = [line.strip() for line in after[new_start:new_end] if "PRINTFORM" in line]
        count = max(len(old_lines), len(new_lines))
        for offset in range(count):
            pairs.append((new_start + offset + 1, old_lines[offset] if offset < len(old_lines) else "(なし)", new_lines[offset] if offset < len(new_lines) else "(なし)"))
    return pairs


def main() -> int:
    out = [
        "# 前回キャラ別口上修正：修正前後一覧",
        "",
        "対象は前回の人格汚染・重複監査で変更したPRINTFORM行。行番号は現行ファイル基準。",
        "CHAR53は専用の2026-09-08編集前バックアップが存在しないため、HEADとの差分を補助表示として収録し、完全な作業前状態とは区別する。",
        "",
    ]
    total = 0
    for label, before_path, after_path in SPECS:
        if label.startswith("CHAR53"):
            before = read_head(after_path)
            before_label = "HEAD（専用バックアップなし）"
        else:
            before = read_before(before_path)
            before_label = before_path
        after = read_current(after_path)
        pairs = emit_pairs(before, after)
        total += len(pairs)
        out.extend([f"## {label}", "", f"修正前ソース: `{before_label}`", f"修正後ソース: `{after_path}`", f"変更台詞行: {len(pairs)}", ""])
        for line_number, old, new in pairs:
            out.extend([f"### 現行行 {line_number}", "", "```diff", f"- {old}", f"+ {new}", "```", ""])
    out.extend([f"## 合計", "", f"一覧に収録した変更台詞行: {total}", ""])
    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"wrote {OUT} ({total} before/after dialogue pairs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
