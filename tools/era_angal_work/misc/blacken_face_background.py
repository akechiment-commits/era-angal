"""Replace baked-in pale checkerboard background with solid black.

The generated face images are RGB PNGs with the preview checkerboard baked in,
not transparent PNGs. This keeps character pixels intact by selecting only
large, near-neutral bright connected regions that touch the image edge or are
large enclosed background holes.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def blacken_background(source: Path, destination: Path) -> None:
    image = Image.open(source).convert("RGB")
    pixels = np.asarray(image)

    # The baked checkerboard is nearly neutral and very bright. Character
    # whites are usually warm-tinted, so the chroma guard keeps them intact.
    low = pixels.min(axis=2)
    high = pixels.max(axis=2)
    background_like = ((high - low) <= 8) & (low >= 218)

    labels, count = ndimage.label(
        background_like,
        structure=np.ones((3, 3), dtype=np.uint8),
    )
    areas = np.bincount(labels.ravel(), minlength=count + 1)
    edge_labels = np.unique(
        np.concatenate(
            [labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]]
        )
    )

    # Large enclosed regions are the white gaps between hair strands. Small
    # neutral regions are highlights and are intentionally left untouched.
    # A few outer hair loops create smaller gaps, so retain those only when
    # they sit close to the left/right canvas edge. The large white eye-like
    # markings on hats are kept out by the crown cutoff.
    objects = ndimage.find_objects(labels)
    height, width = labels.shape
    selected = np.zeros(count + 1, dtype=bool)
    selected[edge_labels] = True
    for label_id in range(1, count + 1):
        area = areas[label_id]
        if area < 500 or label_id in edge_labels:
            continue
        box = objects[label_id - 1]
        if box is None:
            continue
        y_slice, x_slice = box
        near_side_edge = (
            x_slice.start <= 180 or x_slice.stop >= width - 180
        )
        large_lower_gap = area >= 1500 and y_slice.start >= 260
        if near_side_edge or large_lower_gap:
            selected[label_id] = True
    selected[0] = False
    replace = selected[labels]

    result = pixels.copy()
    result[replace] = (0, 0, 0)
    destination.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(result).save(destination, format="PNG")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    blacken_background(args.source, args.destination)


if __name__ == "__main__":
    main()
