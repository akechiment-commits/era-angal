import argparse
import json
from pathlib import Path

import UnityPy


def main():
    ap = argparse.ArgumentParser(description='Extract a Cubism MOC3 and texture from a Unity Live2D bundle.')
    ap.add_argument('bundle', type=Path)
    ap.add_argument('--out', type=Path, default=Path('cubism_model'))
    ap.add_argument('--name', default='model')
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    env = UnityPy.load(str(args.bundle))
    moc = None
    texture = None
    for obj in env.objects:
        if obj.type.name == 'MonoBehaviour':
            data = obj.read()
            raw = getattr(data, '_bytes', None)
            if isinstance(raw, list) and bytes(raw).startswith(b'MOC3'):
                moc = bytes(raw)
        elif obj.type.name == 'Texture2D' and texture is None:
            data = obj.read()
            if getattr(data, 'image', None):
                texture = data.image.copy()

    if moc is None:
        raise RuntimeError('Cubism MOC3 data was not found')
    if texture is None:
        raise RuntimeError('Texture2D data was not found')

    moc_name = f'{args.name}.moc3'
    texture_name = f'{args.name}.png'
    (args.out / moc_name).write_bytes(moc)
    texture.save(args.out / texture_name)
    model = {
        'Version': 3,
        'FileReferences': {
            'Moc': moc_name,
            'Textures': [texture_name],
        },
    }
    (args.out / f'{args.name}.model3.json').write_text(
        json.dumps(model, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    print(f'MOC3: {len(moc):,} bytes')
    print(f'Texture: {texture.width}x{texture.height}')
    print(f'Output: {args.out.resolve()}')


if __name__ == '__main__':
    main()
