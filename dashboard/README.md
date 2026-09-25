# Dashboard

An interactive [Plotly Dash](https://dash.plotly.com/) app for exploring SpaceX
Falcon 9 first-stage landing outcomes.

## Run it

From this directory:

```bash
python app.py
```

Then open <http://127.0.0.1:8050> in a browser. The app reads
`../data/processed/spacex_launch_dash.csv`, so run it from the repository (or keep
the `dashboard/` directory inside the repo).

## What it shows

| Control | Behaviour |
|---------|-----------|
| **Launch-site dropdown** | `All Sites` selects the whole fleet; any other value filters to that launch site. |
| **Outcome pie chart** | For *All Sites*, the total number of successful landings per site; for a single site, the success vs. failure split. |
| **Payload range slider** | Restricts the launches shown in the scatter chart to a payload-mass window (kg). |
| **Payload vs. success scatter** | One point per launch, coloured by booster version, with the site on hover. Useful for spotting how heavier payloads behave across sites. |

The dropdown defaults to `All Sites` so the dashboard renders a complete view on
first load.
