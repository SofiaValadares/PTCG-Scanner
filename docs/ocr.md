# OCR — reading the bands

The ROI detector ([`roi.md`](roi.md)) already boxed `name` / `number` / `colection`. This stage **reads** those strips. EasyOCR is pretrained — we do not train a recognizer.

Notebook: [`notebooks/train_ocr.ipynb`](../notebooks/train_ocr.ipynb).

Code: `src/ocr/read_card.py`. Ground truth for the 29-card test sheet: `src/ocr/data/cards_read.csv`.

## How it reads

OCR uses detector boxes; if `name`/`number` is missing it falls back to a fixed template. Missing `collection` stays empty (no OCR on a template collection band).

## Engine comparison / metrics

[`notebooks/train_ocr.ipynb`](../notebooks/train_ocr.ipynb) loads `src/roi/` weights, crops the test split, and scores EasyOCR, PaddleOCR, and Tesseract against the spreadsheet:

- field accuracy (PT/EN-style fold for names, number rules, 3-letter set codes)
- mean character error rate (CER)
- card-level hit (all three fields)
- accuracy on collection **only where YOLO found a box**

Tables: `src/ocr/runs/ocr_metrics.csv` and `ocr-roi-v1_vs_planilha.csv` (gitignored).

## Pipeline metrics

[`notebooks/pipeline.ipynb`](../notebooks/pipeline.ipynb) does not retrain. After reading `data/input/` it reports OCR field accuracy / CER (when a sibling CSV exists) and the end-to-end catalog funnel. ROI mAP on the strip test set is measured in `train_roi.ipynb` (and optionally again in the pipeline if `data/roi` is present).

Part of [PTCG Scanner](../README.md). License: [CC BY-NC 4.0](../LICENSE).
