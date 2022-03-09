import dash
import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc
import pathlib
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from datetime import date
from altair_data_server import data_server

# Save a vega-lite spec and a PNG blob for each plot in the notebook
alt.renderers.enable("mimetype")
# Handle large data sets without embedding them in the notebook
# alt.data_transformers.enable("data_server")


root_dir = pathlib.Path(__file__).parent.parent
file_path = root_dir.joinpath("data/energydata_complete.csv")
energydata = pd.read_csv(file_path)

# create a day of week column and month column and day column
energydata["date"] = pd.to_datetime(energydata["date"])
energydata["day_of_week"] = energydata["date"].dt.day_name()
energydata["month"] = energydata["date"].dt.strftime("%b")
energydata["day"] = energydata["date"].dt.date


sort_order = ["Jan", "Feb", "Mar", "Apr", "May"]


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


## Plotting
# bar chart for day of week
def bar_plot_altair(start_date, end_date):
    # select date range
    selected_data = energydata[
        (energydata["day"] <= end_date) & (energydata["day"] >= start_date)
    ]
    # group by day of week and sum the energy consumption
    selected_data = selected_data.groupby(["day_of_week"]).sum().reset_index()

    # make Appliances vs Day of week bar plot
    chart = (
        alt.Chart(selected_data)
        .mark_bar(color="#D35400", size=20)
        .encode(
            x=alt.X(
                "Appliances:Q",
                axis=alt.Axis(title="Appliances energy consumption in Wh"),
            ),
            y=alt.Y(
                "day_of_week:N",
                axis=alt.Axis(title="Day of the week"),
                sort=[
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
            ),
        )
        .properties(width=300, height=300, title="Energy Used in Each Day of Week")
    )
    return chart.to_html()


def plot_outsidetemp(start_date, end_date, xcol="T_out"):
    # select date range
    selected_data = energydata[
        (energydata["day"] <= end_date) & (energydata["day"] >= start_date)
    ]
    chart = (
        alt.Chart(selected_data)
        .mark_area()
        .encode(
            x=alt.X(
                xcol,
                axis=alt.Axis(title="Temperature Outside in Celsius"),
            ),
            y=alt.X(
                "RH_out",
                axis=alt.Axis(title="Humidity outside in %"),
            ),
        )
        .properties(width=350, height=300, title="Outside Temperature vs Humidity")
    )

    return chart.interactive().to_html()


# pie chart for day of week
def pie_chart(start_date, end_date):
    # select date range
    selected_data = energydata[
        (energydata["day"] <= end_date) & (energydata["day"] >= start_date)
    ]
    # group by day of week and sum the energy consumption
    selected_data = selected_data.groupby(["day_of_week"]).sum().reset_index()

    chart = (
        alt.Chart(selected_data)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(field="Appliances", type="quantitative"),
            color=alt.Color(
                field="day_of_week",
                type="nominal",
                legend=alt.Legend(title="Day of the week"),
                sort=[
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
            ),
        )
        .configure_axis(grid=False)
        .configure_view(strokeWidth=0)
        .properties(width=250, height=300)
    )
    return chart.to_html()


def plot_temp_hum(start_date, end_date, room="T1RH_1"):
    # select date range
    selected_data = energydata[
        (energydata["day"] <= end_date) & (energydata["day"] >= start_date)
    ]

    room_temp = room[0:2]
    room_hum = room[2:6]

    temp = (
        alt.Chart(selected_data)
        .mark_line(color="red")
        .encode(
            alt.Y(room_temp + ":Q", title="Temperature"),
            alt.X("date", title="Date"),
        )
    )

    hum = (
        alt.Chart(selected_data)
        .mark_line(color="blue")
        .encode(
            alt.Y(room_hum + ":Q", title="Humidity"),
            alt.X("date", title="Date"),
        )
    )

    plot = (
        alt.layer(temp, hum)
        .resolve_scale(y="independent")
        .properties(width=320, height=300, title="Temperature and Humidity Trend")
    )

    return plot.to_html()


def area_plot(start_date, end_date):

    selected_data = energydata[
        (energydata["day"] <= end_date) & (energydata["day"] >= start_date)
    ]

    energy_data_subset = selected_data[["Appliances", "lights", "month"]]

    energy_data_subset = (
        energy_data_subset.groupby("month", sort=False).sum().reset_index()
    )
    energy_data_subset = pd.melt(
        energy_data_subset, id_vars=["month"], value_vars=["Appliances", "lights"]
    )

    plot = (
        alt.Chart(energy_data_subset)
        .mark_area()
        .encode(
            x=alt.X(
                "month",
                sort=sort_order,
                axis=alt.Axis(
                    title="Month",
                    tickCount=10,
                    grid=False,
                    labelAngle=-360,
                    titleFontSize=12,
                    labelFontSize=10,
                ),
                scale=alt.Scale(zero=False, domain=list(sort_order)),
            ),
            y=alt.Y(
                "value",
                axis=alt.Axis(
                    title="Energy use in Wh",
                    grid=False,
                    titleFontSize=12,
                    labelFontSize=10,
                ),
                scale=alt.Scale(zero=False),
            ),
            color=alt.Color("variable"),
        )
        .properties(height=300, width=350, title="Energy Used in House")
        .configure_axis(labelFontSize=14, titleFontSize=18)
        .configure_mark(opacity=0.5)
    )

    return plot.to_html()


temp_hum = html.Iframe(
    id="temp_hum",
    srcDoc=plot_temp_hum(
        start_date=energydata["day"].min(), end_date=energydata["day"].max()
    ),
    style={"width": "100%", "height": "400px"},
)

# bar chart for day of week
energy_bar = html.Iframe(
    id="barchart",
    srcDoc=bar_plot_altair(
        start_date=energydata["day"].min(), end_date=energydata["day"].max()
    ),
    style={"width": "100%", "height": "400px"},
)

# pie chart for day of week
energy_pie = html.Iframe(
    id="pie_chart",
    srcDoc=pie_chart(
        start_date=energydata["day"].min(), end_date=energydata["day"].max()
    ),
    style={"width": "100%", "height": "400px"},
)

temp_hum_out = html.Iframe(
    id="altair_chart",
    srcDoc=plot_outsidetemp(
        start_date=energydata["day"].min(),
        end_date=energydata["day"].max(),
        xcol="T_out",
    ),
    style={"width": "100%", "height": "400px"},
)

energy_month = html.Iframe(
    id="energy_month",
    srcDoc=area_plot(
        start_date=energydata["day"].min(), end_date=energydata["day"].max()
    ),
    style={"width": "130%", "height": "400px"},
)

header = dcc.Markdown(
    """

        # Energy Use of Appliance in a Low-Energy House        
    """
)

random_text = dcc.Markdown(
    """ 
        **Collaborators:**  
        Harpreet Kaur  
        Chad Wheeler  
        Neslson Tang  
        Nyanda Redwood   
    """
)

date_range = dcc.Markdown(
    """

        **Select date range:** 


        """
)

pick_room = dcc.Markdown(
    """
        &nbsp
        
        **Pick a room:**  
        
        
    """
)


# dropdown to select room
room_dropdown = dcc.Dropdown(
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
)

# date range controller
date_picker = dcc.DatePickerRange(
    id="my-date-picker-range",
    min_date_allowed=date(2016, 1, 11),
    max_date_allowed=date(2016, 5, 27),
    initial_visible_month=date(2016, 1, 11),
    start_date=date(2016, 1, 11),
    end_date=date(2016, 5, 27),
)

row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [random_text, date_range, date_picker, pick_room, room_dropdown]
                    )
                ),
                dbc.Col(html.Div(temp_hum)),
                dbc.Col(html.Div(temp_hum_out)),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(energy_bar)),
                dbc.Col(html.Div(energy_pie)),
                dbc.Col(html.Div(energy_month)),
            ]
        ),
    ]
)

app.layout = dbc.Container(
    [
        header,
        html.Div(
            [
                row,
            ]
        ),
    ]
)


@app.callback(
    Output("temp_hum", "srcDoc"),
    Output("barchart", "srcDoc"),
    Output("pie_chart", "srcDoc"),
    Output("altair_chart", "srcDoc"),
    Output("energy_month", "srcDoc"),
    Input("room", "value"),
    Input("my-date-picker-range", "start_date"),
    Input("my-date-picker-range", "end_date"),
)
def update_output(room, start_date, end_date):
    # convert the outputs to date object
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    return (
        plot_temp_hum(
            start_date=start_date_object, end_date=end_date_object, room=room
        ),
        bar_plot_altair(start_date=start_date_object, end_date=end_date_object),
        pie_chart(start_date=start_date_object, end_date=end_date_object),
        plot_outsidetemp(
            start_date=start_date_object, end_date=end_date_object, xcol="T_out"
        ),
        area_plot(start_date=start_date_object, end_date=end_date_object),
    )


if __name__ == "__main__":
    app.run_server(debug=True)
