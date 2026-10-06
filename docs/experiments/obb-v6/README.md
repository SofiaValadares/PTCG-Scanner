# obb-v6 — architecture sweep (YOLOv26 / 12 / 8 / RT-DETR / 11)

Same dataset and **obb-v5 edge recipe** (no mosaic/mixup, HSV + pose). One **s** (or n) checkpoint per family. Early stop `patience=40`, cap 300 epochs. Winner: best val **mAP50-95**, then lowest infer ms among models within **0.002** of that best.

Official downloads: [`src/detection/weights/`](../../../src/detection/weights/README.md).  
Run folders: `src/detection/runs/obb/obb-v6/<id>/` (gitignored).  
Notebook: [`notebooks/train_detector.ipynb`](../../../notebooks/train_detector.ipynb).

The **pipeline** and the cropper CLI use **obb-v6**.

## Ranking (val / test)

From `src/detection/runs/obb/obb-v6/ranking.csv` (re-run the notebook sections 4.x for per-family plots).

| Family | Checkpoint | Epochs | Val P | Val R | Val F1 | Val mAP50 | Val mAP50-95 | Val ms | Test mAP50-95 |
|---|---|---|---|---|---|---|---|---|---|
| **YOLOv26** ← | `yolo26s-obb.pt` | 103 | 0.997 | 1.000 | **0.999** | 0.995 | **0.9938** | 7.9 | **0.9939** |
| YOLOv8 | `yolov8s-obb.pt` | 104 | 0.995 | 1.000 | 0.997 | 0.995 | 0.9937 | 8.2 | 0.9926 |
| YOLOv11 | `yolo11s-obb.pt` | 79 | 0.999 | 1.000 | 0.999 | 0.995 | 0.9915 | 7.3 | 0.9927 |
| YOLOv12 | `yolo12n-obb.yaml` | 120 | 0.989 | 0.997 | 0.993 | 0.995 | 0.9818 | 6.3 | 0.9791 |
| RT-DETR-L | `rtdetr-l.pt` (AABB) | 120 | 0.985 | 0.997 | 0.991 | 0.994 | 0.9390 | 15.6 | 0.9373 |

Winner: **YOLOv26s-OBB** (best val mAP50-95; YOLOv8 is within 0.002 but slower). Weights: `src/detection/runs/obb/obb-v6/weights/obb-v6.pt`.

Test (winner): P 1.000 · R 1.000 · F1 1.000 · mAP50 0.995 · mAP50-95 **0.9939** · ~8.0 ms.

RT-DETR has **no official OBB** in Ultralytics; it was trained on axis-aligned boxes from the same photos. Do not drop it into the cropper as-is.

The notebook **does not elect the winner in the train cell**. Sections **4.1–4.5** each show that family’s val/test tables, `results.png`, PR/F1 curves, and `val_batch*` photos (`…/obb-v6/<id>/report/`). Section **5** writes the `←` column and copies `obb-v6.pt`.

## What this sweep was for

v5 already sat at the YOLO mAP ceiling. v6 asks: is another backbone more accurate **and** faster? YOLOv26s matches v5-level mAP50-95 (~0.994) at ~8 ms. Larger v8/v11 sizes in an earlier draft were slower with no mAP gain.

Keep mosaic/mixup **off**.
