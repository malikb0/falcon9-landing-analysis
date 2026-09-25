# Data dictionary

Column descriptions for the processed datasets in `data/processed/`.

## `dataset_part_1.csv` (90 rows, 17 columns)

The Falcon 9 launch table before labelling.

| Column | Type | Description |
|--------|------|-------------|
| `FlightNumber` | int | Sequential flight number (1–90). |
| `Date` | date | Launch date (YYYY-MM-DD). |
| `BoosterVersion` | text | Booster family (all `Falcon 9`). |
| `PayloadMass` | float | Payload mass in kg; missing values filled with the column mean. |
| `Orbit` | text | Target orbit (LEO, ISS, GTO, …). |
| `LaunchSite` | text | Launch site name. |
| `Outcome` | text | Landing outcome string (e.g. `True ASDS`, `False Ocean`, `None None`). |
| `Flights` | int | Number of flights of this core (including the current one). |
| `GridFins` | bool | Whether grid fins were used. |
| `Reused` | bool | Whether the core had flown before. |
| `Legs` | bool | Whether landing legs were used. |
| `LandingPad` | text | Landing pad ID; null when no pad was involved. |
| `Block` | int | Booster block number. |
| `ReusedCount` | int | Number of prior reuses of the core. |
| `Serial` | text | Core serial number. |
| `Longitude` | float | Launch-site longitude. |
| `Latitude` | float | Launch-site latitude. |

## `dataset_part_2.csv` (90 rows, 18 columns)

`dataset_part_1.csv` plus:

| Column | Type | Description |
|--------|------|-------------|
| `Class` | int | Landing-success label: `1` = landed successfully, `0` = did not (including `None None`, i.e. no attempt). |

## `dataset_part_3.csv` (90 rows, 83 columns)

The one-hot encoded feature matrix used by the models. Numeric columns:

- `FlightNumber`, `PayloadMass`, `Flights`, `Block`, `ReusedCount`
- `Orbit_*` — one column per orbit family
- `LaunchSite_*` — one column per launch site
- `LandingPad_*` — one column per landing pad
- `Serial_*` — one column per core serial
- `GridFins_False`/`True`, `Reused_False`/`True`, `Legs_False`/`True`

All values are `float64`; the matrix contains no missing values.

## `spacex_launch_geo.csv` (56 rows, 13 columns)

A launch table covering 2010–2018 with coordinates, used by the map and the
launch-site charts: `Flight Number`, `Date`, `Time (UTC)`, `Booster Version`,
`Launch Site`, `Payload`, `Payload Mass (kg)`, `Orbit`, `Customer`,
`Landing Outcome`, `class`, `Lat`, `Long`.

## `spacex_launch_dash.csv` (56 rows, 6 columns)

The slim dashboard table: `Flight Number`, `Launch Site`, `class`,
`Payload Mass (kg)`, `Booster Version`, `Booster Version Category`.

## Raw files

| File | Description |
|------|-------------|
| `data/raw/launch_dict.csv` | API launch records before filtering/labelling (includes Falcon 1). |
| `data/raw/spacex_web_scraped.csv` | Rows scraped from the Wikipedia launch table. |
| `data/raw/spacex_launch.csv` | Launch table used for the SQL analysis (raw column names). |
