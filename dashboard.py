import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title="Use Cases Analysis Dashboard", layout="wide")

# Data preparation
use_cases = {
    'Use Case': [
        'Dynamic Menu Pricing & Promotions',
        'Delivery Time Optimization',
        'Store Workforce Optimization',
        'Inventory Waste Reduction',
        'Personalized Upselling Engine',
        'Location Selection & Expansion',
        'Customer Sentiment Analysis',
        'Energy Use Optimization',
        'Next Product to Launch',
        'Franchise Performance Benchmarking',
        'Churn Prediction (Loyalty)'
    ],
    'Revenue': [5, 4, 3, 3, 5, 5, 3, 2, 4, 3, 4],
    'Cost': [3, 3, 4, 5, 2, 3, 2, 4, 1, 3, 2],
    'Ease': [4, 4, 4, 4, 3, 3, 4, 3, 3, 3, 3],
    'Human': [2, 2, 3, 2, 3, 3, 4, 3, 4, 4, 3],
    'Budget': [0.38, 0.40, 0.35, 0.35, 0.345, 0.45, 0.275, 0.30, 0.15, 0.20, 0.30]
}

df = pd.DataFrame(use_cases)
df['Total'] = df['Revenue'] + df['Cost'] + df['Ease'] + (6 - df['Human'])
df['Category'] = df['Total'].apply(lambda x: 'High' if x >= 14 else ('Medium' if x >= 11 else 'Low'))

# Title
st.title("Use Cases Prioritization Analysis Dashboard")
st.markdown("---")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Budget", f"${df['Budget'].sum():.2f}B")
with col2:
    st.metric("High Priority Cases", len(df[df['Category'] == 'High']))
with col3:
    st.metric("Medium Priority Cases", len(df[df['Category'] == 'Medium']))
with col4:
    st.metric("Low Priority Cases", len(df[df['Category'] == 'Low']))

# Filters
st.sidebar.header("Filters")
category_filter = st.sidebar.multiselect(
    "Select Categories",
    options=sorted(df['Category'].unique()),
    default=sorted(df['Category'].unique())
)

filtered_df = df[df['Category'].isin(category_filter)]

# Main content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Score vs Budget")
    fig = px.scatter(filtered_df, 
                    x='Total', 
                    y='Budget',
                    size='Budget',
                    color='Category',
                    hover_data=['Use Case'],
                    title="Use Cases: Total Score vs Budget Allocation")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Budget Distribution by Category")
    fig = px.pie(filtered_df, 
                 values='Budget', 
                 names='Category',
                 title="Budget Distribution by Priority Category")
    st.plotly_chart(fig, use_container_width=True)

# RCEH Scores Comparison
st.subheader("RCEH Scores Comparison")
rceh_data = filtered_df.melt(id_vars=['Use Case', 'Category'], 
                            value_vars=['Revenue', 'Cost', 'Ease', 'Human'],
                            var_name='Metric', 
                            value_name='Score')
fig = px.bar(rceh_data, 
             x='Use Case', 
             y='Score',
             color='Metric',
             barmode='group',
             title="RCEH Scores by Use Case")
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

# Detailed Table
st.subheader("Detailed Analysis Table")
styled_df = filtered_df.sort_values('Total', ascending=False).style.background_gradient(subset=['Total', 'Budget'])
st.dataframe(styled_df, use_container_width=True)

# Correlation Analysis
st.subheader("Correlation Analysis")
correlation_matrix = filtered_df[['Revenue', 'Cost', 'Ease', 'Human', 'Total', 'Budget']].corr()
fig = px.imshow(correlation_matrix,
                title="Correlation Matrix",
                color_continuous_scale='RdBu')
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Dashboard created for analyzing use cases prioritization and budget allocation")