# PTCG Scanner

End-to-end computer-vision pipeline that **finds Pokémon TCG cards in a photo or PDF**, **warps each one to real card size**, **reads name / number / set**, and **matches the result against a catalog**.

This repository is the experimental code of a bachelor’s thesis (TCC) by **Sofia Valadares**.

License: [CC BY-NC 4.0](LICENSE) — you may study, teach, and build on this work **with credit**. **Commercial use is reserved to the author** (or anyone she authorizes in writing: `sofiav.cav@gmail.com`). Trademarks and third-party libraries: [NOTICE](NOTICE). How to cite: [CITATION.cff](CITATION.cff).

---

## What problem this solves

Photos of binders, tables, or set checklists are messy: cards sit at an angle, several appear in one frame, and the text on the card is small. A catalog lookup only works if you know *which* card you are looking at.

PTCG Scanner splits that into three models plus a catalog step, instead of one opaque “read the card” network:

1. **Detection** — is there a card here, and at what rotation? (YOLO OBB, class `card`; pipeline **obb-v6**)
2. **Crop** — warp that quadrilateral to a **63 mm × 88 mm** portrait image (the physical TCG size), in color. 90° is fixed here; **180°** is chosen in the pipeline with the ROI layout.
3. **OCR** — on the cropped card, find the **name**, **collector number**, and **set name** (when printed) and read them with RapidOCR (Paddle ONNX), including Japanese, Chinese, Korean, and Russian prints.
4. **Catalog** — score the reading against `data/catalog/{lang}/` (default `en`; PkmnCards `setId`s). For evaluation PDFs, cards are paired **in spreadsheet order**.

English catalog names count as a hit for Portuguese prints (e.g. `N's Castle` ↔ `Castelo do N`).

---

## Pipeline (what actually runs)

```
set PDF or photo
    → rasterize pages (PyMuPDF, 200 DPI)
    → YOLO OBB (card boxes; **obb-v6**)
    → perspective warp 63×88 mm @ 300 DPI (744×1039 px; 90° landscape → portrait)
    → ROI OBB on the crop at **0° and 180°** (keep printed-up: name above number)
    → RapidOCR on those bands
    → nearest row in data/catalog/{lang}/ (name, then number, then collection)
    → compare to identify GT (OBB IoU) or the CSV next to the PDF
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
│   ├── train_ocr.ipynb        compare EasyOCR / RapidOCR / Tesseract on data/ocr/
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
| [`notebooks/pipeline.ipynb`](notebooks/pipeline.ipynb) | Full pipeline on `data/identify/` (or `data/input/`) |
| [`src/detection/`](src/detection/) | Card detector: `weights/` (official `.pt`) and `runs/obb/` |
| [`src/cropper/`](src/cropper/) | `python -m cropper` after putting `src` on `PYTHONPATH` |
| [`src/roi/`](src/roi/) | Strip detector: `ocr-roi-v2` in production; v3 is the architecture sweep |
| [`src/ocr/`](src/ocr/) | `read_card.py` and the OCR test spreadsheet |
| [`data/`](data/README.md) | Catalog, training datasets, and pipeline photos |
| [`output/`](output/README.md) | Stage-by-stage PDFs to debug OBB vs crop vs OCR vs match |
| [`docs/`](docs/README.md) | Detector metrics, cropper/OCR details, version comparisons |

Training images (`data/detection/{train,valid,test}/`, `data/roi/{train,valid,test}/`) and `.pt` weights are **not** in Git. Unzip the Roboflow YOLOv8 OBB exports locally. Photos you drop in `data/input/` are also local.

Notebooks work with the working directory at the **repo root** or inside **`notebooks/`**; they walk parents until they see `src/cropper/rectify.py`.

---

## Data

**Catalog.** `data/catalog/{lang}/` holds `cards.csv` (`Name`, `Number`, `Rarity`, `setId`, [PkmnCards](https://pkmncards.com/sets/) codes) and `sets.csv` (set id → display name). The pipeline defaults to `en`. Other folders overlay TCGdex names when that language has the card.

**Eval.** [`notebooks/pipeline.ipynb`](notebooks/pipeline.ipynb) defaults to `data/identify/` (class name = `SET number name`, boxes matched by IoU). `EVAL_SOURCE = "input"` uses photos in `data/input/` and an optional sibling CSV in **row order**.

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

GPU is strongly recommended (YOLO). RapidOCR runs on ONNX Runtime.

### 2. Weights

After training (or after copying runs onto this machine):

- Card detector: `src/detection/runs/obb/obb-v6/weights/obb-v6.pt` (pipeline and cropper). Official YOLO downloads: `src/detection/weights/`. Fallback: `src/cropper/weights/obb-v5.pt`.
- Text bands: `src/roi/runs/ocr-roi-v3/weights/ocr-roi-v3.pt` (pipeline; fallback v2, then v1). Official YOLO downloads: `src/detection/weights/`.

The cropper looks for **v6**, then v5, then v4, then v3, then `PTCG_CROPPER_WEIGHTS`. Inference size is **960** for v6/v5/v4 and **800** for v3.

### 3. Full pipeline

Open [`notebooks/pipeline.ipynb`](notebooks/pipeline.ipynb) and run all cells (`EVAL_SOURCE = "identify"` by default). For ad-hoc photos, set `EVAL_SOURCE = "input"` and drop files in `data/input/`.

Identify mode writes global CSVs plus three report PDFs. Per-file stage dumps (`pdfs/<name>/00`–`05`) are only written when `SAVE_STAGES` is on (`EVAL_SOURCE = "input"`).

| Output | Meaning |
|---|---|
| `output/pdfs/01_obb.pdf` | card boxes on each photo |
| `output/pdfs/03_acertos.pdf` | catalog hits, ROI bands on the crop |
| `output/pdfs/03_erros.pdf` | catalog misses: crop + ROI + LIDO × CORRETO |
| `output/pipeline_extract.csv` | OCR + catalog match (`orient_deg` is 0 or 180) |
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
2. [`notebooks/train_detector.ipynb`](notebooks/train_detector.ipynb) — **obb-v6** trains YOLOv26 / 12 / 8 / RT-DETR / 11 and keeps the best (YOLOv26s, val mAP50-95 ≈ 0.994). Plots for every family are in the notebook; write-up: [`docs/experiments/obb-v6`](docs/experiments/obb-v6/README.md). Pipeline and cropper use that winner. Earlier: [`docs/experiments/obb-v3-v5`](docs/experiments/obb-v3-v5/README.md).
3. [`notebooks/train_roi.ipynb`](notebooks/train_roi.ipynb) — **ocr-roi-v3** trains YOLOv26 / 12 / 8 / 11 on the text bands (same v2 augmentation; per-class mAP). Each family has its own metrics/plots section; the winner is elected at the end. Pipeline still loads **ocr-roi-v2** until you copy it.
4. [`notebooks/train_ocr.ipynb`](notebooks/train_ocr.ipynb) — does **not** train a recognizer. It crops the labeled boxes in `data/ocr/` (class name = ground-truth text) and ranks EasyOCR, RapidOCR/Paddle, and Tesseract.

Label **printed card edges**, not binder plastic, or the crop (and then OCR) will include the sleeve.

---

## Design notes (short)

- **OBB, not axis-aligned boxes**, because cards are rotated on the table and in photos.
- **Full card crop**, not pre-cut text strips: OCR regions stay a template (or a second OBB) on a stable 63×88 mm image.
- **Color crop** at 63×88 mm. OCR converts each text strip to grayscale internally.
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
