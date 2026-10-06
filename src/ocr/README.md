# OCR — reading the bands

RapidOCR (Paddle ONNX) on strips whose boxes already exist. EasyOCR and Tesseract stay in the comparison notebook.

- Pipeline reading: `read_card.py` (`create_reader(catalog_root)`, multilingual RapidOCR, cleaners, template fallback). **0°/180°** orientation is chosen in the pipeline *before* this file runs. Name OCR keeps CJK / Hangul / Cyrillic; extra rec models load when `data/catalog/` has `ko/` or `ru/`.
- Engine ranking: [`notebooks/train_ocr.ipynb`](../../notebooks/train_ocr.ipynb) on [`data/ocr/`](../../data/ocr/) — each YOLO class name is the ground-truth string.

Eval tables go to `runs/` (gitignored).

Docs: [`docs/ocr.md`](../../docs/ocr.md)
