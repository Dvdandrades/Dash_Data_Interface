import pandas as pd
from dash import Dash, dcc, html, Input, Output

data = (
    pd.read_csv("top_100_movies_full_best_effort.csv")
    .assign(Date=lambda data: pd.to_datetime(data["Year"], format="%Y"))
    .sort_values(by="Year")
)
metacritic_score = data["Metacritic Score"].dropna().sort_values().unique()
oscar_wins = data["Oscars Won"].sort_values().unique()


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
                    children=[
                        html.Div(children="Metacritic Score", className="menu-title"),
                        dcc.Dropdown(
                            id="metacritic-score-filter",
                            options=[
                                {
                                    "label": score, 
                                    "value": score,
                                }
                                for score in metacritic_score
                            ],
                            value=min(metacritic_score),
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Oscars Won", className="menu-title"),
                        dcc.Dropdown(
                            id="oscar-wins-filter",
                            options=[
                                {
                                    "label": oscar_win, 
                                    "value": oscar_win,
                                }
                                for oscar_win in oscar_wins
                            ],
                            value=min(oscar_wins),
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Year Released", className="menu-title"
                        ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=data["Date"].min().date(), 
                            max_date_allowed=data["Date"].max().date(),
                            start_date=data["Date"].min().date(),
                            end_date=data["Date"].max().date(),
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="movies-scatter-plot", 
                        config={"displayModeBar": False}
                    ),
                    className="card",
                ),
                html.Div(
                    children=dcc.Graph(
                        id="movies-histogram",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)
       

if __name__ == "__main__":
    app.run(debug=True)