# OCR — reading the bands

RapidOCR (Paddle ONNX) on strips whose boxes already exist. EasyOCR and Tesseract stay in the comparison notebook.

- Pipeline reading: `read_card.py` (`create_reader()`, allowlists, cleaners, template fallback).
- Engine ranking: [`notebooks/train_ocr.ipynb`](../../notebooks/train_ocr.ipynb) on [`data/ocr/`](../../data/ocr/) — each YOLO class name is the ground-truth string.

Eval tables go to `runs/` (gitignored).

Docs: [`docs/ocr.md`](../../docs/ocr.md)
