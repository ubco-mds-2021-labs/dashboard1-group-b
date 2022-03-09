import dash
import dash_bootstrap_components as dbc
import altair as alt
import pandas as pd
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
from datetime import date

# Save a vega-lite spec and a PNG blob for each plot in the notebook
alt.renderers.enable("mimetype")
# Handle large data sets without embedding them in the notebook
alt.data_transformers.enable("data_server")

energydata = pd.read_csv("../data/energydata_complete.csv")

# create a day of week column and month column and day column
energydata["date"] = pd.to_datetime(energydata["date"])
energydata['day_of_week'] = energydata["date"].dt.day_name()
energydata['month'] = energydata["date"].dt.strftime('%b')
energydata['day'] = energydata["date"].dt.date

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


## Plotting
# bar chart for day of week
def bar_plot_altair(start_date, end_date):
    # select date range
    selected_data = energydata[(energydata['day'] <= end_date) & (energydata['day'] >= start_date)]
    # group by day of week and sum the energy consumption
    selected_data = selected_data.groupby(['day_of_week']).sum().reset_index()

    # make Appliances vs Day of week bar plot
    chart = alt.Chart(selected_data).mark_bar(color='#D35400', size=20).encode(
        x=alt.X('Appliances:Q', axis=alt.Axis(title='Appliances energy consumption in Wh')),
        y=alt.Y('day_of_week:N', axis=alt.Axis(title='Day of the week'),
                sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    ).properties(
        width=400,
        height=300
    )
    return chart.to_html()


# pie chart for day of week
def pie_chart(start_date, end_date):
    # select date range
    selected_data = energydata[(energydata['day'] <= end_date) & (energydata['day'] >= start_date)]
    # group by day of week and sum the energy consumption
    selected_data = selected_data.groupby(['day_of_week']).sum().reset_index()

    chart = alt.Chart(selected_data).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Appliances", type="quantitative"),
        color=alt.Color(field="day_of_week", type="nominal", legend=alt.Legend(title="Day of the week"),
                        sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
    ).configure_axis(grid=False).configure_view(strokeWidth=0)
    return chart.to_html()


def plot_temp_hum(start_date, end_date, room="T1RH_1"):
    # select date range
    selected_data = energydata[(energydata['day'] <= end_date) & (energydata['day'] >= start_date)]

    room_temp = room[0:2]
    room_hum = room[2:6]

    temp = (
        alt.Chart(selected_data)
            .mark_line(color="red")
            .encode(
            alt.Y(f"{room_temp}:Q", title="Temperature"),
            alt.X("date", title="Date"),
        )
    )

    hum = (
        alt.Chart(selected_data)
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
    srcDoc=plot_temp_hum(start_date=energydata['day'].min(), end_date=energydata['day'].max()),
    style={"width": "100%", "height": "400px"},
)

# bar chart for day of week
plot2 = html.Iframe(
    id='barchart',
    srcDoc=bar_plot_altair(start_date=energydata['day'].min(), end_date=energydata['day'].max()),
    style={'border-width': '0', 'width': '100%', 'height': '400px'})

# pie chart for day of week
plot3 = html.Iframe(
    id='pie_chart',
    srcDoc=pie_chart(start_date=energydata['day'].min(), end_date=energydata['day'].max()),
    style={'border-width': '0', 'width': '100%', 'height': '400px'})

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
        # date range controller
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(2016, 1, 11),
            max_date_allowed=date(2016, 5, 27),
            initial_visible_month=date(2016, 1, 11),
            start_date=date(2016, 1, 11),
            end_date=date(2016, 5, 27)
        ),
        plot1,  # temp and hum plot for different room
        plot2,  # bar chart for day of week
        plot3,  # pie chart for day of week
    ]
)


@app.callback(
    Output("temp_hum", "srcDoc"),
    Output('barchart', 'srcDoc'),
    Output('pie_chart', 'srcDoc'),
    Input("room", "value"),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)
def update_output(room, start_date, end_date):
    # convert the outputs to date object
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    return (plot_temp_hum(start_date=start_date_object, end_date=end_date_object, room=room),
            bar_plot_altair(start_date=start_date_object, end_date=end_date_object),
            pie_chart(start_date=start_date_object, end_date=end_date_object))


if __name__ == "__main__":
    app.run_server(debug=True)
