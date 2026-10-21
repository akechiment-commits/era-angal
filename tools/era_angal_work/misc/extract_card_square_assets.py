from __future__ import annotations

import csv
import io
import re
from pathlib import Path

import UnityPy


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "server_assets" / "addressable" / "resources" / "Android" / "packedassets_assets_assets" / "image" / "card" / "square"
OUTPUT_ROOT = ROOT / "tools" / "usable_assets" / "cards" / "square"
MANIFEST = OUTPUT_ROOT / "manifest.csv"


def extract_one(bundle: Path) -> bytes:
    env = UnityPy.load(str(bundle))
    for obj in env.objects:
        if obj.type.name not in {"Texture2D", "Sprite"}:
            continue
        data = obj.read()
        image = getattr(data, "image", None)
        if image is None:
            continue
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        return buf.getvalue()
    raise ValueError("Texture2D/Sprite image not found")


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    bundles = []
    for kind in ("default", "evolved"):
        bundles.extend((kind, path) for path in sorted((SOURCE_ROOT / kind).glob("*.bundle")))

    for index, (kind, bundle) in enumerate(bundles, start=1):
        match = re.match(r"^(\d+)\.png_", bundle.name)
        if not match:
            continue
        card_id = int(match.group(1))
        output = OUTPUT_ROOT / kind / f"{card_id}.png"
        output.parent.mkdir(parents=True, exist_ok=True)
        payload = extract_one(bundle)
        output.write_bytes(payload)
        rows.append(
            {
                "kind": kind,
                "card_id": card_id,
                "source": str(bundle.relative_to(ROOT)).replace("\\", "/"),
                "output": str(output.relative_to(ROOT)).replace("\\", "/"),
                "bytes": len(payload),
            }
        )
        if index % 250 == 0 or index == len(bundles):
            print(f"processed={index}/{len(bundles)}", flush=True)

    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["kind", "card_id", "source", "output", "bytes"])
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: (row["kind"], int(row["card_id"]))))
    print(f"bundles={len(bundles)}")
    print(f"images={len(rows)}")
    print(f"default={sum(row['kind'] == 'default' for row in rows)}")
    print(f"evolved={sum(row['kind'] == 'evolved' for row in rows)}")
    print(f"manifest={MANIFEST}")


if __name__ == "__main__":
    main()
