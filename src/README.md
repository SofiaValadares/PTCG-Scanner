# Source

All pipeline stages live here so the repo root stays documentation, notebooks, and data.

| Folder | Stage |
|---|---|
| [`detection/`](detection/) | YOLOv8 OBB **card** detector (training runs) |
| [`cropper/`](cropper/) | Perspective warp to 63×88 mm |
| [`roi/`](roi/) | YOLOv8 OBB **text-band** detector (weights) |
| [`ocr/`](ocr/) | EasyOCR on those bands (`read_card.py`) |

Written guides: [`docs/`](../docs/).
