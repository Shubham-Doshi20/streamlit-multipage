import altair as alt
import pandas as pd
import streamlit as st
from urllib.error import URLError

st.set_page_config(
    page_title="DataFrame Demo",
    page_icon="📊",
)

st.title("DataFrame Demo")
st.sidebar.header("DataFrame Demo")

st.write(
    "Compare gross agricultural production across countries. "
    "Choose countries below to update the table and chart."
)


@st.cache_data
def get_UN_data():
    url = (
        "https://streamlit-demo-data.s3-us-west-2."
        "amazonaws.com/agri.csv.gz"
    )
    return pd.read_csv(url).set_index("Region")


try:
    df = get_UN_data()

    countries = st.multiselect(
        "Choose countries",
        options=df.index.tolist(),
        default=["China", "United States of America"],
    )

    if not countries:
        st.info("Please select at least one country.")

    else:
        selected = df.loc[countries].copy()
        selected = selected.apply(pd.to_numeric, errors="coerce")
        selected = selected / 1_000_000

        st.subheader("Gross agricultural production ($ billions)")
        st.dataframe(selected.sort_index())

        chart_data = (
            selected.rename_axis("Country")
            .reset_index()
            .melt(
                id_vars="Country",
                var_name="Year",
                value_name="Production",
            )
        )

        chart_data["Year"] = pd.to_numeric(
            chart_data["Year"], errors="coerce"
        )

        chart_data = chart_data.dropna(
            subset=["Year", "Production"]
        )

        chart_data["Year"] = chart_data["Year"].astype(int)

        chart = (
            alt.Chart(chart_data)
            .mark_area(opacity=0.3)
            .encode(
                x=alt.X(
                    "Year:Q",
                    title="Year",
                    axis=alt.Axis(format="d"),
                    scale=alt.Scale(zero=False),
                ),
                y=alt.Y(
                    "Production:Q",
                    title="Gross agricultural production ($ billions)",
                    stack=None,
                ),
                color=alt.Color(
                    "Country:N",
                    title="Country",
                ),
                tooltip=[
                    "Country:N",
                    alt.Tooltip("Year:Q", format="d"),
                    alt.Tooltip(
                        "Production:Q",
                        title="Production ($ billions)",
                        format=",.2f",
                    ),
                ],
            )
            .properties(height=400)
        )

        st.altair_chart(chart, use_container_width=True)

    st.caption(
        "Source: UN Data Explorer data supplied through "
        "the Streamlit multipage tutorial."
    )

except URLError as error:
    st.error(f"Could not download the data: {error.reason}")
