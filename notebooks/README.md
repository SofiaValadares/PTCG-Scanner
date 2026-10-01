# Notebooks

Run from the repo root or from this folder. Each notebook walks parent directories until it finds `src/cropper/` and `src/detection/`.

| Notebook | Stage |
|---|---|
| [pipeline.ipynb](pipeline.ipynb) | `data/input/` → detect → crop → OCR → catalog |
| [train_detector.ipynb](train_detector.ipynb) | Train YOLOv8 OBB (`data/detection/`, weights in `src/detection/`) |
| [train_roi.ipynb](train_roi.ipynb) | Train text-band OBB (`data/roi/`, weights in `src/roi/`) |
| [train_ocr.ipynb](train_ocr.ipynb) | Compare EasyOCR / RapidOCR / Tesseract on `data/ocr/` (class = text) |
| [crop_cards.ipynb](crop_cards.ipynb) | Preview 63×88 mm crops |
