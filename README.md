# Oil Price Shocks and Texas Employment

## Project Summary

This project examines whether changes in WTI oil prices predict employment growth in Texas energy-related industries and whether this relationship changes after major oil price shocks. Using data from FRED and the BLS QCEW (2010–2025), we construct a county-level dataset and analyze it using exploratory data analysis, regression models, and a Difference-in-Differences (DiD) approach. The results show that higher oil prices are associated with slightly higher employment growth, but the effect is small, and oil prices alone do not explain much of the variation in employment. Additionally, there is no strong evidence that the relationship changed after the 2020 oil price shock.


## How to Run the Project

Assume a fresh Python environment.

### 1. Download the repository

Download or clone the project from GitHub, then navigate into the project folder:

```bash
git clone https://github.com/yourname/oil-employment-project.git
cd oil-employment-project

Due to file size limitations, raw QCEW data is not stored in this repository.

To reproduce results:
1. Download QCEW data from:
https://www.bls.gov/cew/downloadable-data-files.htm
2. Select: CSVs Single Files → Quarterly → [desired years] - this study uses 2010-2025
3. Place files in the `data_raw/` folder

FRED data can be downloaded directly or accessed via API.
