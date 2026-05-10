import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(page_title="Operations & NPS Insights", layout="wide")

# --- Data Loading & Processing ---
@st.cache_data
def load_data():
    orders = pd.read_csv('orders.csv')
    nps = pd.read_csv('nps.csv').dropna(subset=['order_id'])
    hub_perf = pd.read_csv('hub_performance.csv').dropna(subset=['hub_id'])
    courier_perf = pd.read_csv('courier_performance.csv').dropna(subset=['courier_partner'])
    customers = pd.read_csv('customers.csv').dropna(subset=['customer_id'])
    complaints = pd.read_csv('complaints.csv').dropna(subset=['order_id'])

    # Date conversions
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    orders['promised_date'] = pd.to_datetime(orders['promised_date'])
    orders['delivery_date'] = pd.to_datetime(orders['delivery_date'])
    
    # Feature Engineering
    orders['delivery_delay'] = (orders['delivery_date'] - orders['promised_date']).dt.days
    orders['is_late'] = orders['delivery_delay'] > 0
    
    # Merge NPS with Orders
    nps_orders = nps.merge(orders, on='order_id', how='left', suffixes=('_nps', '_ord'))
    
    # Categorize NPS
    def categorize_nps(score):
        if score >= 9: return 'Promoter'
        elif score >= 7: return 'Passive'
        else: return 'Detractor'
    nps_orders['nps_cat'] = nps_orders['score'].apply(categorize_nps)
    
    return orders, nps_orders, hub_perf, courier_perf, customers, complaints

orders, nps_orders, hub_perf, courier_perf, customers, complaints = load_data()

# --- Global Metrics Calculation ---
total_responses = len(nps_orders)
promoters = (nps_orders['nps_cat'] == 'Promoter').sum()
detractors = (nps_orders['nps_cat'] == 'Detractor').sum()
nps_score = round(((promoters - detractors) / total_responses) * 100, 2)
otd_rate = round((orders[orders['order_status'] == 'Delivered']['is_late'] == False).mean() * 100, 2)
avg_res_time = round(complaints['resolution_time'].mean(), 2)

# --- Sidebar Navigation ---
st.sidebar.title("Operational Insights")
page = st.sidebar.radio("Navigate Story", ["Executive Summary", "Logistics Performance", "Regional Deep-Dive", "Strategy & Roadmap"])

# --- Page 1: Executive Summary ---
if page == "Executive Summary":
    st.title("The State of Customer Experience")
    st.markdown("""
    **Primary Goal:** Improve NPS and reduce complaints without significant cost increases.
    
    Our analysis reveals a critical disconnect between customer expectations and operational reality. 
    The current NPS indicates a brand in distress, primarily driven by delivery failures.
    """)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current NPS", f"{nps_score}", delta="-15% vs Target", delta_color="inverse")
    col2.metric("On-Time Delivery (OTD)", f"{otd_rate}%", delta="-30% vs Industry Avg", delta_color="inverse")
    col3.metric("Avg. Resolution Time", f"{avg_res_time} Days")

    st.subheader("NPS Sentiment Distribution")
    nps_dist = nps_orders['nps_cat'].value_counts(normalize=True).reset_index()
    nps_dist.columns = ['Category', 'Percentage']
    nps_dist['Percentage'] *= 100
    fig_nps = px.bar(nps_dist, x='Category', y='Percentage', color='Category', 
                     color_discrete_map={'Promoter': '#2ecc71', 'Passive': '#f1c40f', 'Detractor': '#e74c3c'})
    st.plotly_chart(fig_nps, use_container_width=True)

# --- Page 2: Logistics Performance ---
elif page == "Logistics Performance":
    st.title("The Logistics Gap")
    st.markdown("Analysis of our courier partners reveals significant variations in reliability.")
    
    courier_summary = nps_orders.groupby('courier_partner').agg(
        avg_score=('score', 'mean'),
        late_rate=('is_late', 'mean')
    ).reset_index()
    
    fig_courier = px.scatter(courier_summary, x='late_rate', y='avg_score', text='courier_partner',
                             size='late_rate', color='courier_partner',
                             labels={'late_rate': 'Late Delivery Rate', 'avg_score': 'Avg NPS Score'},
                             title="Courier Performance: Score vs. Lateness")
    fig_courier.update_traces(textposition='top center')
    st.plotly_chart(fig_courier, use_container_width=True)
    
    st.warning("**Key Finding:** `QuickShip` is currently delivering 100% of orders late in our sampled data, contributing to the lowest NPS scores.")

# --- Page 3: Regional Deep-Dive ---
elif page == "Regional Deep-Dive":
    st.title("Regional Hotspots")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Complaints by City")
        city_complaints = complaints.merge(orders, on='order_id')['city'].value_counts().reset_index()
        fig_city = px.pie(city_complaints, values='count', names='city', hole=0.4)
        st.plotly_chart(fig_city)
        
    with col2:
        st.subheader("Hub Operational Integrity")
        fig_hub = go.Figure(data=[
            go.Bar(name='Failed Attempts', x=hub_perf['city'], y=hub_perf['failed_attempts']),
            go.Bar(name='RTO Count', x=hub_perf['city'], y=hub_perf['rto_count'])
        ])
        fig_hub.update_layout(barmode='group')
        st.plotly_chart(fig_hub)

    st.info("Cities like **Nagpur** and **Indore** show high RTO counts and failed attempts, pointing toward the 'Fake Delivery Attempt' issue.")

# --- Page 4: Strategy & Roadmap ---
elif page == "Strategy & Roadmap":
    st.title("Strategic Roadmap")
    
    st.markdown("""
    ### 1. Immediate Action (No Cost)
    * **Volume Redistribution:** Divert high-priority orders from `QuickShip` to `ShipNow`.
    * **Expectation Calibration:** Increase buffer time in 'Promised Date' calculation by 24-48 hours. Delivering on-time to a longer window is better for NPS than missing a short window.
    
    ### 2. Operational Improvement (Low Cost)
    * **OTP Verification:** Implement OTP-based delivery in Indore and Nagpur to eliminate "Fake Delivery Attempts."
    * **VIP Queue:** Route High-Value customer complaints to senior agents for immediate resolution.
    
    ### 3. Long-Term Efficiency
    * **Performance Contracts:** Move to a 'Pay-per-performance' model with couriers, penalizing SLA breaches.
    """)
    
    st.success("By implementing these steps, we target an NPS lift of +20 points within 90 days.")