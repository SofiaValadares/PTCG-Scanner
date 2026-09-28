# OCR — regions on the card + reading

The cropper delivers the full card (63×88 mm, B&W). This module does two things:

1. **Regions of interest** — YOLOv8 OBB with 3 classes on the cropped card: `name`, `number`, `colection`.
2. **Reading** — EasyOCR on those strips only (the OCR model itself is not trained here).

Notebook: [`notebooks/train_ocr.ipynb`](../notebooks/train_ocr.ipynb).

## Dataset (local, not in Git)

Export **YOLOv8 OBB** from Roboflow into `src/ocr/data/` (`data.yaml`, `train/`, `valid/`, `test/`).

Images = cropper cards in B&W. Labels = four corners of the text band.

| Split | Images |
|---|---|
| Train | 205 |
| Val | 59 |
| Test | 29 |
| **Total** | **293** cards · **292** name · **292** number · **190** colection |

Class `colection` (Roboflow typo) is **missing on many cards** — only when the set name is printed. Do not rename it in `data.yaml`.

## Train / test

1. Open [`notebooks/train_ocr.ipynb`](../notebooks/train_ocr.ipynb).
2. `VERSION = "v1"` → weights at `src/ocr/runs/ocr-roi-v1/weights/ocr-roi-v1.pt`.
3. Run dataset → YOLO train → box gallery → EasyOCR on strips.

OCR uses detector boxes; if `name`/`number` is missing it falls back to a fixed template. Missing `collection` stays empty.

Code: `src/ocr/read_card.py`. Train/val/test splits and `src/ocr/runs/` are gitignored.

Part of [PTCG Scanner](../README.md). License: [CC BY-NC 4.0](../LICENSE).
