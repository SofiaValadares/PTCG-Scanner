# Catalogs

Each language folder has `cards.csv` (`Name`, `Number`, `Rarity`, `setId`) and `sets.csv` (`id`, `name`).

`Number` and `setId` are the [PkmnCards](https://pkmncards.com/sets/) codes used by the pipeline. `Name` (and set names in `sets.csv`) follow that language when [TCGdex](https://api.tcgdex.net/v2/{lang}/cards) has the card; otherwise the English name is kept.

The pipeline (`notebooks/pipeline.ipynb`) reads `data/catalog/{CATALOG_LANG}/`, default **`en`**. Switch `CATALOG_LANG` to `pt` (or another folder) to match against localized names.

| Folder | Language |
|---|---|
| `en/` | English (evaluation catalog) |
| `fr/` | French |
| `es/` | Spanish |
| `it/` | Italian |
| `pt/` | Portuguese (Brazil) |
| `pt-pt/` | Portuguese (Portugal) — empty in the API |
| `de/` | German |
| `nl/` | Dutch |
| `pl/` | Polish |
| `ru/` | Russian |
| `ja/` | Japanese |
| `ko/` | Korean |
| `zh-tw/` | Chinese (Traditional) |
| `zh-cn/` | Chinese (Simplified) |
| `id/` | Indonesian |
