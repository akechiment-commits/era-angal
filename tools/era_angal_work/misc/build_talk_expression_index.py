from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SOURCE_ROOT = ROOT / "server_assets" / "asset_bundles" / "android" / "image" / "character" / "talk"
OUTPUT = ROOT / "server_research" / "artifacts" / "usable_assets" / "talk_character" / "expression_index.json"
HASH_SUFFIX = re.compile(r"_[0-9a-f]{32}$", re.IGNORECASE)


def bundle_label(path: Path) -> str:
    value = HASH_SUFFIX.sub("", path.stem)
    if not value.endswith(".png"):
        return ""
    return value[:-4]


def main() -> None:
    if not SOURCE_ROOT.is_dir():
        raise SystemExit(f"source directory not found: {SOURCE_ROOT}")

    index: dict[str, dict[str, dict[str, str]]] = {}
    bundle_count = 0
    for path in sorted(SOURCE_ROOT.rglob("*.unity3d"), key=lambda p: p.as_posix().lower()):
        group = path.parent.name
        if not group.endswith("_expression"):
            continue
        label = bundle_label(path)
        if not label:
            continue

        pose = ""
        expression = label
        prefix, separator, remainder = label.partition("_")
        if prefix in {"1", "2"} and separator:
            pose = prefix
            expression = remainder

        character = path.parent.parent.name
        group_index = index.setdefault(character, {}).setdefault(group, {})
        # A group normally has one file per expression, or one per pose/expression.
        # Keep the first deterministic path if a malformed duplicate exists.
        key = f"{pose}:{expression}"
        group_index.setdefault(key, path.relative_to(ROOT).as_posix())
        bundle_count += 1

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(
            {
                "source_root": SOURCE_ROOT.relative_to(ROOT).as_posix(),
                "bundles": bundle_count,
                "characters": index,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    entries = sum(len(group) for character in index.values() for group in character.values())
    print(f"bundles={bundle_count}")
    print(f"entries={entries}")
    print(f"characters={len(index)}")
    print(f"output={OUTPUT}")


if __name__ == "__main__":
    main()
