# ROI detector — name / number / collection

The cropper delivers the full card (63×88 mm). This stage finds the **text bands** with YOLOv8 OBB (`name`, `number`, `colection`). It does **not** read the characters.

Notebook: [`notebooks/train_roi.ipynb`](../notebooks/train_roi.ipynb). Production checkpoint after you train: **ocr-roi-v2**.

Reading: [`ocr.md`](ocr.md). Card detector metrics (1 class, no per-class table): [`detection.md`](detection.md).

## Dataset (Roboflow zip, not in Git)

In Roboflow, open [PTCG Scanner - ROI](https://universe.roboflow.com/pokemon-tcc/ptcg-scanner-roi), **Download Dataset → YOLOv8 Oriented Bounding Boxes**, and unzip into `data/roi/` (`data.yaml`, `train/`, `valid/`, `test/`).

Images = cropper cards. Labels = four corners of the text band. The counts below are from **v1**; a newer zip may differ.

| Split | Images |
|---|---|
| Train | 205 |
| Val | 59 |
| Test | 29 |
| **Total** | **293** cards · **292** name · **292** number · **190** colection |

Class `colection` (Roboflow typo) is **missing on many cards** — only when the set name is printed. Do not rename it in `data.yaml`. That class pulling mean mAP down is expected.

## Training (`ocr-roi-v2`)

In the notebook, `VERSION = "v2"`. Fine-tune from `ocr-roi-v1.pt` if present, else `yolov8n-obb.pt`.

Augmentation follows the **same idea as obb-v5** (HSV h/s/v `0.02 / 0.7 / 0.5`) but **weaker geometry**: the card is already 63×88 mm.

| Item | v1 | **v2** |
|---|---|---|
| HSV | 0 / 0.2 / 0.2 | **0.02 / 0.7 / 0.5** (same as card v5) |
| Rotation | 8° | **10°** (not 30° — that is for table photos) |
| Flip U/L | 0 | **0** (TCG layout is not symmetric) |
| Mosaic | 0.2 | **0** |
| Box / DFL / angle / cls | 7.5 / 1.5 / 1.0 / default | **10 / 2.0 / 1.5 / 0.75** |

Mosaic, mixup, erasing, perspective, and flips stay off so the OCR crop still sits on a real text band.

## Metrics (3 classes)

Unlike the card detector (`nc=1`), **per-class AP is required**: `name`, `number`, `colection`. Global mAP is the mean of those three.

| Metric | Role here |
|---|---|
| Precision / Recall / F1 | Extra band vs missed band (OCR garbage vs missing catalog field) |
| mAP@0.50 | Found the strip? |
| mAP@0.75 and mAP@0.50:0.95 | Box tight enough to crop **text**, not half the card |
| Per-class AP + TP/FP/FN | `number` vs `colection` both sit at the bottom; `colection` is often unlabeled |
| Class loss | Separates the three bands (it did **not** matter on the 1-class card model) |

Do **not** treat ROI mAP as OCR accuracy. Character error is [`ocr.md`](ocr.md).

The notebook explains each number **before** `model.val()`, then reports val and test. Confusion-matrix **counts** are kept (3-way mix-ups). The normalized matrix is still misleading on the background column.

Weights: `src/roi/runs/ocr-roi-v2/weights/ocr-roi-v2.pt`. The pipeline prefers v2, then v1.

Splits and `src/roi/runs/` are gitignored.

Part of [PTCG Scanner](../README.md). License: [CC BY-NC 4.0](../LICENSE).
