import dash
import dash_bootstrap_components as dbc
import altair as alt
import pandas as pd
from vega_datasets import data
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Save a vega-lite spec and a PNG blob for each plot in the notebook
alt.renderers.enable("mimetype")
# Handle large data sets without embedding them in the notebook
alt.data_transformers.enable("data_server")

data = pd.read_csv("data/energydata_complete.csv")

data["date"] = pd.to_datetime(data["date"])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

## Plotting


def plot_temp_hum(room="T1RH_1"):

    room_temp = room[0:2]
    room_hum = room[2:6]

    temp = (
        alt.Chart(data)
        .mark_line(color="red")
        .encode(
            alt.Y(f"{room_temp}:Q", title="Temperature"),
            alt.X("date", title="Date"),
        )
    )

    hum = (
        alt.Chart(data)
        .mark_line(color="blue")
        .encode(
            alt.Y(f"{room_hum}:Q", title="Humidity"),
            alt.X("date", title="Date"),
        )
    )

    plot = alt.layer(temp, hum).resolve_scale(y="independent")

    return plot.to_html()


plot1 = html.Iframe(
    id="temp_hum",
    srcDoc=plot_temp_hum(),
    style={"width": "100%", "height": "1000px"},
)


app.layout = dbc.Container(
    [
        dcc.Dropdown(
            id="room",
            value="T1RH_1",
            options=[
                {"label": "Room 1", "value": "T1RH_1"},
                {"label": "Room 2", "value": "T2RH_2"},
                {"label": "Room 3", "value": "T3RH_3"},
                {"label": "Room 4", "value": "T4RH_4"},
                {"label": "Room 5", "value": "T5RH_5"},
                {"label": "Room 6", "value": "T6RH_6"},
                {"label": "Room 7", "value": "T7RH_7"},
                {"label": "Room 8", "value": "T8RH_8"},
                {"label": "Room 9", "value": "T9RH_9"},
            ],
            clearable=False,
        ),
        plot1,
    ]
)


@app.callback(Output("temp_hum", "srcDoc"), Input("room", "value"))
def update_output(room):
    return plot_temp_hum(room)


if __name__ == "__main__":
    app.run_server(debug=True)
