# Comparison `obb-v3` → `obb-v4` (recipe) → `obb-v5`

The cropper and pipeline now use **obb-v6**. This page is the v3→v5 comparison.

Plots for v5: [`../obb-v5/`](../obb-v5/).  
v3 curves (historical): [`../obb-v3/`](../obb-v3/).  
Older dataset change: [`../obb-v2-v3/README.md`](../obb-v2-v3/README.md).

v4 was a **notebook recipe** (tighter edge, weaker augmentation) that was not kept as a production checkpoint. v5 starts from the same parent as that recipe (`obb-v3.pt`) and turns **color + pose jitter** back up, without mosaic/mixup.

## What changed

| | **obb-v3** | v4 (not shipped) | **obb-v5** |
|---|---|---|---|
| Role | Previous production | Edge-focused draft | **Current production** |
| Start checkpoint | `yolov8n-obb.pt` | `obb-v3.pt` | **`obb-v3.pt`** |
| Dataset (this repo) | 245 / 75 / 36 imgs · 1680 / 490 / 255 cards | same family | **249 / 71 / 35 imgs · 1681 / 477 / 255 cards** |
| `imgsz` | 800 | 960 | **960** |
| Mosaic / erasing | 1.0 / 0.10 | 0 / 0 | **0 / 0** |
| HSV h / s / v | 0.015 / 0.7 / 0.4 | 0.01 / 0.5 / 0.3 | **0.02 / 0.7 / 0.5** |
| Rotation / scale / translate | 30° / 0.4 / 0.10 | 15° / 0.3 / 0.05 | **30° / 0.4 / 0.10** + shear 2° |
| Box / DFL / angle | 10 / 2.0 / 1.5 | 12 / 2.5 / 2.0 | **12 / 2.5 / 2.0** |
| Optimizer / LR | auto / 0.01 | AdamW / 0.001 | **AdamW / 0.001** |
| Epochs run | 99 / 120 | — | **55 / 80** (early stop, patience 20) |
| Time (RTX 5060) | ~27 min | — | **~18 min** |
| Weights | `…/obb-v3/weights/obb-v3.pt` | — | `…/obb-v5/weights/obb-v5.pt` |

Two kinds of numbers:

1. **Own-run val/test** — each model on the split of that run (v3 zip vs current zip). Counts differ slightly; mAP is already at the Ultralytics ceiling (~0.995), so do not over-read 0.001 gaps.
2. **What v5 was for** — not a higher mAP on Roboflow val, but **train-time** HSV/rotation so photos with odd light and pose still get a box tight enough for the 63×88 mm warp.

## 1. Own-run metrics

| Metric | v3 val (75 imgs / 490 cards) | **v5 val (71 imgs / 477 cards)** | v3 test (36 / 255) | **v5 test (35 / 255)** |
|---|---|---|---|---|
| Precision | 0.994 | 0.994 | 0.996 | **1.000** |
| Recall | 0.994 | **0.995** | **1.000** | 0.992 |
| F1 | — | **0.994** | — | **0.996** |
| mAP@0.50 | 0.995 | 0.995 | 0.995 | 0.995 |
| mAP@0.75 | 0.995 | 0.995 | 0.995 | 0.995 |
| **mAP@0.50:0.95** | **0.994** | 0.993 | **0.994** | 0.992 |
| TP / FP / FN (val) | 489 / 11 / 1 | **477 / 13 / 0** | — | — |
| Val box / cls / DFL / angle | **0.185 / 0.123 / 1.132 / 0.002** | 0.289 / 0.143 / 1.512 / 0.006 | — | — |

v5 **losses are higher** because each epoch jitters color and angle. That is training difficulty, not a worse val mAP.

The failure mode we watched for — **mAP50 high, mAP75 down** (loose boxes) — did **not** happen: both stay at 0.995.

Val **FN = 0** on 477 cards (v3 had 1 miss on 490). Test recall 0.992 is about two misses out of 255; v3 had a perfect test recall on a 36-image split. Precision on v5 test is 1.0 (no extra boxes).

### Curves (v5)

![v5 results](../obb-v5/results.png)

![v5 PR](../obb-v5/BoxPR_curve.png)

![v5 F1](../obb-v5/BoxF1_curve.png)

### Val predictions (v5)

![v5 labels](../obb-v5/val_batch0_labels.jpg)

![v5 pred](../obb-v5/val_batch0_pred.jpg)

Confusion-matrix **figures** are omitted (one class `card`; the normalized plot is misleading). Counts are in the table above.

## 2. Why not ship v4

v4 only reduced HSV/rotation to squeeze the edge. v3 was already at mAP50-95 ≈ 0.994. v5 keeps the v4 **960 px + no mosaic** setup and spends the budget on **augmentation the cropper actually sees** (light, sleeve color, table angle). There is no separate v4 `best.pt` in production.

## Conclusion

**Use obb-v6** in the cropper today (`imgsz=960`, `conf=0.8`). This write-up is why **v5** replaced v3; v6 is the later architecture sweep.

- Detection quality stays at the YOLO reporting ceiling (mAP50 = mAP75 = 0.995).
- Extra HSV/rotation did not open a gap between mAP50 and mAP75.
- Do not turn mosaic/mixup back on for a “better” mAP: those transforms fight the rigid card quad the warp needs.

Do not go back to v3 unless you must run at 800 px for memory. Do not use v2 on the native (non-stretch) dataset — see [obb-v2 vs v3](../obb-v2-v3/README.md).
