# Cropper

Perspective warp to 63×88 mm. Default detector: **obb-v6** (`imgsz=960`). 90° landscape → portrait here; 180° printed-up is handled in [`notebooks/pipeline.ipynb`](../../notebooks/pipeline.ipynb). Docs: [`docs/cropper.md`](../../docs/cropper.md)

```powershell
$env:PYTHONPATH="src"
python -m cropper photo.jpg --out src/cropper/output/cards --conf 0.8
python -m cropper export path/to/folder
```
