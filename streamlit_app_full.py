# streamlit run streamlit_app2.py

# To deploy:
# https://share.streamlit.io/

# https://cheat-sheet.streamlit.app/
# https://docs.streamlit.io/library/api-reference/layout
# https://folium.streamlit.app/dynamic_updates

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from folium.plugins import HeatMap

st.set_page_config(layout="wide")

@st.cache_data
def load_data(fuente_info):
    tx = pd.read_csv("./cr_geocode_full_viv_to_st.csv")
    tx = tx.drop(columns="cedula")
    tx = tx.dropna()

    df_fuente  = pd.Series(data=fuente_info)

    tx = tx[tx["Fuente"].isin(values=df_fuente)]
    tx.reset_index(drop=True, inplace=True)
    return tx

@st.cache_resource
def create_map(map_type, zoom, fuente_info):
    tx = load_data(fuente_info = fuente_info)
    heatmap_data = []
    for i in range(tx.shape[0]):
        lat, lon = tx.loc[i,["y","x"]]
        heatmap_data.append([lat, lon])

    gradient = {
        0.6: 'blue',
        0.7: 'green',
        0.8: 'yellow',
        0.9: 'orange',
        1: 'red'
    }
    init_location = [9.936543, -84.098601]
    #init_location = [9.860764,-83.931041]
    if map_type == "OpenStreetMap":
        m = folium.Map(location=init_location, 
            zoom_start=zoom)
    elif map_type == "Stamen Terrain":
        m = folium.Map(location=init_location, 
                    zoom_start=zoom, 
                    tiles="https://tiles.stadiamaps.com/tiles/stamen_terrain/{z}/{x}/{y}{r}.png?api_key=cea0e921-fd8d-41c9-b807-37db53fdc9ba", 
                    attr="Esri")
    elif map_type == "Stamen Toner":
        m = folium.Map(location=init_location, 
                    zoom_start=zoom, 
                    tiles="https://tiles.stadiamaps.com/tiles/stamen_toner/{z}/{x}/{y}{r}.png?api_key=cea0e921-fd8d-41c9-b807-37db53fdc9ba", 
                    attr="Esri")
    elif map_type == "Stamen Watercolor":
        m = folium.Map(location=init_location, 
                       zoom_start=zoom, 
                       tiles="https://tiles.stadiamaps.com/tiles/stamen_watercolor/{z}/{x}/{y}.jpg?api_key=cea0e921-fd8d-41c9-b807-37db53fdc9ba", 
                       attr="Esri")
    elif map_type == "Alidade Smooth":
        m = folium.Map(location=init_location, 
                       zoom_start=zoom, 
                       tiles="https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png?api_key=cea0e921-fd8d-41c9-b807-37db53fdc9ba", 
                       attr="Esri")
    elif map_type == "Alidade Smooth Dark":
        m = folium.Map(location=init_location, 
                       zoom_start=zoom, 
                       tiles="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png?api_key=cea0e921-fd8d-41c9-b807-37db53fdc9ba", 
                       attr="Esri")   
    elif map_type == "Osm Bright":
        m = folium.Map(location=init_location, 
                       zoom_start=zoom, 
                       tiles="https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png?api_key=cea0e921-fd8d-41c9-b807-37db53fdc9ba", 
                       attr="Esri")   
    elif map_type == "Outdoors":
        m = folium.Map(location=init_location, 
                       zoom_start=zoom, 
                       tiles="https://tiles.stadiamaps.com/tiles/outdoors/{z}/{x}/{y}{r}.png?api_key=cea0e921-fd8d-41c9-b807-37db53fdc9ba", 
                       attr="Esri")           

        
    HeatMap(data=heatmap_data, gradient=gradient, radius=13,opacity =1).add_to(parent=m)

    return m


st.sidebar.header('Mapa 1')
map_type = st.sidebar.selectbox(
    label="Estilo Mapa", 
    options=["Stamen Toner","OpenStreetMap", "Stamen Terrain", "Stamen Watercolor",
            "Alidade Smooth","Alidade Smooth Dark","Osm Bright",
            "Outdoors"],
            key = "map_type1"
    )
foco = st.sidebar.selectbox(label="Foco", 
                            options=["San José","Nacional"],
                            key = "foco1")
fuente_info = st.sidebar.multiselect(label="Fuente Información", 
                                    options=["Vivienda","Laboral"], 
                                    default = ["Vivienda"],
                                    key = "fuente_info1")


#st.text(body=carrera)
if foco == "San José":
    zoom = 12
if foco == "Nacional":
    zoom = 8

st.sidebar.markdown('---') 
st.sidebar.header('Mapa 2')
map_type2 = st.sidebar.selectbox(
    label="Estilo Mapa", 
    options=["Stamen Toner","OpenStreetMap", "Stamen Terrain", "Stamen Watercolor",
            "Alidade Smooth","Alidade Smooth Dark","Osm Bright",
            "Outdoors"],
    key = "map_type2"
    )
foco2 = st.sidebar.selectbox(label="Foco", 
                            options=["San José","Nacional"],
                            key = "foco2")
fuente_info2 = st.sidebar.multiselect(label="Fuente Información", 
                                    options=["Vivienda","Laboral"], 
                                    default = ["Vivienda"],
                                    key = "fuente_info2")
marca2 = st.sidebar.multiselect(label="Marca", 
                                options=["UAM","Latina"], 
                                default =["UAM"],
                                key = "marca2" )

#st.text(body=carrera)
if foco2 == "San José":
    zoom2 = 12
if foco2 == "Nacional":
    zoom2 = 8

m1 = create_map(map_type=map_type, 
            zoom = zoom,
            fuente_info = fuente_info)

m2 = create_map(map_type=map_type, 
            zoom = zoom2,
            fuente_info = fuente_info2)


col1, col2 = st.columns(spec=2)

with col1:
    st.header("Mapa 1")
    st_folium(fig=m1, width=700, height=500, key= "map1")
with col2:
    st.header("Mapa 2")
    st_folium(fig=m2, width=700, height=500, key= "map2")

