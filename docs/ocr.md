# OCR — reading the bands

The ROI detector ([`roi.md`](roi.md)) already boxed `name` / `number` / `colection` on a 63×88 mm crop. This stage **reads** those strips. Production uses **RapidOCR** (Paddle ONNX) — winner of the engine comparison in [`notebooks/train_ocr.ipynb`](../notebooks/train_ocr.ipynb). We do not train a recognizer.

Notebook: [`notebooks/train_ocr.ipynb`](../notebooks/train_ocr.ipynb).

Code: `src/ocr/read_card.py`.

## Ground truth for engine comparison

[`data/ocr/`](../data/ocr/) (Roboflow [ptcg-scanner-ocr](https://universe.roboflow.com/pokemon-tcc/ptcg-scanner-ocr)) labels each OBB with a class whose **name is the printed text** (`Scatterbug`, `005-66`, `TEF`, `--`, …). That is not a 3-class detector problem: there are hundreds of distinct strings. The notebook therefore **does not** report mAP.

The evaluation warps each annotated quad (no ROI YOLO in the loop), infers the field type from the GT string only to pick allowlist/`_clean`, and scores three engines: EasyOCR, **RapidOCR (Paddle ONNX)**, and Tesseract. RapidOCR won (`exact_clean` 81% vs 54% / 30%) and is what `src/ocr/read_card.py` uses.

Illegible classes (`--`, `-----ex`, …) are reported separately and **do not** enter the ranking.

## How it reads (pipeline)

OCR uses detector boxes; if `name`/`number` is missing it falls back to a fixed template. Missing `collection` stays empty (no OCR on a template collection band). Collector numbers accept `-` or `/` (`005-66` = `5/66`).

## Metrics (ranking)

Primary: **normalized exact match** after `read_card` cleaners (`exact_clean`) on readable boxes.

Tie-break (difference under 1 percentage point): mean **CER** on folded strings.

Then: latency (ms/box).

Also reported, not used to pick a winner: raw exact match, WER on names, accuracy by inferred field, empty-prediction rate, empty rate on illegible boxes.

Tables: `src/ocr/runs/ocr-cmp-v1_boxes.csv` and `ocr-cmp-v1_summary.csv` (gitignored).

The old 29-card spreadsheet (`src/ocr/data/cards_read.csv`) mixed ROI detection error with OCR. It is no longer the ranking protocol.

## Pipeline metrics

[`notebooks/pipeline.ipynb`](../notebooks/pipeline.ipynb) does not retrain. Default eval is [`data/identify/`](../data/identify/) (class name = `SET number name`): OBB IoU matching, then OCR field accuracy / CER and catalog hit. `EVAL_SOURCE = "input"` still uses sibling CSVs in `data/input/`.

Part of [PTCG Scanner](../README.md). License: [CC BY-NC 4.0](../LICENSE).
