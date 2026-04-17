#!/usr/bin/env python3
"""Load and inspect a sample from M2-Verify-Med.

Images are embedded directly in the Hugging Face dataset — no extra download needed.
"""
from datasets import load_dataset


def main() -> None:
    print("Loading M2-Verify-Med (train split, 1 sample)...")
    ds = load_dataset("AbolfazlAnsari/M2-Verify-Med", split="train[:1]")
    row = ds[0]

    print(f"\nclaim            : {row['claim']}")
    print(f"label            : {row['label']}")
    print(f"perturbation_type: {row.get('perturbation_type', 'N/A')}")
    print(f"caption          : {row['caption'][:120]}...")
    print(f"explanation      : {row.get('explanation', '')[:120]}...")
    print(f"image type       : {type(row['image']).__name__}  size={row['image'].size}")


if __name__ == "__main__":
    main()
