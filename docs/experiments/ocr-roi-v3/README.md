# ocr-roi-v3 — architecture sweep (YOLOv26 / 12 / 8 / 11)

Same ROI dataset and **ocr-roi-v2 recipe** (HSV like the card detector, weak geometry, no flip/mosaic). One **s** (or n) OBB checkpoint per family. Early stop `patience=40`, cap **300** epochs. Winner: best val **mAP50-95**, then lowest infer ms among models within **0.002** of that best.

RT-DETR is **not** in this sweep (no official OBB; text bands are rotated boxes).

Official downloads: [`src/detection/weights/`](../../../src/detection/weights/README.md).  
Run folders: `src/roi/runs/ocr-roi-v3/<id>/` (gitignored).  
Notebook: [`notebooks/train_roi.ipynb`](../../../notebooks/train_roi.ipynb).

The **pipeline** uses **ocr-roi-v3**. After the 63×88 mm crop it runs this ROI model at **0° and 180°** (printed-up).

## Notebook layout

| Section | What it does |
|---|---|
| 3 | Train all families (`plots=False`). Writes `ranking.csv` **without** electing a winner |
| 4 | How metrics are read (no per-family plots) |
| 5 | Elect winner → `ocr-roi-v3.pt` |
| 6 | Graphs **only for the winner**: globais + per-class (`name` / `number` / `colection`), curves, val photos |
| 7 | Test-set preview with the winner |

## Ranking

Fill after `train_roi.ipynb` finishes (this table is empty until then).

| Family | Checkpoint | Epochs | Val mAP50-95 | Val F1 | Test mAP50-95 | name AP50-95 | number AP50-95 | colection AP50-95 |
|---|---|---|---|---|---|---|---|---|
| YOLOv26 | `yolo26s-obb.pt` | — | — | — | — | — | — | — |
| YOLOv12 | `yolo12n-obb.yaml` | — | — | — | — | — | — | — |
| YOLOv8 | `yolov8s-obb.pt` | — | — | — | — | — | — | — |
| YOLOv11 | `yolo11s-obb.pt` | — | — | — | — | — | — | — |

`colection` is often unlabeled (set name not printed). A lower AP there is expected and should not be read as OCR failure.
