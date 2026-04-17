#!/usr/bin/env python3
"""Load and inspect a sample from M2-Verify-Gen.

M2-Verify-Gen is built on top of SciMMIR (arXiv figures).
The HF dataset stores relative image_path values; you must supply the path to
the root directory of the SciMMIR image archive via --image-root.

Usage:
    python examples/load_gen.py --image-root /path/to/scimmir/images
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
        help="Root directory of the SciMMIR image archive (image_path values are relative to this)",
    )
    args = parser.parse_args()

    print("Loading M2-Verify-Gen (train split, 1 sample)...")
    ds = load_dataset("AbolfazlAnsari/M2-Verify-Gen", split="train[:1]")
    row = ds[0]

    rel_path = row.get("image_path", "")
    full_path = os.path.join(os.path.expanduser(args.image_root), rel_path)

    if not os.path.isfile(full_path):
        raise FileNotFoundError(
            f"Image not found: {full_path}\n"
            "Obtain the SciMMIR image archive and point --image-root to its root directory.\n"
            "See: https://github.com/Wusiwei0410/SciMMIR"
        )

    image = Image.open(full_path).convert("RGB")

    print(f"\nclaim      : {row['claim']}")
    print(f"label      : {row['label']}")
    print(f"domain     : {row.get('domain', 'N/A')}")
    print(f"caption    : {row['caption'][:120]}...")
    print(f"explanation: {row.get('explanation', '')[:120]}...")
    print(f"image_path : {rel_path}")
    print(f"image size : {image.size}")


if __name__ == "__main__":
    main()
