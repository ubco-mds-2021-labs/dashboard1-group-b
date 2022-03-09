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

data = pd.read_csv("../data/energydata_complete.csv")

data["date"] = pd.to_datetime(data["date"])

energy_data['month'] = energy_data['date'].dt.month
energy_data_subset=energy_data[['Appliances','lights','date']]
energy_data_subset['month_full'] = energy_data_subset['date'].dt.month_name()
energy_data_subset=energy_data_subset.groupby('month_full', sort=False).sum().reset_index()
energy_data_subset=pd.melt(energy_data_subset,id_vars =['month_full'], value_vars=['Appliances', 'lights'])
energy_data_subset.head()
sort_order = ['January', 'February','March','April','May']

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

def area_plot(start_date,end_date):
    
    selected_data = energydata[(energydata['day'] <= end_date) & (energydata['day'] >= start_date)]
    
    plot = alt.Chart(energy_data_subset).mark_area().encode(
        x = alt.X('month_full', sort = sort_order, axis = alt.Axis(title = 'Month', tickCount = 10, grid = False, labelAngle = -360),
        scale = alt.Scale(zero = False, domain = list(sort_order))),
        y = alt.Y('value', axis = alt.Axis(title = 'Energy use in Wh', grid = False),scale = alt.Scale(zero = False) ),
        color = alt.Color('variable')
        ).properties(height = 300, width = 500, title = "Energy Used in house"
        ).configure_axis(labelFontSize = 14, titleFontSize = 18) 

    return plot.to_html()

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
