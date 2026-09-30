# PTCG Scanner

End-to-end computer-vision pipeline that **finds Pokémon TCG cards in a photo or PDF**, **warps each one to real card size**, **reads name / number / set**, and **matches the result against a catalog**.

This repository is the experimental code of a bachelor’s thesis (TCC) by **Sofia Valadares**.

License: [CC BY-NC 4.0](LICENSE) — you may study, teach, and build on this work **with credit**. **Commercial use is reserved to the author** (or anyone she authorizes in writing: `sofiav.cav@gmail.com`). Trademarks and third-party libraries: [NOTICE](NOTICE). How to cite: [CITATION.cff](CITATION.cff).

---

## What problem this solves

Photos of binders, tables, or set checklists are messy: cards sit at an angle, several appear in one frame, and the text on the card is small. A catalog lookup only works if you know *which* card you are looking at.

PTCG Scanner splits that into three models plus a catalog step, instead of one opaque “read the card” network:

1. **Detection** — is there a card here, and at what rotation? (YOLOv8 OBB, class `card`)
2. **Crop** — warp that quadrilateral to a **63 mm × 88 mm** portrait image (the physical TCG size), in color.
3. **OCR** — on the cropped card, find the **name**, **collector number**, and **set name** (when printed) and read them with EasyOCR (`en` + `pt`).
4. **Catalog** — score the reading against `data/catalog/{lang}/` (default `en`; PkmnCards `setId`s). For evaluation PDFs, cards are paired **in spreadsheet order**.

English catalog names count as a hit for Portuguese prints (e.g. `N's Castle` ↔ `Castelo do N`).

---

## Pipeline (what actually runs)

```
set PDF or photo
    → rasterize pages (PyMuPDF, 200 DPI)
    → YOLOv8 OBB (card boxes)
    → perspective warp 63×88 mm @ 300 DPI (744×1039 px)
    → YOLOv8 OBB on the crop (name / number / collection bands)
    → EasyOCR on those bands
    → nearest row in data/catalog/{lang}/ (name, then number, then collection)
    → compare to the CSV next to the PDF (same order as the page)
```

Nothing in the full pipeline **trains** a model. Training lives in the two train notebooks. The cropper has no trainable weights of its own; it consumes the detector.

Typical settings used in the thesis experiments: card confidence **0.8**, OCR-ROI confidence **0.4**, about **20 seconds per PDF page** on a consumer GPU (detect + crop + OCR).

---

## Repository layout

Code for the three stages is grouped under **`src/`** so the root only has docs, notebooks, and data.

```
PTCG Scanner/
├── README.md, LICENSE, NOTICE, CITATION.cff
├── requirements.txt, pyproject.toml
├── notebooks/                 Jupyter (all experiments)
│   ├── pipeline.ipynb         photos → catalog (start here)
│   ├── train_detector.ipynb   train the card OBB model
│   ├── train_roi.ipynb        train the text-band OBB (name / number / set)
│   ├── train_ocr.ipynb        compare EasyOCR / PaddleOCR / Tesseract
│   └── crop_cards.ipynb       inspect 63×88 mm crops
├── src/
│   ├── detection/             Ultralytics card-detector runs
│   ├── cropper/               warp / enhance / CLI
│   ├── roi/                   Ultralytics text-band runs
│   └── ocr/                   read_card.py + OCR eval
├── data/                      catalog, datasets, pipeline input
│   ├── catalog/{lang}/        cards.csv + sets.csv (pipeline uses `en`)
│   ├── detection/             card OBB dataset
│   ├── roi/                   text-band OBB dataset
│   └── input/                 photos (or PDFs) for the pipeline
├── output/                    pipeline dumps (CSV, plots, per-stage PDFs)
└── docs/                      longer guides + training comparison figures
```

| Path | You use it for |
|---|---|
| [`notebooks/pipeline.ipynb`](notebooks/pipeline.ipynb) | Run the full system on `data/input/` |
| [`src/detection/`](src/detection/) | Card detector weights `runs/obb/obb-v5` |
| [`src/cropper/`](src/cropper/) | `python -m cropper` after putting `src` on `PYTHONPATH` |
| [`src/roi/`](src/roi/) | Strip detector weights `ocr-roi-v1.pt` |
| [`src/ocr/`](src/ocr/) | `read_card.py` and the OCR test spreadsheet |
| [`data/`](data/README.md) | Catalog, training datasets, and pipeline photos |
| [`output/`](output/README.md) | Stage-by-stage PDFs to debug OBB vs crop vs OCR vs match |
| [`docs/`](docs/README.md) | Detector metrics, cropper/OCR details, version comparisons |

Training images (`data/detection/{train,valid,test}/`, `data/roi/{train,valid,test}/`) and `.pt` weights are **not** in Git. Unzip the Roboflow YOLOv8 OBB exports locally. Photos you drop in `data/input/` are also local.

Notebooks work with the working directory at the **repo root** or inside **`notebooks/`**; they walk parents until they see `src/cropper/rectify.py`.

---

## Data

**Catalog.** `data/catalog/{lang}/` holds `cards.csv` (`Name`, `Number`, `Rarity`, `setId`, [PkmnCards](https://pkmncards.com/sets/) codes) and `sets.csv` (set id → display name). The pipeline defaults to `en`. Other folders overlay TCGdex names when that language has the card.

**Input.** Drop photos (or PDFs) in `data/input/`. An optional CSV with the **same stem** is ground truth (`photo.jpg` ↔ `photo.csv`). When a CSV is present, cards are scored **in spreadsheet order** (1st detection ↔ 1st row).

**Training (local).** Unzip the Roboflow YOLOv8 OBB export of [PTCG Scanner - Detection](https://universe.roboflow.com/pokemon-tcc/ptcg-scanner-detection) into `data/detection/`, and [PTCG Scanner - ROI](https://universe.roboflow.com/pokemon-tcc/ptcg-scanner-roi) into `data/roi/`. Details: [`docs/detection.md`](docs/detection.md), [`docs/roi.md`](docs/roi.md).

---

## How to run

### 1. Environment

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install -e .
```

The last line makes `python -m cropper` work from the repo root. If you skip it, set `$env:PYTHONPATH="src"` in the same PowerShell session.

GPU is strongly recommended (YOLO + EasyOCR).

### 2. Weights

After training (or after copying runs onto this machine):

- Card detector: `src/detection/runs/obb/obb-v5/weights/obb-v5.pt` (cropper also copies this to `src/cropper/weights/`)
- Text bands: `src/roi/runs/ocr-roi-v1/weights/ocr-roi-v1.pt`

The cropper looks for **v5**, then v4, then v3, then `PTCG_CROPPER_WEIGHTS`. Inference size is **960** for v5/v4 and **800** for v3.

### 3. Full pipeline

Put files in `data/input/`, open [`notebooks/pipeline.ipynb`](notebooks/pipeline.ipynb), and run all cells.

It processes each photo or PDF, writes **per-file** stage dumps when that file finishes, then writes the global CSVs after the last file:

| Output | Meaning |
|---|---|
| `output/pdfs/<name>/00_original.*` | copy of the input |
| `01_pages.pdf` | rasterized pages (or the photo) |
| `02_obb.pdf` | card boxes, numbered in reading order |
| `03_crops.pdf` | 63×88 mm crops |
| `04_ocr.pdf` | bands + raw OCR text |
| `05_match.pdf` | catalog match (OK / error vs spreadsheet when a CSV exists) |
| `output/pipeline_extract.csv` | OCR + catalog match |
| `output/pipeline_eval.csv` | per-slot ROI source, OCR fields, catalog hit |
| `output/pipeline_metrics.csv` | ROI / OCR / end-to-end summary |
| `output/pipeline_*.png` | funnel, ROI coverage, OCR, catalog plots |

The card detector already has YOLO mAP in [`docs/detection.md`](docs/detection.md). The pipeline notebook adds:

1. **ROI** — strip detector mAP on `data/roi` (if the test split is present), plus how often each band came from YOLO vs the template.
2. **OCR** — name / number / collection accuracy vs the spreadsheet (when present), and mean character error rate (CER).
3. **End-to-end** — catalog hit at that slot, and a funnel: detected → ROI box → OCR field → catalog.

A catalog hit at a given slot is **name (PT or EN) or number** matching the spreadsheet row.

### 4. Crop photos only

```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m cropper path\to\photo.jpg --out src\cropper\output\cards --conf 0.8
```

Each card becomes `*_card_00_0.96.jpg` (color). Preview notebook: [`notebooks/crop_cards.ipynb`](notebooks/crop_cards.ipynb).

To ship the cropper to another folder (code + `.pt`):

```powershell
python -m cropper export C:\other-project\ptcg_cropper
```

### 5. Train models

1. Unzip the Roboflow YOLOv8 OBB zips into `data/detection/` and `data/roi/`.
2. [`notebooks/train_detector.ipynb`](notebooks/train_detector.ipynb) — production checkpoint is **obb-v5** (fine-tune from v3, color/geometry augmentation, `imgsz=960`). Val/test mAP@0.50 = 0.995; val mAP@0.50:0.95 = 0.993. Comparisons: [`docs/experiments/obb-v3-v5`](docs/experiments/obb-v3-v5/README.md) (current) · [`docs/experiments/obb-v2-v3`](docs/experiments/obb-v2-v3/README.md) (historical).
3. [`notebooks/train_roi.ipynb`](notebooks/train_roi.ipynb) — trains the three-class ROI detector (`ocr-roi-v1.pt`).
4. [`notebooks/train_ocr.ipynb`](notebooks/train_ocr.ipynb) — does **not** train a recognizer; it loads those boxes and compares EasyOCR, PaddleOCR, and Tesseract on the test sheet.

Label **printed card edges**, not binder plastic, or the crop (and then OCR) will include the sleeve.

---

## Design notes (short)

- **OBB, not axis-aligned boxes**, because cards are rotated on the table and in photos.
- **Full card crop**, not pre-cut text strips: OCR regions stay a template (or a second OBB) on a stable 63×88 mm image.
- **Color crop** at 63×88 mm. EasyOCR converts each text strip to grayscale internally.
- **Catalog restricted to the file’s `setId`** (from a sibling CSV, if present), then number, then name.
- **Order-based evaluation**, not greedy matching, when a ground-truth CSV follows the same order as the page.

Longer write-ups: [`docs/detection.md`](docs/detection.md), [`docs/cropper.md`](docs/cropper.md), [`docs/roi.md`](docs/roi.md), [`docs/ocr.md`](docs/ocr.md).

---

## License and citation

- Academic / educational / research use: **allowed**, with attribution.
- Commercial use (product, SaaS, paid identification, etc.): **not allowed** unless the author agrees in writing.

```
Valadares, Sofia. PTCG Scanner. 2026. CC BY-NC 4.0.
```

This project is **not** affiliated with Nintendo, The Pokémon Company, or Creatures Inc.
