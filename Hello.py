import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.title("Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

st.markdown("""
Streamlit is an open-source framework for building interactive
data apps with Python.

**👈 Select a demo from the sidebar** to explore:

- **Plotting Demo:** an animated chart.
- **Mapping Demo:** interactive transport maps.
- **DataFrame Demo:** agricultural production data.

### Learn more
- [Streamlit website](https://streamlit.io)
- [Documentation](https://docs.streamlit.io)
- [Community forum](https://discuss.streamlit.io)
""")