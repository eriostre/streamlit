import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('ireland_trade.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Ireland Trade Dashboard", style={'textAlign': 'center'}),
    
    # Filters
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': str(year), 'value': year} for year in df['year'].unique()],
            value=df['year'].max(),
            placeholder="Select a year"
        ),
        html.Label("Select Trade Flow:"),
        dcc.Dropdown(
            id='flow-dropdown',
            options=[{'label': flow, 'value': flow} for flow in df['flow'].unique()],
            value='Export',
            placeholder="Select trade flow"
        ),
        html.Label("Select Commodity Category:"),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': cat, 'value': cat} for cat in df['category'].unique()],
            value=None,
            placeholder="Select a category (optional)"
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    
    # Graphs
    html.Div([
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='line-chart'),
        dcc.Graph(id='pie-chart'),
    ], style={'width': '65%', 'display': 'inline-block'}),
])

# Callbacks for interactivity
@app.callback(
    [Output('bar-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('year-dropdown', 'value'),
     Input('flow-dropdown', 'value'),
     Input('category-dropdown', 'value')]
)
def update_graphs(selected_year, selected_flow, selected_category):
    # Filter data based on selections
    filtered_df = df[(df['year'] == selected_year) & (df['flow'] == selected_flow)]
    if selected_category:
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    # Bar chart: Top commodities by trade_usd
    bar_chart = px.bar(
        filtered_df.nlargest(10, 'trade_usd'),
        x='commodity',
        y='trade_usd',
        title=f"Top 10 Commodities by Trade Value ({selected_flow}, {selected_year})",
        labels={'trade_usd': 'Trade Value (USD)', 'commodity': 'Commodity'},
    )
    
    # Line chart: Trade trends over years
    line_chart = px.line(
        df[(df['flow'] == selected_flow) & (df['category'] == selected_category)] if selected_category else df[df['flow'] == selected_flow],
        x='year',
        y='trade_usd',
        color='commodity',
        title=f"Trade Trends Over Years ({selected_flow})",
        labels={'trade_usd': 'Trade Value (USD)', 'year': 'Year'}
    )
    
    # Pie chart: Trade distribution by weight_kg
    pie_chart = px.pie(
        filtered_df,
        names='commodity',
        values='weight_kg',
        title=f"Trade Distribution by Weight ({selected_flow}, {selected_year})"
    )
    
    return bar_chart, line_chart, pie_chart

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8054)