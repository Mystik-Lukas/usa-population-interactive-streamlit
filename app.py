import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.header("USA Population")

df = pd.read_csv('data.csv')

# Change state/region to state
df = df.rename(columns={ 'state/region': "state" })

# Only NA values are PR and we wont be using PR so just remove PR
df = df[df.state != "PR"]

# Change population from float to int
df.population = df.population.astype(int)

# Graph
# 1990 top 10 populations
st.subheader("(1) Top states population based on year")

st.sidebar.subheader("Global Options")

type = st.sidebar.selectbox(
    'Type of graph',
    ['Bar', 'Line', 'Area'],
    )

minor_only = 'under18' if st.sidebar.checkbox(
    'Minor Only',
    False,
    help="If checked, it will only show data for people under 18. Unchecked will show the total population"
    ) is True else 'total'

st.sidebar.write("---")

st.sidebar.subheader("Options for Graph 1")

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

df2 = df.query('ages == @minor_only and state != "USA" and year == @year') \
    .sort_values("population", ascending=False)[:int(range)]

eval(f'st.{type.lower()}_chart(df2, x = "state", y = "population", use_container_width=True)')

st.sidebar.write("---")
"---"
st.sidebar.subheader("Options for Graph 2")

selected_state = st.sidebar.selectbox('State',
                                        states,
                                        index=0,
                                        help = "The state the data will be from"
                                    )

st.subheader(f"(2) {selected_state} population ({df.year.min()} to {df.year.max()})")

df3 = df.query("state == @selected_state and ages == @minor_only")

eval(f'st.{type.lower()}_chart(df3, x = "year", y = "population", use_container_width=True)')