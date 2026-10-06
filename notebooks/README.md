# Notebooks

Run from the repo root or from this folder. Each notebook walks parent directories until it finds `src/cropper/` and `src/detection/`.

Official Ultralytics `.pt` files belong in [`src/detection/weights/`](../src/detection/weights/README.md), not the repo root.

| Notebook | Stage |
|---|---|
| [pipeline.ipynb](pipeline.ipynb) | Identify/input → detect (**obb-v6**) → 63×88 mm → ROI **ocr-roi-v3** at 0°/180° → RapidOCR (catalog langs) → catalog |
| [train_detector.ipynb](train_detector.ipynb) | **obb-v6** sweep (YOLOv26 / 12 / 8 / RT-DETR / 11). Metrics+plots **per family** (4.x); winner only at the end |
| [train_roi.ipynb](train_roi.ipynb) | **ocr-roi-v3** sweep (YOLOv26 / 12 / 8 / 11), 300 epochs or early stop. Same report layout as the detector |
| [train_ocr.ipynb](train_ocr.ipynb) | Compare EasyOCR / RapidOCR / Tesseract on `data/ocr/` (class = printed text). Does **not** train |
| [crop_cards.ipynb](crop_cards.ipynb) | Preview 63×88 mm crops (90° portrait only; 180° is the pipeline) |

Reports: [`docs/experiments/obb-v6`](../docs/experiments/obb-v6/README.md) · [`docs/experiments/ocr-roi-v3`](../docs/experiments/ocr-roi-v3/README.md)
