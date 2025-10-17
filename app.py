"""
Top Movies Analysis — Dash Web Application
==========================================

This module defines a Dash web application that enables users to explore
a dataset containing the “Top 100 Movies” with metadata such as Metacritic
score, Oscar wins, and release year.

The app provides interactive filters and dynamic visualizations to help
users understand how movie quality (Metacritic score) and recognition
(Oscar wins) vary over time.

---------------------------------------------------------------------
Project Structure
---------------------------------------------------------------------
- `app.py` :
    The main entry point for the Dash application (this file).

- `top_100_movies_full_best_effort.csv` :
    CSV dataset file (must be in the same directory). The file must contain
    at least the following columns:
        - `Title` : movie title (string)
        - `Year` : release year (integer or string, convertible to datetime)
        - `Metacritic Score` : numeric Metacritic rating (may include NaN)
        - `Oscars Won` : integer number of Oscars received

---------------------------------------------------------------------
How to Run
---------------------------------------------------------------------
1. Install Python 3.8+ and dependencies:
       pip install dash pandas
2. Ensure the CSV file is in the current working directory.
3. Run the app:
       python app.py
4. Open the URL displayed in the console (e.g., http://127.0.0.1:8050).

---------------------------------------------------------------------
Notes & Assumptions
---------------------------------------------------------------------
- The `Year` column is parsed into a datetime object (year-only).
- Minimal validation is performed: if required columns are missing,
  pandas will raise an error on startup.
- The app uses simple static dropdowns for filtering; the dataset is small
  (100 rows), so no performance optimization is required.
"""

import pandas as pd
from dash import Dash, dcc, html, Input, Output

# Load and prepare dataset
data = (
    pd.read_csv("top_100_movies_full_best_effort.csv")
    # Convert release year to datetime (year-only precision)
    .assign(Date=lambda df: pd.to_datetime(df["Year"], format="%Y"))
    .sort_values(by="Year")
)

# Extract unique values for dropdown menus
metacritic_score = data["Metacritic Score"].dropna().sort_values().unique()
oscar_wins = data["Oscars Won"].sort_values().unique()

# App configuration and styling
external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Top Movies Analysis"


# Layout definition
app.layout = html.Div(
    children=[
        # Header section
        html.Div(
            children=[
                html.P(children="🎬", className="header-emoji"),
                html.H1(children="Top Movies Analysis", className="header-title"),
                html.P(
                    children=(
                        "An interactive analysis of top movies with "
                        "high Metacritic scores and Oscar wins."
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),

        # Filter controls (menu)
        html.Div(
            children=[
                # Filter: Metacritic score
                html.Div(
                    children=[
                        html.Div(children="Metacritic Score", className="menu-title"),
                        dcc.Dropdown(
                            id="metacritic-score-filter",
                            options=[
                                {"label": score, "value": score}
                                for score in metacritic_score
                            ],
                            value=min(metacritic_score),
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                # Filter: Oscars won
                html.Div(
                    children=[
                        html.Div(children="Oscars Won", className="menu-title"),
                        dcc.Dropdown(
                            id="oscar-wins-filter",
                            options=[
                                {"label": win, "value": win} for win in oscar_wins
                            ],
                            value=min(oscar_wins),
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                # Filter: Year range
                html.Div(
                    children=[
                        html.Div(children="Year Released", className="menu-title"),
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

        # Visualization cards
        html.Div(
            children=[
                # Scatter plot: Metacritic score over time
                html.Div(
                    children=dcc.Graph(
                        id="movies-scatter-plot",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
                # Histogram: Movie count by Oscars won
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

# Callback: Update both graphs based on user filters
@app.callback(
    Output("movies-scatter-plot", "figure"),
    Output("movies-histogram", "figure"),
    Input("metacritic-score-filter", "value"),
    Input("oscar-wins-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_graphs(metacritic_score, oscar_wins, start_date, end_date):
    """
    Update both the scatter plot and histogram figures based on user-selected filters.

    Parameters
    ----------
    metacritic_score : int
        Minimum Metacritic score selected by the user.
    oscar_wins : int
        Minimum number of Oscars won selected by the user.
    start_date : str
        Start of the release year range (YYYY-MM-DD format).
    end_date : str
        End of the release year range (YYYY-MM-DD format).

    Returns
    -------
    tuple[dict, dict]
        A tuple containing the updated scatter plot and histogram figure configurations.
    """
    # Filter data by date range
    date_filtered = data.query("(`Date` >= @start_date) & (`Date` <= @end_date)")

    # Filter separately for each visualization
    filtered_metacritic = date_filtered.query(
        "(`Metacritic Score` >= @metacritic_score)"
    )
    filtered_oscars = date_filtered.query("(`Oscars Won` >= @oscar_wins)")

    # Scatter plot: Metacritic score over time
    scatter_figure = {
        "data": [
            {
                "x": filtered_metacritic["Date"],
                "y": filtered_metacritic["Metacritic Score"],
                "type": "scatter",
                "mode": "markers",
                "hovertemplate": (
                    "Title: %{text}<br>"
                    "Year: %{x|%Y}<br>"
                    "Score: %{y}<extra></extra>"
                ),
                "text": filtered_metacritic["Title"],
            },
        ],
        "layout": {
            "title": {"text": "Metacritic Score Over Time", "x": 0.05, "xanchor": "left"},
            "xaxis": {"title": "Year", "fixedrange": True},
            "yaxis": {"title": "Metacritic Score", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    # Histogram: Number of movies by Oscars won
    histogram_figure = {
        "data": [
            {
                "x": filtered_oscars["Oscars Won"].value_counts().sort_index().index,
                "y": filtered_oscars["Oscars Won"].value_counts().sort_index().values,
                "type": "bar",
                "hovertemplate": (
                    "Oscars Won: %{x}<br>"
                    "Movies: %{y}<extra></extra>"
                ),
            },
        ],
        "layout": {
            "title": {
                "text": "Number of Movies by Oscars Won",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"title": "Oscars Won"},
            "yaxis": {"title": "Number of Movies"},
            "colorway": ["#E12D39"],
        },
    }

    return scatter_figure, histogram_figure


# Application entry point
if __name__ == "__main__":
    app.run(debug=True)

