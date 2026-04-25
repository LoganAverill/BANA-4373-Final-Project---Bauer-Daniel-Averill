# Oil Price Shocks and Texas Employment

## Project Summary

This project examines whether changes in WTI oil prices predict employment growth in Texas energy-related industries and whether this relationship changes after major oil price shocks. Using data from FRED and the BLS QCEW (2010–2025), we construct a county-level dataset and analyze it using exploratory data analysis, regression models, and a Difference-in-Differences (DiD) approach. The results show that higher oil prices are associated with slightly higher employment growth, but the effect is small, and oil prices alone do not explain much of the variation in employment. Additionally, there is no strong evidence that the relationship changed after the 2020 oil price shock.


## How to Run the Project

Assume a fresh Python environment.

### 1. Download the repository

Download or clone the project from GitHub, then navigate into the project folder:

```bash
git clone https://github.com/LoganAverill/BANA-4373-Final-Project---Bauer-Daniel-Averill
cd oil-employment-project

```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Run Notebooks in Order
Location: notebooks/
Run the following notebooks in sequence: 
1. ETL Notebook
   - Purpose: Load raw data, clean it, and create the final dataset
   - Output: data_clean/final.dataset.csv
2. EDA Notebook
   - Purpose: Explore distributions, time trends, and relationships
   - Output: Figures saved to exports/
3. Analysis Notebook
   - Purpose: Run OLS regressions and Difference-in-Difference (DiD) analysis
   - Output: Model results and interpretations
   
### Data Sources
- FRED (Federal Reserve Economic Data)
  - WTI Oil Prices (WTISPLC): https://fred.stlouisfed.org/series/WTISPLC
  - Texas Unemployment Rate: https://fred.stlouisfed.org/
- BLS QCEW (Quarterly Census of Employment and Wages)
  - https://www.bls.gov/cew/downloadable-data-files.htm
  - 
Due to file size limitations, raw QCEW data is not stored in this repository.

To reproduce results:
1. Download QCEW data from:
https://www.bls.gov/cew/downloadable-data-files.htm
2. Select: CSVs Single Files → Quarterly → [desired years] - this study uses 2010-2025
3. Place files in the `data_raw/` folder

FRED data can be downloaded directly. 

### Team Members
- Anthony Bauer:
- Jackson Daniel:
- Logan Averill:

### Notes
- All code is written to be fully reproducible
- Data is stored in data_raw/ and data_clean/
- Figures are saved to exports/
