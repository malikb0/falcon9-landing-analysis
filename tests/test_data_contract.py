"""Data-contract tests for the processed datasets.

These assert the shape, columns and value ranges that the notebooks and figures
rely on, so a broken rebuild fails loudly.
"""

from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"


@pytest.fixture(scope="module")
def part1():
    return pd.read_csv(PROCESSED / "dataset_part_1.csv")


@pytest.fixture(scope="module")
def part2():
    return pd.read_csv(PROCESSED / "dataset_part_2.csv")


@pytest.fixture(scope="module")
def part3():
    return pd.read_csv(PROCESSED / "dataset_part_3.csv")


def test_part1_is_upstream_of_part2(part1, part2):
    assert part1.shape == (90, 17)
    assert "Class" not in part1.columns
    # part_2 is part_1 plus the Class label
    assert list(part2.columns) == list(part1.columns) + ["Class"]
    pd.testing.assert_frame_equal(part1, part2.drop(columns=["Class"]))


def test_part2_label(part2):
    assert part2.shape == (90, 18)
    assert set(part2["Class"].unique()) <= {0, 1}
    assert part2["Class"].isnull().sum() == 0
    expected_successes = int(part2["Class"].sum())
    assert expected_successes == 60


def test_part2_payload_is_filled(part2):
    assert part2["PayloadMass"].isnull().sum() == 0
    assert (part2["PayloadMass"] >= 0).all()
    # LandingPad intentionally keeps nulls
    assert part2["LandingPad"].isnull().sum() > 0


def test_part3_feature_matrix(part3):
    assert part3.shape == (90, 83)
    assert part3.select_dtypes(include="number").shape[1] == 83
    assert part3.isnull().sum().sum() == 0
    # One-hot groups used by the model
    for prefix in ("Orbit_", "LaunchSite_", "Serial_", "GridFins_", "Reused_", "Legs_"):
        assert any(c.startswith(prefix) for c in part3.columns), prefix


def test_geo_dataset():
    geo = pd.read_csv(PROCESSED / "spacex_launch_geo.csv")
    assert geo.shape[0] == 56
    assert set(geo["class"].unique()) <= {0, 1}
    assert geo["Lat"].between(-90, 90).all()
    assert geo["Long"].between(-180, 180).all()
    assert (geo["Payload Mass (kg)"] >= 0).all()


def test_dashboard_dataset():
    dash = pd.read_csv(PROCESSED / "spacex_launch_dash.csv")
    assert dash.shape[0] == 56
    for col in ("Flight Number", "Launch Site", "class", "Payload Mass (kg)", "Booster Version Category"):
        assert col in dash.columns


def test_raw_files_present():
    for name in ("launch_dict.csv", "spacex_web_scraped.csv", "spacex_launch.csv"):
        assert (RAW / name).is_file(), name
