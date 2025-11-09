import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout='wide', page_title='India Water Footprint Dashboard')
st.title('India Water Footprint — Starter Dashboard')

@st.cache_data
def load_data():
    df_states = pd.read_csv('data/state_monthly_water.csv')
    df_crops = pd.read_csv('data/crop_water_footprint.csv')
    df_house = pd.read_csv('data/household_survey.csv')
    return df_states, df_crops, df_house

df_states, df_crops, df_house = load_data()

# Sidebar controls
st.sidebar.header('User Inputs')
state = st.sidebar.selectbox('Select State', sorted(df_states['state'].unique()))
year = st.sidebar.selectbox('Select Year', sorted(df_states['year'].unique(), reverse=True))
month = st.sidebar.selectbox('Select Month (1-12)', list(range(1,13)), index=0)

st.sidebar.markdown('---')
st.sidebar.header('Personal Footprint Calculator')
persons = st.sidebar.number_input('Household size (persons)', min_value=1, value=4, step=1)
daily_l_pp = st.sidebar.number_input('Daily liters per person', min_value=20, value=150, step=10)
diet = st.sidebar.selectbox('Diet profile', ['Vegetarian','Mixed','High Meat','High Dairy'])
laundry = st.sidebar.slider('Laundry per week (loads)', 0, 14, 2)
showers = st.sidebar.slider('Showers per week (per person)', 0, 21, 7)
st.sidebar.markdown('---')
if st.sidebar.button('Estimate My Footprint'):
    domestic_monthly_ML = (daily_l_pp * persons * 30) / 1e6  # convert liters to ML
    # Estimate food footprint from diet
    diet_factor = {'Vegetarian':0.9,'Mixed':1.0,'High Meat':1.4,'High Dairy':1.2}[diet]
    food_m3_per_month = diet_factor * 200  # simple proxy; replace with crop-based calc
    food_ML = food_m3_per_month / 1000  # convert cubic meters to ML for consistency
    total_ML = domestic_monthly_ML + food_ML
    st.sidebar.success(f'Estimated monthly household water footprint: {total_ML:.3f} ML')

# Main area: show state time-series
st.subheader(f'{state} — Consumption by sector ({year}-{month})')
df_sel = df_states[(df_states['state']==state) & (df_states['year']==year) & (df_states['month']==month)]
if df_sel.empty:
    st.info('No data for selection.')
else:
    dom = df_sel['domestic_ML'].sum()
    ag = df_sel['agriculture_ML'].sum()
    ind = df_sel['industrial_ML'].sum()
    st.metric('Domestic (ML)', f'{dom:.2f}')
    st.metric('Agriculture (ML)', f'{ag:.2f}')
    st.metric('Industrial (ML)', f'{ind:.2f}')
    st.markdown('### Time series (Total consumption per month)')
    df_ts = df_states[df_states['state']==state].groupby(['year','month'])['total_consumption_ML'].sum().reset_index()
    df_ts['date'] = pd.to_datetime(df_ts['year'].astype(str)+'-'+df_ts['month'].astype(str)+'-01')
    st.line_chart(df_ts.set_index('date')['total_consumption_ML'])

st.markdown('---')
st.subheader('Crop Water Footprint Lookup')
crop = st.selectbox('Select crop', df_crops['crop'].unique())
state_for_crop = st.selectbox('State for crop', df_crops['state'].unique(), index=0)
val = df_crops[(df_crops['crop']==crop) & (df_crops['state']==state_for_crop) & (df_crops['year']==2020)]
if not val.empty:
    st.write(f"Estimated water footprint for {crop} in {state_for_crop} (2020): {val['water_m3_per_ton'].values[0]} m³/ton")
else:
    st.write('No exact match — showing median across states:')
    st.write(df_crops[df_crops['crop']==crop]['water_m3_per_ton'].median())

st.markdown('---')
st.subheader('Household Survey Snapshot (sample)')
st.dataframe(df_house[df_house['state']==state].head(50))
