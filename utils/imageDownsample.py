#!/usr/bin/env python3
"""
resize_pngs.py
Down‑sample all PNG images in a source directory (optionally recursive)
and save the resized copies to a target directory.

Example:
    python resize_pngs.py --src ./full_res_pngs \
                          --dst ./downsampled_pngs \
                          --scale 4 \
                          --workers 8 \
                          --recursive
"""

import cv2
import argparse
import os
from pathlib import Path
from functools import partial
from multiprocessing import Pool
from tqdm import tqdm


def parse_args():
    parser = argparse.ArgumentParser(
        description="Batch downsample 4096*3000 PNG images to (width/scale)*(height/scale)."
    )
    parser.add_argument("--src", required=True, help="Source directory containing PNG files")
    parser.add_argument("--dst", required=True, help="Destination directory for resized PNGs")
    parser.add_argument(
        "--scale",
        type=int,
        default=4,
        help="Downsampling factor (default 4 → from 4096*3000 to 1024*750)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=0,
        help="Number of parallel worker processes (0 = singleprocess)",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively search for PNGs in subdirectories",
    )
    return parser.parse_args()


def resize_single(path: Path, dst_root: Path, fx: float, fy: float):
    """Read one PNG, downsample, and write to the destination path."""
    img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise RuntimeError(f"Failed to read file: {path}")

    # Drop alpha channel if present
    if img.ndim == 3 and img.shape[2] == 4:
        img = img[:, :, :3]

    resized = cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_AREA)

    # Re‑create relative path inside destination directory
    rel_path = path.relative_to(path.parents[0]) if not args.recursive else path.relative_to(args.src)
    out_path = dst_root / rel_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), resized)


def main():
    global args
    args = parse_args()

    src_root = Path(args.src)
    dst_root = Path(args.dst)
    dst_root.mkdir(parents=True, exist_ok=True)

    pattern = "**/*.png" if args.recursive else "*.png"
    png_files = sorted(src_root.glob(pattern))
    if not png_files:
        print("No PNG files found. Check the --src path.")
        return

    fx = fy = 1.0 / args.scale
    worker_fn = partial(resize_single, dst_root=dst_root, fx=fx, fy=fy)

    if args.workers > 1:
        with Pool(processes=args.workers) as pool:
            list(
                tqdm(
                    pool.imap_unordered(worker_fn, png_files),
                    total=len(png_files),
                    desc="Resizing",
                )
            )
    else:
        for p in tqdm(png_files, desc="Resizing"):
            worker_fn(p)

    print(f"\nDone! Processed {len(png_files)} images → {dst_root}")


if __name__ == "__main__":
    main()
