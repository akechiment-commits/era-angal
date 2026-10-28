from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_koujo_integrity import char_files, char_number, extract_blocks, read_cp932  # noqa: E402


def main() -> int:
    if not sys.argv[1:]:
        raise SystemExit("usage: python inspect_command_lines_20260904.py COM [CHAR ...]")
    command = int(sys.argv[1])
    selected = {int(value) for value in sys.argv[2:]}
    for path in char_files():
        number = char_number(path)
        if selected and number not in selected:
            continue
        block = extract_blocks(read_cp932(path)).get(command)
        if block is None:
            continue
        prints = [
            f"L{block.start + offset + 1}: {line.strip()}"
            for offset, line in enumerate(block.lines)
            if line.lstrip().startswith("PRINTFORM")
        ]
        if prints:
            print(f"--- CHAR{number:02d} {path.name} COM{command} ---")
            print("\n".join(prints))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
