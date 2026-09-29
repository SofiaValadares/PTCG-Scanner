# Notebooks

Run from the repo root or from this folder. Each notebook walks parent directories until it finds `src/cropper/` and `src/detection/`.

| Notebook | Stage |
|---|---|
| [pipeline.ipynb](pipeline.ipynb) | PDFs → detect → crop → OCR → catalog |
| [train_detector.ipynb](train_detector.ipynb) | Train YOLOv8 OBB (`src/detection/`) |
| [train_roi.ipynb](train_roi.ipynb) | Train text-band OBB (`src/roi/`) |
| [train_ocr.ipynb](train_ocr.ipynb) | Read bands (`src/ocr/`) vs spreadsheet |
| [crop_cards.ipynb](crop_cards.ipynb) | Preview 63×88 mm crops |
