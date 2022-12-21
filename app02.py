import dash
from dash import html, dcc
from dash import Input, Output

import plotly.express as px

import pandas as pd

app = dash.Dash(__name__)
app.title = "DAC Dashboard"
#server = app.server

df = pd.read_csv('unemployment.csv')

id_vars = df.columns[:2]
value_vars = df.columns[2:]
    
dfMolten = pd.melt(df, id_vars = id_vars, value_vars = value_vars, var_name='Year', value_name='Unemployment')

fig = px.choropleth(
    dfMolten,  
    locations= dfMolten['Country Code'], 
    color="Unemployment", 
    animation_frame=dfMolten["Year"],
    animation_group=dfMolten["Country Name"],
    hover_name=dfMolten["Country Name"],
    color_continuous_scale= 'Portland',
    projection="mercator",
    labels={ 'Unemployment' : 'Unemployment Rate'},
)

fig.update_layout(height = 600, margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(coloraxis_showscale=False)

#fig1 = px.scatter(dfMolten, x ='Year', y ='Unemployment', color="Country Name")
#fig1.update_traces(mode='lines+markers')
#fig1.update_layout(height=300, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
#fig1.update_layout(coloraxis_showscale=False)
#fig1.update_traces(showlegend=False)
app.layout = html.Div(
    children = [
        html.Div(
            [
                html.Img(src=app.get_asset_url("dac_01.png"), className="logo", width='300px'),
                html.H4("DAC BOARD"),
            ],
            className="header__title",
        ),
        html.Div([
            dcc.Graph(figure=fig, id='world-map')
        ], style={'width': '60%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        html.Div([dcc.Graph(id='yearly-chart')], style={'height':300}),
        html.Div([dcc.Graph(id='y-time-series')], style={'height':300}),
    ], style={'display': 'inline-block', 'width': '35%'}),       
])


#@app.callback(
#    Output('yearly-chart', 'figure'),
#    Input('world-map', 'hoverData'))
#def update_line_chart(hoverData):
#    fig = None
#    if hoverData:
#        hData = hoverData["points"][0]
#        countryCode = hData.get('location', None)
#        if countryCode:
#            print("Hover")
#            dfCountry = dfMolten[dfMolten['Country Code'] == countryCode]
#            fig = px.scatter(dfCountry, x ='Year', y ='Unemployment')
#            fig.update_traces(mode='lines+markers')
#            fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
#            return fig
#    return fig

        
@app.callback(
    Output('yearly-chart', 'figure'),
    Input('world-map', 'clickData'))
def update_line_chart(clickData):
    countryCode = None
    if clickData:
        hData = clickData["points"][0]
        countryCode = hData.get('location', None)
    if countryCode is None:
        countryCode = 'CAN'

    dfCountry = dfMolten[dfMolten['Country Code'] == countryCode]
    fig = px.scatter(dfCountry, x ='Year', y ='Unemployment')
    fig.update_traces(mode='lines+markers')
    fig.update_layout(height=300, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})
    return fig

app.run_server(debug=True) 