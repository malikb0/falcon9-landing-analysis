# Data

All datasets are derived from public sources (the SpaceX API and a Wikipedia launch
table). No credentials or private data are included.

## `raw/` — as collected

| File | Rows | Description | Produced by |
|------|-----:|-------------|-------------|
| `launch_dict.csv` | 94 | Full launch history flattened from the SpaceX API (includes Falcon 1). | `notebooks/01-data-collection-api.ipynb` |
| `spacex_web_scraped.csv` | 121 | Falcon 9 / Falcon Heavy launch rows scraped from the 2021 Wikipedia snapshot. | `notebooks/02-web-scraping.ipynb` |
| `spacex_launch.csv` | 101 | Launch table used for the SQL analysis (raw column names, e.g. `PAYLOAD_MASS__KG_`). | Owner's archived dataset |

## `processed/` — analysis-ready

| File | Rows | Columns | Description | Produced by |
|------|-----:|--------:|-------------|-------------|
| `dataset_part_1.csv` | 90 | 17 | Falcon 9 launches with `PayloadMass` mean-filled and `LandingPad` left null. | Reconstructed from `dataset_part_2.csv` (its upstream) — see note below |
| `dataset_part_2.csv` | 90 | 18 | `dataset_part_1` plus the binary `Class` landing-success label. | `notebooks/03-data-wrangling.ipynb` |
| `dataset_part_3.csv` | 90 | 83 | One-hot encoded feature matrix (`Orbit_*`, `LaunchSite_*`, `LandingPad_*`, `Serial_*`, `GridFins_*`, `Reused_*`, `Legs_*`). | `notebooks/05-eda-visualization.ipynb` |
| `spacex_launch_geo.csv` | 56 | 13 | Launch records (2010–2018) with latitude/longitude for each site. | Owner's archived dataset |
| `spacex_launch_dash.csv` | 56 | 6 | Slim table for the dashboard: flight number, site, class, payload, booster version/category. | Owner's archived dataset |

### Note on `dataset_part_1.csv`

The archived copy of `dataset_part_1.csv` was a later API pull that (a) used the
current `CCSFS SLC 40` site label and (b) filled **every** column — including the
categorical `LandingPad` — with the mean payload mass, corrupting that column. To
keep the shipped pipeline internally consistent, `dataset_part_1.csv` is rebuilt
here as `dataset_part_2.csv` without its `Class` column. This is the exact upstream
of the canonical label file: re-running `03-data-wrangling.ipynb` on it reproduces
`dataset_part_2.csv` value-for-value, and `05-eda-visualization.ipynb` reproduces
`dataset_part_3.csv`. The raw API pull is still reproducible by running
notebook 01 (which needs network and may differ from the pinned snapshot).

Wikipedia-derived content is licensed CC BY-SA 4.0 — see [`../NOTICE.md`](../NOTICE.md).

## Rebuilding

```bash
# processed tables (offline, from the shipped dataset_part_1.csv)
jupyter nbconvert --to notebook --execute --inplace notebooks/03-data-wrangling.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/05-eda-visualization.ipynb
```

Notebooks 01, 02 and 06 require network access and are not executed automatically.
