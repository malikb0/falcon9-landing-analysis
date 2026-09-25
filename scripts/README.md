# Scripts

- [`make_figures.py`](make_figures.py) — regenerates the curated figures in
  `reports/figures/` and the interactive map in `reports/maps/launch_sites.html`
  from `data/processed/`. The model metrics it computes use the same deterministic
  pipeline as `notebooks/07-ml-landing-prediction.ipynb` (seed 2, stratified split,
  scaler fitted on the training split), so the numbers match the notebook.

## Usage

```bash
python scripts/make_figures.py
```

Run it from the repository root after installing `requirements.txt`.
