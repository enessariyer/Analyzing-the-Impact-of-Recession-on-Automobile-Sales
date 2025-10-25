# --- Load Libraries ---

# Standard Python Libraries
from io import BytesIO
import datetime as dt

# Third-Party Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from dash import Dash, dcc, html, Input, Output


# --- Load and Prepare Data ---

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
response = requests.get(URL)
text = BytesIO(response.content)
df = pd.read_csv(text)

df["Date"] = pd.to_datetime(df["Date"])
df["MonthN"] = df["Date"].dt.month


# --- Initialize Dash App ---

app = Dash(__name__)


# --- Application Layout ---

app.layout = html.Div([

    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            "textAlign": "center",
            "color": "#503D36",
            "fontSize": "24px"
        }
    ),

    # Dropdown Container 1 (Report Type)
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

    # Dropdown Container 2 (Year Selection)
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
                options=[{"label": year, "value": year} for year in df["Year"].unique()],
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

    # Output Container (for Graphs)
    html.Div([
        html.Div(
            id="output-container",
            className="chart-grid",
            style={"display": "flex", "flex-direction": "column", "align-items": "center"}
        )
    ])

])


# ===== CALLBACKS (Interactivity) =====

# Callback 1: Enable/disable the year dropdown
@app.callback(
    Output("select-year", "disabled"),
    Input("dropdown-statistics", "value")
)
def update_input_container(selected_statistics):
    if selected_statistics == "Yearly Statistics":
        return False
    else:
        return True


# Callback 2: Update graphs
@app.callback(
    Output("output-container", "children"),
    [Input("dropdown-statistics", "value"),
     Input("select-year", "value")]
)
def update_ouput_container(selected_statistics, input_year):
    
    if selected_statistics == "Recession Period Statistics":
        recession_data = df[df["Recession"] == 1]
        
        # --- Graph 1: Sales Over Recession Period (Year Wise) ---
        rec_data1 = recession_data.groupby("Year", as_index=False)["Automobile_Sales"].mean()
        fig_line = px.line(
            data_frame=rec_data1,
            x="Year",
            y="Automobile_Sales",
            title="Automobile Sales Over Recession Period (Year Wise)",
            labels={"Year": "Year", "Automobile_Sales": "Automobile Sales"}
        )
        fig_line.update_layout(plot_bgcolor='#f5f5f5', font=dict(size=13), title_x=0.45)
        fig_line.update_traces(mode="lines+markers")

        # --- Graph 2: Average Sales by Vehicle Type during Recession ---
        rec_data2 = recession_data.groupby("Vehicle_Type", as_index=False)["Automobile_Sales"].mean()
        fig_bar = px.bar(
            data_frame=rec_data2, x="Vehicle_Type", y="Automobile_Sales",
            color="Vehicle_Type", title="Average number of vehicles sold by vehicle type",
            labels={"Vehicle_Type": "Vehicle Type", "Automobile_Sales": "Automobile Sales"}
        )
        fig_bar.update_layout(font=dict(size=13), plot_bgcolor='#f5f5f5')

        # --- Graph 3: Advertising Expenditure Share by Vehicle Type during Recession ---
        rec_data3 = recession_data.groupby("Vehicle_Type", as_index=False)["Advertising_Expenditure"].sum()
        fig_pie = px.pie(
            data_frame=rec_data3, names="Vehicle_Type", values="Advertising_Expenditure",
            title="Total expenditure share by vehicle type during recessions"
        )

        # --- Graph 4: Effect of Unemployment Rate during Recession ---
        fig_bar2 = px.bar(
            data_frame=recession_data, x="unemployment_rate", y="Automobile_Sales", color="Vehicle_Type",
            title="Effect of Unemployment Rate on Vehicle Type and Sales",
            labels={"unemployment_rate": "Unemployment Rate", "Automobile_Sales": "Automobile Sales"}
        )

        # Return graphs in a 2x2 grid
        return [
            html.Div(className="chart-item", children=[
                html.Div(children=dcc.Graph(figure=fig_line)),
                html.Div(children=dcc.Graph(figure=fig_bar))
            ], style={"display": "flex"}),
            
            html.Div(className="chart-item", children=[
                html.Div(children=dcc.Graph(figure=fig_pie)),
                html.Div(children=dcc.Graph(figure=fig_bar2))
            ], style={"display": "flex"})
        ]
    
    # If "Yearly Statistics" is selected
    elif (input_year and selected_statistics == "Yearly Statistics"):
        if isinstance(input_year, int):
            yearly_data = df[df["Year"] == input_year]
            
            # --- Graph 1: Average Sales Over All Years ---
            yas = df.groupby("Year", as_index=False)["Automobile_Sales"].mean()
            r1 = px.line(
                data_frame=yas, x="Year", y="Automobile_Sales", title="Yearly Automobile Sales",
                labels={"Automobile_Sales": "Automobile Sales"}
            )
            
            # --- Graph 2: Total Monthly Sales Over All Years ---
            mas = df.groupby(["Month", "MonthN"], as_index=False)["Automobile_Sales"].sum().sort_values(by="MonthN")
            r2 = px.line(
                data_frame=mas, x="Month", y="Automobile_Sales", title="Total Monthly Automobile Sales",
                labels={"Automobile_Sales": "Automobile Sales"}
            )

            # --- Graph 3: Average Sales by Vehicle Type in Selected Year ---
            avg_vdata = yearly_data.groupby("Vehicle_Type", as_index=False)["Automobile_Sales"].mean()
            r3 = px.bar(
                data_frame=avg_vdata, x="Vehicle_Type", y="Automobile_Sales",
                title=f'Average Vehicles Sold by Vehicle Type in the {input_year}',
                labels={"Vehicle_Type": "Vehicle Type", "Automobile_Sales": "Automobile Sales"}
            )
        
            # --- Graph 4: Advertising Expenditure by Vehicle Type in Selected Year ---
            exp_data = yearly_data.groupby("Vehicle_Type", as_index=False)["Advertising_Expenditure"].sum()
            r4 = px.pie(
                data_frame=exp_data, values="Advertising_Expenditure", names="Vehicle_Type",
                title="Total Advertisement Expenditure for Each Vehicle"
            )

            # Return graphs in a 2x2 grid
            return [
                html.Div(className="chart-item", children=[
                    html.Div(children=dcc.Graph(figure=r1)),
                    html.Div(children=dcc.Graph(figure=r2))
                ], style={"display": "flex"}),
                
                html.Div(className="chart-item", children=[
                    html.Div(children=dcc.Graph(figure=r3)),
                    html.Div(children=dcc.Graph(figure=r4))
                ], style={"display": "flex"})
            ]
            
        else:
            # If no year is selected (still "Select Year"), return empty
            return []
            
    else:
        # At start (still "Select Statistics"), return empty
        return None


# --- Run the Application ---
if __name__ == "__main__":
    app.run()
