import pandas as pd, numpy as np
import matplotlib.pyplot as plt, seaborn as sb
import streamlit as st
import altair as alt

st. set_page_config(layout="wide")


st.markdown("<h1 style=text-align:center;'position:relative;font-size:80px; color: '#fafafa';'>WebTract</h1>",unsafe_allow_html=True)
st.markdown("<h1 style=text-align:center;'position:relative;font-size:40px; color: '#fafafa';'>COVID-19 data visualisation</h1>",unsafe_allow_html=True)



option2= st.sidebar.selectbox(
'Select', ('Maps','Graphs', 'Table','Singapore'))


if option2== 'Maps':

    option= st.selectbox(
    'Select Map',
    ('Cases', 'Deaths','Cases last 7 days')
    )


    ds = pd.read_csv('WHO-COVID-19-global-table-data.csv',index_col=False)
    ds2=ds[ds.Name !="Global"]
    ds3=ds2[ds2.Name !="Other"]

    cases_df = ds2.groupby('Name').max().reset_index()
    cases = cases_df.drop(columns = ['Deaths - cumulative total'])
    deaths = cases_df.drop(columns = ['Cases - cumulative total'])
    cases7 = cases_df.drop(columns = ['Deaths - cumulative total', 'Cases - cumulative total'])




    from plotly.offline import plot
    import plotly.graph_objects as go


    fig_cases = go.Figure(data = go.Choropleth(locations = cases['Name'],
                                         z = cases['Cases - cumulative total'].astype(int),
                                         locationmode = 'country names',
                                         colorscale = 'YlOrRd',
                                         colorbar_title = "Infections"))

    fig_cases.update_layout(title_text = 'COVID 19: Global Infections Count',
                      geo = dict(bgcolor= 'rgba(0,0,0,0)',
                      showframe = False,
                               showcoastlines = False,
                               projection_type = 'equirectangular',
                               resolution = 50),
                    height=700, width=1200,

                    annotations = [dict(x = 0.5,
                                        y = 0.1,
                                        text='',
                                        showarrow = False)])





    fig_deaths = go.Figure(data = go.Choropleth(locations = deaths['Name'],
                                                z = deaths['Deaths - cumulative total'].astype(int),
                                                locationmode = 'country names',
                                                colorscale = 'YlOrRd',
                                                colorbar_title = "Deaths"))

    fig_deaths.update_layout(title_text = 'COVID 19: Global Death Count',
                             geo = dict(bgcolor= 'rgba(0,0,0,0)',
                             showframe = False,
                                        showcoastlines = False,
                                        projection_type = 'equirectangular',
                                        resolution = 50),

                            height=700, width=1200,



                             annotations = [dict(x = 0.5,
                                                 y = 0.1,
                                                 text='',
                                                 showarrow = False)])

    fig_cases7 = go.Figure(data = go.Choropleth(locations = cases['Name'],
                                             z = cases['Cases - newly reported in last 7 days'].astype(int),
                                             locationmode = 'country names',
                                             colorscale = 'YlOrRd',
                                             colorbar_title = "Infections last 7 days"))

    fig_cases7.update_layout(title_text = 'COVID 19: Global Infections Count last 7 days',
                          geo = dict(bgcolor= 'rgba(0,0,0,0)',
                          showframe = False,
                                   showcoastlines = False,
                                   projection_type = 'equirectangular',
                                   resolution = 50),
                        height=700, width=1200,

                        annotations = [dict(x = 0.5,
                                            y = 0.1,
                                            text='',
                                            showarrow = False)])



    if option == 'Cases':
        st.plotly_chart(fig_cases)


    if option == 'Deaths':
        st.plotly_chart(fig_deaths)

    if option == 'Cases last 7 days':
        st.plotly_chart(fig_cases7)




if option2== 'Graphs':
    df2= pd.read_excel('owidvac.xlsx', usecols=["new_cases","new_vaccinations_smoothed","date","location"])
    df3=df2[df2.location !="Asia"]
    df4=df3[df3.location !="North America"]
    df5=df4[df4.location !="Africa"]
    df6=df5[df5.location !="Australia"]
    df7=df6[df6.location !="Europe"]
    df8=df7[df7.location != "World"]
    df9=df8[df8.location != "South America"]
    df10=df9[df9.location !="European Union"]




    subset_data=df10
    country_name_input = st.multiselect(
    'Country name',
    df10.groupby('location').count().reset_index()['location'].tolist())

    if len(country_name_input)>0:
        subset_data = df10[df10['location'].isin(country_name_input)]
    st.subheader('Trend of Cases past month')
    total_cases_graph  =alt.Chart(subset_data).mark_line().encode(
        x=alt.X('date',type= "nominal", title='Date'),
        y=alt.Y('new_cases',  title='New cases'),
        color='location',
        tooltip = ('new_cases','date','location'),
    ).properties(
        width=1200,
        height=600
    ).configure_axis(
        labelFontSize=17,
        titleFontSize=20
    )
    vaccination_graph =alt.Chart(subset_data).mark_line().encode(
        x=alt.X('date',type= "nominal", title='Date'),
        y=alt.Y('new_vaccinations_smoothed',  title='No. of vaccinations'),
        color='location',

        tooltip = ('new_vaccinations_smoothed','date','location'),
    ).properties(
        width=1200,
        height=600
    ).configure_axis(
        labelFontSize=17,
        titleFontSize=20
    )
    st.altair_chart(total_cases_graph)
    st.altair_chart(vaccination_graph)

if option2=='Table':
    df = pd.read_csv('WHO-COVID-19-global-table-data.csv',index_col=False)

    df = df.drop(columns = ['Cases - cumulative total per 100000 population', 'Cases - newly reported in last 7 days', 'Cases - newly reported in last 7 days per 100000 population', 'Cases - newly reported in last 24 hours', 'Deaths - cumulative total per 100000 population', 'Deaths - newly reported in last 7 days', 'Deaths - newly reported in last 7 days per 100000 population', 'Deaths - newly reported in last 24 hours' ])


    option3= st.multiselect('Find country, e.g. Singapore',df.groupby('Name').count().reset_index()['Name'].tolist())
    if len(option3)>0:
        df = df[df['Name'].isin(option3)]



    st.dataframe(df)

if option2=='Singapore':
    from IPython.display import IFrame
    import streamlit as st
    import pandas as pd
    from streamlit_folium import folium_static
    df = pd.read_csv("covloc.csv")
    import folium
    import streamlit.components.v1 as components
    def folium_static(fig, width=1100, height=1000):
        if isinstance(fig, folium.Map):
            fig = folium.Figure().add_child(fig)
            return components.html(
            fig.render(), height=(fig.height or height) + 10, width=width
            )
    m = folium.Map(location = [1.3601710211245763, 103.81762899301569],zoom_start=11.5)
    def cm(x):
        folium.Circle(location = [x[0],x[1]],
                 radius = 400,
                 color='red',
                 fill = True,
                 popup = x[2]).add_to(m)

    df[['Latitude','Longitude','Location']].apply(lambda x: cm(x), axis=1)








    st.write("Active COVID-19 cases in Singapore")
    folium_static(m)
