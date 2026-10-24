import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError

st.set_page_config(page_title="Mapping Demo", page_icon="🌍")

st.title("Mapping Demo")
st.sidebar.header("Mapping Demo")

st.write(
    "Explore transport data around San Francisco. "
    "Use the sidebar checkboxes to show or hide map layers."
)


@st.cache_data
def from_data_file(filename):
    url = (
        "https://raw.githubusercontent.com/streamlit/"
        f"example-data/master/hello/v1/{filename}"
    )
    return pd.read_json(url)


try:
    all_layers = {
        "Bike Rentals": pdk.Layer(
            "HexagonLayer",
            data=from_data_file("bike_rental_stats.json"),
            get_position=["lon", "lat"],
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            extruded=True,
            pickable=True,
        ),
        "BART Stop Exits": pdk.Layer(
            "ScatterplotLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_fill_color=[200, 30, 0, 160],
            get_radius="exits",
            radius_scale=0.05,
            pickable=True,
        ),
        "BART Stop Names": pdk.Layer(
            "TextLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_text="name",
            get_color=[0, 0, 0, 200],
            get_size=15,
            get_alignment_baseline="'bottom'",
        ),
        "Outbound Flow": pdk.Layer(
            "ArcLayer",
            data=from_data_file("bart_path_stats.json"),
            get_source_position=["lon", "lat"],
            get_target_position=["lon2", "lat2"],
            get_source_color=[200, 30, 0, 160],
            get_target_color=[200, 30, 0, 160],
            auto_highlight=True,
            width_scale=0.0001,
            get_width="outbound",
            width_min_pixels=3,
            width_max_pixels=30,
        ),
    }

    st.sidebar.subheader("Map Layers")

    selected_layers = [
        layer
        for name, layer in all_layers.items()
        if st.sidebar.checkbox(name, value=True)
    ]

    if selected_layers:
        st.pydeck_chart(
            pdk.Deck(
                map_provider="carto",
                map_style="light",
                initial_view_state=pdk.ViewState(
                    latitude=37.76,
                    longitude=-122.4,
                    zoom=11,
                    pitch=50,
                ),
                layers=selected_layers,
            )
        )
    else:
        st.info("Please choose at least one map layer.")

    st.caption("Source: Streamlit tutorial example datasets.")

except URLError as error:
    st.error(f"Could not download the data: {error.reason}")
