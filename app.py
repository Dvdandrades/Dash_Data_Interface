import pandas as pd
from dash import Dash, dcc, html

data = (
    pd.read_csv("top_100_movies_full_best_effort.csv")
    .query("Metacritic Score > 75 and Oscars Won > 0")
    .assign(Date=lambda data: pd.to_datetime(data["Year"], format="%Y"))
    .sort_values(by="Year")
)

app = Dash(__name__)