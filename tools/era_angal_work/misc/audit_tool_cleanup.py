from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1] / "tools"
LEGACY = ROOT / "viewable_other_assets"
MANIFEST = ROOT / "tool_cleanup_manifest.csv"


def main() -> None:
    targets: dict[Path, set[str]] = {}
    for path in LEGACY.rglob("*"):
        if not path.is_file():
            continue
        key = path.as_posix().lower()
        if "/ios/" in key or "/ios_" in key:
            targets.setdefault(path, set()).add("iOS duplicate extracted copy")
        if path.suffix.lower() != ".png":
            continue
        try:
            with Image.open(path) as image:
                rgba = image.convert("RGBA")
                extrema = rgba.getextrema()
                if extrema[0][1] == 0 and extrema[1][1] == 0 and extrema[2][1] == 0 and extrema[3][1] > 0:
                    targets.setdefault(path, set()).add("black RGB Alpha8 mask")
        except Exception:
            continue

    for relative in (
        Path("card_samples/server_alpha_1385.png"),
        Path("card_samples/server_alpha_1776.png"),
        Path("card_samples/server_alpha_972.png"),
        Path("card_samples/server_alpha_inverted_1385.png"),
        Path("card_samples/server_alpha_inverted_1776.png"),
        Path("card_samples/server_alpha_inverted_972.png"),
        Path("color_recovered_other/unresolved_mask_samples.png"),
    ):
        path = ROOT / relative
        if path.is_file():
            targets.setdefault(path, set()).add("temporary monochrome sample")

    rows = []
    for path in sorted(targets, key=lambda item: item.as_posix().lower()):
        rows.append(
            {
                "relative": path.relative_to(ROOT.parent).as_posix(),
                "bytes": path.stat().st_size,
                "reason": "; ".join(sorted(targets[path])),
            }
        )
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["relative", "bytes", "reason"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"targets={len(rows)}")
    print(f"bytes={sum(int(row['bytes']) for row in rows)}")
    print(f"manifest={MANIFEST}")


if __name__ == "__main__":
    main()
