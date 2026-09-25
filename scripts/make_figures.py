"""Regenerate every portfolio figure from the processed data.

Run from the repository root::

    python scripts/make_figures.py

Outputs (all 150 dpi, seaborn ``whitegrid`` theme, ``bbox_inches='tight'``):

* ``reports/figures/*.png``  -- curated charts (EDA + model evaluation)
* ``reports/maps/launch_sites.html`` -- interactive Folium map

The model metrics are recomputed with the same deterministic pipeline used in
``notebooks/07-ml-landing-prediction.ipynb`` (seed 2, stratified split, scaler
fitted on the training split), so the numbers here match the notebook.
"""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED = os.path.join(ROOT, "data", "processed")
FIGURES = os.path.join(ROOT, "reports", "figures")
MAPS = os.path.join(ROOT, "reports", "maps")
DPI = 150

SUCCESS, FAILURE = 1, 0
CLASS_COLORS = {FAILURE: "#d1495b", SUCCESS: "#3a7d44"}
CLASS_LABELS = {FAILURE: "Failure", SUCCESS: "Success"}


def _setup_theme() -> None:
    sns.set_theme(style="whitegrid")
    plt.rcParams.update(
        {
            "figure.autolayout": False,
            "axes.titlesize": 13,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
        }
    )


def _save(fig: plt.Figure, slug: str) -> str:
    path = os.path.join(FIGURES, slug)
    fig.savefig(path, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    return path


def load_geo() -> pd.DataFrame:
    df = pd.read_csv(os.path.join(PROCESSED, "spacex_launch_geo.csv"))
    df["Year"] = df["Date"].astype(str).str.slice(0, 4).astype(int)
    return df


# ---------------------------------------------------------------------------
# EDA figures
# ---------------------------------------------------------------------------
def fig_outcome_distribution(df: pd.DataFrame) -> None:
    counts = df["class"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(
        [CLASS_LABELS[i] for i in counts.index],
        counts.values,
        color=[CLASS_COLORS[i] for i in counts.index],
    )
    ax.bar_label(bars, padding=3, fontsize=10)
    ax.set_title("First-stage landing outcomes")
    ax.set_xlabel("Outcome")
    ax.set_ylabel("Number of launches")
    ax.set_ylim(0, counts.max() * 1.15)
    _save(fig, "01-outcome-distribution.png")


def fig_flight_vs_payload(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(9, 4.5))
    sns.scatterplot(
        data=df,
        x="Flight Number",
        y="Payload Mass (kg)",
        hue="class",
        palette=CLASS_COLORS,
        s=55,
        edgecolor="white",
        ax=ax,
    )
    ax.set_title("Flight number vs. payload mass")
    ax.set_xlabel("Flight number")
    ax.set_ylabel("Payload mass (kg)")
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles, [CLASS_LABELS[FAILURE], CLASS_LABELS[SUCCESS]], title="Outcome")
    _save(fig, "02-flight-number-vs-payload-mass.png")


def fig_flight_vs_site(df: pd.DataFrame) -> None:
    order = sorted(df["Launch Site"].unique())
    fig, ax = plt.subplots(figsize=(9, 4.5))
    sns.stripplot(
        data=df,
        x="Flight Number",
        y="Launch Site",
        hue="class",
        order=order,
        palette=CLASS_COLORS,
        size=6,
        jitter=0.15,
        ax=ax,
    )
    ax.set_title("Flight number vs. launch site")
    ax.set_xlabel("Flight number")
    ax.set_ylabel("Launch site")
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles, [CLASS_LABELS[FAILURE], CLASS_LABELS[SUCCESS]], title="Outcome")
    _save(fig, "03-flight-number-vs-launch-site.png")


def fig_success_by_orbit(df: pd.DataFrame) -> None:
    rate = df.groupby("Orbit")["class"].mean().sort_values(ascending=False)
    counts = df.groupby("Orbit")["class"].size()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.bar(rate.index, rate.values, color="#3d5a80")
    ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=9)
    ax.set_title("Average landing success rate by orbit")
    ax.set_xlabel("Orbit")
    ax.set_ylabel("Success rate")
    ax.set_ylim(0, 1.12)
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha("right")
    ax.text(
        0.99,
        0.95,
        "n = " + ", ".join(f"{k}:{v}" for k, v in counts.items()),
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=7,
        color="#555555",
    )
    _save(fig, "04-success-rate-by-orbit.png")


def fig_yearly_trend(df: pd.DataFrame) -> None:
    yearly = df.groupby("Year")["class"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.lineplot(data=yearly, x="Year", y="class", marker="o", color="#3a7d44", ax=ax)
    ax.set_title("Landing success rate by year")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average success rate")
    ax.set_ylim(-0.05, 1.05)
    ax.set_xticks(sorted(df["Year"].unique()))
    _save(fig, "05-yearly-success-trend.png")


def fig_payload_vs_site(df: pd.DataFrame) -> None:
    order = sorted(df["Launch Site"].unique())
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.boxplot(
        data=df,
        x="Launch Site",
        y="Payload Mass (kg)",
        order=order,
        color="#c9d6df",
        ax=ax,
    )
    sns.stripplot(
        data=df,
        x="Launch Site",
        y="Payload Mass (kg)",
        order=order,
        hue="class",
        palette=CLASS_COLORS,
        dodge=False,
        size=4,
        ax=ax,
    )
    ax.set_title("Payload mass distribution by launch site")
    ax.set_xlabel("Launch site")
    ax.set_ylabel("Payload mass (kg)")
    for label in ax.get_xticklabels():
        label.set_rotation(15)
        label.set_ha("right")
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles, [CLASS_LABELS[FAILURE], CLASS_LABELS[SUCCESS]], title="Outcome")
    _save(fig, "06-payload-mass-vs-launch-site.png")


def fig_success_by_site(df: pd.DataFrame) -> None:
    rate = df.groupby("Launch Site")["class"].mean().sort_values(ascending=False)
    launches = df.groupby("Launch Site")["class"].size()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(rate.index, rate.values, color="#ee6c4d")
    ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=9)
    ax.set_title("Landing success rate by launch site")
    ax.set_xlabel("Launch site")
    ax.set_ylabel("Success rate")
    ax.set_ylim(0, 1.12)
    for label in ax.get_xticklabels():
        label.set_rotation(15)
        label.set_ha("right")
    _save(fig, "09-success-rate-by-launch-site.png")


# ---------------------------------------------------------------------------
# Model evaluation (deterministic replica of notebook 07)
# ---------------------------------------------------------------------------
def run_models():
    from sklearn import preprocessing
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import (
        confusion_matrix,
        f1_score,
        jaccard_score,
        precision_score,
        recall_score,
        roc_auc_score,
    )
    from sklearn.model_selection import GridSearchCV, train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier

    np.random.seed(2)

    data = pd.read_csv(os.path.join(PROCESSED, "dataset_part_2.csv"))
    X = pd.read_csv(os.path.join(PROCESSED, "dataset_part_3.csv"))
    Y = pd.Series(data["Class"].to_numpy())

    X_train, X_test, Y_train, Y_test = train_test_split(
        X, Y, test_size=0.2, random_state=2, stratify=Y
    )
    transform = preprocessing.StandardScaler()
    X_train = transform.fit_transform(X_train)
    X_test = transform.transform(X_test)

    models = {}
    models["LogReg"] = GridSearchCV(
        LogisticRegression(),
        {"C": [0.01, 0.1, 1], "penalty": ["l2"], "solver": ["lbfgs"]},
        cv=10,
    ).fit(X_train, Y_train)
    models["SVM"] = GridSearchCV(
        SVC(),
        {
            "kernel": ("linear", "rbf", "poly", "rbf", "sigmoid"),
            "C": np.logspace(-3, 3, 5),
            "gamma": np.logspace(-3, 3, 5),
        },
        cv=10,
    ).fit(X_train, Y_train)
    models["Tree"] = GridSearchCV(
        DecisionTreeClassifier(),
        {
            "criterion": ["gini", "entropy"],
            "splitter": ["best", "random"],
            "max_depth": [2 * n for n in range(1, 10)],
            "max_features": ["sqrt", "log2"],
            "min_samples_leaf": [1, 2, 4],
            "min_samples_split": [2, 5, 10],
        },
        cv=10,
    ).fit(X_train, Y_train)
    models["KNN"] = GridSearchCV(
        KNeighborsClassifier(),
        {
            "n_neighbors": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "algorithm": ["auto", "ball_tree", "kd_tree", "brute"],
            "p": [1, 2],
        },
        cv=10,
    ).fit(X_train, Y_train)

    def auc_scores(model, features):
        if hasattr(model, "predict_proba"):
            scores = model.predict_proba(features)[:, 1]
        else:
            scores = model.decision_function(features)
        return roc_auc_score(Y_test, scores)

    order = ["LogReg", "SVM", "Tree", "KNN"]
    rows = {"Accuracy": [], "Precision": [], "Recall": [], "F1": [], "AUC": []}
    matrices = {}
    for name in order:
        model = models[name]
        yhat = model.predict(X_test)
        matrices[name] = confusion_matrix(Y_test, yhat)
        rows["Accuracy"].append(model.score(X_test, Y_test))
        rows["Precision"].append(precision_score(Y_test, yhat))
        rows["Recall"].append(recall_score(Y_test, yhat))
        rows["F1"].append(f1_score(Y_test, yhat))
        rows["AUC"].append(auc_scores(model, X_test))
    metrics = pd.DataFrame(rows, index=order)
    cv = pd.Series({name: models[name].best_score_ for name in order})
    return order, metrics, matrices, cv


def fig_model_scores(order, metrics: pd.DataFrame) -> None:
    plot_df = metrics.reset_index(names="Model").melt(
        id_vars="Model", var_name="Metric", value_name="Score"
    )
    fig, ax = plt.subplots(figsize=(9, 4.5))
    sns.barplot(
        data=plot_df, x="Model", y="Score", hue="Metric", palette="muted", ax=ax
    )
    ax.set_title("Model evaluation on the 18-launch test set")
    ax.set_xlabel("Model")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.08)
    ax.legend(title="Metric", ncol=3, loc="lower right", fontsize=8)
    _save(fig, "07-model-evaluation-scores.png")


def fig_confusion_matrices(order, matrices) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(9, 8))
    for ax, name in zip(axes.flatten(), order):
        sns.heatmap(
            matrices[name],
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=False,
            ax=ax,
            xticklabels=["Failure", "Success"],
            yticklabels=["Failure", "Success"],
        )
        ax.set_title(name)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
    fig.suptitle("Confusion matrices (test set)", fontsize=14, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    _save(fig, "08-confusion-matrices.png")


# ---------------------------------------------------------------------------
# Interactive Folium map
# ---------------------------------------------------------------------------
def build_map(df: pd.DataFrame) -> str:
    import folium
    from folium.plugins import MarkerCluster

    site_map = folium.Map(location=[29.5, -80.6], zoom_start=5, tiles="OpenStreetMap")

    site_centers = df.groupby("Launch Site")[["Lat", "Long"]].first()
    for site, row in site_centers.iterrows():
        successes = int(df.loc[df["Launch Site"] == site, "class"].sum())
        total = int((df["Launch Site"] == site).sum())
        folium.Circle(
            [row["Lat"], row["Long"]],
            radius=1500,
            color="#d35400",
            fill=True,
            fill_opacity=0.4,
            popup=f"{site}: {successes}/{total} successful landings",
        ).add_to(site_map)
        folium.map.Marker(
            [row["Lat"], row["Long"]],
            icon=folium.DivIcon(
                icon_size=(20, 20),
                icon_anchor=(0, 0),
                html=(
                    '<div style="font-size: 11px; color:#d35400;">'
                    f"<b>{site}</b></div>"
                ),
            ),
        ).add_to(site_map)

    cluster = MarkerCluster(name="Launches").add_to(site_map)
    colors = {1: "green", 0: "red"}
    for _, record in df.iterrows():
        folium.Marker(
            location=[record["Lat"], record["Long"]],
            popup=(
                f"Flight {record['Flight Number']} &mdash; {record['Launch Site']}"
                f" &mdash; {'Success' if record['class'] == 1 else 'Failure'}"
            ),
            icon=folium.Icon(color=colors[int(record["class"])]),
        ).add_to(cluster)
    folium.LayerControl().add_to(site_map)

    os.makedirs(MAPS, exist_ok=True)
    out = os.path.join(MAPS, "launch_sites.html")
    site_map.save(out)
    return out


def main() -> None:
    os.makedirs(FIGURES, exist_ok=True)
    _setup_theme()
    df = load_geo()

    fig_outcome_distribution(df)
    fig_flight_vs_payload(df)
    fig_flight_vs_site(df)
    fig_success_by_orbit(df)
    fig_yearly_trend(df)
    fig_payload_vs_site(df)
    fig_success_by_site(df)

    order, metrics, matrices, cv = run_models()
    fig_model_scores(order, metrics)
    fig_confusion_matrices(order, matrices)

    build_map(df)

    print("Figures written to", FIGURES)
    print("\nTest-set metrics (should match notebook 07):")
    print(metrics.round(4).to_string())
    print("\nCross-validated accuracy:")
    print(cv.round(4).to_string())


if __name__ == "__main__":
    main()
