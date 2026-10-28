from __future__ import annotations

import hashlib
import io
import json
import re
from collections import defaultdict
from pathlib import Path

import UnityPy


ROOT = Path(__file__).resolve().parents[3]
RAW_ROOT = ROOT / "server_assets" / "asset_bundles" / "android" / "image" / "character" / "talk"
OUTPUT_ROOT = ROOT / "server_research" / "artifacts" / "legacy_talk_png"
OUTPUT_INDEX = OUTPUT_ROOT / "talk_png_index.json"
HASH_SUFFIX = re.compile(r"_[0-9a-f]{32}$", re.IGNORECASE)


def image_from_bundle(bundle: Path):
    env = UnityPy.load(str(bundle))
    for obj in env.objects:
        if obj.type.name != "Texture2D":
            continue
        try:
            image = obj.read().image
            if image is not None:
                return image
        except Exception:
            continue
    return None


def png_digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def base_pose_label(bundle: Path) -> str:
    value = HASH_SUFFIX.sub("", bundle.stem)
    if value.endswith(".png"):
        value = value[:-4]
    return value if value.isdigit() else ""


def main() -> None:
    if not RAW_ROOT.is_dir():
        raise SystemExit(f"raw talk directory not found: {RAW_ROOT}")
    if OUTPUT_ROOT.exists():
        raise SystemExit(f"output already exists: {OUTPUT_ROOT}")
    OUTPUT_ROOT.mkdir(parents=True)

    sources: dict[str, str] = {}
    base_poses: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    errors: list[dict[str, str]] = []
    canonical_by_hash: dict[str, Path] = {}
    bundles = sorted(RAW_ROOT.rglob("*.unity3d"), key=lambda p: p.as_posix().lower())

    for index, bundle in enumerate(bundles, start=1):
        source = bundle.relative_to(ROOT).as_posix()
        target = OUTPUT_ROOT / bundle.relative_to(RAW_ROOT).with_name(bundle.name + ".png")
        target.parent.mkdir(parents=True, exist_ok=True)
        if bundle.parent.name.endswith("_expression") is False:
            label = base_pose_label(bundle)
            if label:
                base_poses[bundle.parent.parent.name][bundle.parent.name].append(label)
        try:
            image = image_from_bundle(bundle)
            if image is None:
                raise ValueError("Texture2D image not found")
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            payload = buffer.getvalue()
            digest = png_digest(payload)
            canonical = canonical_by_hash.get(digest)
            if canonical is not None:
                target.hardlink_to(canonical)
            else:
                target.write_bytes(payload)
                canonical_by_hash[digest] = target
            sources[source] = target.relative_to(ROOT).as_posix()
        except Exception as exc:
            errors.append({"source": source, "error": f"{type(exc).__name__}: {exc}"})
        if index % 500 == 0 or index == len(bundles):
            print(f"processed={index}/{len(bundles)} mapped={len(sources)} errors={len(errors)}", flush=True)

    for characters in base_poses.values():
        for outfit, labels in characters.items():
            characters[outfit] = sorted(set(labels), key=lambda value: (int(value), value))

    payload = {
        "raw_root": RAW_ROOT.relative_to(ROOT).as_posix(),
        "output_root": OUTPUT_ROOT.relative_to(ROOT).as_posix(),
        "bundles": len(bundles),
        "mapped": len(sources),
        "errors": errors,
        "sources": sources,
        "base_poses": base_poses,
        "physical_pngs": len(canonical_by_hash),
    }
    OUTPUT_INDEX.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"bundles={len(bundles)}")
    print(f"mapped={len(sources)}")
    print(f"errors={len(errors)}")
    print(f"physical_pngs={len(canonical_by_hash)}")
    print(f"output={OUTPUT_ROOT}")


if __name__ == "__main__":
    main()
