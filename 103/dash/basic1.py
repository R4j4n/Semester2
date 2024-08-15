from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = Dash(__name__)

df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
    }
)


app.layout = html.Div(
    [
        html.H1("Fruits in cities."),
        # add the dropdown
        html.Label("Select city:"),
        dcc.Dropdown(
            id="city_select",
            options=[{"label": city, "value": city} for city in df["City"].unique()],
            value="SF",
        ),
        dcc.Graph(id="sales_graph"),
    ]
)


@app.callback(Output("sales_graph", "figure"), [Input("city_select", "value")])
def update_graph(city_select):

    # filter the df
    df_filtered = df[df["City"] == city_select]
    fig = px.bar(
        df_filtered, x="Fruit", y="Amount", title=f"Fruit Sales in {city_select}"
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
