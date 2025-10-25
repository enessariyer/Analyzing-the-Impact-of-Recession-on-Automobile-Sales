import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import requests
from io import BytesIO
import datetime as dt


URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
response = requests.get(URL)
text = BytesIO(response.content)
df = pd.read_csv(text)


df["Date"] = pd.to_datetime(df["Date"])
df["MonthN"] = df["Date"].dt.month

app = Dash(__name__)


app.layout = html.Div([


    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            "textAlign":"center",
            "color":"#503D36",
            "fontSize":"24px"
        }
    ),


    html.Div(
        style={
            'width': '80%',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'padding-bottom': '10px'
        },
        children=[
            dcc.Dropdown(
                id="dropdown-statistics",
                options=[
                    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                ],
                placeholder='Select a report type',
                value="Select Statistics",
                style={
                    'width': '100%', 
                    'padding': '3px', 
                    'font-size': '20px', 
                    'text-align-last': 'center'
                }
            )
        ]
    ),


    html.Div(
        style={
            'width': '80%',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'padding-bottom': '10px'
        },
        children=[
            dcc.Dropdown(
                id="select-year",
                options=[{"label":year, "value":year} for year in df["Year"].unique()],
                placeholder="Select Year",
                value="Select Year",
                style={
                    'width': '100%', 
                    'padding': '3px', 
                    'font-size': '20px', 
                    'text-align-last': 'center'
                }
            )
        ]
    ),


    html.Div([
        html.Div(
            id = "output-container",
            className = "chart-grid",
            style={"display":"flex", "flex-direction":"column", "align-items":"center"}
        )
    ])

])


@app.callback(
    Output("select-year", "disabled"),
    Input("dropdown-statistics", "value")
)

def update_input_container(selected_statistics):
    if selected_statistics == "Yearly Statistics":
        return False
    else:
        return True


@app.callback(
    Output("output-container", "children"),
    [Input("dropdown-statistics", "value"),
     Input("select-year", "value")]
)

def update_ouput_container(selected_statistics, input_year):
    if selected_statistics == "Recession Period Statistics":
        recession_data = df[df["Recession"] == 1]
        rec_data1 = recession_data.groupby("Year", as_index=False)["Automobile_Sales"].mean()
        
        # First Recession Graph
        fig_line = px.line(
                data_frame=rec_data1, 
                x="Year", 
                y="Automobile_Sales",
                title="Automobile Sales Over Recession Period (Year Wise)",
                labels={"Year": "Year", "Automobile_Sales": "Automobile Sales"} 
            )

        fig_line.update_layout(
            plot_bgcolor='#f5f5f5',
            font=dict(size=13),
            title_x=0.45
        )

        fig_line.update_traces(mode="lines+markers")

        # Second Recession Graph
        rec_data2 = recession_data.groupby("Vehicle_Type", as_index=False)["Automobile_Sales"].mean()
        fig_bar = px.bar(data_frame=rec_data2, x="Vehicle_Type", y="Automobile_Sales",
             color="Vehicle_Type", title="Average number of vehicles sold by vehicle type",
             labels={"Vehicle_Type":"Vehicle Type", "Automobile_Sales":"Automobile Sales"})

        fig_bar.update_layout(font=dict(size=13), plot_bgcolor='#f5f5f5')

        # Third Recession Graph
        rec_data3 = recession_data.groupby("Vehicle_Type", as_index=False)["Advertising_Expenditure"].sum()
        fig_pie = px.pie(data_frame=rec_data3, names="Vehicle_Type", values="Advertising_Expenditure", title="Total expenditure share by vehicle type during recessions")


        # Fourth Recession Graph

        fig_bar2 = px.bar(data_frame=recession_data, x="unemployment_rate", y="Automobile_Sales", color="Vehicle_Type",
        title="Effect of Unemployment Rate on Vehicle Type and Sales",
        labels={"unemployment_rate":"Unemployment Rate", "Automobile_Sales":"Automobile Sales"})
        return [html.Div(className="chart-item", children=[html.Div(children=dcc.Graph(figure=fig_line)), html.Div(children=dcc.Graph(figure=fig_bar))], style={"display": "flex"}),
                html.Div(className="chart-item", children=[html.Div(children=dcc.Graph(figure=fig_pie)), html.Div(children=dcc.Graph(figure=fig_bar2))], style={"display": "flex"})]
    

    elif (input_year and selected_statistics == "Yearly Statistics"):
         if isinstance(input_year, int):
            # First
            yearly_data = df[df["Year"] == input_year]
            yas = df.groupby("Year", as_index=False)["Automobile_Sales"].mean()
            r1 = px.line(data_frame=yas, x="Year", y="Automobile_Sales", title="Yearly Automobile Sales",
                    labels={"Automobile_Sales":"Automobile Sales"})
            # Second
            mas = df.groupby(["Month", "MonthN"], as_index=False)["Automobile_Sales"].sum().sort_values(
                by="MonthN")

            r2 = px.line(data_frame=mas, x="Month", y="Automobile_Sales", title="Total Monthly Automobile Sales",
            labels={"Automobile_Sales":"Automobile Sales"})

            # Third
            avg_vdata = yearly_data.groupby("Vehicle_Type", as_index=False)["Automobile_Sales"].mean()
            r3 = px.bar(data_frame=avg_vdata, x="Vehicle_Type", y="Automobile_Sales", 
               title=f'Average Vehicles Sold by Vehicle Type in the {input_year}',
               labels={"Vehicle_Type":"Vehicle Type", "Automobile_Sales":"Automobile Sales"})
        
            # Fourth
            exp_data = yearly_data.groupby("Vehicle_Type", as_index=False)["Advertising_Expenditure"].sum()
            r4 = px.pie(data_frame=exp_data, values="Advertising_Expenditure", names="Vehicle_Type",
                title="Total Advertisement Expenditure for Each Vehicle")


            return [html.Div(className="chart-item", children=[html.Div(children=dcc.Graph(figure=r1)), html.Div(children=dcc.Graph(figure=r2))],style={"display": "flex"}),
                    html.Div(className="chart-item", children=[html.Div(children=dcc.Graph(figure=r3)), html.Div(children=dcc.Graph(figure=r4))],style={"display": "flex"})]
    else:
        return None


if __name__ == "__main__":
    app.run(debug=True)