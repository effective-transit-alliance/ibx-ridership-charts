# IBX Ridership Charts

A chart comparing ridership projections for the Interborough Express (IBX)
with projected and current ridership of related lines.

![IBX and Related Ridership](ridership.svg)

## Data

The numbers are in [`ridership.csv`](ridership.csv),
in average weekday riders.
Each row has a `label`, a `riders_per_day` value, and a `group`,
which sets the bar color:

- `IBX Projection`: IBX ridership projections
  (the feasibility study, PEL, 20YN, STOPS runs, Hai Yang et al., and the current projection).
- `Other Projection`: projections for other lines (SAS Phase 2, SAS West).
- `Current Ridership`: existing lines (G, BQE, SAS Phase 1).

Bars are sorted by ridership, so rows can be in any order.

## Generating the Charts

[`make_charts.py`](make_charts.py) renders `ridership.csv`
to `ridership.svg` and `ridership.png`.
The PNG is meant for pasting into Google Docs
and isn't committed.

Tools (Python, `uv`, and ImageMagick) are managed by `mise` via [`mise.toml`](mise.toml).
Run either of:

```sh
./make_charts.py
mise run charts
```
