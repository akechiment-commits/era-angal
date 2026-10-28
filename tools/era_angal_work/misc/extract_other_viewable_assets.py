import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

import UnityPy


CATALOG = Path(sys.argv[1])
ROOT = Path(sys.argv[2])
OUT = Path(sys.argv[3])

SKIP_CATEGORIES = {
    "Image-Card", "Image-Character", "Voice", "Movie", "Live2D",
    "Story", "Image-Background", "Audio"
}
CONTAINER_EXTENSIONS = {".unity3d", ".bundle"}


def safe(value):
    value = str(value or "asset")
    value = re.sub(r"[^0-9A-Za-z._-]+", "_", value)
    return value[:180] or "asset"


def text_bytes(data):
    raw = getattr(data, "m_Script", None)
    if raw is None:
        raw = getattr(data, "script", None)
    if raw is None:
        raw = getattr(data, "data", None)
    if raw is None:
        raw = getattr(data, "m_Data", None)
    if raw is None:
        return None
    if isinstance(raw, str):
        return raw.encode("utf-8", errors="replace")
    if isinstance(raw, bytes):
        return raw
    try:
        return bytes(raw)
    except Exception:
        return str(raw).encode("utf-8", errors="replace")


def guess_text_extension(container_name, asset_name):
    source = f"{container_name} {asset_name}".lower()
    for extension in (".json", ".atlas", ".txt", ".asset", ".mat", ".bytes", ".xml"):
        if extension in source:
            return extension
    return ".txt"


rows = list(csv.DictReader(CATALOG.open(encoding="utf-8-sig")))
targets = []
for row in rows:
    relative = row["relative_path"].replace("/", "\\")
    if row["category"] in SKIP_CATEGORIES:
        continue
    if row["extension"] not in CONTAINER_EXTENSIONS:
        continue
    if "\\standalone\\" in f"\\{relative}":
        continue
    path = ROOT / relative
    if path.exists():
        targets.append((row["category"], relative, path))

targets.sort(key=lambda item: item[1].lower())
OUT.mkdir(parents=True, exist_ok=True)
manifest_path = OUT / "extraction_manifest.csv"
manifest_rows = []
failed = []
object_counts = Counter()
asset_counts = Counter()

for number, (category, relative, bundle_path) in enumerate(targets, 1):
    container_dir = OUT / category / Path(relative).parent / safe(bundle_path.name)
    container_dir.mkdir(parents=True, exist_ok=True)
    extracted = []
    try:
        env = UnityPy.load(str(bundle_path))
        object_names = []
        local_counts = Counter()
        for index, obj in enumerate(env.objects):
            kind = obj.type.name
            local_counts[kind] += 1
            data = obj.read()
            object_names.append({"index": index, "type": kind, "name": getattr(data, "m_Name", "")})
            if kind in {"Texture2D", "Sprite"}:
                try:
                    image = getattr(data, "image", None)
                except Exception as exc:
                    image = None
                    extracted.append(("image_error", f"{index}:{kind}:{type(exc).__name__}"))
                if image is not None:
                    output = container_dir / f"{index:05d}_{safe(getattr(data, 'm_Name', '') or kind)}.png"
                    image.convert("RGBA").save(output, "PNG")
                    extracted.append(("image", str(output.relative_to(OUT))))
            elif kind == "TextAsset":
                raw = text_bytes(data)
                if raw is not None:
                    extension = guess_text_extension(bundle_path.name, getattr(data, "m_Name", ""))
                    output = container_dir / f"{index:05d}_{safe(getattr(data, 'm_Name', '') or 'TextAsset')}{extension}"
                    output.write_bytes(raw)
                    extracted.append(("text", str(output.relative_to(OUT))))

        object_counts.update(local_counts)
        if category in {"Spine", "SpriteStudio", "KimisakiAnimation", "Other"} or any(kind == "TextAsset" for kind in local_counts):
            structure = container_dir / "__objects.json"
            structure.write_text(json.dumps({
                "source": relative,
                "object_counts": dict(sorted(local_counts.items())),
                "objects": object_names,
            }, ensure_ascii=False, indent=2), encoding="utf-8")
            extracted.append(("structure", str(structure.relative_to(OUT))))
        asset_counts[category] += len(extracted)
        manifest_rows.append({
            "category": category,
            "source": relative,
            "status": "ok",
            "outputs": len(extracted),
            "output_examples": " | ".join(path for _kind, path in extracted[:8]),
        })
    except Exception as exc:
        failed.append(f"{relative}\t{type(exc).__name__}: {exc}")
        manifest_rows.append({
            "category": category,
            "source": relative,
            "status": "failed",
            "outputs": 0,
            "output_examples": "",
        })
    if number % 250 == 0 or number == len(targets):
        print(f"{number}/{len(targets)}")

with manifest_path.open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=["category", "source", "status", "outputs", "output_examples"])
    writer.writeheader()
    writer.writerows(manifest_rows)

(OUT / "object_type_counts.json").write_text(json.dumps(dict(sorted(object_counts.items())), indent=2), encoding="utf-8")
(OUT / "category_output_counts.json").write_text(json.dumps(dict(sorted(asset_counts.items())), indent=2), encoding="utf-8")
if failed:
    (OUT / "failed.txt").write_text("\n".join(failed), encoding="utf-8")
else:
    (OUT / "failed.txt").unlink(missing_ok=True)

print(f"containers={len(targets)} failed={len(failed)}")
print(f"output={OUT.resolve()}")
