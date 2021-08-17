import requests
import time
import streamlit as st
import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sb
def whodata():
    url = requests.get("https://covid19.who.int/WHO-COVID-19-global-table-data.csv")
    content = url.content
    data = open('WHO-COVID-19-global-data.csv', 'wb')
    data.write(content)
    data.close()

def main():
    while(True):
        whodata()
        data1=pd.read_csv("WHO-COVID-19-global-data.csv")
        print(data1)
        time.sleep(86400)
        st. set_page_config(layout="wide")
        st.markdown("<h1 style=text-align:center;'position:relative;font-size:80px; color: '#fafafa';'>WebTract</h1>",unsafe_allow_html=True)

        ds = pd.read_csv('WHO-COVID-19-global-data.csv')


        ds = ds.drop(columns = ['WHO_region', 'New_cases', 'New_deaths'])


        cases_df = ds.groupby('Country').max().reset_index()

        cases = cases_df.drop(columns = ['Country_code', 'Cumulative_deaths'])
        deaths = cases_df.drop(columns = ['Country_code', 'Cumulative_cases'])


        from plotly.offline import plot
        import plotly.graph_objects as go

        fig_cases = go.Figure(data = go.Choropleth(locations = cases['Country'],
                                             z = cases['Cumulative_cases'].astype(int),
                                             locationmode = 'country names',
                                             colorscale = 'YlOrRd',

                                             colorbar_title = "Infections"))


        fig_cases.update_layout(title_text = 'COVID 19: Global Infections Count',
                          geo = dict(showframe = False,
                                   showcoastlines = False,
                                   projection_type = 'equirectangular'),
                        height=1000, width=2000,

                        annotations = [dict(x = 0.5,
                                            y = 0.1,
                                            text='Source: <a href="https://covid19.who.int/info">\
                                            WHO</a>',
                                            showarrow = False)])

        st.plotly_chart(fig_cases,config = dict({'scrollZoom': False}))


        fig_deaths = go.Figure(data = go.Choropleth(locations = deaths['Country'],
                                                    z = deaths['Cumulative_deaths'].astype(int),
                                                    locationmode = 'country names',
                                                    colorscale = 'ylgnbu',
                                                    colorbar_title = "Deaths"))

        fig_deaths.update_layout(title_text = 'COVID 19: Global Death Count',
                                 geo = dict(showframe = False,
                                            showcoastlines = False,
                                            projection_type = 'equirectangular'),

                                    height=1000, width=2000,
                                 annotations = [dict(x = 0.5,
                                                     y = 0.1,
                                                     text='Source: <a href="https://covid19.who.int/info">\
                                                     WHO</a>',
                                                     showarrow = False)])
        st.plotly_chart(fig_deaths,config = dict({'scrollZoom': False}))
main()
