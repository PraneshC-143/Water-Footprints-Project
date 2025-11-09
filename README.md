# Water Footprint Dashboard - Starter Data & Streamlit App
This project contains synthetic but realistic sample datasets to help you build a water footprint dashboard covering all Indian states.

Files included (in `data/`):
- state_monthly_water.csv : State-wise monthly water consumption (ML) for 2015-2025 with sectoral breakup and population estimate.
- crop_water_footprint.csv : Crop water footprint (m^3 per ton) by state for 2010-2025.
- household_survey.csv : Synthetic household survey (2018-2025) samples with daily water use and behaviors.

How to use
1. Install dependencies: `pip install -r requirements.txt`
2. Run the Streamlit app: `streamlit run streamlit_app.py`
3. The app loads CSVs from `data/` and provides:
   - Time-series charts by state and sector
   - Simple per-person footprint calculator using household inputs
   - Crop footprint lookup to estimate food-related water use

Note
- Datasets are synthetic for demo/prototyping. Replace with real data when available (e.g., CGWB, NITI Aayog, IWMI).
- You can expand the household survey or map state names to ISO codes for mapping components.
