import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Inventory Intelligence Hub",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #F0F2F6; }

    /* KPI Cards */
    div[data-testid="metric-container"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 5% 5% 5% 10%;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.08);
    }

    /* Force dark text on KPIs regardless of theme */
    div[data-testid="metric-container"] label,
    div[data-testid="metric-container"] div,
    div[data-testid="metric-container"] p,
    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricValue"] {
        color: #0F172A !important;
    }

    /* Insight Boxes */
    .insight-box {
        background: linear-gradient(135deg, #EFF6FF 0%, #F8FAFF 100%);
        border-left: 5px solid #2563EB;
        padding: 16px 20px;
        border-radius: 6px;
        margin-top: 10px;
        margin-bottom: 20px;
        color: #1E293B;
        font-size: 0.93rem;
        line-height: 1.6;
    }

    /* Warning insight */
    .warning-box {
        background: linear-gradient(135deg, #FFF7ED 0%, #FFFBF5 100%);
        border-left: 5px solid #F97316;
        padding: 16px 20px;
        border-radius: 6px;
        margin-top: 10px;
        margin-bottom: 20px;
        color: #1E293B;
        font-size: 0.93rem;
        line-height: 1.6;
    }

    /* Recommendations Box */
    .rec-box {
        background: linear-gradient(135deg, #F0FDF4 0%, #F8FFFA 100%);
        border-left: 5px solid #16A34A;
        padding: 24px 28px;
        border-radius: 8px;
        margin-top: 20px;
        color: #1E293B;
        line-height: 1.8;
    }

    /* Section headers */
    .section-header {
        font-size: 1.05rem;
        font-weight: 600;
        color: #64748B;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING & CLEANING ───────────────────────────────────────────────────
@st.cache_data
def load_and_clean_data():
    df = pd.read_csv("data/inventory_movements.csv")

    df_clean = df.drop_duplicates(subset='movement_id', keep='first').copy()
    df_clean['movement_date'] = pd.to_datetime(df_clean['movement_date'], errors='coerce')
    df_clean['expected_date'] = pd.to_datetime(df_clean['expected_date'], errors='coerce')

    # Core indicator flags
    df_clean['is_negative_stock'] = df_clean['stock_after'] < 0
    df_clean['is_discrepancy']    = df_clean['status'] == 'Discrepancy'
    df_clean['movement_month']    = df_clean['movement_date'].dt.strftime('%B')
    df_clean['month_num']         = df_clean['movement_date'].dt.month
    df_clean['cost_per_unit']     = df_clean['unit_cost']

    return df_clean

df = load_and_clean_data()


# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4413/4413697.png", width=55)
    st.title("Inventory Filters")
    st.markdown("Drill down into specific warehouses, suppliers, SKUs, or movement types.")
    st.divider()

    sel_warehouse = st.multiselect(
        "Warehouse City",
        options=sorted(df['warehouse_city'].unique()),
        default=sorted(df['warehouse_city'].unique())
    )
    sel_supplier = st.multiselect(
        "Supplier",
        options=sorted(df['supplier_id'].dropna().unique()),
        default=sorted(df['supplier_id'].dropna().unique())
    )
    sel_movement = st.multiselect(
        "Movement Type",
        options=df['movement_type'].unique(),
        default=df['movement_type'].unique()
    )
    sel_sku = st.multiselect(
        "SKU (top 20 shown by default)",
        options=sorted(df['sku_id'].unique()),
        default=sorted(df['sku_id'].unique())[:20]
    )

# ─── APPLY FILTERS ─────────────────────────────────────────────────────────────
filtered = df[
    (df['warehouse_city'].isin(sel_warehouse)) &
    (df['movement_type'].isin(sel_movement)) &
    (df['sku_id'].isin(sel_sku))
]

# Supplier filter applies only to rows that have a supplier_id
filtered_supplier = filtered[
    (filtered['supplier_id'].isna()) | (filtered['supplier_id'].isin(sel_supplier))
]


# ─── HEADER ────────────────────────────────────────────────────────────────────
st.title("📦 Inventory Intelligence Hub")
st.markdown("""
<div style='font-size:1.1rem; color:#475569; margin-bottom:24px;'>
    Executive overview of stock discrepancy rates, supplier cost anomalies, and inventory integrity across all warehouses.
</div>
""", unsafe_allow_html=True)


# ─── KPI CARDS ─────────────────────────────────────────────────────────────────
st.markdown("<p class='section-header'>Executive Summary KPIs</p>", unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns(5)

total_movements   = len(filtered_supplier)
disc_rate         = filtered_supplier['is_discrepancy'].mean() * 100 if total_movements > 0 else 0
neg_stock_count   = filtered_supplier['is_negative_stock'].sum()
avg_unit_cost     = filtered_supplier['unit_cost'].mean() if total_movements > 0 else 0
total_warehouses  = filtered_supplier['warehouse_city'].nunique()

k1.metric("Total Movements",       f"{total_movements:,}")
k2.metric("Discrepancy Rate",      f"{disc_rate:.1f}%")
k3.metric("Negative Stock Events", f"{neg_stock_count:,}")
k4.metric("Avg Unit Cost",         f"₹{avg_unit_cost:,.2f}")
k5.metric("Active Warehouses",     f"{total_warehouses}")

st.markdown("<hr style='border-top:1px solid #E2E8F0; margin:28px 0;'>", unsafe_allow_html=True)


# ─── ROW 1: DISCREPANCY BY WAREHOUSE & MOVEMENT TYPE ──────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.subheader("📍 Stock Discrepancy Rate by Warehouse")
    wh_disc = (filtered_supplier
               .groupby('warehouse_city')['is_discrepancy']
               .mean().mul(100).round(2)
               .reset_index()
               .sort_values('is_discrepancy', ascending=False))

    fig1 = px.bar(
        wh_disc, x='warehouse_city', y='is_discrepancy',
        color='is_discrepancy', color_continuous_scale='Reds',
        text='is_discrepancy',
        labels={'warehouse_city': 'Warehouse', 'is_discrepancy': 'Discrepancy Rate (%)'}
    )
    fig1.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig1.update_layout(
        template='plotly_white', font=dict(color='#1E293B'),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0), coloraxis_showscale=False
    )
    st.plotly_chart(fig1, use_container_width=True, theme=None)
    st.markdown("""
    <div class='insight-box'>
        <strong>💡 Insight:</strong> <strong>Pune</strong> leads with the highest stock discrepancy rate at <strong>11.34%</strong>.
        However, all warehouses are clustered between 8-11%, confirming this is a systemic network-wide issue rather than a single warehouse failure.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.subheader("🔄 Discrepancy Rate by Movement Type")
    mov_disc = (filtered_supplier
                .groupby('movement_type')['is_discrepancy']
                .mean().mul(100).round(2)
                .reset_index()
                .sort_values('is_discrepancy', ascending=False))

    fig2 = px.bar(
        mov_disc, x='movement_type', y='is_discrepancy',
        color='is_discrepancy', color_continuous_scale='Oranges',
        text='is_discrepancy',
        labels={'movement_type': 'Movement Type', 'is_discrepancy': 'Discrepancy Rate (%)'}
    )
    fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig2.update_layout(
        template='plotly_white', font=dict(color='#1E293B'),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0), coloraxis_showscale=False
    )
    st.plotly_chart(fig2, use_container_width=True, theme=None)
    st.markdown("""
    <div class='insight-box'>
        <strong>💡 Insight:</strong> <strong>Adjustments</strong> generate the most discrepancies (11.11%).
        Adjustments are manual overrides of the inventory ledger, meaning staff in multiple warehouses are entering incorrect stock counts manually rather than the system calculating them automatically.
    </div>
    """, unsafe_allow_html=True)


st.markdown("<hr style='border-top:1px solid #E2E8F0; margin:28px 0;'>", unsafe_allow_html=True)


# ─── ROW 2: SUPPLIER COST COMPARISON & SCATTER ────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.subheader("💰 Average Unit Cost by Supplier")
    inbound = filtered_supplier[filtered_supplier['movement_type'] == 'Inbound'].copy()
    supplier_cost = (inbound.groupby('supplier_id')['unit_cost']
                     .mean().round(2).reset_index()
                     .sort_values('unit_cost', ascending=False))
    supplier_cost.columns = ['supplier_id', 'avg_unit_cost']

    fig3 = px.bar(
        supplier_cost, x='supplier_id', y='avg_unit_cost',
        color='avg_unit_cost', color_continuous_scale='Blues',
        text='avg_unit_cost',
        labels={'supplier_id': 'Supplier', 'avg_unit_cost': 'Avg Unit Cost (₹)'}
    )
    fig3.update_traces(texttemplate='₹%{text:,.0f}', textposition='outside')
    fig3.update_layout(
        template='plotly_white', font=dict(color='#1E293B'),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0), coloraxis_showscale=False
    )
    st.plotly_chart(fig3, use_container_width=True, theme=None)
    st.markdown("""
    <div class='warning-box'>
        <strong>🚨 Critical Finding:</strong> <strong>SUP_09</strong> is charging an average of <strong>₹10,559 per unit</strong>,
        which is <strong>10.3x higher</strong> than the team average of ₹1,026. This contract requires an immediate procurement audit and renegotiation.
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.subheader("📊 Unit Cost vs Quantity (Inbound)")
    fig4 = px.scatter(
        inbound, x='quantity', y='unit_cost', color='supplier_id',
        labels={'quantity': 'Quantity Ordered', 'unit_cost': 'Unit Cost (₹)', 'supplier_id': 'Supplier'}
    )
    fig4.update_layout(
        template='plotly_white', font=dict(color='#1E293B'),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig4, use_container_width=True, theme=None)
    st.markdown("""
    <div class='insight-box'>
        <strong>💡 Insight:</strong> All other suppliers show predictable, flat unit costs regardless of quantity.
        SUP_09's data points float aggressively above all others across all quantity levels,
        confirming their overpricing is not volume-based — it appears to be a systemic billing issue.
    </div>
    """, unsafe_allow_html=True)


st.markdown("<hr style='border-top:1px solid #E2E8F0; margin:28px 0;'>", unsafe_allow_html=True)


# ─── ROW 3: NEGATIVE STOCK ANALYSIS ───────────────────────────────────────────
c5, c6 = st.columns(2)

with c5:
    st.subheader("⚠️ Top SKUs with Negative Stock Events")
    neg_df = filtered_supplier[filtered_supplier['is_negative_stock'] == True]
    top_neg_skus = (neg_df['sku_id'].value_counts().head(10)
                    .reset_index())
    top_neg_skus.columns = ['sku_id', 'occurrences']

    fig5 = px.bar(
        top_neg_skus, x='sku_id', y='occurrences',
        color='occurrences', color_continuous_scale='Purples',
        text='occurrences',
        labels={'sku_id': 'SKU', 'occurrences': 'Negative Stock Events'}
    )
    fig5.update_traces(textposition='outside')
    fig5.update_layout(
        template='plotly_white', font=dict(color='#1E293B'),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0), coloraxis_showscale=False
    )
    st.plotly_chart(fig5, use_container_width=True, theme=None)
    st.markdown("""
    <div class='warning-box'>
        <strong>🚨 Critical Finding:</strong> <strong>SKU_0172</strong> has the highest occurrence of going into negative stock (4 events).
        Root cause analysis shows the WMS (Warehouse Management System) is dispatching this SKU even when stock_before &lt; quantity being shipped,
        and in some cases the subtraction math is corrupted entirely.
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.subheader("🔴 Negative Stock by Warehouse")
    neg_by_wh = (neg_df.groupby('warehouse_city').size()
                 .reset_index(name='negative_events')
                 .sort_values('negative_events', ascending=False))

    fig6 = px.bar(
        neg_by_wh, x='warehouse_city', y='negative_events',
        color='negative_events', color_continuous_scale='Reds',
        text='negative_events',
        labels={'warehouse_city': 'Warehouse', 'negative_events': 'Negative Stock Events'}
    )
    fig6.update_traces(textposition='outside')
    fig6.update_layout(
        template='plotly_white', font=dict(color='#1E293B'),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0), coloraxis_showscale=False
    )
    st.plotly_chart(fig6, use_container_width=True, theme=None)
    st.markdown("""
    <div class='insight-box'>
        <strong>💡 Insight:</strong> Negative stock events are distributed across all warehouses (Hyderabad leads slightly with 43 events).
        The even distribution across all cities confirms this is a <strong>system-wide ERP bug</strong>,
        not a warehouse-specific operational failure.
    </div>
    """, unsafe_allow_html=True)


st.markdown("<hr style='border-top:1px solid #E2E8F0; margin:28px 0;'>", unsafe_allow_html=True)


# ─── ROW 4: MOVEMENT BREAKDOWN & MONTHLY TREND ────────────────────────────────
c7, c8 = st.columns(2)

with c7:
    st.subheader("📋 Inventory Status Distribution")
    status_dist = filtered_supplier['status'].value_counts().reset_index()
    status_dist.columns = ['status', 'count']

    fig7 = px.pie(
        status_dist, values='count', names='status', hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig7.update_layout(
        template='plotly_white', font=dict(color='#1E293B'),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig7, use_container_width=True, theme=None)
    st.markdown("""
    <div class='insight-box'>
        <strong>💡 Insight:</strong> While ~78% of movements are "Completed", a notable 9.4% are flagged as "Discrepancy".
        Additionally, 545 "Completed" transactions have a missing <code>stock_after</code> value,
        meaning the system confirmed the movement but failed to update the inventory ledger.
    </div>
    """, unsafe_allow_html=True)

with c8:
    st.subheader("📅 Monthly Inventory Movement Volume")
    monthly = (filtered_supplier
               .groupby(['month_num', 'movement_month']).size()
               .reset_index(name='movement_count')
               .sort_values('month_num'))

    fig8 = px.line(
        monthly, x='movement_month', y='movement_count',
        markers=True,
        labels={'movement_month': 'Month', 'movement_count': 'Number of Movements'}
    )
    fig8.update_traces(line_color='#2563EB', marker_color='#1D4ED8', line_width=2.5)
    fig8.update_layout(
        template='plotly_white', font=dict(color='#1E293B'),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=30, b=0)
    )
    st.plotly_chart(fig8, use_container_width=True, theme=None)
    st.markdown("""
    <div class='insight-box'>
        <strong>💡 Insight:</strong> Inventory movement volumes remain fairly consistent month-over-month,
        with no dramatic seasonal spike. This rules out seasonal demand as a driver of discrepancies.
    </div>
    """, unsafe_allow_html=True)


# ─── RECOMMENDATIONS ──────────────────────────────────────────────────────────
st.markdown("<hr style='border-top:1px solid #E2E8F0; margin:28px 0;'>", unsafe_allow_html=True)
st.header("📋 Strategic Recommendations")
st.markdown("""
<div class='rec-box'>
    <h4>1. 🔴 Urgent: WMS Hard-Block for Negative Dispatches</h4>
    <p>The ERP system is physically permitting dispatch orders where <code>quantity > stock_before</code>.
    IT must implement a hard validation block at the point of dispatch. No transaction should be allowed to proceed
    unless <code>quantity ≤ stock_before</code>. This alone will eliminate phantom inventory dispatches.</p>

    <h4>2. 🔴 Urgent: Supplier Contract Audit for SUP_09</h4>
    <p>SUP_09 is billing at ₹10,559 per unit on average — 10.3x more than the market average of ₹1,026.
    This cannot be a cost-of-goods difference alone. The procurement team must audit every invoice from SUP_09 going back 6 months
    and immediately renegotiate or terminate their contract.</p>

    <h4>3. 🟡 Operational: Replace Manual Adjustments with Cycle Counts</h4>
    <p>Adjustments are the worst-performing movement type for discrepancies (11.11%).
    Manual adjustments are a symptom of poor physical inventory discipline.
    Replace ad-hoc manual adjustments with weekly structured cycle counts, especially in <strong>Pune</strong> and <strong>Bengaluru</strong>.</p>

    <h4>4. 📊 Monitoring: Weekly Adjustment Spike Dashboard</h4>
    <p>Track the <strong>weekly count of manual adjustments per warehouse</strong> as the primary leading indicator.
    A sudden spike in adjustments at any warehouse signals that the physical inbound/outbound process has broken down that week,
    enabling managers to intervene before end-of-month write-offs occur.</p>
</div>
""", unsafe_allow_html=True)
