# Notebook guide

A short walkthrough of each notebook and the artefact it produces.

## `01-data-collection-api.ipynb`
Queries `https://api.spacexdata.com/v4/launches/past`, resolves the nested
rocket/launchpad/payload/core IDs with helper functions, keeps the Falcon 9
launches and writes `data/raw/launch_dict.csv` and `data/processed/dataset_part_1.csv`.
Needs network access.

## `02-web-scraping.ipynb`
Downloads a pinned 2021 Wikipedia revision of *List of Falcon 9 and Falcon Heavy
launches*, parses the launch table with BeautifulSoup and writes
`data/raw/spacex_web_scraped.csv`. Needs network access.

## `03-data-wrangling.ipynb`
Loads `data/processed/dataset_part_1.csv`, inspects missing values, sites, orbits
and outcomes, defines `Class` (`0`/`1`) and writes
`data/processed/dataset_part_2.csv`. Runs offline.

## `04-eda-sql.ipynb`
Loads `data/raw/spacex_launch.csv` into a local SQLite database and answers ten
questions in SQL (sites, NASA CRS payload, first ground-pad landing, drone-ship
successes, outcome counts, heaviest payload, 2015 failures, outcome ranking).
Requires `jupysql`; the database (`../my_data1.db`) is created at run time and is
git-ignored.

## `05-eda-visualization.ipynb`
Visual EDA of payload, launch site, orbit and year against the landing outcome,
then one-hot encodes the categorical features and writes
`data/processed/dataset_part_3.csv`. Runs offline and reproduces the shipped
feature matrix value-for-value.

## `06-interactive-map.ipynb`
Builds a Folium map of the launch sites, colour-codes launches by outcome and
measures distances to coastline, railway, highway and city. Reads
`data/processed/spacex_launch_geo.csv` via the configurable `GEO_CSV` path. The
interactive map is committed at `reports/maps/launch_sites.html`.

## `07-ml-landing-prediction.ipynb`
Trains logistic regression, SVM, decision tree and KNN with `GridSearchCV(cv=10)`
on a stratified split, then reports accuracy, precision, recall, F1, AUC and
confusion matrices. Runs offline and writes no files; `scripts/make_figures.py`
reproduces the same metrics for the report figures.
