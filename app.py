import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import altair as alt
import pandas as pd

#Read in data
data = pd.read_csv("data/energydata_complete.csv")

# Save a vega-lite spec and a PNG blob for each plot in the notebook
alt.renderers.enable("mimetype")
# Handle large data sets without embedding them in the notebook
alt.data_transformers.enable("data_server")

#app = dash.Dash(__name__,external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])


## Plotting

def plot_outsidetemp(xcol = 'T_out'):
    chart = alt.Chart(data).mark_area().encode(
        x=xcol,
        y='RH_out')

    return chart.interactive().to_html()

## Layout Components
plot1 = html.Iframe(id='altair_chart',srcDoc=plot_outsidetemp(xcol = 'T_out'),
style={'width': '100%', 'height': '400px'})

row = html.Div(
    [
         dbc.Row(
            [
                dbc.Col(html.Div(plot1)),
                dbc.Col(html.Div("One of six plots")),
                dbc.Col(html.Div("One of six plots")),
            ]
         ),
        dbc.Row(
            [
                dbc.Col(html.Div("One of six plots")),
                dbc.Col(html.Div("One of six plots")),
                dbc.Col(html.Div("One of six plots")),
            ]
        ),
    ]
)



random_text= dcc.Markdown('''

        # Energy Use of Appliance in a Low-Energy House
        
        Collaborators  
        Harpreet Kaur  
        Chad Wheeler  
        Neslson Tang  
        Nyanda Redwood   

        
        ''')

## Layout
app.layout = dbc.Container([random_text,

    dbc.Alert("Welcome to my app!", color="info"),
    html.Div(
    [
        # html.H1("Energy Use of Appliance in a Low-Energy House"),
        # html.H2("Collaborators"),
        # html.H3("Harpreet Kaur"),
        # html.H4("Chad Wheeler"),
        # html.H5("Neslson Tang"),
        # html.H6("Nyanda Redwood"),
        # html.Blockquote("This is a really really long paragraph."),
        # DCC
        row,
        # dcc.Checklist(["New York", "Vancouver", "Kelowna"], ["YXX", "YVR", "YYZ"]),
        # # dcc.Slider(
        #     min=-5,
        #     max=10,
        #     value=0,
        #     marks={-5: "Really Cold", 0: "Freezing", 3: "Kelowna", 10: "Really Hot"},
        # ),
        #dcc.Dropdown(id='chart_dropdown',value='Horsepower',options = [{'label': i, 'value': i} for i in cars.columns if i not in ['Name'] ]),
        #plot1,

    ])
])

## Callback functions
@app.callback(
    Output('altair_chart','srcDoc')) #Specifies where the output of plot_outsidetemp() "goes"
    #Input('chart_dropdown', 'value'))
def update_plot(xcol):
    return plot_outsidetemp(xcol)

if __name__ == "__main__":
    app.run_server(host="127.0.0.1", debug=True)

