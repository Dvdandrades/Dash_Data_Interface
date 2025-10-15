import pandas as pd
from dash import Dash, dcc, html

data = (
    pd.read_csv("top_100_movies_full_best_effort.csv")
    .query("`Metacritic Score` > 75 and `Oscars Won` > 0")
    .assign(Date=lambda data: pd.to_datetime(data["Year"], format="%Y"))
    .sort_values(by="Year")
)

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Top Movies Analysis"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🎬", className="header-emoji"),
                html.H1(
                    children="Top Movies Analysis", className="header-title"
                ),
                html.P(
                    children=(
                        "An analysis of top movies with high Metacritic scores and Oscar wins."
                ),
                className="header-description",
            ),
        ],
        className="header",
    ),
    html.Div(
        children=[
            html.Div(
                children=dcc.Graph(
                    id="metacritic-score",
                    config={"displayModeBar": False},
                    figure={
                        "data": [
                            {
                                "x": data["Date"],
                                "y": data["Metacritic Score"],
                                "type": "lines",
                                "hovertemplate": (
                                    "%{y}<extra></extra>"
                                ),
                            },
                        ],
                        "layout": {
                            "title": {
                                "text": "Metacritic Scores Over Time",
                                "x": 0.05,
                                "xanchor": "left",
                            },
                            "xaxis": {"fixedrange": True},
                            "yaxis": {
                                "fixedrange": True,
                            },
                            "colorway": ["#17b897"],
                        },
                    },
                ),
                className="card",
            ),
            html.Div(
                children=dcc.Graph(
                    id="oscar-wins",
                    config={"displayModeBar": False},
                    figure={
                        "data": [
                            {
                                "x": data["Date"],
                                "y": data["Oscars Won"],
                                "type": "lines",
                            },
                        ],
                        "layout": {
                            "title": {
                                "text": "Oscar Wins Over Time",
                                "x": 0.05,
                                "xanchor": "left",
                            },
                            "xaxis": {"fixedrange": True},
                            "yaxis": {"fixedrange": True},
                            "colorway": ["#E12D39"],
                            },
                        },

                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ],
)
       

if __name__ == "__main__":
    app.run(debug=True)