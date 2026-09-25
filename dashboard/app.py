"""Interactive SpaceX Falcon 9 landing dashboard.

Run from this directory with::

    python app.py

It reads the processed launch table from ``data/processed/spacex_launch_dash.csv``
and exposes four controls: a launch-site dropdown, an outcome pie chart, a payload
range slider and a payload-vs-success scatter chart.
"""

import os

import dash
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html

DATA_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "data",
    "processed",
    "spacex_launch_dash.csv",
)

spacex_df = pd.read_csv(DATA_FILE)
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Round the slider ceiling up so the full payload range is selectable.
payload_slider_max = int(max_payload) + (100 - int(max_payload) % 100)
slider_marks = {
    i: f"{i}" for i in range(0, payload_slider_max + 1, 2500)
}

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Falcon 9 Landing Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "fontSize": 40},
        ),
        html.P(
            "Explore the relationship between launch site, payload mass and "
            "first-stage landing success.",
            style={"textAlign": "center"},
        ),
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "All Sites"},
                {"label": "CCAFS LC-40", "value": "CCAFS LC-40"},
                {"label": "VAFB SLC-4E", "value": "VAFB SLC-4E"},
                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"},
            ],
            value="All Sites",
            placeholder="Select a launch site",
            searchable=True,
        ),
        html.Br(),
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (kg):"),
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=payload_slider_max,
            step=500,
            marks=slider_marks,
            value=[min_payload, max_payload],
        ),
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(launch_site):
    """Show successful-landing totals for all sites, or the outcome split for one."""
    if launch_site == "All Sites":
        successes = spacex_df.groupby("Launch Site")["class"].sum()
        fig = px.pie(
            values=successes.values,
            names=successes.index,
            title="Total Successful Launches by Site",
        )
    else:
        counts = (
            spacex_df.loc[spacex_df["Launch Site"] == launch_site, "class"]
            .value_counts()
            .sort_index()
        )
        labels = counts.index.map({0: "Failure", 1: "Success"})
        fig = px.pie(
            values=counts.values,
            names=labels,
            title=f"Landing Outcomes for {launch_site}",
        )
    return fig


@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def get_payload_chart(launch_site, payload_mass):
    """Scatter payload mass against landing success, filtered by site and payload."""
    low, high = payload_mass
    in_range = spacex_df["Payload Mass (kg)"].between(low, high)
    if launch_site == "All Sites":
        filtered = spacex_df.loc[in_range]
        title = "Payload vs. Landing Success for All Sites"
    else:
        filtered = spacex_df.loc[(spacex_df["Launch Site"] == launch_site) & in_range]
        title = f"Payload vs. Landing Success for {launch_site}"

    fig = px.scatter(
        filtered,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        hover_data=["Launch Site"],
        title=title,
    )
    fig.update_yaxes(tickvals=[0, 1], ticktext=["Failure", "Success"], title="Outcome")
    return fig


if __name__ == "__main__":
    app.run(debug=True)
