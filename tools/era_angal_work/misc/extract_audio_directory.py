#!/usr/bin/env python3
"""Extract all AudioClip samples from a directory of Unity bundles."""

import csv
import hashlib
import sys
from pathlib import Path

import UnityPy
from UnityPy.export.AudioClipConverter import extract_audioclip_samples


def main() -> None:
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    bundles = sorted(source.rglob("*.unity3d"))
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    errors = []
    for index, bundle in enumerate(bundles, 1):
        try:
            env = UnityPy.load(str(bundle))
            for obj in env.objects:
                if obj.type.name != "AudioClip":
                    continue
                clip = obj.read()
                for filename, data in extract_audioclip_samples(clip).items():
                    target = output / Path(filename).name
                    target.write_bytes(data)
                    rows.append({
                        "source": str(bundle),
                        "clip": getattr(clip, "m_Name", ""),
                        "output": str(target),
                        "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest(),
                    })
        except Exception as exc:
            errors.append(f"{bundle}\t{type(exc).__name__}: {exc}")
        if index % 10 == 0 or index == len(bundles):
            print(f"{index}/{len(bundles)}")
    with (output / "manifest.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source", "clip", "output", "bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)
    if errors:
        (output / "errors.txt").write_text("\n".join(errors), encoding="utf-8")
    print(f"bundles={len(bundles)} clips={len(rows)} errors={len(errors)}")
    print(f"output={output.resolve()}")


if __name__ == "__main__":
    main()
