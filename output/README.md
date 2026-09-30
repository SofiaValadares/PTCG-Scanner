# Pipeline output

Written by [`notebooks/pipeline.ipynb`](../notebooks/pipeline.ipynb). Use this folder to inspect **each stage**.

| Item | Contents |
|---|---|
| `pipeline_extract.csv` | OCR and catalog match (includes `roi_*_src`) |
| `pipeline_eval.csv` | Spreadsheet check: ROI source, OCR field flags, CER, catalog hit |
| `pipeline_metrics.csv` | ROI / OCR / end-to-end rates |
| `pipeline_acertos.png` / `pipeline_acertos_etapas.png` / `pipeline_erros.png` | Funnel, ROI coverage, OCR, catalog, errors |
| `pdfs/<name>/00_original.*` | Copy of the input file |
| `pdfs/<name>/01_pages.pdf` | Rasterized pages (or the photo) |
| `pdfs/<name>/02_obb.pdf` | OBB detections |
| `pdfs/<name>/03_crops.pdf` | 63×88 mm crops |
| `pdfs/<name>/04_ocr.pdf` | ROIs and read text |
| `pdfs/<name>/05_match.pdf` | Catalog match (OK / error vs spreadsheet when a CSV exists) |

`01`–`04` are saved **when that file finishes**. `05_match` and the CSVs are written after evaluation.
