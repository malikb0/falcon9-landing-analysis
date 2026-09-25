# File catalog

Every tracked file in the repository and its purpose.

## Root

| File | Purpose |
|------|---------|
| `README.md` | Project hub: pitch, results, quickstart, layout, attribution. |
| `NOTICE.md` | Attribution and licensing notes (IBM capstone origin, SpaceX API, Wikipedia CC BY-SA 4.0). |
| `LICENSE` | MIT licence for the owner's code and notebooks. |
| `CITATION.cff` | Citation metadata. |
| `requirements.txt` | Pinned Python dependencies. |
| `Makefile` | `install`, `test`, `nb`, `report` targets. |
| `.gitignore` | Excludes virtualenvs, caches, databases and build output. |

## Data

| File | Purpose |
|------|---------|
| `data/README.md` | Data dictionary and provenance notes. |
| `data/raw/launch_dict.csv` | API launch records before labelling. |
| `data/raw/spacex_web_scraped.csv` | Wikipedia-scraped launch records. |
| `data/raw/spacex_launch.csv` | Launch table for the SQL analysis. |
| `data/processed/dataset_part_1.csv` | Falcon 9 launch table before labelling. |
| `data/processed/dataset_part_2.csv` | Labelled data with `Class`. |
| `data/processed/dataset_part_3.csv` | One-hot encoded feature matrix. |
| `data/processed/spacex_launch_geo.csv` | Launch records with coordinates. |
| `data/processed/spacex_launch_dash.csv` | Slim table for the dashboard. |

## Notebooks

| File | Purpose |
|------|---------|
| `notebooks/README.md` | Notebook index and how to run them. |
| `notebooks/01-data-collection-api.ipynb` | SpaceX API collection. |
| `notebooks/02-web-scraping.ipynb` | Wikipedia scraping. |
| `notebooks/03-data-wrangling.ipynb` | EDA and labelling. |
| `notebooks/04-eda-sql.ipynb` | SQL EDA. |
| `notebooks/05-eda-visualization.ipynb` | Visual EDA and feature engineering. |
| `notebooks/06-interactive-map.ipynb` | Folium launch-site map. |
| `notebooks/07-ml-landing-prediction.ipynb` | Classifier training and evaluation. |

## Dashboard

| File | Purpose |
|------|---------|
| `dashboard/README.md` | How to run the dashboard and what it shows. |
| `dashboard/app.py` | Plotly Dash application. |

## Reports

| File | Purpose |
|------|---------|
| `reports/README.md` | Index of the reporting artefacts. |
| `reports/report.md` | The report of record, with embedded figures. |
| `reports/limitations.md` | Limitations and next steps. |
| `reports/figures/README.md` | Figure manifest (figure → meaning → source). |
| `reports/figures/*.png` | Curated, regenerated figures. |
| `reports/maps/launch_sites.html` | Interactive Folium map. |

## Docs

| File | Purpose |
|------|---------|
| `docs/README.md` | Documentation index. |
| `docs/methodology.md` | End-to-end pipeline with a Mermaid diagram. |
| `docs/data-dictionary.md` | Column descriptions for the processed data. |
| `docs/NOTEBOOK_GUIDE.md` | Per-notebook walkthrough. |
| `docs/STRUCTURE.md` | Repository hierarchy and tree. |
| `docs/FILE_CATALOG.md` | This file. |

## Scripts and tests

| File | Purpose |
|------|---------|
| `scripts/README.md` | Script usage. |
| `scripts/make_figures.py` | Regenerates figures and the interactive map. |
| `tests/README.md` | How to run the tests. |
| `tests/test_data_contract.py` | Processed-data contract checks. |
| `tests/test_model_smoke.py` | Model accuracy smoke test. |
