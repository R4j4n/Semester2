import dash
import pandas as pd
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

# Load the updated dataset
df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
        "Season": [
            "Summer",
            "Winter",
            "Summer",
            "Winter",
            "Summer",
            "Winter",
        ],  # New column
    }
)

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div(
    [
        html.H1("Interactive Fruit Dashboard"),
        # Dropdown for X-axis selection
        html.Label("Select X-axis:"),
        dcc.Dropdown(
            id="city_drop_down",
            options=[{"label": city, "value": city} for city in df["City"].unique()],
            value="SF",
        ),
        # Radio items for City or Season selection
        html.Label("Filter by City or Season:"),
        dcc.RadioItems(
            id="radio_season",
            options=[
                {"label": "Summer", "value": "Summer"},
                {"label": "Winter", "value": "Winter"},
            ],
            value="Winter",
        ),
        # Graph
        dcc.Graph(id="bar-plot"),
    ]
)


# Define callback to update the graph based on user input
@app.callback(
    Output("bar-plot", "figure"),
    [Input("city_drop_down", "value"), Input("radio_season", "value")],
)
def update_graph(selected_x, selected_filter):
    # Filter the data based on the selected radio option
    filtered_df = df.loc[(df.City == selected_x) & (df.Season == selected_filter)]
    print(filtered_df.head())
    # Create a bar plot
    bar_fig = px.bar(
        filtered_df,
        x="Fruit",
        y="Amount",
        title=f"{selected_x}'s Amount by {selected_filter}",
    )

    return bar_fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
