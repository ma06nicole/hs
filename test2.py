import firebase_admin
from firebase_admin import db
import pandas as pd
import numpy as np

cred_object = firebase_admin.credentials.Certificate('cred_obj.json')
default_app = firebase_admin.initialize_app(cred_object, {
	'databaseURL': "https://hatespeech-abd47-default-rtdb.firebaseio.com"
	})

ref = db.reference("/")
data = ref.get()

locations = ["Invalid Location", "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

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

print(df3)
# print(d)

for i in range(len(df3)):
    for j in range(len(d)):
        if df3['State'][i] == d['State'][j]:
            d['loc'][j] = df3['loc'][i]

print(d)
            
# @app.callback(Output('choropleth_map', 'figure'),
#               Input('interval-component', 'n_intervals'))
# def update_graph_live(n):
#     data = ref.get()
#     print(data)
#     df = pd.DataFrame.from_dict(data)
#     df = df.transpose()
#     # print(df)
#     df2 = df["loc"].value_counts()
#     print(df2)
#     row_names = df2.index
#     print(row_names)
#     # df2 = df.groupby("loc").count()
#     # print(df2)
#     # print(df2.shape)
#     # df3 = row_names.concat(df2)
#     # print(df3)
#     df3 = pd.DataFrame(df2 , index = row_names)
#     df3.reset_index(inplace=True)
#     df3 = df3.rename(columns = {'index':'State'})
#     fig = px.choropleth(        
#         data_frame=df3,
#         locationmode='USA-states',
#         locations='State',
#         scope="usa",
#         color='loc',
#         hover_data=['State', 'loc'],
#         color_continuous_scale=px.colors.sequential.Plasma,
#         labels={'loc': 'Number of Tweets'},
#         # template='plotly_dark'
#         )

#     return fig


    
        




   
        

    

