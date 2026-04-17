#!/usr/bin/env python3
"""Download SciMMIR images needed by M2-Verify-Gen.

Uses the SciMMIR HuggingFace dataset (m-a-p/SciMMIR) to fetch only the images
referenced in M2-Verify-Gen, saving them as flat PNG files.

Storage estimates: test split ~30 GB, full dataset ~150 GB.

Usage:
    # test split only (recommended to start)
    python examples/download_scimmir_images.py --output-dir ~/scimmir_images --split test

    # single domain to save space
    python examples/download_scimmir_images.py --output-dir ~/scimmir_images --split test --domain cs

    # everything (~150 GB)
    python examples/download_scimmir_images.py --output-dir ~/scimmir_images
"""
import argparse
import os
from datasets import load_dataset
from tqdm import tqdm

SPLITS = ["train", "validation", "test"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, help="Where to save images")
    parser.add_argument("--split", choices=SPLITS, default=None,
                        help="Download one split only (default: all)")
    parser.add_argument("--domain", default=None,
                        help="Filter by arXiv category prefix, e.g. 'cs' (optional)")
    args = parser.parse_args()

    out = os.path.expanduser(args.output_dir)
    os.makedirs(out, exist_ok=True)

    # Collect image_paths needed from M2-Verify-Gen
    splits = [args.split] if args.split else SPLITS
    needed = set()
    print("Collecting required image paths from M2-Verify-Gen...")
    for split in splits:
        ds = load_dataset("AbolfazlAnsari/M2-Verify-Gen", split=split)
        for row in ds:
            if args.domain and not row.get("categories", "").startswith(args.domain):
                continue
            needed.add(row["image_path"])
    print(f"  {len(needed):,} unique images needed")

    # Stream all SciMMIR splits to find and save matching images.
    # SciMMIR uses `file_name_index` for the filename (e.g. $2305.00001v1-Figure2-1.png).
    print("Streaming SciMMIR (m-a-p/SciMMIR) to find matches...")
    saved = 0
    remaining = set(needed)
    for scimmir_split in ["train", "validation", "test"]:
        if not remaining:
            break
        scimmir = load_dataset("m-a-p/SciMMIR", split=scimmir_split, streaming=True)
        for row in tqdm(scimmir, desc=f"Scanning SciMMIR/{scimmir_split}"):
            fname = row.get("file_name_index", "")
            if fname not in remaining:
                continue
            dest = os.path.join(out, fname)
            if not os.path.exists(dest):
                img = row.get("image")
                if img is not None:
                    img.save(dest)
            remaining.discard(fname)
            saved += 1

    print(f"Done. Saved {saved:,} images to {out}")
    if remaining:
        print(f"  {len(remaining):,} images not found in SciMMIR.")
        print("  See: https://github.com/Wusiwei0410/SciMMIR")


if __name__ == "__main__":
    main()
