# Cropper — full card at scanner size

Takes the OBB box and returns the **whole card**, front-facing, at Pokémon card size.

It does **not** train a model and does **not** read the name. Training: [`notebooks/train_detector.ipynb`](../notebooks/train_detector.ipynb). Preview: [`notebooks/crop_cards.ipynb`](../notebooks/crop_cards.ipynb).

## Output

Each crop is **63 mm × 88 mm** (portrait). At 300 DPI: **744 × 1039 px**. Two JPEGs per card:

| File | Use |
|---|---|
| `<photo>_card_00_0.96.jpg` | color |
| `<photo>_card_00_0.96_bw.jpg` | black and white (OCR) |

## Pipeline

```
photo  →  OBB (rotated box)  →  63×88 mm warp
      →  2% inset (drops some sleeve)
      →  flatter light + less glare
      →  color JPEG + B&W JPEG
```

The OBB must sit on the **printed edge**. If the annotation includes the pocket, the crop inherits it.

## Usage

From the repo root (`PYTHONPATH` must include `src/`):

```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m cropper path\to\photo.jpg --out src\cropper\output\cards --conf 0.8
.\.venv\Scripts\python.exe -m cropper src\detection\dataset\test\images --out src\cropper\output\cards --conf 0.8
```

## Export to another project

```powershell
$env:PYTHONPATH="src"
.\.venv\Scripts\python.exe -m cropper export C:\other-project\ptcg_cropper
```

```powershell
python C:\other-project\ptcg_cropper\crop_from_obb.py photo.jpg --out cards
python -m pip install -e C:\other-project\ptcg_cropper
ptcg-crop photo.jpg --out cards
```

Weights go in `ptcg_cropper/weights/`. Alternative: `PTCG_CROPPER_WEIGHTS` or `--weights`.

| Item | Default |
|---|---|
| Size | 63×88 mm → 744×1039 px |
| Confidence | 0.8 |
| `imgsz` | 800 (`obb-v3`) or 960 (`obb-v4`) |
| inset | 2% toward box center |
| enhance | lighting / glare / mild sharpen |
| frame | off (`--frame` paints ~2% light border) |

Part of [PTCG Scanner](../README.md). License: [CC BY-NC 4.0](../LICENSE).
