# ROI detector — name / number / collection

The cropper delivers the full card (63×88 mm). This stage finds the **text bands** with YOLOv8 OBB (`name`, `number`, `colection`). It does **not** read the characters.

Notebook: [`notebooks/train_roi.ipynb`](../notebooks/train_roi.ipynb).

Reading: [`ocr.md`](ocr.md).

## Dataset (Roboflow zip, not in Git)

In Roboflow, open [PTCG Scanner - ROI](https://universe.roboflow.com/pokemon-tcc/ptcg-scanner-roi), **Download Dataset → YOLOv8 Oriented Bounding Boxes**, and unzip into `data/roi/` (`data.yaml`, `train/`, `valid/`, `test/`).

Images = cropper cards. Labels = four corners of the text band. The counts below are from **v1**; a newer zip may differ.

| Split | Images |
|---|---|
| Train | 205 |
| Val | 59 |
| Test | 29 |
| **Total** | **293** cards · **292** name · **292** number · **190** colection |

Class `colection` (Roboflow typo) is **missing on many cards** — only when the set name is printed. Do not rename it in `data.yaml`.

## Train / metrics

1. Open [`notebooks/train_roi.ipynb`](../notebooks/train_roi.ipynb).
2. `VERSION = "v1"` → weights at `src/roi/runs/ocr-roi-v1/weights/ocr-roi-v1.pt`.
3. Run dataset → YOLO train → **val and test** mAP, precision, recall, per-class AP.

The metrics cell writes `src/roi/runs/ocr-roi-v1/metrics.csv` (and a per-class CSV). Same family of numbers as the card detector in [`detection.md`](detection.md).

Splits and `src/roi/runs/` are gitignored.

Part of [PTCG Scanner](../README.md). License: [CC BY-NC 4.0](../LICENSE).
