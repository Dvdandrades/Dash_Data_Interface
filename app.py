import pandas as pd
from dash import Dash, dcc, html

data = (
    pd.read_csv("top_100_movies_full_best_effort.csv")
    .query("`Metacritic Score` > 75 and `Oscars Won` > 0")
    .assign(Date=lambda data: pd.to_datetime(data["Year"], format="%Y"))
    .sort_values(by="Year")
)

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Top Movies Analysis"),
        html.P(
            children=(
                "An analysis of top movies with high Metacritic scores and Oscar wins."
            )
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["Metacritic Score"],
                        "type": "lines",
                    },
                ],
                "layout": {
                    "title": {"text": "Metacritic Scores Over Time"},
                },
            }
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["Oscars Won"],
                        "type": "lines",
                    },
                ],
                "layout": {
                    "title": {"text": "Oscar Wins Over Time"},
                },
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)