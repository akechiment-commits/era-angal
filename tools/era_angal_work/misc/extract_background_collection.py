import csv
import sys
from pathlib import Path

import UnityPy
from PIL import Image


source_root = Path(sys.argv[1])
output_root = Path(sys.argv[2])
output_root.mkdir(parents=True, exist_ok=True)
manifest_path = output_root / "manifest.csv"

bundles = sorted(source_root.glob("*.bundle"), key=lambda path: path.name)
rows = []
seen_names = set()
failed = []

for bundle_path in bundles:
    try:
        env = UnityPy.load(str(bundle_path))
        found = False
        for obj in env.objects:
            if obj.type.name not in {"Texture2D", "Sprite"}:
                continue
            data = obj.read()
            image = getattr(data, "image", None)
            if image is None:
                continue
            image = image.convert("RGBA")
            stem = bundle_path.name.split(".png_")[0]
            if not stem.endswith(".png"):
                stem += ".png"
            name = stem
            if name in seen_names:
                suffix = 2
                while f"{Path(name).stem}_{suffix}.png" in seen_names:
                    suffix += 1
                name = f"{Path(name).stem}_{suffix}.png"
            seen_names.add(name)
            output_path = output_root / name
            image.save(output_path, "PNG")

            rgb_extrema = [image.getchannel(channel).getextrema() for channel in "RGB"]
            alpha_extrema = image.getchannel("A").getextrema()
            alpha_only = all(extrema == (0, 0) for extrema in rgb_extrema) and alpha_extrema != (255, 255)
            rows.append({
                "asset_name": getattr(data, "m_Name", ""),
                "source_bundle": str(bundle_path),
                "output_png": str(output_path),
                "width": image.width,
                "height": image.height,
                "alpha_only_mask": str(alpha_only),
            })
            found = True
            break
        if not found:
            failed.append((str(bundle_path), "no Texture2D/Sprite image"))
    except Exception as exc:
        failed.append((str(bundle_path), f"{type(exc).__name__}: {exc}"))

with manifest_path.open("w", encoding="utf-8-sig", newline="") as handle:
    writer = csv.DictWriter(handle, fieldnames=[
        "asset_name", "source_bundle", "output_png", "width", "height", "alpha_only_mask"
    ])
    writer.writeheader()
    writer.writerows(rows)

if failed:
    (output_root / "failed.txt").write_text("\n".join(f"{path}\t{reason}" for path, reason in failed), encoding="utf-8")

print(f"bundles={len(bundles)} extracted={len(rows)} failed={len(failed)}")
print(f"output={output_root.resolve()}")
