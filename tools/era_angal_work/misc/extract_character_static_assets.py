from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from collections import Counter
from pathlib import Path

import UnityPy


ROOT = Path(__file__).resolve().parents[1]
CHARACTER_ROOT = ROOT / "server_assets" / "addressable" / "resources" / "Android" / "remote_assets_assets" / "resource" / "image" / "character"
OUTPUT_ROOT = ROOT / "tools" / "usable_assets" / "character_static"
MANIFEST = OUTPUT_ROOT / "manifest.csv"


def safe_name(value: str) -> str:
    return re.sub(r"[^0-9A-Za-z._-]+", "_", value)[:120] or "unnamed"


def logical_name(path: Path) -> str:
    value = path.stem
    value = re.sub(r"_[0-9a-f]{32}$", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\.png$", "", value, flags=re.IGNORECASE)
    return safe_name(value)


def bundle_images(bundle: Path) -> tuple[dict[str, int], list[tuple[int, str, bytes]]]:
    env = UnityPy.load(str(bundle))
    counts = Counter(obj.type.name for obj in env.objects)
    images: list[tuple[int, str, bytes]] = []
    seen: set[str] = set()
    for index, obj in enumerate(env.objects):
        if obj.type.name not in {"Texture2D", "Sprite"}:
            continue
        try:
            data = obj.read()
            image = getattr(data, "image", None)
            if image is None:
                continue
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            payload = buffer.getvalue()
            digest = hashlib.sha256(payload).hexdigest()
            if digest in seen:
                continue
            seen.add(digest)
            images.append((index, obj.type.name, payload))
        except Exception:
            continue
    return {key: int(value) for key, value in sorted(counts.items())}, images


def main() -> None:
    sources = {
        "name": sorted((CHARACTER_ROOT / "name").glob("*.bundle")),
        "whole_body": sorted((CHARACTER_ROOT / "whole_body").glob("*.bundle")),
        "mini_icon": [next(CHARACTER_ROOT.glob("mini_icon_*.bundle"))],
        "story_cast": [next(CHARACTER_ROOT.glob("story_cast_*.bundle"))],
    }
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, str]] = []
    for asset_kind, bundles in sources.items():
        for bundle in bundles:
            source = bundle.relative_to(ROOT).as_posix()
            output_dir = OUTPUT_ROOT / asset_kind / logical_name(bundle)
            output_dir.mkdir(parents=True, exist_ok=True)
            counts, images = bundle_images(bundle)
            for ordinal, (object_index, object_type, payload) in enumerate(images):
                if asset_kind in {"name", "whole_body"}:
                    stem = logical_name(bundle)
                    filename = f"{stem}.png"
                else:
                    filename = f"{ordinal:03d}_{object_type}.png"
                output_path = output_dir / filename
                output_path.write_bytes(payload)
                rows.append(
                    {
                        "kind": asset_kind,
                        "source": source,
                        "bundle": bundle.name,
                        "object_index": str(object_index),
                        "output": str(output_path.relative_to(ROOT)).replace("\\", "/"),
                    }
                )
            (output_dir / "objects.json").write_text(
                json.dumps({"bundle": bundle.name, "objects": counts, "saved_images": len(images)}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["kind", "source", "bundle", "object_index", "output"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"bundles={sum(len(value) for value in sources.values())}")
    for key, value in sources.items():
        print(f"{key}_bundles={len(value)}")
    print(f"images={len(rows)}")
    print(f"manifest={MANIFEST}")


if __name__ == "__main__":
    main()
