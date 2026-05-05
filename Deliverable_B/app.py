"""
Oil Price Shocks and Texas Energy Employment - Interactive Dashboard
BANA 4373 Final Project | Spring 2026
Authors: Logan Averill, Anthony Bauer, Jackson Daniel

Companion to the team's analytical pipeline. Lets a user explore the
relationship between WTI oil prices and county-level Texas energy-sector
employment growth (NAICS 211 + 213) across selectable time windows and counties.

Run with:  python app.py
Then open: http://127.0.0.1:8050  in your browser.
"""

import os
import numpy as np
import pandas as pd
import statsmodels.api as sm
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output

# ---------------------------------------------------------------------------
# 1. Load merged county-level panel (9,295 obs after cleaning)
# ---------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(HERE, "final_dataset.csv"))

# Drop divide-by-zero growth rows (prior-quarter emplvl == 0)
df = df[~np.isinf(df["emplvl_growth"])].copy()

# Build a quarterly date for plotting
# Build a quarterly timestamp from year + quarter (no PeriodIndex deprecation noise)
_q_to_month = {1: 1, 2: 4, 3: 7, 4: 10}
df["date"] = pd.to_datetime(
    df["year"].astype(str) + "-" + df["qtr"].map(_q_to_month).astype(str).str.zfill(2) + "-01"
)

# Selected counties for the dropdown — top 12 by mean energy employment, plus "All Texas"
top_counties = (
    df.groupby("area_fips")["emplvl"]
    .mean()
    .sort_values(ascending=False)
    .head(12)
    .index.tolist()
)

# Friendly county names for the FIPS codes that show up most
COUNTY_NAMES = {
    48001: "Anderson", 48029: "Bexar (San Antonio)", 48039: "Brazoria",
    48085: "Collin", 48113: "Dallas", 48121: "Denton",
    48135: "Ector (Odessa)", 48141: "El Paso", 48157: "Fort Bend",
    48167: "Galveston", 48183: "Gregg (Longview)", 48201: "Harris (Houston)",
    48215: "Hidalgo", 48309: "McLennan (Waco)", 48329: "Midland",
    48339: "Montgomery", 48355: "Nueces (Corpus Christi)", 48439: "Tarrant (Fort Worth)",
    48453: "Travis (Austin)", 48485: "Wichita", 48999: "Unallocated",
}

def county_label(fips):
    name = COUNTY_NAMES.get(int(fips), f"County {int(fips)}")
    return f"{name} ({int(fips)})"

county_options = [{"label": "ALL TEXAS (panel average)", "value": "ALL"}] + [
    {"label": county_label(f), "value": int(f)} for f in top_counties
]

YEAR_MIN = int(df["year"].min())
YEAR_MAX = int(df["year"].max())

# ---------------------------------------------------------------------------
# 2. App layout
# ---------------------------------------------------------------------------
app = Dash(__name__)
app.title = "Texas Oil-Employment Explorer"

app.layout = html.Div(
    style={"fontFamily": "Arial, sans-serif", "maxWidth": "1200px", "margin": "20px auto", "padding": "0 24px"},
    children=[
        html.H1("Oil Price Shocks and Texas Energy Employment"),
        html.P(
            "Interactive companion to the BANA 4373 final project. "
            "Pick a county and time window to see how WTI oil prices co-move with "
            "energy-sector employment growth (NAICS 211 + 213). "
            "The OLS panel below recomputes on every selection.",
            style={"color": "#444"},
        ),
        html.Hr(),

        # Controls row
        html.Div(
            style={"display": "flex", "gap": "32px", "flexWrap": "wrap", "marginBottom": "20px"},
            children=[
                html.Div(
                    style={"flex": "1.5", "minWidth": "260px"},
                    children=[
                        html.Label("County:", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="county-dropdown",
                            options=county_options,
                            value="ALL",
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    style={"flex": "1", "minWidth": "200px"},
                    children=[
                        html.Label("Sample split:", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="sample-dropdown",
                            options=[
                                {"label": "Full window (selected)", "value": "all"},
                                {"label": "Pre-2020 only", "value": "pre"},
                                {"label": "Post-2020 only", "value": "post"},
                            ],
                            value="all",
                            clearable=False,
                        ),
                    ],
                ),
                html.Div(
                    style={"flex": "2", "minWidth": "320px"},
                    children=[
                        html.Label("Time window (years):", style={"fontWeight": "bold"}),
                        dcc.RangeSlider(
                            id="year-slider",
                            min=YEAR_MIN, max=YEAR_MAX, step=1,
                            value=[YEAR_MIN, YEAR_MAX],
                            marks={y: str(y) for y in range(YEAR_MIN, YEAR_MAX + 1, 2)},
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),
                    ],
                ),
            ],
        ),

        # Chart
        dcc.Graph(id="ts-chart"),

        # Live model output panel
        html.Div(
            id="model-output",
            style={
                "marginTop": "12px",
                "padding": "20px",
                "backgroundColor": "#f7f7f7",
                "border": "1px solid #ddd",
                "borderRadius": "6px",
            },
        ),

        html.Hr(),
        html.P(
            "Sources: WTI Spot Price (FRED, WTISPLC); Texas Unemployment Rate (FRED, TXUR); "
            "Energy-sector employment from BLS QCEW (NAICS 211 + 213), Texas counties, 2010 Q2 – 2025 Q3. "
            "Model: OLS regression of quarterly county-level employment growth on WTI oil price. "
            "ALL TEXAS option averages county-level growth rates by quarter (unweighted, matching the team's analysis).",
            style={"fontSize": "12px", "color": "#666"},
        ),
    ],
)

# ---------------------------------------------------------------------------
# 3. Helpers
# ---------------------------------------------------------------------------
def filter_df(county, year_range, sample):
    lo, hi = year_range
    sub = df[(df["year"] >= lo) & (df["year"] <= hi)].copy()
    if county != "ALL":
        sub = sub[sub["area_fips"] == int(county)]
    if sample == "pre":
        sub = sub[sub["year"] < 2020]
    elif sample == "post":
        sub = sub[sub["year"] >= 2020]
    return sub

def make_aggregate_series(sub):
    """Quarterly mean of growth rates across counties (matches team's slide)."""
    g = sub.groupby("date").agg(
        emplvl_growth=("emplvl_growth", "mean"),
        WTISPLC=("WTISPLC", "first"),
    ).reset_index()
    return g

# ---------------------------------------------------------------------------
# 4. Callback
# ---------------------------------------------------------------------------
@app.callback(
    [Output("ts-chart", "figure"), Output("model-output", "children")],
    [Input("county-dropdown", "value"),
     Input("year-slider", "value"),
     Input("sample-dropdown", "value")],
)
def update(county, year_range, sample):
    sub = filter_df(county, year_range, sample)

    # Build a single time-series view
    if county == "ALL":
        plot_df = make_aggregate_series(sub)
        county_title = "All Texas (panel average)"
    else:
        plot_df = sub[["date", "emplvl_growth", "WTISPLC"]].sort_values("date")
        county_title = county_label(county)

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=plot_df["date"], y=plot_df["WTISPLC"], name="WTI Oil Price ($)",
                   line=dict(color="#1f77b4", width=2)),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=plot_df["date"], y=plot_df["emplvl_growth"], name="Energy Employment Growth (QoQ)",
                   line=dict(color="#d62728", width=2, dash="dash")),
        secondary_y=True,
    )
    sample_tag = "" if sample == "all" else f" — {sample}-2020"
    fig.update_layout(
        title=dict(
            text=f"{county_title}: WTI vs. Energy Employment Growth, {year_range[0]}–{year_range[1]}{sample_tag}",
            y=0.97, x=0.02, xanchor="left", yanchor="top",
            font=dict(size=15),
        ),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="left", x=0),
        margin=dict(l=60, r=40, t=60, b=80),
        plot_bgcolor="white",
        height=480,
    )
    fig.update_xaxes(title_text="Quarter", showgrid=True, gridcolor="#eee")
    fig.update_yaxes(title_text="WTI Oil Price ($/barrel)", secondary_y=False, showgrid=True, gridcolor="#eee")
    fig.update_yaxes(title_text="Employment Growth (decimal)", secondary_y=True)

    # Live OLS: emplvl_growth ~ WTISPLC, on the *raw* (county-level if applicable) sample
    reg_input = sub.dropna(subset=["WTISPLC", "emplvl_growth"])
    if len(reg_input) < 10:
        panel = html.Div("Not enough observations in this slice to fit a model (need at least 10).")
    else:
        X = sm.add_constant(reg_input["WTISPLC"].values)
        y = reg_input["emplvl_growth"].values
        res = sm.OLS(y, X).fit()
        beta = res.params[1]
        pval = res.pvalues[1]
        r2 = res.rsquared
        n = int(res.nobs)

        sign = "lower" if beta < 0 else "higher"
        magnitude_per_10 = beta * 10 * 100  # in percentage points per $10 oil move
        plain = (
            f"In this slice, a $1 increase in WTI is associated with about "
            f"{abs(beta)*100:.3f} percentage points {sign} quarterly employment growth "
            f"(≈ {abs(magnitude_per_10):.2f} pp per $10 oil move). "
            f"R² = {r2:.3f} — oil prices alone explain only {r2*100:.1f}% of the variation."
        )

        panel = html.Div([
            html.H3("Live OLS: Employment Growth ~ WTI", style={"marginTop": 0}),
            html.Div(
                style={"display": "grid", "gridTemplateColumns": "repeat(4, 1fr)", "gap": "20px"},
                children=[
                    html.Div([html.Div("Coefficient on WTI", style={"fontSize": 12, "color": "#666"}),
                              html.Div(f"{beta:+.4f}", style={"fontSize": 24, "fontWeight": "bold"})]),
                    html.Div([html.Div("p-value", style={"fontSize": 12, "color": "#666"}),
                              html.Div(f"{pval:.4f}", style={"fontSize": 24, "fontWeight": "bold"})]),
                    html.Div([html.Div("R²", style={"fontSize": 12, "color": "#666"}),
                              html.Div(f"{r2:.4f}", style={"fontSize": 24, "fontWeight": "bold"})]),
                    html.Div([html.Div("N (observations)", style={"fontSize": 12, "color": "#666"}),
                              html.Div(f"{n:,}", style={"fontSize": 24, "fontWeight": "bold"})]),
                ],
            ),
    
