import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config("Static Map",
                    layout="wide")

hide_st_style = """
            <style>
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@500&display=swap" rel="stylesheet">
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

df = pd.read_csv('data.csv')

# Change state/region to state
df = df.rename(columns={ 'state/region': "state" })

# Only NA values are PR and we wont be using PR so just remove PR
df = df[df.state != "PR"]

# Change population from float to int
df.population = df.population.astype(int)

st.title("USA Population")

col1, col2 = st.columns(2)

with col1:
    year = st.selectbox('Year (1990-2013)', 
                                list(range(int(df.year.min()), int(df.year.max())+1)),
                                help="The year that your data will be from",
                                index=(len(df.year.unique()) - 1)
                            )

df = df[df.state != "USA"]

df = df \
    .query("year == @year") \
    .pivot_table(
                index="state",
                columns = 'ages',
                values = "population"
                )


df['adult'] = df.total - df.under18
df = df.rename(columns={"under18": "minors", "adult": "adults"})


with col2:
    ages = st.selectbox("Ages", 
                        [col.title() for col in df.columns],
                        help="Age range your data will be from",
                        ).lower()

domain = [col for col in df.columns]
range = ["sunsetdark", "burg", "teal"] #peach
range_hover_label = [
    {
        'bgcolor': "#9c225e",
        'fontcolor': "white"
    },
    {
        'bgcolor': "#ffd6e9",
        'fontcolor': "black"
    },
    {
        'bgcolor': "#98E4FF",
        'fontcolor': "black"
    }
]

map2 = go.Figure(data=go.Choropleth(
    locations = df.index,
    z = df[ages].astype(float),
    locationmode = "USA-states",
    colorscale = range[domain.index(ages)],
    colorbar_title="Population",
    text = df.apply(lambda row: f"{row.name}:<br>{row['adults']:,} Adults<br>{row['minors']:,} Minors<br>Total: {row['total']:,}", axis=1).tolist(),
    hoverinfo = "text"
))

map2.update_layout(geo = {'bgcolor': "rgba(0,0,0,0)"},
                    height = 700,
                    title = f"<span style='font-size: 24px;'>USA Population in {year} by {ages.title()} Population</span>",
                    geo_scope = 'usa',
                    dragmode = False,
                    hoverlabel={'bgcolor': range_hover_label[domain.index(ages)]['bgcolor'], 'font': {'color': range_hover_label[domain.index(ages)]['fontcolor'], 'family': 'Roboto'}}
                    )

st.plotly_chart(map2,
                config = {'displayModeBar': False},
                use_container_width=True
                )

