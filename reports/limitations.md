# Limitations and next steps

This project is a compact, honest first pass. The following caveats matter when
reading the results.

## Data

- **Two sources, two coverage windows.** The launch-site/dashboard analysis uses a
  56-launch dataset covering 2010–2018 (`spacex_launch_geo.csv`), while the
  modelling notebooks use a 90-launch dataset covering 2010–2020
  (`dataset_part_2.csv`). The earlier window contains a much higher share of
  failures, so the "success rate by site/orbit" charts and the classifier metrics
  are not computed on the same rows.
- **Snapshot, not live data.** `dataset_part_1/2/3.csv` come from a pinned snapshot
  of the public SpaceX API. A fresh API pull (notebook 01) now returns more
  launches and uses the current `CCSFS SLC 40` site label rather than the snapshot's
  `CCAFS SLC 40`. The shipped processed tables are the pinned snapshot.
- **The `None None` outcome counts as failure.** Nineteen early flights did not
  attempt a landing. The target treats "no attempt" as a non-success, which is
  defensible for "will the stage land?" but inflates the early failure rate.
- **Wikipedia data is CC BY-SA 4.0.** The scraped launch table is derivative of
  Wikipedia content and carries that licence (see `../NOTICE.md`).

## Modelling

- **Small sample.** Ninety launches, with only 18 in the holdout set (stratified:
  12 successes, 6 failures). Every metric has wide uncertainty; a single
  differently-classified launch moves accuracy by ~5.6 percentage points.
- **Many features, few rows.** The one-hot encoded matrix has 83 columns for 90
  rows. Several dummy columns are collinear (e.g. `GridFins_False`/`GridFins_True`)
  and `Serial_*` is sparse. Overfitting is a real risk — the decision tree shows it
  clearly (cross-validated accuracy 0.943 vs. test accuracy 0.667).
- **Cross-validation is not stratified.** `GridSearchCV(cv=10)` uses ordinary
  K-fold, so some folds are class-imbalanced. A `StratifiedKFold` would be more
  stable; this is left as a next step so the owner's search stays recognisable.
- **AUC is computed from decision scores.** AUC is reported from
  `predict_proba`/`decision_function` rather than hard 0/1 labels (a fix over the
  original), but with 18 test points it remains a coarse estimate.
- **No target leakage.** `Class` is never used as a feature, and the scaler is
  fitted on the training split only. Post-hoc columns such as `LandingPad` and
  `Serial` are kept as the owner had them, but they can encode information about
  how a flight ended and should be reviewed before operational use.

## Method

- **Headline metric.** Classes are imbalanced, so accuracy is optimistic; F1 for the
  `land` class is the headline, supported by recall and the confusion matrices.
- **Correlation, not causation.** The EDA shows associations between orbit, site,
  payload and success, not causal effects.

## Next steps

1. Re-collect the full launch history and rebuild all three datasets on one
   consistent window and label definition.
2. Switch the grid search to `StratifiedKFold` and add repeated cross-validation.
3. Try regularised models on a reduced feature set (drop sparse `Serial_*`, collapse
   collinear dummies) and compare with a majority-class baseline.
4. Add calibration and a proper ROC/PR analysis once the sample is large enough.
5. Refresh the dashboard screenshot from the modernised app in `dashboard/app.py`.
