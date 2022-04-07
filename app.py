from matplotlib import container
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
# from firebase_data import ref
  # pip install dash (version 2.0.0 or higher)
from dash.dependencies import Input, Output
import numpy as np

import firebase_admin
import pandas as pd
import time
import json

cred_object = firebase_admin.credentials.Certificate('cred_obj.json')
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL': "https://hatespeech-abd47-default-rtdb.firebaseio.com"
	})

from firebase_admin import db

ref = db.reference("/")

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

locations = ["Invalid Location", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

app = Dash(__name__)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div(
    children=[
        # html.Br(),
        
        html.Div(className = 'header' , children=[
        html.H1(
            "Twitter Hate Speech", 
            style={'text-align': 'center'})]), 
     
        html.Br(), 
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        
        html.Div(children=[
            dcc.Graph(id = "choropleth_map", 
            style={'display': 'inline-block'},
            # figure = {'layout':
            # {'plot_bgcolor' : '#111111' , 'paper_bgcolor' : '#111111'}}
            ),
            
            dcc.Graph(id="categorial_pie_chart", style={'display': 'inline-block'},
            # figure = {'layout':
            # {'plot_bgcolor' : '#111111' , 'paper_bgcolor' : '#111111'}}
            )
            ]),
        
        # html.Div(children=[
        #     html.Pre(id='hover-data', style=styles['pre'])
        # ]),

        dcc.Interval(
            id='interval-component',
            interval=1*30000, # in milliseconds
            n_intervals=0),   
        ])

@app.callback(Output('choropleth_map', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    data = ref.get()
    df = pd.DataFrame.from_dict(data)
    df = df.transpose()
    # print(df)

    df2 = df["loc"].value_counts()
    row_names = df2.index

    df3 = pd.DataFrame(df2 , index = row_names)
    df3.reset_index(inplace=True)
    df3 = df3.rename(columns = {'index':'State'})
    # print(df3)

    df4 = df[['category' , 'loc']]
    df4.reset_index(inplace=True)
    df4 = df4[['category','loc']]
    # print(df4)

    zero_data = np.zeros(shape=(51,7))
    d = pd.DataFrame(zero_data, columns=["State", 'loc' , "sexual orientation" , "special needs" , "race" , "gender" , "other"])

    for i in range(len(d)):
        d['State'][i] = locations[i]
    # print(d)

    for i in range(len(locations)):
        s_o_count = 0
        s_n_count = 0
        r_count = 0
        g_count = 0
        o_count = 0
        for j in range(len(df4['loc'])):
            if df4['loc'][j] == locations[i]:
                if df4['category'][j] == "sexual orientation":
                    s_o_count += 1
                elif df4['category'][j] == "special needs":
                    s_n_count += 1
                elif df4['category'][j] == "race":
                    r_count += 1
                elif df4['category'][j] == "gender":
                    g_count += 1
                else:
                    o_count += 1
        d.loc[i, 'sexual orientation'] = s_o_count
        d.loc[i, 'special needs'] = s_n_count
        d.loc[i, 'race'] = r_count
        d.loc[i, 'gender'] = g_count
        d.loc[i, 'other'] = o_count

    for i in range(len(df3)):
        for j in range(len(d)):
            if df3['State'][i] == d['State'][j]:
                d['loc'][j] = df3['loc'][i]
    fig = px.choropleth(        
        data_frame=d,
        locationmode='USA-states',
        locations='State',
        scope="usa",
        color='loc',
        hover_data=['State', 'loc', 'sexual orientation' , 'special needs' , 'race' , 'gender', 'other'],
        color_continuous_scale=px.colors.sequential.Plasma,
        labels={'loc': 'Number of Tweets'},
        # template='plotly_dark'
        )
    fig.update_layout(font = dict(family = 'sans-serif'))
    return fig

# @app.callback(Output("categorial_pie_chart" , "figure"),
#             Input("choropleth_map" , "hoverData"))
# def update_pie_chart(hoverData):
#     categories = ['sexual orientation' , 'special needs' , 'race' , 'gender' , 'other']
#     df_pie = hoverData['customdata']
#     fig = px.pie(df_pie, values = categories, names = "State")
#     return fig

# @app.callback(
#     Output('hover-data', 'children'),
#     Input('choropleth_map', 'hoverData'))
# def display_hover_data(hoverData):
#     data = [hoverData['points'][0]['customdata']]
#     df_pie = pd.DataFrame(data, columns =['State', 'Total', 'Sexual Orientation', 'Special Needs' , 'Race', 'Gender', 'Other'])
#     return json.dumps(df_pie['State'], indent=2)

@app.callback(
    Output('categorial_pie_chart', 'figure'),
    Input('choropleth_map', 'hoverData'))   
def update_pie_chart(hoverData):
    data = [hoverData['points'][0]['customdata']]
    df_pie = pd.DataFrame(data, columns =['State', 'Total', 'Sexual Orientation', 'Special Needs' , 'Race', 'Gender', 'Other'])
    df_pie_final = pd.DataFrame({'Category' : ['Sexual Orientation' , 'Special Needs' , 'Race', 'Gender', 'Other'], 'Amount':[int(df_pie['Sexual Orientation']) , int(df_pie["Special Needs"]) ,int(df_pie['Race']), int(df_pie["Gender"]), int(df_pie["Other"])]})
    fig = px.pie(df_pie_final,  values = "Amount", names = 'Category', title = f"Breakdown of Categories in {df_pie['State'][0]}", color_discrete_sequence=px.colors.sequential.Plasma)
    fig.update_layout(font = dict(family = 'sans-serif'))
    return fig
    
if __name__ == '__main__':
    app.run_server(debug=True)