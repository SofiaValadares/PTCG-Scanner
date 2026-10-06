# Source

All pipeline stages live here so the repo root stays documentation, notebooks, and data.

| Folder | Stage |
|---|---|
| [`detection/`](detection/) | Card detector (`weights/` official `.pt`, `runs/` experiments) |
| [`cropper/`](cropper/) | Perspective warp to 63×88 mm |
| [`roi/`](roi/) | YOLOv8 OBB **text-band** detector (weights) |
| [`ocr/`](ocr/) | RapidOCR on those bands (`read_card.py`, scripts from `data/catalog/`) |

Written guides: [`docs/`](../docs/).
