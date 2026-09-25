# Notebooks

The notebooks follow the study from raw collection to a trained classifier. All
narration has been rewritten in the owner's voice; the original instruction text
and assignment prompts are gone. Relative paths point at `../data/raw/` and
`../data/processed/`.

| Notebook | Purpose | Needs network? |
|----------|---------|----------------|
| [`01-data-collection-api.ipynb`](01-data-collection-api.ipynb) | Query the SpaceX API and flatten the launch history. | Yes |
| [`02-web-scraping.ipynb`](02-web-scraping.ipynb) | Scrape the Wikipedia Falcon 9 / Falcon Heavy launch table. | Yes |
| [`03-data-wrangling.ipynb`](03-data-wrangling.ipynb) | EDA and definition of the `Class` label. | No |
| [`04-eda-sql.ipynb`](04-eda-sql.ipynb) | SQL queries against the launch table in SQLite. | No (needs `jupysql`) |
| [`05-eda-visualization.ipynb`](05-eda-visualization.ipynb) | Visual EDA and one-hot feature engineering. | No |
| [`06-interactive-map.ipynb`](06-interactive-map.ipynb) | Folium map of launch sites and proximities. | Read only (map tiles) |
| [`07-ml-landing-prediction.ipynb`](07-ml-landing-prediction.ipynb) | Train and compare four classifiers. | No |

## Running them

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# offline notebooks (03, 05, 07) can be executed end to end
jupyter nbconvert --to notebook --execute --inplace notebooks/03-data-wrangling.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/05-eda-visualization.ipynb
jupyter nbconvert --to notebook --execute --inplace notebooks/07-ml-landing-prediction.ipynb
```

Notebook 04 reads `../data/raw/spacex_launch.csv`, loads it into a local SQLite
database (`../my_data1.db`, git-ignored) and queries it with `jupysql`:

```bash
pip install jupysql prettytable
jupyter notebook notebooks/04-eda-sql.ipynb
```

Notebook 06 reads `../data/processed/spacex_launch_geo.csv`; its data path is set by
the `GEO_CSV` variable near the top so it can run offline. Notebooks 01, 02 and 06
still use the network for their data sources and are validated for parsing but not
executed automatically.

See [`../docs/NOTEBOOK_GUIDE.md`](../docs/NOTEBOOK_GUIDE.md) for a per-notebook
walkthrough.
