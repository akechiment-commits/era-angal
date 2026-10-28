import sys
from pathlib import Path

import UnityPy


source, target = Path(sys.argv[1]), Path(sys.argv[2])
target.mkdir(parents=True, exist_ok=True)
for bundle in sorted(source.glob("*.bundle"), key=lambda p: int(p.name.split(".")[0])):
    env = UnityPy.load(str(bundle))
    for obj in env.objects:
        if obj.type.name == "Texture2D":
            data = obj.read()
            data.image.save(target / f"{bundle.name.split('.')[0]}.png")
            break
print(target)
