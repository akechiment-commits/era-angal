import argparse
from pathlib import Path

import UnityPy


def main():
    ap = argparse.ArgumentParser(description='Extract images and text assets from a Unity AssetBundle.')
    ap.add_argument('bundle', type=Path)
    ap.add_argument('--out', type=Path, default=Path('extracted_assets'))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    env = UnityPy.load(str(args.bundle))
    counts = {}
    for index, obj in enumerate(env.objects):
        kind = obj.type.name
        counts[kind] = counts.get(kind, 0) + 1
        try:
            data = obj.read()
            name = getattr(data, 'name', '') or f'{kind}_{index}'
            safe = ''.join(c if c.isalnum() or c in '._-' else '_' for c in name)
            stem = f'{index:05d}_{safe}'
            if kind in {'Texture2D', 'Sprite'} and getattr(data, 'image', None):
                data.image.save(args.out / f'{stem}.png')
            elif kind == 'TextAsset':
                raw = getattr(data, 'script', None)
                if raw is None:
                    raw = getattr(data, 'm_Script', None)
                if raw is None:
                    raw = getattr(data, 'data', b'')
                if raw is None:
                    raw = getattr(data, 'm_Data', b'')
                if isinstance(raw, str):
                    raw = raw.encode('utf-8', errors='replace')
                (args.out / f'{stem}.bin').write_bytes(raw)
        except Exception as exc:
            print(f'warning: {kind} {index}: {exc}')
    print('objects:', sum(counts.values()))
    for kind, count in sorted(counts.items()):
        print(f'  {kind}: {count}')
    print('output:', args.out.resolve())


if __name__ == '__main__':
    main()
