# Evaluation data

Inputs for [`notebooks/pipeline.ipynb`](../notebooks/pipeline.ipynb). This is not the YOLO training set (`detection/dataset/` and `roi/data/`, gitignored).

| Path | Contents |
|---|---|
| `cards-list.csv` | Unified catalog: `Name`, `Number`, `Rarity`, `setId` ([PkmnCards](https://pkmncards.com/sets/) codes) |
| `sets-id.csv` | Set `id` and display name |
| `pdf/` | One evaluation PDF per set plus a ground-truth CSV with the same stem (`Base.pdf` ↔ `Base.csv`) |

Cards appear in the PDF in the **same order** as the matching spreadsheet.
