# Pipeline output

Written by [`notebooks/pipeline.ipynb`](../notebooks/pipeline.ipynb). Use this folder to inspect **each stage**.

| Item | Contents |
|---|---|
| `pipeline_extract.csv` | OCR and catalog match |
| `pipeline_eval.csv` | Check against the spreadsheet (PDF order) |
| `pipeline_acertos.png` / `pipeline_acertos_etapas.png` / `pipeline_erros.png` | Plots |
| `pdfs/<set>/00_original.pdf` | Copy of the input PDF |
| `pdfs/<set>/01_pages.pdf` | Rasterized pages |
| `pdfs/<set>/02_obb.pdf` | OBB detections |
| `pdfs/<set>/03_crops.pdf` | 63×88 mm crops |
| `pdfs/<set>/04_ocr.pdf` | ROIs and read text |
| `pdfs/<set>/05_match.pdf` | OK / error vs spreadsheet |

`01`–`04` are saved **when that PDF finishes**. `05_match` and the CSVs are written after evaluation.
