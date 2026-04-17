#!/usr/bin/env python3
"""Load and inspect a sample from M2-Verify-Gen.

M2-Verify-Gen stores relative image_path values pointing to images from the
SciMMIR dataset. You must supply the path to your local SciMMIR image directory
via --image-root.

To download SciMMIR images, run:
    python examples/download_scimmir_images.py --output-dir ~/scimmir_images --split test

Usage:
    python examples/load_gen.py --image-root ~/scimmir_images
"""
import argparse
import os

from PIL import Image
from datasets import load_dataset


def main() -> None:
    parser = argparse.ArgumentParser(description="Load one sample from M2-Verify-Gen")
    parser.add_argument(
        "--image-root",
        required=True,
        help="Root directory containing SciMMIR images (image_path values are relative to this)",
    )
    args = parser.parse_args()

    print("Loading M2-Verify-Gen (train split, 1 sample)...")
    ds = load_dataset("AbolfazlAnsari/M2-Verify-Gen", split="train[:1]")
    row = ds[0]

    rel_path = row.get("image_path", "")
    full_path = os.path.join(os.path.expanduser(args.image_root), rel_path)

    if not os.path.isfile(full_path):
        raise FileNotFoundError(
            f"Image not found: {full_path}\n\n"
            "Download SciMMIR images first:\n"
            "    python examples/download_scimmir_images.py --output-dir ~/scimmir_images --split train\n"
            "Then re-run with --image-root ~/scimmir_images\n"
            "See also: https://github.com/Wusiwei0410/SciMMIR"
        )

    image = Image.open(full_path).convert("RGB")

    print(f"\nclaim      : {row['claim']}")
    print(f"label      : {row['label']}")
    print(f"categories : {row.get('categories')}")
    print(f"caption    : {row['caption'][:120]}...")
    print(f"explanation: {row.get('explanation', '')[:120]}...")
    print(f"image_path : {rel_path}")
    print(f"image size : {image.size}")


if __name__ == "__main__":
    main()
