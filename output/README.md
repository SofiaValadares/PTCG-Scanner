# Pipeline output

Written by [`notebooks/pipeline.ipynb`](../notebooks/pipeline.ipynb).

## Identify eval (`EVAL_SOURCE = "identify"`)

| Item | Contents |
|---|---|
| `pipeline_extract.csv` | OCR and catalog match (`roi_*_src`, **`orient_deg`** 0 or 180) |
| `pipeline_eval.csv` | ROI source, OCR field flags, CER, catalog hit |
| `pipeline_metrics.csv` | ROI / OCR / end-to-end rates |
| `pipeline_acertos.png` / `pipeline_acertos_etapas.png` / `pipeline_erros.png` | Funnel, ROI coverage, OCR, catalog, errors |
| `pipeline_errors.csv` | Catalog misses (lido × correto) |
| `pdfs/01_obb.pdf` | OBB on each photo |
| `pdfs/03_acertos.pdf` | Hits with ROI bands on the crop (green = name, blue = number, yellow = set) |
| `pdfs/03_erros.pdf` | Misses: crop + ROI + LIDO × CORRETO |

There is no separate ROI PDF. The text-band boxes are drawn on the hit/miss crops.

## Input mode (`EVAL_SOURCE = "input"`, `SAVE_STAGES=True`)

Per-file folders under `pdfs/<name>/` (`00_original` … `05_match`) are written as each file finishes. CSVs are written after evaluation.
