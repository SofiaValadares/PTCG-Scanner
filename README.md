# PTCG Scanner

End-to-end computer-vision pipeline that **finds Pokémon TCG cards in a photo or PDF**, **warps each one to real card size**, **reads name / number / set**, and **matches the result against a catalog**.

This repository is the experimental code of a bachelor’s thesis (TCC) by **Sofia Valadares**.

License: [CC BY-NC 4.0](LICENSE) — you may study, teach, and build on this work **with credit**. **Commercial use is reserved to the author** (or anyone she authorizes in writing: `sofiav.cav@gmail.com`). Trademarks and third-party libraries: [NOTICE](NOTICE). How to cite: [CITATION.cff](CITATION.cff).

---

## What problem this solves

Photos of binders, tables, or set checklists are messy: cards sit at an angle, several appear in one frame, and the text on the card is small. A catalog lookup only works if you know *which* card you are looking at.

PTCG Scanner splits that into three models plus a catalog step, instead of one opaque “read the card” network:

1. **Detection** — is there a card here, and at what rotation? (YOLOv8 OBB, class `card`)
2. **Crop** — warp that quadrilateral to a **63 mm × 88 mm** portrait image (the physical TCG size), in color and black-and-white.
3. **OCR** — on the cropped card, find the **name**, **collector number**, and **set name** (when printed) and read them with EasyOCR (`en` + `pt`).
4. **Catalog** — score the reading against `data/cards-list.csv` (PkmnCards `setId`s). For evaluation PDFs, cards are paired **in spreadsheet order**.

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
    → nearest row in cards-list.csv (filtered by the PDF’s setId)
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
│   ├── pipeline.ipynb         PDF → catalog (start here to reproduce results)
│   ├── train_detector.ipynb   train the card OBB model
│   ├── crop_cards.ipynb       inspect 63×88 mm crops
│   └── train_ocr.ipynb        train text-band OBB + compare OCR engines
├── src/
│   ├── detection/             card detector dataset + Ultralytics runs
│   ├── cropper/               warp / enhance / CLI
│   └── ocr/                   read_card.py + ROI dataset + runs
├── data/                      evaluation catalog (versioned)
│   ├── cards-list.csv         Name, Number, Rarity, setId
│   ├── sets-id.csv            set id → display name
│   └── pdf/                   one PDF + ground-truth CSV per set
├── output/                    pipeline dumps (CSV, plots, per-stage PDFs)
└── docs/                      longer guides + training comparison figures
```

| Path | You use it for |
|---|---|
| [`notebooks/pipeline.ipynb`](notebooks/pipeline.ipynb) | Run the full system on `data/pdf/` |
| [`src/detection/`](src/detection/) | Roboflow export + `runs/obb/obb-v3` (or v4) weights |
| [`src/cropper/`](src/cropper/) | `python -m cropper` after putting `src` on `PYTHONPATH` |
| [`src/ocr/`](src/ocr/) | ROI weights `ocr-roi-v1.pt` and `read_card.py` |
| [`data/`](data/README.md) | Catalog and the PDFs used to score the pipeline |
| [`output/`](output/README.md) | Stage-by-stage PDFs to debug OBB vs crop vs OCR vs match |
| [`docs/`](docs/README.md) | Detector metrics, cropper/OCR details, v1–v3 comparisons |

Training images (`src/detection/dataset/`, `src/ocr/data/{train,valid,test}/`) and `.pt` weights are **not** in Git. Export them from Roboflow and train locally. Evaluation PDFs under `data/pdf/` *are* versioned.

Notebooks work with the working directory at the **repo root** or inside **`notebooks/`**; they walk parents until they see `src/cropper/rectify.py`.

---

## Data

**Catalog.** `data/cards-list.csv` is a unified list of cards (`Name`, `Number`, `Rarity`, `setId`). Set codes follow [PkmnCards](https://pkmncards.com/sets/) (e.g. `BS`, `MEW`, `ASR`). `data/sets-id.csv` maps those ids to human-readable set names.

**Evaluation.** Each file in `data/pdf/` is a set checklist (or promo sheet). A CSV with the **same stem** is the ground truth (`Base.pdf` ↔ `Base.csv`). Cards are printed in the **same order** as the spreadsheet rows. The pipeline uses that order when it scores hits and errors (1st detection ↔ 1st row, and so on).

**Training (local).** Card OBB: Roboflow project [Pokemon TCC](https://universe.roboflow.com/pokemon-tcc/pokemon-tcc) v8, YOLO OBB export into `src/detection/dataset/`. Text-band OBB: cropped B&W cards into `src/ocr/data/`. Details and split sizes: [`docs/detection.md`](docs/detection.md), [`docs/ocr.md`](docs/ocr.md).

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

- Card detector: `src/detection/runs/obb/obb-v3/weights/obb-v3.pt` (v4 if you trained it)
- Text bands: `src/ocr/runs/ocr-roi-v1/weights/ocr-roi-v1.pt`

The cropper looks for v4, then v3, then `PTCG_CROPPER_WEIGHTS`.

### 3. Full evaluation (thesis experiment)

Open [`notebooks/pipeline.ipynb`](notebooks/pipeline.ipynb) and run all cells.

It rasterizes every PDF in `data/pdf/`, writes **per-PDF** stage files when that PDF finishes, then writes the global CSVs after the last file:

| Output | Meaning |
|---|---|
| `output/pdfs/<set>/00_original.pdf` | copy of the input |
| `01_pages.pdf` | rasterized pages |
| `02_obb.pdf` | card boxes, numbered in reading order |
| `03_crops.pdf` | 63×88 mm crops |
| `04_ocr.pdf` | bands + raw OCR text |
| `05_match.pdf` | OK / error vs the spreadsheet (after the eval cell) |
| `output/pipeline_extract.csv` | OCR + catalog match |
| `output/pipeline_eval.csv` | hit / miss per slot |
| `output/pipeline_*.png` | summary plots |

A hit at a given slot is **name (PT or EN) or number** matching the spreadsheet row.

### 4. Crop photos only

```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m cropper path\to\photo.jpg --out src\cropper\output\cards --conf 0.8
```

Each card becomes `*_card_00_0.96.jpg` (color) and `*_bw.jpg` (OCR). Preview notebook: [`notebooks/crop_cards.ipynb`](notebooks/crop_cards.ipynb).

To ship the cropper to another folder (code + `.pt`):

```powershell
python -m cropper export C:\other-project\ptcg_cropper
```

### 5. Train models

1. Export YOLO OBB into `src/detection/dataset/`.
2. [`notebooks/train_detector.ipynb`](notebooks/train_detector.ipynb) — current line of work is **obb-v4** fine-tuned from v3; reported metrics in the docs are **obb-v3** (val/test mAP@0.50:0.95 ≈ 0.994, test recall 1.0). Comparisons: [`docs/experiments/obb-v2-v3`](docs/experiments/obb-v2-v3/README.md).
3. Export text-band OBB into `src/ocr/data/`.
4. [`notebooks/train_ocr.ipynb`](notebooks/train_ocr.ipynb) — trains the three-class ROI detector and compares EasyOCR with PaddleOCR and Tesseract on the test sheet.

Label **printed card edges**, not binder plastic, or the crop (and then OCR) will include the sleeve.

---

## Design notes (short)

- **OBB, not axis-aligned boxes**, because cards are rotated on the table and in PDFs.
- **Full card crop**, not pre-cut text strips: OCR regions stay a template (or a second OBB) on a stable 63×88 mm image.
- **Two JPEGs** (color + B&W): B&W is what EasyOCR sees; color is for inspection.
- **Catalog restricted to the PDF’s `setId`**, then number, then name — PDFs in this repo are single-set checklists.
- **Order-based evaluation**, not greedy matching, because the PDF follows the CSV.

Longer write-ups: [`docs/detection.md`](docs/detection.md), [`docs/cropper.md`](docs/cropper.md), [`docs/ocr.md`](docs/ocr.md).

---

## License and citation

- Academic / educational / research use: **allowed**, with attribution.
- Commercial use (product, SaaS, paid identification, etc.): **not allowed** unless the author agrees in writing.

```
Valadares, Sofia. PTCG Scanner. 2026. CC BY-NC 4.0.
```

This project is **not** affiliated with Nintendo, The Pokémon Company, or Creatures Inc.
