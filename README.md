# M2-Verify

**M2-Verify** is a large-scale multimodal benchmark for scientific claim consistency checking, covering **469K instances** across **16 scientific domains** sourced from PubMed and arXiv.

| Subset | Source | Size | Images |
|---|---|---|---|
| **M2-Verify-Med** | PubMed Central (via MedICaT) | 15,953 | Embedded in HF dataset |
| **M2-Verify-Gen** | arXiv (via SciMMIR) | 453,311 | Requires SciMMIR images (~150 GB full) |

Each instance contains a `claim`, `caption`, visual evidence, a binary `label` (`support` / `refute`), and a natural-language `explanation` (~100 words).

---

## Datasets on Hugging Face

- [`AbolfazlAnsari/M2-Verify-Med`](https://huggingface.co/datasets/AbolfazlAnsari/M2-Verify-Med)
- [`AbolfazlAnsari/M2-Verify-Gen`](https://huggingface.co/datasets/AbolfazlAnsari/M2-Verify-Gen)

---

## Schema

| Field | Type | Med | Gen |
|---|---|---|---|
| `claim` | `str` | ✓ | ✓ |
| `caption` | `str` | ✓ | ✓ |
| `label` | `str` | ✓ | ✓ |
| `explanation` | `str` | ✓ | ✓ |
| `image` | `PIL.Image` | ✓ | — |
| `image_path` | `str` | — | ✓ |
| `perturbation` | `str` | ✓ | — |
| `categories` | `str` | — | ✓ |

**Splits:** `train` / `validation` / `test` — 60 / 20 / 20, enforced at the paper level to prevent leakage.

---

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

---

## M2-Verify-Med

Images are bundled directly inside the Hugging Face dataset as `PIL.Image` objects — no extra download needed.

```python
from datasets import load_dataset

ds = load_dataset("AbolfazlAnsari/M2-Verify-Med", split="train")
row = ds[0]

print(row["claim"])
print(row["label"])          # "support" or "refute"
print(row["perturbation"])   # perturbation type for refuted claims, else None
row["image"].show()          # PIL.Image
```

**Perturbation types** (refuted claims only):

| Type | Example |
|---|---|
| Status Swap | No evidence of X → Evidence of X |
| Numeric Change | Tumor size 2 cm → 4 cm |
| Attribute Flip | significant edema ↔ minimal edema |
| Directional Flip | A > B ↔ B > A |
| Diagnosis Swap | cancer ↔ infection |
| Location Shift | thalamus ↔ basal ganglia |
| Certainty Shift | suspicious for → diagnostic of |

---

## M2-Verify-Gen

The HF dataset stores `image_path` values pointing to image files from **SciMMIR** (arXiv figures). You must obtain those images separately.

### Storage estimate

| What | Approx. size |
|---|---|
| Full dataset (all splits) | ~150 GB |
| Test split only | ~30 GB |
| Single domain (e.g. `cs`) | ~10–15 GB |

> If disk space is limited, use the helper script below to download only the split or domain you need.

### Step 1 — Download SciMMIR images

Use the provided helper script, which loads the [SciMMIR HF dataset](https://huggingface.co/datasets/m-a-p/SciMMIR), matches the filenames used in M2-Verify-Gen, and saves them locally:

```bash
# Download images for the test split only (~30 GB)
python examples/download_scimmir_images.py --output-dir ~/scimmir_images --split test

# Download a single domain (saves space)
python examples/download_scimmir_images.py --output-dir ~/scimmir_images --split test --domain cs

# Download everything (all splits, ~150 GB)
python examples/download_scimmir_images.py --output-dir ~/scimmir_images
```

Alternatively, follow the official [SciMMIR download instructions](https://github.com/Wusiwei0410/SciMMIR) to obtain the full image archive.

### Step 2 — Load and use

```python
import os
from PIL import Image
from datasets import load_dataset

IMAGE_ROOT = os.path.expanduser("~/scimmir_images")   # set to your download path

ds = load_dataset("AbolfazlAnsari/M2-Verify-Gen", split="test")
row = ds[0]

img = Image.open(os.path.join(IMAGE_ROOT, row["image_path"])).convert("RGB")
print(row["claim"])
print(row["label"])       # "support" or "refute"
print(row["categories"])  # arXiv category string, e.g. "eess.SP cs.LG"
print(img.size)
```

**Domains (arXiv categories):** `astro`, `cond`, `cs`, `econ`, `eess`, `gr-qc`, `hep`, `math`, `math-ph`, `nlin`, `nucl-th`, `physics`, `q-bio`, `q-fin`, `quant-ph`, `stat`

---

## Starter scripts

```bash
# Med — images are already inside HF
python examples/load_med.py

# Gen — set --image-root to wherever you saved SciMMIR images
python examples/load_gen.py --image-root ~/scimmir_images
```

---

## Citation

```bibtex
@article{ansari2025m2verify,
  title     = {M2-Verify: A Large-Scale Multidomain Benchmark for Checking Multimodal Claim Consistency},
  author    = {Ansari, Abolfazl and Zhang, Delvin Ce and Zou, Zhuoyang and Yin, Wenpeng and Lee, Dongwon},
  journal   = {arXiv preprint},
  year      = {2026}
}
```
