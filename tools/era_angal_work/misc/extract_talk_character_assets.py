from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

import UnityPy


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "server_assets" / "addressable" / "resources" / "Android" / "remote_assets_assets" / "resource" / "image" / "character" / "talk"
OUTPUT_ROOT = ROOT / "tools" / "usable_assets" / "talk_character"
MANIFEST = OUTPUT_ROOT / "manifest.csv"


def safe_name(value: str) -> str:
    value = re.sub(r"[^0-9A-Za-z._-]+", "_", value)
    return value[:120] or "unnamed"


def asset_name(bundle: Path) -> str:
    value = bundle.stem
    value = re.sub(r"_[0-9a-f]{32}$", "", value, flags=re.IGNORECASE)
    return safe_name(value)


def save_unique_image(image, output_dir: Path, index: int, kind: str, name: str, seen: set[str]) -> str | None:
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    payload = buffer.getvalue()
    digest = hashlib.sha256(payload).hexdigest()
    if digest in seen:
        return None
    seen.add(digest)
    filename = f"{index:03d}_{safe_name(name or kind)}.png"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / filename).write_bytes(payload)
    return filename


def extract_bundle(bundle: Path, output_dir: Path) -> tuple[dict[str, int], int, str]:
    env = UnityPy.load(str(bundle))
    objects = list(env.objects)
    counts = Counter(obj.type.name for obj in objects)
    is_expression = "_expression_" in bundle.name.lower()
    sprites = []
    textures = []
    for index, obj in enumerate(objects):
        if obj.type.name not in {"Sprite", "Texture2D"}:
            continue
        try:
            data = obj.read()
            image = getattr(data, "image", None)
            if image is None:
                continue
            item = (index, obj.type.name, getattr(data, "name", ""), image)
            if obj.type.name == "Sprite":
                sprites.append(item)
            else:
                textures.append(item)
        except Exception:
            continue

    # Expression bundles contain both Sprite objects and their backing Texture2D
    # objects. The Sprite images are the useful individual face parts, so avoid
    # writing the duplicate backing textures when sprites are available.
    selected = sprites if is_expression and sprites else (textures + sprites if not is_expression else textures)
    seen: set[str] = set()
    saved = 0
    for index, kind, name, image in selected:
        filename = save_unique_image(image, output_dir, index, kind, name, seen)
        if filename is not None:
            saved += 1

    summary = {key: int(value) for key, value in sorted(counts.items())}
    (output_dir / "objects.json").write_text(
        json.dumps({"bundle": bundle.name, "objects": summary, "saved_images": saved}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary, saved, ""


def main() -> None:
    if not SOURCE_ROOT.is_dir():
        raise SystemExit(f"source directory not found: {SOURCE_ROOT}")
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    old_rows: dict[str, dict[str, str]] = {}
    if MANIFEST.exists():
        with MANIFEST.open("r", encoding="utf-8-sig", newline="") as handle:
            old_rows = {row["source"]: row for row in csv.DictReader(handle)}

    bundles = sorted(
        (path for path in SOURCE_ROOT.rglob("*.bundle") if path.is_file()),
        key=lambda path: (path.parent.name, "_expression_" in path.name.lower(), path.name.lower()),
    )
    rows: list[dict[str, str]] = []
    completed = 0
    for bundle in bundles:
        source = bundle.relative_to(ROOT).as_posix()
        existing = old_rows.get(source)
        if existing and existing.get("status") == "ok" and Path(existing["output_dir"]).is_dir():
            rows.append(existing)
            completed += 1
            continue

        character = bundle.parent.name
        kind = "expression" if "_expression_" in bundle.name.lower() else "base"
        outfit = asset_name(bundle)
        output_dir = OUTPUT_ROOT / safe_name(character) / kind / outfit
        error = ""
        object_counts: dict[str, int] = {}
        saved = 0
        try:
            object_counts, saved, error = extract_bundle(bundle, output_dir)
        except Exception as exc:  # keep going if one platform bundle is malformed
            error = f"{type(exc).__name__}: {exc}"

        rows.append(
            {
                "source": source,
                "character": character,
                "kind": kind,
                "outfit": outfit,
                "status": "error" if error else "ok",
                "objects": json.dumps(object_counts, ensure_ascii=False, sort_keys=True),
                "saved_images": str(saved),
                "output_dir": str(output_dir.relative_to(ROOT)).replace("\\", "/"),
                "error": error,
            }
        )
        completed += 1
        if completed % 50 == 0 or completed == len(bundles):
            print(f"processed={completed}/{len(bundles)}", flush=True)

    rows.sort(key=lambda row: row["source"].lower())
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
        fields = ["source", "character", "kind", "outfit", "status", "objects", "saved_images", "output_dir", "error"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    ok = [row for row in rows if row["status"] == "ok"]
    errors = [row for row in rows if row["status"] != "ok"]
    print(f"bundles={len(rows)}")
    print(f"ok={len(ok)} errors={len(errors)}")
    print(f"saved_images={sum(int(row['saved_images']) for row in ok)}")
    print(f"manifest={MANIFEST}")
    if errors:
        print("error_samples:")
        for row in errors[:10]:
            print(f"  {row['source']}: {row['error']}")


if __name__ == "__main__":
    main()
