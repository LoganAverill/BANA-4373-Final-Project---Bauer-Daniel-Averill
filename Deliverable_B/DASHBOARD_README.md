# Deliverable B — Interactive Dashboard

**BANA 4373 Final Project | Spring 2026**
**Authors:** Logan Averill, Anthony Bauer, Jackson Daniel
**Topic:** Oil Price Shocks and Texas Energy Employment

---

## What this is

An interactive dashboard companion to the team's analytical pipeline. The grader can pick any Texas county, time window, and pre/post-2020 split, and a live OLS regression of energy-sector employment growth on WTI oil price recomputes on every selection.

## What's in this folder

| File | Purpose |
|---|---|
| `04_dashboard.ipynb` | Jupyter notebook — recommended way to run the dashboard |
| `app.py` | Standalone Python script — alternative to the notebook |
| `final_dataset.csv` | Merged county-level panel (9,295 obs, 202 counties) |
| `requirements.txt` | Pinned Python dependencies |
| `Executive_Brief.pdf` | 3-page executive brief (the graded artifact) |
| `DASHBOARD_README.md` | This file |

---

## How to run (pick one path)

Both paths require Python 3.10 or newer. All dependencies are listed in `requirements.txt`.

### Path A — Jupyter notebook (recommended)

This matches the rest of the project's notebook-based workflow.

1. Open a terminal in this folder.
2. Install dependencies:
   - macOS / Linux: `python3 -m pip install -r requirements.txt`
   - Windows: `python -m pip install -r requirements.txt`
3. Launch Jupyter:
   - macOS / Linux: `python3 -m notebook`
   - Windows: `python -m notebook`
4. In the browser tab that opens, click `04_dashboard.ipynb`.
5. Click `Cell` -> `Run All`. The dashboard will render inline at the bottom of the notebook.

### Path B — Standalone script

Use this if you'd rather not run Jupyter.

1. Open a terminal in this folder.
2. Install dependencies (same as Path A step 2).
3. Run the app:
   - macOS / Linux: `python3 app.py`
   - Windows: `python app.py`
4. Open `http://127.0.0.1:8050` in any browser.

---

## What the dashboard does

Three interactive controls:

- **County dropdown** — switch between "ALL TEXAS" (panel average) and the top 12 Texas counties by mean energy employment (Harris, Midland, Ector, Tarrant, Dallas, etc.).
- **Sample-split dropdown** — restrict the regression to pre-2020, post-2020, or the full window.
- **Time-window slider** — any year span from 2010 to 2025.

Below the chart, a live OLS panel updates on every selection: coefficient on WTI, p-value, R-squared, and N.

## Data sources

| Variable | Source | Notes |
|---|---|---|
| WTI oil price | FRED, `WTISPLC` | Monthly, averaged to quarterly |
| Texas unemployment | FRED, `TXUR` | Monthly, averaged to quarterly |
| County energy employment | BLS QCEW, NAICS 211 + 213 | Texas counties, 2010 Q2 - 2025 Q3 |

Final merged panel: 9,295 observations across 202 Texas counties.

---

## Troubleshooting

**`pip` or `python` not found** — use `python3` and `python3 -m pip` on macOS / Linux.

**`error: externally-managed-environment`** (macOS/Linux with Homebrew) — add `--user`: `python3 -m pip install --user -r requirements.txt`.

**Port 8050 in use** (Path B only) — open `app.py`, change the last line's `port=8050` to `port=8051`.

**Jupyter won't open** (Path A) — make sure you're in this folder when you run the install and launch commands.

**`ModuleNotFoundError`** — re-run `pip install -r requirements.txt`.

**Stop the server** — press `Ctrl+C` in the terminal.
