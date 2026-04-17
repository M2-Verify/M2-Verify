#!/usr/bin/env python3
"""Download SciMMIR images needed by M2-Verify-Gen.

Uses the SciMMIR HuggingFace dataset (Wusiwei/SciMMIR) to fetch only the images
referenced in M2-Verify-Gen, saving them as flat PNG files.

Storage estimates: test ~30 GB, full dataset ~150 GB.

Usage:
    # test split only (recommended to start)
    python examples/download_scimmir_images.py --output-dir ~/scimmir_images --split test

    # single domain
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

    # Stream SciMMIR and save matching images
    print("Streaming SciMMIR (Wusiwei/SciMMIR) to find matches...")
    scimmir = load_dataset("Wusiwei/SciMMIR", split="train", streaming=True)
    saved = 0
    for row in tqdm(scimmir, desc="Scanning SciMMIR"):
        fname = row.get("image_path") or row.get("figure_id") or row.get("id", "")
        if fname not in needed:
            continue
        dest = os.path.join(out, fname)
        if not os.path.exists(dest):
            img = row.get("image")
            if img is not None:
                img.save(dest)
                saved += 1
        if saved >= len(needed):
            break

    print(f"Done. Saved {saved:,} images to {out}")
    missing = len(needed) - saved
    if missing:
        print(f"  {missing:,} images not found in SciMMIR HF stream.")
        print("  For those, follow: https://github.com/Wusiwei0410/SciMMIR")


if __name__ == "__main__":
    main()
