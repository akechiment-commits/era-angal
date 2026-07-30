#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""透過済みのすごろくコマを、盤面タイルに収まる寸法へ整える。"""

from pathlib import Path
from PIL import Image

source = Path('resources/sugoroku_pawn.png')
target = Path('resources/sugoroku_pawn_token.png')

image = Image.open(source).convert('RGBA')
alpha = image.getchannel('A')
bbox = alpha.getbbox()
if bbox is None:
    raise SystemExit('コマ画像に不透明部分がありません。')

left, top, right, bottom = bbox
padding = 12
crop = image.crop((max(0, left - padding), max(0, top - padding), min(image.width, right + padding), min(image.height, bottom + padding)))
scale = 220 / crop.height
size = (round(crop.width * scale), 220)
crop.resize(size, Image.Resampling.LANCZOS).save(target)
print(f'すごろくコマを {size[0]}x{size[1]} に保存しました。')
