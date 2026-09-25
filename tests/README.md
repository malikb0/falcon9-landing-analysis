# Tests

Lightweight checks that the processed data and the modelling path stay healthy.

```bash
make test
# or
python -m pytest -q
```

- `test_data_contract.py` — shape, columns and value ranges of the processed CSVs,
  including that `dataset_part_2.csv` is exactly `dataset_part_1.csv` plus `Class`.
- `test_model_smoke.py` — trains a logistic regression on the stratified split and
  asserts it clears a sensible accuracy floor, and that the split is stratified.

The tests need `pandas` and `scikit-learn` (see `../requirements.txt`).
