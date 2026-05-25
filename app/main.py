import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import duckdb
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ── PAGE CONFIG ────────────────────────────────────────────────
st.set_page_config(
    page_title="EcomCo Analyst Co-Pilot",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── DARK THEME CSS ─────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f0f1a; }
    .stApp { background-color: #0f0f1a; }
    .metric-card {
        background: #1a1a2e;
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #2d2d44;
        text-align: center;
    }
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #4fc3f7;
    }
    .metric-label {
        font-size: 13px;
        color: #888;
        margin-top: 4px;
    }
    .metric-delta-good { color: #2ecc71; font-size: 13px; }
    .metric-delta-bad  { color: #e74c3c; font-size: 13px; }
    .anomaly-box {
        background: #2d1a1a;
        border-left: 4px solid #e74c3c;
        border-radius: 6px;
        padding: 12px 16px;
        margin: 8px 0;
    }
    .good-box {
        background: #1a2d1a;
        border-left: 4px solid #2ecc71;
        border-radius: 6px;
        padding: 12px 16px;
        margin: 8px 0;
    }
    .insight-box {
        background: #1a1a2e;
        border-left: 4px solid #4fc3f7;
        border-radius: 6px;
        padding: 16px;
        margin: 12px 0;
        font-size: 15px;
        line-height: 1.7;
        color: #ddd;
    }
    h1, h2, h3 { color: white !important; }
    .stSelectbox label { color: #888 !important; }
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──────────────────────────────────────────────────
@st.cache_data
def load_report():
    return pd.read_csv('outputs/weekly_report.csv')

@st.cache_data
def load_full_metrics():
    con = duckdb.connect('ecom.db')
    df = con.execute("""
        SELECT w.*, t.top_category, t.top_category_revenue
        FROM weekly_metrics w
        LEFT JOIN weekly_top_category t ON w.week_label = t.week_label
        ORDER BY w.week_start
    """).df()
    con.close()
    return df

report = load_report()
metrics = load_full_metrics()

# ── SIDEBAR ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📊 EcomCo Analyst Co-Pilot")
    st.markdown("*LLM-powered weekly business intelligence*")
    st.markdown("---")
    
    page = st.radio(
    "Navigate",
    ["📈 Weekly Dashboard", "🤖 AI Report", "🔍 Anomaly Explorer"],
    label_visibility="collapsed",
    key="navigation"
  )
    
    st.markdown("---")
    st.markdown("**Data Summary**")
    st.markdown(f"-  {metrics['total_orders'].sum():,} total orders")
    st.markdown(f"-  ₹{metrics['total_revenue'].sum()/100000:.1f}L total revenue")
    st.markdown(f"-  {len(metrics)} weeks of data")
    st.markdown(f"-  {report['anomaly_flags'].sum()} anomalies detected")
    st.markdown("---")
    st.markdown("**Tech Stack**")
    st.markdown("dbt · DuckDB · Groq · Llama 3.3 · RAG · Streamlit")

# ── PAGE 1: WEEKLY DASHBOARD ───────────────────────────────────
if page == "📈 Weekly Dashboard":
    st.markdown("# 📈 Weekly Business Dashboard")
    st.markdown("*Full year 2024 — EcomCo e-commerce performance*")
    
    # KPI cards — full year
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{metrics['total_revenue'].sum()/100000:.1f}L</div>
            <div class="metric-label">Total Revenue</div>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{metrics['total_orders'].sum():,}</div>
            <div class="metric-label">Total Orders</div>
        </div>""", unsafe_allow_html=True)
    
    with col3:
        avg_return = metrics['return_rate_pct'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_return:.1f}%</div>
            <div class="metric-label">Avg Return Rate</div>
        </div>""", unsafe_allow_html=True)
    
    with col4:
        avg_aov = metrics['avg_order_value'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{avg_aov:.0f}</div>
            <div class="metric-label">Avg Order Value</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Revenue trend
    fig_rev = go.Figure()
    fig_rev.add_trace(go.Scatter(
        x=metrics['week_label'],
        y=metrics['total_revenue'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#4fc3f7', width=2),
        marker=dict(size=4),
        fill='tozeroy',
        fillcolor='rgba(79, 195, 247, 0.1)'
    ))
    
    # Highlight anomaly weeks
    anomaly_weeks = report[report['anomaly_flags'] == True]['week'].tolist()
    anomaly_data = metrics[metrics['week_label'].isin(anomaly_weeks)]
    
    fig_rev.add_trace(go.Scatter(
        x=anomaly_data['week_label'],
        y=anomaly_data['total_revenue'],
        mode='markers',
        name='⚠️ Anomaly',
        marker=dict(color='#e74c3c', size=10, symbol='x')
    ))
    
    fig_rev.update_layout(
        title='Weekly Revenue — Full Year 2024',
        plot_bgcolor='#1a1a2e',
        paper_bgcolor='#0f0f1a',
        font=dict(color='white'),
        height=350,
        xaxis=dict(showgrid=False, tickangle=45),
        yaxis=dict(showgrid=True, gridcolor='#2d2d44'),
        legend=dict(bgcolor='#1a1a2e'),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    st.plotly_chart(fig_rev, use_container_width=True)
    
    # Return rate + WoW growth side by side
    col1, col2 = st.columns(2)
    
    with col1:
        fig_ret = px.bar(
            metrics,
            x='week_label',
            y='return_rate_pct',
            color='return_rate_pct',
            color_continuous_scale=['#2ecc71', '#e74c3c'],
            title='Weekly Return Rate %'
        )
        fig_ret.add_hline(y=12, line_dash="dash",
                          line_color="#f39c12",
                          annotation_text="12% benchmark")
        fig_ret.update_layout(
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#0f0f1a',
            font=dict(color='white'),
            height=300,
            coloraxis_showscale=False,
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=True, gridcolor='#2d2d44'),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_ret, use_container_width=True)
    
    with col2:
        wow_data = metrics.dropna(subset=['revenue_wow_growth_pct'])
        fig_wow = px.bar(
            wow_data,
            x='week_label',
            y='revenue_wow_growth_pct',
            color='revenue_wow_growth_pct',
            color_continuous_scale=['#e74c3c', '#2ecc71'],
            title='Week-over-Week Revenue Growth %'
        )
        fig_wow.add_hline(y=0, line_color="white", line_width=1)
        fig_wow.update_layout(
            plot_bgcolor='#1a1a2e',
            paper_bgcolor='#0f0f1a',
            font=dict(color='white'),
            height=300,
            coloraxis_showscale=False,
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(showgrid=True, gridcolor='#2d2d44'),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        st.plotly_chart(fig_wow, use_container_width=True)
    
    # Top category breakdown
    st.markdown("### Top Category by Week")
    cat_counts = metrics['top_category'].value_counts().reset_index()
    cat_counts.columns = ['category', 'weeks_as_top']
    
    fig_cat = px.pie(
        cat_counts,
        values='weeks_as_top',
        names='category',
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4
    )
    fig_cat.update_layout(
        plot_bgcolor='#1a1a2e',
        paper_bgcolor='#0f0f1a',
        font=dict(color='white'),
        height=300,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# ── PAGE 2: AI REPORT ──────────────────────────────────────────
elif page == "🤖 AI Report":
    st.markdown("# 🤖 AI-Generated Weekly Report")
    st.markdown("*Groq LLM (Llama 3.3) reads your metrics and writes analyst insights*")
    
    st.markdown("---")
    
    # Week selector
    selected_week = st.selectbox(
        "Select week to view",
        report['week'].tolist(),
        index=len(report)-1
    )
    
    week_data = report[report['week'] == selected_week].iloc[0]
    
    # Metrics for selected week
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">₹{week_data['revenue']/1000:.1f}K</div>
            <div class="metric-label">Revenue</div>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{week_data['orders']}</div>
            <div class="metric-label">Orders</div>
        </div>""", unsafe_allow_html=True)
    
    with col3:
        color = "metric-delta-bad" if week_data['return_rate'] > 12 else "metric-delta-good"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{week_data['return_rate']}%</div>
            <div class="metric-label">Return Rate</div>
            <div class="{color}">{'⚠️ Above benchmark' if week_data['return_rate'] > 12 else '✅ Normal'}</div>
        </div>""", unsafe_allow_html=True)
    
    with col4:
        wow = week_data['wow_growth']
        if pd.notna(wow):
            color = "metric-delta-good" if wow > 0 else "metric-delta-bad"
            arrow = "↑" if wow > 0 else "↓"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{wow:+.1f}%</div>
                <div class="metric-label">WoW Growth</div>
                <div class="{color}">{arrow} vs last week</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">—</div>
                <div class="metric-label">WoW Growth</div>
            </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Anomaly status
    if week_data['anomaly_flags']:
        st.markdown(f"""
        <div class="anomaly-box">
            ⚠️ <strong>Anomaly detected this week</strong> — metrics outside normal thresholds
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="good-box">
            ✅ <strong>No anomalies this week</strong> — all metrics within normal range
        </div>""", unsafe_allow_html=True)
    
    # LLM insight
    st.markdown("### 💡 AI Analyst Insight")
    st.markdown(f"""
    <div class="insight-box">
        {week_data['llm_insight']}
    </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Generate fresh button
    st.markdown("### 🔄 Generate Fresh Insight")
    st.markdown("*Calls Groq API live — takes ~5 seconds*")
    
    if st.button("Generate Fresh Report for This Week"):
        with st.spinner("Groq LLM analyzing metrics..."):
            try:
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                
                with open("rag/context.md", "r") as f:
                    context = f.read()
                
                prompt = f"""You are a senior data analyst at EcomCo.

BUSINESS CONTEXT:
{context}

WEEK: {week_data['week']}
Revenue: ₹{week_data['revenue']:,.0f}
Orders: {week_data['orders']}
Return Rate: {week_data['return_rate']}%
WoW Growth: {week_data['wow_growth']}%
Top Category: {week_data['top_category']}
Anomaly: {week_data['anomaly_flags']}

Write a 3-sentence analyst insight. Be specific, use numbers, sound like a real analyst."""

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                    temperature=0.3
                )
                
                fresh_insight = response.choices[0].message.content.strip()
                st.markdown(f"""
                <div class="insight-box">
                    {fresh_insight}
                </div>""", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"API error: {e}")
    
    st.markdown("---")
    st.markdown("### 📋 All Weeks Summary")
    
    display_df = report[['week', 'revenue', 'orders', 'return_rate', 'wow_growth', 'top_category', 'anomaly_flags']].copy()
    display_df['revenue'] = display_df['revenue'].apply(lambda x: f"₹{x/1000:.1f}K")
    display_df['anomaly_flags'] = display_df['anomaly_flags'].apply(lambda x: "⚠️ Yes" if x else "✅ No")
    display_df.columns = ['Week', 'Revenue', 'Orders', 'Return %', 'WoW %', 'Top Category', 'Anomaly']
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ── PAGE 3: ANOMALY EXPLORER ───────────────────────────────────
elif page == "🔍 Anomaly Explorer":
    st.markdown("# 🔍 Anomaly Explorer")
    st.markdown("*Weeks where metrics crossed critical thresholds*")
    
    anomalies = report[report['anomaly_flags'] == True]
    normal = report[report['anomaly_flags'] == False]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#e74c3c">{len(anomalies)}</div>
            <div class="metric-label">Anomaly Weeks</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#2ecc71">{len(normal)}</div>
            <div class="metric-label">Normal Weeks</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        pct = len(anomalies)/len(report)*100
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value" style="color:#f39c12">{pct:.0f}%</div>
            <div class="metric-label">Anomaly Rate</div>
        </div>""", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚠️ Anomaly Weeks — AI Insights")
    
    for _, row in anomalies.iterrows():
        with st.expander(f"⚠️ {row['week']} — Revenue ₹{row['revenue']/1000:.1f}K | Returns {row['return_rate']}% | WoW {row['wow_growth']:+.1f}%"):
            st.markdown(f"""
            <div class="insight-box">
                {row['llm_insight']}
            </div>""", unsafe_allow_html=True)