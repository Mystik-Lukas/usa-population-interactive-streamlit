import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Basic Graphs", layout="wide")

hide_st_style = """
            <style>
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("USA Population")

df = pd.read_csv('data.csv')

# Change state/region to state
df = df.rename(columns={ 'state/region': "state" })

# Only NA values are PR and we wont be using PR so just remove PR
df = df[df.state != "PR"]

# Change population from float to int
df.population = df.population.astype(int)

# Graph
# 1990 top 10 populations

### GRAPH 1 ###
st.sidebar.subheader("Options")

states = sorted(df.state \
                    .unique() \
                    .tolist())

states.remove("USA")

year = st.sidebar.slider('Year (1990-2013)', 
                            int(df.year.min()), 
                            int(df.year.max()), 
                            int(df.year.max()),
                            help="The year that your data will be from"
                        )

range = st.sidebar.slider('Data Range (amount of top states to show)', 
                            5, 
                            50,
                            10,
                            help="The amount of states to show in the data"
                        )

selected_state = st.sidebar.selectbox('State',
                                        states,
                                        index=0,
                                        help = "The state the data will be from"
                                    )

minor_only = 'under18' if st.sidebar.checkbox(
    'Minor Only',
    False,
    help="If checked, it will only show data for people under 18. Unchecked will show the total population",
    key="1minor_only"
    ) is True else 'total'

df2 = df.query('ages == @minor_only and state != "USA" and year == @year') \
    .sort_values("population", ascending=False)[:int(range)]

plot3 = px.bar(df2,
                title = f"(1) Top States {'Total' if minor_only == 'total' else 'Minor (under 18)'} Population Based on Year",
                template = "plotly_dark",
                x = "state",
                y = "population"
                )

st.plotly_chart(plot3, use_container_width=True)

### GRAPH 2 ###

"---"

df3 = df.query("state == @selected_state and ages == @minor_only")

plot3 = px.bar(df3,
                title = f"(2) {selected_state} {'Total' if minor_only == 'total' else 'Minor (under 18)'} Population ({df.year.min()} to {df.year.max()})",
                template = "plotly_dark",
                x = "year",
                y = "population"
                )

st.plotly_chart(plot3, use_container_width=True)

### GRAPH 3 ###

"---"

df4 = df.query('state == @selected_state')

df4 = df4.pivot(index="year",
                columns = 'ages',
                values = "population"
                )

df4['adult'] = df4.total - df4.under18

df4 = df4.rename(columns={ "under18": "minors", "adult": "adults" })

df4 = df4.drop('total', axis = 1)

plot3 = px.area(df4,
                title = f"(3) {selected_state} Adult and Minor Population ({df.year.min()} to {df.year.max()})",
                template = "plotly_dark",
                )

st.plotly_chart(plot3, use_container_width=True)