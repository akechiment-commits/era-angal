import sys
from pathlib import Path

import UnityPy
from UnityPy.export.AudioClipConverter import extract_audioclip_samples


bundle_path = Path(sys.argv[1])
out_dir = Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)
env = UnityPy.load(str(bundle_path))
count = 0
for obj in env.objects:
    if obj.type.name != "AudioClip":
        continue
    clip = obj.read()
    samples = extract_audioclip_samples(clip)
    for filename, data in samples.items():
        (out_dir / filename).write_bytes(data)
        print(out_dir / filename, len(data))
        count += 1
print(f"clips={count}")
