import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('ireland_trade.csv')

# Streamlit app
st.title("Ireland Trade Dashboard")

# Filters
st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox("Select Year", options=sorted(df['year'].unique()), index=len(df['year'].unique()) - 1)
selected_flow = st.sidebar.selectbox("Select Trade Flow", options=df['flow'].unique())
selected_category = st.sidebar.selectbox("Select Commodity Category", options=['All'] + df['category'].unique().tolist())

# Filter data based on selections
filtered_df = df[(df['year'] == selected_year) & (df['flow'] == selected_flow)]
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['category'] == selected_category]

# Display summary statistics
st.write(f"## Summary for {selected_flow} in {selected_year}")
st.write(f"Number of Transactions: {filtered_df.shape[0]}")
st.write(f"Total Trade Value (USD): ${filtered_df['trade_usd'].sum():,.2f}")
st.write(f"Total Weight (kg): {filtered_df['weight_kg'].sum():,.2f}")

# Visualizations
st.write("### Top Commodities by Trade Value")
top_commodities = filtered_df.nlargest(10, 'trade_usd')
fig_bar = px.bar(top_commodities, x='commodity', y='trade_usd', labels={'trade_usd': 'Trade Value (USD)', 'commodity': 'Commodity'})
st.plotly_chart(fig_bar)

st.write("### Trade Trends Over Years")
fig_line = px.line(
    df[(df['flow'] == selected_flow) & (df['category'] == selected_category)] if selected_category != 'All' else df[df['flow'] == selected_flow],
    x='year', y='trade_usd', color='commodity', labels={'trade_usd': 'Trade Value (USD)', 'year': 'Year'}
)
st.plotly_chart(fig_line)

st.write("### Trade Distribution by Weight")
fig_pie = px.pie(filtered_df, names='commodity', values='weight_kg', title=f"Trade Distribution by Weight ({selected_year})")
st.plotly_chart(fig_pie)