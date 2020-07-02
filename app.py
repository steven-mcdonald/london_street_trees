import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import pydeck as pdk
import plotly.express as px

# when loading streamlit command below to open larger files
# streamlit run your_script.py --server.maxUploadSize=1028
# ctrl-c in terminal to end script at any time

st.title('Street Trees London')


# Load data
# downloads data from london gov datastore, puts it in a Pandas dataframe,
DATA_URL = ('https://data.london.gov.uk/download/local-authority-maintained-trees/c52e733d-bf7e-44b8-9c97-827cb2bc53be/london_street_trees_gla_20180214.csv')
# note that st.cache before the function means we cache the data
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows,
                        encoding= 'unicode_escape', low_memory=False)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

# Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')
# Load x rows of data into the dataframe.
df = load_data(700000)

# clean data - removing unnecessary columns
df = df.drop(columns=['species_name', 'common_name',
                          'load_date', 'easting', 'northing'])
# clean data - removing lat lon outliers
df = df[(df.longitude > -1) & (df.longitude < 1)]
df = df[(df.latitude > 51) & (df.latitude < 52)]

# clean data - rename long tree name
df['display_name'][df.display_name == 'Chestnut/ Sweet Chestnut'] = 'Chestnut'

# sidebar to select different boroughs and tree types to display
st.sidebar.markdown('An app to display the different trees found on the streets of london')

st.sidebar.subheader('Select Boroughs to Display')
all_boroughs = df.borough.unique().tolist()
boroughs_sel = st.sidebar.multiselect(" ", all_boroughs, default=['Southwark'])
df_sel_b = df[df.borough.isin(boroughs_sel)]

st.sidebar.subheader("Select Tree Types ")
all_types = df.display_name.unique().tolist()
types_sel = st.sidebar.multiselect(" ", all_types, default=['Cherry'])
df_sel_t = df_sel_b[df.display_name.isin(types_sel)]

df_sel_x = df_sel_b[df.display_name == 'Plane']

st.sidebar.subheader('Show common trees in selected boroughs')
if st.sidebar.checkbox('  '):
    temp = df_sel_b['display_name'].value_counts().sort_values()
    y = temp.index
    x = temp.values
    y_pos = [i for i, _ in enumerate(y)]

    fig, ax = plt.subplots(figsize=(6, 4))
    plt.barh(y_pos, x, color='green')
    plt.xlabel("Count")
    plt.title("Tree Type Counts for Selected Boroughs")
    plt.yticks(y_pos, y)
    plt.tight_layout()
    st.pyplot()

st.sidebar.subheader('Select to show a raw data sample')
if st.sidebar.checkbox(''):
    st.subheader('Raw data head')
    st.write(df.head(50))

# set map colours for different trees
colour_dict = {
"Cherry":'[255,0,0, 160]',
"Maple":'[255,127,0, 160]',
"Other":'[255,212,0, 160]',
"Lime":'[255,255,0, 160]',
"Plane":'[191,255,0, 160]',
"Ash":'[106,255,0, 160]',
"Whitebeam":'[0,234,255, 160]',
"Oak":'[0,149,255, 160]',
"Birch":'[0,64,255, 160]',
"Hawthorn":'[237,185,185, 160]',
"Apple":'[231,233,18, 160]',
"Hornbeam":'[185,237,224, 160]',
"Chestnut":'[185,215,237, 160]',
"Pear":'[220,185,237, 160]',
"Cypress":'[143,35,35, 160]',
"Poplar":'[143,106,35, 160]',
"Alder":'[79,143,35, 160]',
"Willow":'[35,98,143, 160]',
"Beech":'[107,35,143, 160]',
"Pine":'[0,0,0, 160]',
"Black Locust":'[115,115,115, 160]',
"Elm":'[204,204,204, 160]',
"Hazel":'[170,0,255, 160]',
"Chestnut":'[255,0,170, 160]',
}

# generate map with selected data using pydeck_chart
def scatter_plotter_layer(type='Plane'):
        return pdk.Layer(
            "ScatterplotLayer",
            data=df_sel_b[df.display_name == type],
            get_position=['longitude', 'latitude'],
            get_fill_color=colour_dict[type],
            get_radius=15,
            pickable=True,
        )

layers=[scatter_plotter_layer(type=x) for x in types_sel]

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    # map_style="open-street-map",
    initial_view_state=pdk.ViewState(
        latitude=51.5,
        longitude=0,
        zoom=10,
        pitch=10,
    ),
    tooltip = {"text": "Tree Type: {display_name}"},

    layers=layers,
))
