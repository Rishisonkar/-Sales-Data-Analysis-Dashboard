import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# 1. PAGE INITIALIZATION & PREMIUM THEME CSS INJECTION
st.set_page_config(page_title="Apple Style Sales Dashboard", layout="wide")

# Custom CSS for Dark Header, Light Body background, and Rounded Shadow Grid Cards
st.markdown("""
    <style>
        /* Main canvas background */
        .stApp {
            background-color: #F3F4F6 !important;
        }
        /* Hide default Streamlit block margins */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 1rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        /* Top Premium Dark Banner */
        .custom-header {
            background-color: #1A1A1A;
            padding: 20px 30px;
            margin-left: -2rem;
            margin-right: -2rem;
            margin-bottom: 25px;
            color: #FFFFFF;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid #3182ce;
        }
        .custom-header h1 {
            color: white !important;
            margin: 0;
            font-size: 24px;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-weight: 600;
        }
        .custom-header span {
            color: #A0AEC0;
            font-size: 14px;
        }
        /* Metric Card Layout styling */
        div[data-testid="stMetricValue"] {
            font-size: 26px !important;
            font-weight: 700 !important;
            color: #FFFFFF !important;
        }
        div[data-testid="stMetricLabel"] {
            font-size: 13px !important;
            color: #A0AEC0 !important;
            font-weight: 500 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Top Custom Navigation Header HTML
st.markdown("""
    <div class="custom-header">
        <h1>Enterprise Sales Performance Analytics</h1>
        <span>Metrics Overview &nbsp;&nbsp;|&nbsp;&nbsp; Multi-Dimensional Canvas Analysis</span>
    </div>
""", unsafe_allow_html=True)


# 2. ETL DATA GENERATION AND PIPELINE CACHE ENGINE
@st.cache_data
def generate_and_clean_data():
    # Data generation
    np.random.seed(42)
    n_records = 10500

    order_ids = [f"CA-2025-{100000 + i}" for i in range(n_records)]
    order_dates = [datetime(2024, 1, 1) + timedelta(days=int(np.random.randint(0, 800))) for i in range(n_records)]
    customer_ids = [f"CS-{np.random.randint(1001, 1500)}" for i in range(n_records)]
    segments = np.random.choice(['Consumer', 'Corporate', 'Home Office'], size=n_records, p=[0.5, 0.3, 0.2])
    regions = np.random.choice(['North', 'South', 'East', 'West'], size=n_records)

    states_map = {
        'North': ['Delhi', 'Punjab', 'Haryana', 'UP'],
        'South': ['Karnataka', 'Tamil Nadu', 'Telangana', 'Kerala'],
        'East': ['West Bengal', 'Odisha', 'Bihar', 'Jharkhand'],
        'West': ['Maharashtra', 'Gujarat', 'Rajasthan', 'Goa']
    }
    states = [np.random.choice(states_map[r]) for r in regions]
    categories = np.random.choice(['Furniture', 'Office Supplies', 'Technology'], size=n_records, p=[0.3, 0.4, 0.3])

    sub_cats_map = {
        'Furniture': ['Chairs', 'Tables', 'Furnishings'],
        'Office Supplies': ['Paper', 'Binders', 'Art', 'Fasteners'],
        'Technology': ['Phones', 'Accessories', 'Copiers']
    }
    sub_cats = [np.random.choice(sub_cats_map[c]) for c in categories]

    quantities = np.random.randint(1, 10, size=n_records)
    base_prices = np.random.uniform(10, 500, size=n_records)
    sales = base_prices * quantities
    discounts = np.random.choice([0.0, 0.1, 0.2, 0.5], size=n_records, p=[0.6, 0.2, 0.1, 0.1])
    sales = sales * (1 - discounts)

    profits = []
    for i in range(n_records):
        if sub_cats[i] == 'Tables' and regions[i] == 'South':
            p = -float(sales[i] * np.random.uniform(0.1, 0.4))
        else:
            p = float(sales[i] * np.random.uniform(0.05, 0.25))
        profits.append(p)

    df = pd.DataFrame({
        'order_id': order_ids, 'order_date': order_dates, 'customer_id': customer_ids,
        'segment': segments, 'region': regions, 'state': states,
        'category': categories, 'sub_category': sub_cats,
        'sales': np.round(sales, 2), 'quantity': quantities, 'discount': discounts, 'profit': np.round(profits, 2)
    })

    # Cleaning operations
    df['discount'].fillna(0.0, inplace=True)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['profit_margin'] = (df['profit'] / df['sales']) * 100
    df['year'] = df['order_date'].dt.year
    return df

df = generate_and_clean_data()


# 3. TOP KPI METRIC GRID LAYER (5 DARK METRIC BLOCKS)
st.markdown("""
    <style>
        [data-testid="stMetric"] {
            background-color: #0F172A !important;
            border: 1px solid #1E293B;
            padding: 15px 20px !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)
total_orders = df['order_id'].nunique()
avg_margin = df['profit_margin'].mean()
total_units = df['quantity'].sum()
avg_sales = df['sales'].mean()
total_revenue = df['sales'].sum()

m1.metric("Total Orders Tracked", f"{total_orders:,}")
m2.metric("Avg Profit Margin", f"{avg_margin:.2f}%")
m3.metric("Total Units Sold", f"{total_units:,}")
m4.metric("Avg Order Value", f"${avg_sales:.2f}")
m5.metric("Gross Revenue Return", f"${total_revenue/1000000:.2f}M")

st.markdown("<br>", unsafe_allow_html=True)


# 4. MIDDLE VISUAL LAYOUT (3 GRID CHARTS CONFIGURATION)
mid_col1, mid_col2, mid_col3 = st.columns([1, 1.5, 1])

with mid_col1:
    st.markdown('<div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
    st.caption("**Sales Split by Customer Segment**")
    segment_df = df.groupby('segment')['sales'].sum().reset_index()
    fig_donut = px.pie(segment_df, names='segment', values='sales', hole=0.6,
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=255, showlegend=True)
    st.plotly_chart(fig_donut, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

with mid_col2:
    st.markdown('<div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
    st.caption("**Historical Revenue Inflow Trend & Categories Stack**")
    trend_df = df.groupby(['year', 'category'])['sales'].sum().reset_index()
    fig_trend = px.bar(trend_df, x='year', y='sales', color='category', barmode='stack',
                       color_discrete_sequence=['#3182ce', '#63b3ed', '#90cdf4'])
    fig_trend.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=255, template="plotly_white")
    st.plotly_chart(fig_trend, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

with mid_col3:
    st.markdown('<div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
    st.caption("**Top Performing States Growth Engine**")
    state_df = df.groupby('state')['sales'].sum().reset_index().sort_values('sales', ascending=False).head(5)
    fig_state = px.bar(state_df, y='state', x='sales', orientation='h',
                       color_discrete_sequence=['#3182ce'])
    fig_state.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=255, template="plotly_white", yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_state, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# 5. BOTTOM RISK MATRIX LAYER (4 DEEP-DIVE CHARTS)
bot_col1, bot_col2, bot_col3, bot_col4 = st.columns(4)

with bot_col1:
    st.markdown('<div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
    st.caption("**Volume Clusters vs Value Return**")
    qty_df = df.groupby('quantity')['sales'].sum().reset_index()
    fig_qty = px.bar(qty_df, x='quantity', y='sales', color_discrete_sequence=['#3182ce'])
    fig_qty.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=200, template="plotly_white")
    st.plotly_chart(fig_qty, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

with bot_col2:
    st.markdown('<div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
    st.caption("**Order Densities across Discount Tiers**")
    disc_df = df.groupby('discount')['order_id'].count().reset_index()
    disc_df['discount'] = disc_df['discount'].astype(str)
    fig_disc = px.bar(disc_df, x='discount', y='order_id', color_discrete_sequence=['#4299e1'])
    fig_disc.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=200, template="plotly_white")
    st.plotly_chart(fig_disc, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

with bot_col3:
    st.markdown('<div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
    st.caption("**Revenue Return by Product Sub-Category**")
    sub_df = df.groupby('sub_category')['sales'].sum().reset_index().sort_values('sales', ascending=False).head(6)
    fig_sub = px.bar(sub_df, y='sub_category', x='sales', orientation='h', color_discrete_sequence=['#63b3ed'])
    fig_sub.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=200, template="plotly_white", yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_sub, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)

with bot_col4:
    st.markdown('<div style="background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">', unsafe_allow_html=True)
    st.caption("**Regional Contribution and Segment Leakage**")
    reg_df = df.groupby(['region', 'segment'])['sales'].sum().reset_index()
    fig_reg = px.bar(reg_df, x='region', y='sales', color='segment', barmode='stack',
                      color_discrete_sequence=['#2b6cb0', '#4299e1', '#bee3f8'])
    fig_reg.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=200, template="plotly_white")
    st.plotly_chart(fig_reg, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)