import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Veridi Logistics Auditor",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Global Styling
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f1f5f9;
    }

    /* Base Elements Override */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6 {
        color: #f8fafc !important;
    }

    /* Glassmorphism KPI Cards */
    div[data-testid="column"] > div > div > div > div.metric-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        margin-bottom: 24px;
        transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    div[data-testid="column"] > div > div > div > div.metric-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 4px;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        opacity: 0.8;
    }

    div[data-testid="column"] > div > div > div > div.metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.2);
    }

    .metric-title {
        color: #94a3b8;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 38px;
        font-weight: 700;
        line-height: 1.1;
        background: linear-gradient(to right, #fff, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-subtitle {
        color: #fb7185;
        font-size: 13px;
        font-weight: 500;
        margin-top: 6px;
        display: inline-block;
        background: rgba(251, 113, 133, 0.1);
        padding: 2px 8px;
        border-radius: 12px;
    }

    .metric-subtitle.positive {
        color: #34d399;
        background: rgba(52, 211, 153, 0.1);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 0;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        border-radius: 8px 8px 0 0;
        background-color: transparent;
        color: #94a3b8;
        border: none !important;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #f8fafc;
        background: rgba(255, 255, 255, 0.05);
    }
    .stTabs [aria-selected="true"] {
        color: #38bdf8 !important;
        background: rgba(56, 189, 248, 0.1) !important;
        border-bottom: 2px solid #38bdf8 !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #cbd5e1 !important;
    }
    
    /* Headers */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        background: linear-gradient(to right, #38bdf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
    }
    h2 {
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        color: #e2e8f0 !important;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 0.5rem;
        margin-top: 2rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Style Dataframes */
    [data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Expander override */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border-radius: 8px;
    }

</style>
""", unsafe_allow_html=True)

# Helper function to render KPI cards
def render_kpi(title, value, col_obj, subtitle=None, positive=False):
    sub_class = "metric-subtitle positive" if positive else "metric-subtitle"
    subtitle_html = f"<div class='{sub_class}'>{subtitle}</div>" if subtitle else ""
    html = f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
        {subtitle_html}
    </div>
    """
    col_obj.markdown(html, unsafe_allow_html=True)

# Shared Plotly Layout Template
def get_premium_layout(title=""):
    return dict(
        title=dict(text=title, font=dict(family="Outfit", size=20, color="#f8fafc")),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Outfit", color="#cbd5e1"),
        hoverlabel=dict(bgcolor="rgba(15, 23, 42, 0.9)", font=dict(family="Outfit", color="white"), bordercolor="rgba(255,255,255,0.2)"),
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.1)")
    )

# Premium Color Palettes
COLORS = {
    'primary': '#38bdf8',
    'secondary': '#818cf8',
    'accent': '#c084fc',
    'success': '#34d399',
    'warning': '#fbbf24',
    'danger': '#f43f5e',
    'status': {'On Time': '#34d399', 'Late': '#fbbf24', 'Super Late': '#f43f5e'}
}


# Data Loading
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("veridi_master_clean.csv")
        # Ensure correct data types
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
        df['order_estimated_delivery_date'] = pd.to_datetime(df['order_estimated_delivery_date'])
        df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("⚠️ Dataset not found! Please run `veridi_logistics.ipynb` first to generate `veridi_master_clean.csv`.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.markdown("<h2 style='text-align: center; margin-top: 0;'>Veridi Logistics Filters</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# State Filter
all_states = sorted(df['customer_state'].unique().tolist())
selected_states = st.sidebar.multiselect("📍 Customer State", options=all_states, default=all_states)

# Delivery Status Filter
all_statuses = sorted(df['delivery_status'].unique().tolist())
selected_statuses = st.sidebar.multiselect("🚚 Delivery Status", options=all_statuses, default=all_statuses)

# Category Filter
df_clean_cats = df.dropna(subset=['product_category_en'])
all_categories = sorted(df_clean_cats['product_category_en'].unique().tolist())
selected_categories = st.sidebar.multiselect("📦 Product Category", options=all_categories, default=all_categories[:20])

# Apply filters
filtered_df = df[
    (df['customer_state'].isin(selected_states)) &
    (df['delivery_status'].isin(selected_statuses)) &
    (df['product_category_en'].isin(selected_categories))
]

filtered_df['is_late'] = filtered_df['delivery_status'].isin(['Late', 'Super Late']).astype(int)

if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust your selection.")
    st.stop()

# --- KPI METRICS ---
st.title("Last Mile Logistics Auditor")
st.markdown("<p style='color: #94a3b8; font-size: 1.1rem; margin-bottom: 2rem;'>Monitor delivery performance, geographic delays, and customer sentiment with precision.</p>", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

total_orders = len(filtered_df)
late_orders = len(filtered_df[filtered_df['delivery_status'] == 'Late'])
super_late_orders = len(filtered_df[filtered_df['delivery_status'] == 'Super Late'])
pct_late = (late_orders / total_orders) * 100 if total_orders > 0 else 0
pct_super_late = (super_late_orders / total_orders) * 100 if total_orders > 0 else 0
avg_review = filtered_df['review_score'].mean()

late_df_only = filtered_df[filtered_df['days_difference'] > 0]
avg_days_late = late_df_only['days_difference'].mean() if not late_df_only.empty else 0

render_kpi("Total Volume", f"{total_orders:,}", col1, subtitle="Processed Orders", positive=True)
render_kpi("Delayed", f"{pct_late:.1f}%", col2, subtitle="1-5 days past ETA")
render_kpi("Critical Delay", f"{pct_super_late:.1f}%", col3, subtitle=">5 days past ETA")

review_pos = True if avg_review >= 4.0 else False
render_kpi("Sentiment", f"{avg_review:.2f}", col4, subtitle="Avg Out of 5.0", positive=review_pos)
render_kpi("Severity", f"{avg_days_late:.1f}", col5, subtitle="Avg Days Late")


# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "🗺️ Geographic", 
    "⭐ Sentiment", 
    "🏷️ Categories", 
    "📈 Trends"
])

# TAB 1: OVERVIEW
with tab1:
    st.header("Overall Delivery Performance")
    c1, c2 = st.columns(2)
    
    with c1:
        # Pie chart of delivery status
        status_counts = filtered_df['delivery_status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig_pie = px.pie(status_counts, values='Count', names='Status', 
                         color='Status', 
                         color_discrete_map=COLORS['status'],
                         hole=0.6,
                         custom_data=['Status'])
        fig_pie.update_traces(textposition='inside', textinfo='percent+label', 
                              hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}<extra></extra>",
                              marker=dict(line=dict(color='#0f172a', width=2)))
        fig_pie.update_layout(**get_premium_layout("Status Distribution"), showlegend=False)
        # Add center text
        fig_pie.add_annotation(text=f"{total_orders:,}<br>Orders", x=0.5, y=0.5, showarrow=False, 
                               font=dict(size=24, color="#f8fafc", family="Outfit"))
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})
        
    with c2:
        # Histogram of delay distribution
        fig_hist = px.histogram(filtered_df, x='days_difference', 
                                nbins=50, 
                                range_x=[-20, 20],
                                color_discrete_sequence=[COLORS['primary']])
        fig_hist.update_traces(marker=dict(line=dict(color='#0f172a', width=1)), opacity=0.85)
        fig_hist.add_vline(x=0, line_dash="dash", line_color=COLORS['danger'], line_width=2,
                           annotation_text="Expected Delivery", annotation_position="top right",
                           annotation_font=dict(color=COLORS['danger']))
        layout = get_premium_layout("Delivery Timing Spread")
        layout['xaxis'].update(title="Days Difference (Positive = Late)")
        layout['yaxis'].update(title="Order Count")
        fig_hist.update_layout(**layout)
        st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})
        
    # Bar chart of avg delay per review score
    st.markdown("<br>", unsafe_allow_html=True)
    avg_delay_score = filtered_df.groupby('review_score')['days_difference'].mean().reset_index()
    fig_bar1 = px.bar(avg_delay_score, x='review_score', y='days_difference',
                      color='review_score', color_continuous_scale="Viridis", text_auto=".1f")
    
    fig_bar1.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False,
                           marker=dict(line=dict(color='#0f172a', width=1)))
    layout = get_premium_layout("Average Delay by Review Score")
    layout['coloraxis_showscale'] = False
    layout['xaxis'].update(title="Review Score", tickmode='linear')
    layout['yaxis'].update(title="Avg Days Difference")
    fig_bar1.update_layout(**layout)
    st.plotly_chart(fig_bar1, use_container_width=True, config={'displayModeBar': False})

# TAB 2: GEOGRAPHIC
with tab2:
    st.header("Geographic Delay Analysis")
    
    # Calculate late rate by state
    state_perf = filtered_df.groupby('customer_state').agg(
        late_rate=('is_late', 'mean'),
        total_orders=('order_id', 'count')
    ).reset_index()
    state_perf['late_rate'] *= 100
    state_perf = state_perf.sort_values('late_rate', ascending=True)
    
    national_avg = filtered_df['is_late'].mean() * 100
    
    c1, c2 = st.columns([2, 1])
    with c1:
        fig_state = px.bar(state_perf, x='late_rate', y='customer_state', orientation='h',
                           color='late_rate', color_continuous_scale="Reds")
        
        fig_state.update_traces(marker=dict(line=dict(color='#0f172a', width=1)))
        fig_state.add_vline(x=national_avg, line_dash="dash", line_color=COLORS['primary'], line_width=2,
                            annotation_text=f"Natl Avg: {national_avg:.1f}%", annotation_position="top right",
                            annotation_font=dict(color=COLORS['primary']))
        
        layout = get_premium_layout("Late Order Rate by State")
        layout['height'] = 600
        layout['xaxis'].update(title="% Late Orders")
        layout['yaxis'].update(title="")
        fig_state.update_layout(**layout)
        fig_state.update_layout(coloraxis_colorbar_title="% Late")
        st.plotly_chart(fig_state, use_container_width=True, config={'displayModeBar': False})
        
    with c2:
        st.markdown("<p style='font-size: 1.2rem; font-weight: 600; color: #e2e8f0; margin-bottom: 1rem;'>State Data Matrix</p>", unsafe_allow_html=True)
        # Format the dataframe nicely
        styled_df = state_perf.sort_values('late_rate', ascending=False).rename(
            columns={'customer_state': 'State', 'late_rate': 'Late Rate (%)', 'total_orders': 'Volume'}
        )
        st.dataframe(styled_df.style.format({'Late Rate (%)': '{:.1f}%', 'Volume': '{:,}'})
                     .background_gradient(cmap='Reds', subset=['Late Rate (%)']), 
                     use_container_width=True, height=550, hide_index=True)

# TAB 3: SENTIMENT
with tab3:
    st.header("Customer Experience Correlates")

    c1, c2 = st.columns(2)
    with c1:
        # Bar chart of avg score by status
        status_score = filtered_df.groupby('delivery_status')['review_score'].mean().reset_index()
        status_order = ['On Time', 'Late', 'Super Late']
        status_score['delivery_status'] = pd.Categorical(status_score['delivery_status'], categories=status_order, ordered=True)
        status_score = status_score.sort_values('delivery_status')
        
        fig_score_bar = px.bar(status_score, x='delivery_status', y='review_score', text_auto=".2f",
                               color='delivery_status',
                               color_discrete_map=COLORS['status'])
                               
        fig_score_bar.update_traces(textfont_size=16, textangle=0, textposition="inside",
                                    marker=dict(line=dict(color='#0f172a', width=1)))
        
        layout = get_premium_layout("Avg Review Score by Outcome")
        layout['yaxis'].update(range=[1, 5], title="Review Score")
        layout['xaxis'].update(title="")
        layout['showlegend'] = False
        fig_score_bar.update_layout(**layout)
        st.plotly_chart(fig_score_bar, use_container_width=True, config={'displayModeBar': False})
        
    with c2:
        # Heatmap
        heatmap_data = pd.crosstab(filtered_df['delivery_status'], filtered_df['review_score'], normalize='index') * 100
        heatmap_data = heatmap_data.reindex(['On Time', 'Late', 'Super Late'])
        
        fig_heat = px.imshow(heatmap_data, 
                             x=heatmap_data.columns, y=heatmap_data.index,
                             color_continuous_scale="Purples", text_auto=".1f")
                             
        layout = get_premium_layout("Score Distribution by Outcome (%)")
        layout['xaxis'].update(title="Review Score", tickmode='linear')
        layout['yaxis'].update(title="")
        fig_heat.update_layout(**layout)
        fig_heat.update_layout(coloraxis_colorbar_title="%")
        st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})
        
    # Line chart of delay vs score
    st.markdown("<br>", unsafe_allow_html=True)
    df_filtered = filtered_df[(filtered_df['days_difference'] >= -20) & (filtered_df['days_difference'] <= 20)].copy()
    df_filtered['days_bin'] = pd.cut(df_filtered['days_difference'], bins=range(-20, 23, 2), right=False)
    binned_scores = df_filtered.groupby('days_bin', observed=True)['review_score'].mean().reset_index()
    binned_scores['days_mid'] = binned_scores['days_bin'].apply(lambda x: x.mid).astype(float)

    fig_line = px.line(binned_scores, x='days_mid', y='review_score', markers=True)

    fig_line.update_traces(line=dict(color=COLORS['accent'], width=4), 
                           marker=dict(size=10, color=COLORS['primary'], line=dict(color='white', width=2)))
                           
    fig_line.add_vline(x=0, line_dash="dash", line_color=COLORS['danger'], line_width=2,
                       annotation_text="Expected Delivery", annotation_position="bottom right",
                       annotation_font=dict(color=COLORS['danger']))
                       
    layout = get_premium_layout("Sentiment Decay Curve")
    layout['xaxis'].update(title="Days Difference (Positive = Late)")
    layout['yaxis'].update(title="Avg Review Score", range=[1, 5])
    fig_line.update_layout(**layout)
    st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})

    # TAB 4: CATEGORIES
with tab4:
    st.header("Category Vulnerability Matrix")
    st.markdown("<p style='color: #94a3b8; margin-bottom: 2rem;'>Identify product lines most susceptible to logistical bottlenecks.</p>", unsafe_allow_html=True)

    top_n = st.slider("Scope Size (Top N Categories)", min_value=5, max_value=50, value=15, step=5)

    cat_perf = filtered_df.dropna(subset=['product_category_en']).groupby('product_category_en').agg(
        late_rate=('is_late', 'mean'),
        total_orders=('order_id', 'count')
    ).reset_index()

    cat_perf = cat_perf[cat_perf['total_orders'] >= 20]
    cat_perf['late_rate'] *= 100

    top_cats = cat_perf.sort_values('late_rate', ascending=False).head(top_n).sort_values('late_rate', ascending=True)

    fig_cats = px.bar(top_cats, x='late_rate', y='product_category_en', orientation='h',
                      color='late_rate', color_continuous_scale="Sunsetdark", text_auto=".1f")
                      
    fig_cats.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False,
                           marker=dict(line=dict(color='#0f172a', width=1)))
                           
    layout = get_premium_layout(f"Top {top_n} Vulnerable Categories (Min 20 orders)")
    layout['height'] = max(500, top_n * 35)
    layout['xaxis'].update(title="Late Rate (%)")
    layout['yaxis'].update(title="")
    fig_cats.update_layout(**layout)
    fig_cats.update_layout(coloraxis_colorbar_title="% Late")
    st.plotly_chart(fig_cats, use_container_width=True, config={'displayModeBar': False})

    # TAB 5: TRENDS
with tab5:
    st.header("Temporal Convergence")
    st.markdown("<p style='color: #94a3b8; margin-bottom: 2rem;'>Candidate's Choice: Visualizing the inverse relationship between lateness and sentiment over time.</p>", unsafe_allow_html=True)
    
    monthly_trends = filtered_df.dropna(subset=['purchase_month']).groupby('purchase_month').agg(
        late_rate=('is_late', 'mean'),
        avg_score=('review_score', 'mean'),
        order_count=('order_id', 'count')
    ).reset_index()
    
    monthly_trends['late_rate'] *= 100
    monthly_trends = monthly_trends[monthly_trends['order_count'] > 50].sort_values('purchase_month')
    
    from plotly.subplots import make_subplots
    
    fig_trends = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_trends.add_trace(
        go.Bar(x=monthly_trends['purchase_month'], y=monthly_trends['late_rate'], 
               name="% Late Rate", marker_color='rgba(244, 63, 94, 0.6)', 
               marker=dict(line=dict(color='#f43f5e', width=2))),
        secondary_y=False,
    )
    
    fig_trends.add_trace(
        go.Scatter(x=monthly_trends['purchase_month'], y=monthly_trends['avg_score'], 
                   name="Avg Review Score", mode='lines+markers', 
                   line=dict(color='#38bdf8', width=4),
                   marker=dict(size=12, color='#0f172a', line=dict(color='#38bdf8', width=2))),
        secondary_y=True,
    )
    
    layout = get_premium_layout()
    layout['hovermode'] = "x unified"
    layout['legend'] = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    
    fig_trends.update_layout(**layout)
    fig_trends.update_xaxes(title_text="", gridcolor="rgba(255,255,255,0.05)")
    fig_trends.update_yaxes(title_text="Late Rate (%)", secondary_y=False, gridcolor="rgba(255,255,255,0.05)")
    fig_trends.update_yaxes(title_text="Avg Review Score", secondary_y=True, range=[1, 5], showgrid=False)
    
    st.plotly_chart(fig_trends, use_container_width=True, config={'displayModeBar': False})
    
    with st.expander("Explore Raw Temporal Data"):
        styled_trends = monthly_trends.rename(columns={'purchase_month': 'Month', 'late_rate': 'Late Rate (%)', 'avg_score': 'Avg Score', 'order_count': 'Volume'})
        st.dataframe(styled_trends.style.format({'Late Rate (%)': '{:.1f}%', 'Avg Score': '{:.2f}', 'Volume': '{:,}'}), 
                     use_container_width=True, hide_index=True)
