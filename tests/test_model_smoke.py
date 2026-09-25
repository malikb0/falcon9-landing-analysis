"""Model smoke test: train one classifier on a small stratified split."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"


@pytest.fixture(scope="module")
def split():
    data = pd.read_csv(PROCESSED / "dataset_part_2.csv")
    X = pd.read_csv(PROCESSED / "dataset_part_3.csv")
    Y = pd.Series(data["Class"].to_numpy())
    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=2, stratify=Y
    )
    scaler = preprocessing.StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, Y_train, Y_test


def test_logistic_regression_above_floor(split):
    X_train, X_test, Y_train, Y_test = split
    model = LogisticRegression(C=0.01, penalty="l2", solver="lbfgs", max_iter=1000)
    model.fit(X_train, Y_train)
    accuracy = model.score(X_test, Y_test)
    # Majority class is 12/18 = 0.667; the model should beat it comfortably.
    assert accuracy >= 0.75, f"accuracy too low: {accuracy}"


def test_split_is_stratified(split):
    _, X_test, _, Y_test = split
    assert len(Y_test) == 18
    assert Y_test.sum() == 12
