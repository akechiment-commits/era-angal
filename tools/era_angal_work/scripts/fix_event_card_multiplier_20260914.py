"""Neutralize the fourth card-stat multiplier for event scores only.

ERB/CSV files are written as CP932 + CRLF, as required by this project.
The shared card recalculation and school deck score remain unchanged.
"""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "ERB/EVENT_BOARD_イベントボード周回.ERB"


def main() -> None:
    text = PATH.read_bytes().decode("cp932").replace("\r\n", "\n")
    replacements = {
        "\tLOCAL:1 += CFLAG:Z:306 * 5":
            "\tLOCAL:1 += (CFLAG:Z:306 / 2) * 5",
        "\tLOCAL:3 = (CFLAG:Z:303 + CFLAG:Z:304 + CFLAG:Z:305 + CFLAG:Z:306) * 5":
            "\tLOCAL:3 = (CFLAG:Z:303 + CFLAG:Z:304 + CFLAG:Z:305 + CFLAG:Z:306 / 2) * 5",
    }
    for old, new in replacements.items():
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"anchor count {count}: {old}")
        text = text.replace(old, new, 1)
    PATH.write_bytes(text.replace("\n", "\r\n").encode("cp932"))


if __name__ == "__main__":
    main()
