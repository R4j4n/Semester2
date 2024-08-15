import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
df = px.data.gapminder()

print(df.head())

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("Interactive Dashboard with Multiple Components"),

    # Dropdown for X-axis selection in the scatter plot
    html.Label("Select X-axis for Scatter Plot:"),
    dcc.Dropdown(
        id="x-axis-dropdown",
        options=[ # list of values or dict with {"label": "", "value": }
            {"label": "GDP per Capita", "value": "gdpPercap"},
            {"label": "Life Expectancy", "value": "lifeExp"},
            {"label": "Population", "value": "pop"}
        ],
        value="gdpPercap" # the deefaut value 
    ),

    # Slider for year selection
    html.Label("Select Year Range:"),
    dcc.RangeSlider(
        id="year-slider",
        min=df["year"].min(),
        max=df["year"].max(),
        step=5,
        marks={str(year): str(year) for year in df["year"].unique()},
        value=[df["year"].min(), df["year"].max()]
    ),

    # Radio items for continent selection
    html.Label("Select Continent:"),
    dcc.RadioItems(
        id="continent-radio",
        options=[{"label": continent, "value": continent} for continent in df["continent"].unique()],
        value="Asia"
    ),

    # Graphs
    dcc.Graph(id="scatter-plot"),
    dcc.Graph(id="line-plot"),
    dcc.Graph(id="bar-plot")
])

# Define callbacks to update the graphs based on user input
@app.callback(
    [Output("scatter-plot", "figure"),
     Output("line-plot", "figure"),
     Output("bar-plot", "figure")],
    [Input("x-axis-dropdown", "value"), # this will be selected_x
     Input("year-slider", "value"), # this will be select selected_years
     Input("continent-radio", "value")] # this will be selected_continent
)
def update_graphs(selected_x, selected_years, selected_continent):
    # Filter the data based on year range and continent
    filtered_df = df[(df["year"] >= selected_years[0]) & (df["year"] <= selected_years[1])]
    filtered_df = filtered_df[filtered_df["continent"] == selected_continent]
    
    # Scatter plot: X vs Life Expectancy
    scatter_fig = px.scatter(
        filtered_df,
        x=selected_x,
        y="lifeExp",
        size="pop",
        color="country",
        title=f"Scatter Plot of {selected_x} vs Life Expectancy",
        labels={selected_x: selected_x.capitalize(), "lifeExp": "Life Expectancy"}
    )
    
    # Line plot: Life Expectancy over Time
    line_fig = px.line(
        filtered_df,
        x="year",
        y="lifeExp",
        color="country",
        title=f"Life Expectancy Over Time in {selected_continent}",
        labels={"year": "Year", "lifeExp": "Life Expectancy"}
    )
    
    # Bar plot: GDP per Capita for each Country
    bar_fig = px.bar(
        filtered_df,
        x="country",
        y="gdpPercap",
        title=f"GDP per Capita in {selected_continent}",
        labels={"country": "Country", "gdpPercap": "GDP per Capita"}
    )
    
    return scatter_fig, line_fig, bar_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
