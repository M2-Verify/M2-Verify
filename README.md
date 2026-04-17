# M2-Verify

**M2-Verify** is a large-scale multimodal benchmark for scientific claim consistency checking, covering **469K instances** across **16 scientific domains** sourced from PubMed and arXiv.

| Subset | Source | Size | Images |
|---|---|---|---|
| **M2-Verify-Med** | PubMed Central (via MedICaT) | 15,953 | Embedded in HF dataset |
| **M2-Verify-Gen** | arXiv (via SciMMIR) | 453,311 | Requires SciMMIR image files |

Each instance contains a `claim`, `caption`, visual evidence (`image` / `image_path`), a binary `label` (`support` / `refute`), and a natural-language `explanation` (~100 words).

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
| `perturbation_type` | `str` | ✓ | — |
| `domain` | `str` | — | ✓ |

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
print(row["perturbation_type"])  # e.g. "Location Shift" (refuted only)
row["image"].show()          # PIL.Image
```

**Splits:** `train` / `validation` / `test` (60 / 20 / 20, paper-level split)

---

## M2-Verify-Gen

The HF dataset stores `image_path` strings pointing to image files from **SciMMIR** — you need to obtain those image files separately.

### Step 1 — Get SciMMIR images

M2-Verify-Gen is built on top of the [SciMMIR](https://github.com/Wusiwei0410/SciMMIR) dataset (arXiv figures). Download or request the full image archive from the SciMMIR authors, then note the local path to the root image directory (referred to below as `IMAGE_ROOT`).

The `image_path` values in M2-Verify-Gen are relative paths matching the structure used in SciMMIR, so your `IMAGE_ROOT` should be the base directory under which those paths resolve.

### Step 2 — Load and use

```python
import os
from PIL import Image
from datasets import load_dataset

IMAGE_ROOT = "/path/to/scimmir/images"   # set this

ds = load_dataset("AbolfazlAnsari/M2-Verify-Gen", split="train")
row = ds[0]

img = Image.open(os.path.join(IMAGE_ROOT, row["image_path"])).convert("RGB")
print(row["claim"])
print(row["label"])     # "support" or "refute"
print(row["domain"])    # e.g. "cs", "math", "physics"
print(img.size)
```

**Splits:** `train` / `validation` / `test` (60 / 20 / 20, paper-level split)

---

## Perturbation Types (Med only)

Refuted claims in M2-Verify-Med are generated via one of seven expert-curated perturbation types:

| # | Type | Example |
|---|---|---|
| 1 | Status Swap | No evidence of X → Evidence of X |
| 2 | Numeric Change | Tumor size 2 cm → 4 cm |
| 3 | Attribute Flip | significant edema ↔ minimal edema |
| 4 | Directional Flip | A > B ↔ B > A |
| 5 | Diagnosis Swap | cancer ↔ infection |
| 6 | Location Shift | thalamus ↔ basal ganglia |
| 7 | Certainty Shift | suspicious for → diagnostic of |

---

## Domains (Gen only)

M2-Verify-Gen spans 16 arXiv categories: `astro`, `cond`, `cs`, `econ`, `eess`, `gr-qc`, `hep`, `math`, `math-ph`, `nlin`, `nucl-th`, `physics`, `q-bio`, `q-fin`, `quant-ph`, `stat`.

---

## Starter scripts

```bash
# Med
python examples/load_med.py

# Gen (set --image-root to your SciMMIR image directory)
python examples/load_gen.py --image-root /path/to/scimmir/images
```

---

## Citation

```bibtex
@article{ansari2025m2verify,
  title     = {M2-Verify: A Large-Scale Multidomain Benchmark for Checking Multimodal Claim Consistency},
  author    = {Ansari, Abolfazl and Zhang, Delvin Ce and Zou, Zhuoyang and Yin, Wenpeng and Lee, Dongwon},
  journal   = {arXiv preprint},
  year      = {2025}
}
```
