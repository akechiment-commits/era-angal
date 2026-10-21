from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_koujo_integrity import char_files, char_number, extract_blocks, read_cp932  # noqa: E402


def main() -> int:
    numbers = {int(value) for value in sys.argv[1:]}
    commands = {30, 191, 312}
    for path in char_files():
        number = char_number(path)
        if number not in numbers:
            continue
        text = read_cp932(path)
        blocks = extract_blocks(text)
        print(f"--- {path.name} ---")
        for command in sorted(commands):
            block = blocks.get(command)
            if block is None:
                continue
            print(f"COM{command} (L{block.start + 1}-{block.end + 1})")
            for offset, line in enumerate(block.lines):
                if line.lstrip().startswith("PRINTFORM") and "「" in line:
                    print(f"L{block.start + offset + 1}: {line.strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
