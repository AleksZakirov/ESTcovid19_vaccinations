import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go



st.title('Vaktsineerimine Eestis')

def load_country_data():
    country_data_raw = pd.read_csv('https://opendata.digilugu.ee/covid19/vaccination/v2/opendata_covid19_vaccination_total.csv')
    country_data_raw = country_data_raw[['StatisticsDate', 'MeasurementType', 'DailyCount', 'TotalCount', 'PopulationCoverage']]
    country_data_raw['StatisticsDate'] = pd.to_datetime(country_data_raw['StatisticsDate'])
    country_data = country_data_raw.rename(columns={'StatisticsDate':'index'}).set_index('index')
    country_data = country_data.rename(columns={'DailyCount':'Vaktsineeritud inimesi', 'TotalCount':'Kokku vaktsineeritud', 'PopulationCoverage':'% vaktsineeritud'})

    return country_data, country_data_raw

st.header('Uute vaktsineerinute arv')

country_data_daily, country_data_daily_raw = load_country_data()
country_data_daily = country_data_daily[country_data_daily['MeasurementType'] == 'DosesAdministered']
country_data_daily['Keskmine 7-päeva jooksul'] = country_data_daily['Vaktsineeritud inimesi'].rolling(window=7).mean()
country_data_daily_raw = country_data_daily_raw[country_data_daily_raw['MeasurementType'] == 'DosesAdministered']
country_data_daily_raw['7-day MA'] = country_data_daily_raw['DailyCount'].rolling(window=7).mean().round()

columns_to_plot = ['DailyCount']
labels_to_plot = {'DailyCount':'Vaktsineeritud inimesi'}


fig = go.Figure()
fig.add_trace(go.Scatter(
    x=country_data_daily_raw['StatisticsDate'],
    y=country_data_daily_raw['DailyCount'],
    name="Vaktsineeritud",
    legendrank=1
))
fig.add_trace(go.Scatter(
        x=country_data_daily_raw['StatisticsDate'],
        y=country_data_daily_raw['7-day MA'],
        name="7-päeva keskmine",
        legendrank=2,
        visible='legendonly'
    ))
fig.update_layout(showlegend=True, legend=dict(orientation='h', x=0, y=1.15), xaxis_showgrid=False, yaxis_showgrid=True, dragmode='pan', hovermode='x')
fig.update_yaxes(fixedrange=True)
st.plotly_chart(fig, config=dict({'scrollZoom': True}))


















#map_data = pd.DataFrame({'lat':58.5953, 'lon':25.0136}, index=[0])
#st.map(map_data, zoom=6.2)

