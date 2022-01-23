# Importing libraries

from msilib.schema import Component
from optparse import Values
import dash 
import plotly.express as px
import pandas as pd
import numpy as np 
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import dash_table


# Reading data from excel
df = pd.read_excel("D:/Book1.xlsx")

# Initialising flask under the hood
app = dash.Dash(__name__)

# Defining App Layout
app.layout = html.Div([
    html.H1("Employee data"),
    dcc.Dropdown(id="Month-choice",options=[{'label':x,'value':x} for x in df.Month.unique()],
    value = 'JAN'
    ),
    dcc.Dropdown(id="Year-choice",options=[{'label':y,'value':y} for y in df.Year.unique()],
    value="2021"),
    dcc.Dropdown(id="Employee-choice",options=[{'label':z,'value':z} for z in df["Manager 1"].unique()],
    value="Employee 1"),
    dash_table.DataTable(id='table'),
    html.H1(id="total_data"),
    dcc.Graph(id="my-graph",figure={}),
    
])
# Callback Function , inputs and outputs
@app.callback(
    Output(component_id="my-graph",component_property='figure'),
    Output(component_id="table",component_property="data"),
    Output(component_id="table",component_property="columns"),
    Output(component_id="total_data",component_property="children"),
    Input(component_id="Month-choice",component_property="value"),
    Input(component_id="Year-choice",component_property="value"),
    Input(component_id="Employee-choice",component_property="value")
)
# Decorative function for updating the graph

def interactive_graphing(value_month,value_year,value_employee):
    print(value_month,value_year,value_employee)
    df_2 = df[df.Month == value_month]
    df_3 = df_2[df["Manager 1"] == value_employee]
    df_4 = df_3[df_2.Year == value_year]
    total_value = df_4["Resource allocation"].sum()
    columns = [{'name': col, 'id': col} for col in df_4.columns]
    data = df_4.to_dict(orient='records')
    fig = px.pie(data_frame=df_4,names="Project Name",values="Resource allocation")
    fig.update_traces(textinfo = 'value')
  
    return [fig,data,columns,"total resource allocation is "+str(total_value.item())]


# Initialisation of server

if(__name__ == '__main__'):
    app.run_server()