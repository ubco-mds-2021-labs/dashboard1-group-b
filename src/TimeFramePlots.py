import pandas as pd
from datetime import datetime, date
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import altair as alt

# Read in global data
energydata = pd.read_csv("../data/energydata_complete.csv")

# create a day of week column and month column and day column
energydata['date'] = pd.to_datetime(energydata['date'])
energydata['day_of_week'] = energydata["date"].dt.day_name()
energydata['month'] = energydata["date"].dt.strftime('%b')
energydata['day'] = energydata["date"].dt.date

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])


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


def pie_chart(start_date, end_date):
    # select date range
    selected_data = energydata[(energydata['day'] <= end_date) & (energydata['day'] >= start_date)]
    # group by day of week and sum the energy consumption
    selected_data = selected_data.groupby(['day_of_week']).sum().reset_index()

    chart = alt.Chart(selected_data).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Appliances", type="quantitative"),
        color=alt.Color(field="day_of_week", type="nominal", legend=alt.Legend(title="Day of the week"),
                        sort=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']),
    )
    return chart.to_html()


app.layout = html.Div([

    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2016, 1, 11),
        max_date_allowed=date(2016, 5, 27),
        initial_visible_month=date(2016, 1, 11),
        start_date=date(2016, 1, 11),
        end_date=date(2016, 5, 27)
    ),

    html.Iframe(
        id='barchart',
        srcDoc=bar_plot_altair(start_date=energydata['day'].min(), end_date=energydata['day'].max()),
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),

    html.Iframe(
        id='piechart',
        srcDoc=pie_chart(start_date=energydata['day'].min(), end_date=energydata['day'].max()),
        style={'border-width': '0', 'width': '100%', 'height': '400px'})
])


@app.callback(
    Output('barchart', 'srcDoc'),
    Output('piechart', 'srcDoc'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    # convert the outputs to date object
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    return (bar_plot_altair(start_date=start_date_object, end_date=end_date_object),
            pie_chart(start_date=start_date_object, end_date=end_date_object))


if __name__ == '__main__':
    app.run_server(debug=True)
