import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

def show():
    st.title("🏭 Real-Time Fermentation Command Center")
    st.markdown("### Monitor & Kontrol Produksi Pupuk Organik Premium")
    
    # --- Sidebar Controls ---
    with st.sidebar:
        st.header("⚙️ Parameter Kontrol")
        input_waste_kg = st.number_input("Input Sampah Organik (kg)", min_value=100, step=50, value=1000)
        target_temp = st.slider("Target Suhu Inti (°C)", 40, 80, 60)
        target_moisture = st.slider("Target Kelembaban (%)", 30, 70, 50)
        batch_id = st.selectbox("Batch ID", ["BATCH-2026-001", "BATCH-2026-002", "BATCH-2026-003"])
        st.button("🔄 Refresh Data Sensor")

    # --- 1. KPI Scorecard ---
    st.subheader("📊 KPI Scorecard (Live)")
    
    # Mock Data for KPIs
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin:0">Quality Score</h4>
            <h1 style="color:#2E7d32; margin:0">94.5</h1>
            <p style="color:green">▲ 2.1% vs Target</p>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi2:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin:0">Batch Progress</h4>
            <h1 style="color:#F9A825; margin:0">Day 12</h1>
            <p style="color:grey">dari 21 Hari</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin:0">C/N Ratio</h4>
            <h1 style="color:#1565C0; margin:0">22:1</h1>
            <p style="color:green">✅ Ideal Range</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
         estimated_yield = input_waste_kg * 0.6 # Approx 40% mass reduction due to moisture loss/co2
         st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0">Estimasi Output</h4>
            <h1 style="color:#424242; margin:0">{estimated_yield:,.0f} kg</h1>
            <p>ASAL: {input_waste_kg} kg Sampah</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # --- 2. Live Monitor (Gauges) ---
    st.subheader("🌡️ Sensor Monitor (Real-Time)")
    
    g1, g2, g3 = st.columns(3)
    
    with g1:
        # Temperature Gauge
        fig_temp = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = target_temp + np.random.uniform(-2, 2), # Simulate reading
            delta = {'reference': 60},
            title = {'text': "Suhu Inti (°C)"},
            gauge = {
                'axis': {'range': [None, 90]},
                'bar': {'color': "#d32f2f"},
                'steps': [
                    {'range': [0, 50], 'color': "#FFEBEE"},
                    {'range': [50, 70], 'color': "#C8E6C9"}, # Ideal
                    {'range': [70, 90], 'color': "#FFEBEE"}],
                'threshold': {'line': {'color': "green", 'width': 4}, 'thickness': 0.75, 'value': target_temp}
            }))
        st.plotly_chart(fig_temp, use_container_width=True)

    with g2:
        # Moisture Gauge
        fig_moist = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = target_moisture + np.random.uniform(-5, 5),
            delta = {'reference': 50},
            title = {'text': "Kelembaban (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#0288D1"},
                'steps': [
                   {'range': [0, 40], 'color': "#E3F2FD"},
                   {'range': [40, 60], 'color': "#E1F5FE"}, # Ideal
                   {'range': [60, 100], 'color': "#E3F2FD"}],
                'threshold': {'line': {'color': "blue", 'width': 4}, 'thickness': 0.75, 'value': target_moisture}
            }))
        st.plotly_chart(fig_moist, use_container_width=True)

    with g3:
        # Oxygen/Aeration Gauge (Simulated)
        fig_o2 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = np.random.uniform(10, 15),
            title = {'text': "Kadar Oksigen (%)"},
            gauge = {
                'axis': {'range': [0, 21]},
                'bar': {'color': "#7CB342"},
                'steps': [
                   {'range': [0, 5], 'color': "#FFEBEE"}, # Anaerobic danger
                   {'range': [5, 21], 'color': "#F1F8E9"}]
            }))
        st.plotly_chart(fig_o2, use_container_width=True)

    # --- 3. Production Analytics ---
    st.subheader("📈 Production Analytics: Temperature & pH Log")
    
    # Mock Time Series Data
    hours = [datetime.now() - timedelta(hours=x) for x in range(24)]
    hours.reverse()
    
    df_log = pd.DataFrame({
        'Waktu': hours,
        'Suhu (°C)': [60 + np.sin(x/4)*5 + np.random.normal(0, 1) for x in range(24)],
        'pH Tanah': [6.8 + np.cos(x/6)*0.2 + np.random.normal(0, 0.05) for x in range(24)]
    })
    
    c1, c2 = st.columns([2, 1])
    
    with c1:
        fig_trend = px.line(df_log, x='Waktu', y='Suhu (°C)', title="Tren Suhu 24 Jam Terakhir", markers=True)
        fig_trend.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Batas Atas (Patogen Mati)")
        fig_trend.add_hline(y=45, line_dash="dash", line_color="blue", annotation_text="Batas Bawah (Lambat)")
        fig_trend.update_traces(line_color='#d32f2f')
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with c2:
        fig_ph = px.line(df_log, x='Waktu', y='pH Tanah', title="Stabilitas pH", markers=False)
        fig_ph.update_traces(line_color='#1565C0')
        fig_ph.update_yaxes(range=[5, 9])
        st.plotly_chart(fig_ph, use_container_width=True)

    # --- 4. Quality Grading ---
    st.subheader("🏆 Final Quality Grading Prediction")
    
    q1, q2 = st.columns([1, 2])
    
    with q1:
        st.image("https://img.icons8.com/fluency/96/guarantee.png", width=100)
        st.markdown("### GRADE A+")
        st.caption("Premium Organic Fertilizer")
    
    with q2:
        st.write("**Assessment Report:**")
        st.progress(95)
        st.caption("Nutrient Content (95/100)")
        st.progress(90)
        st.caption("Pathogen Free (90/100)")
        st.progress(98)
        st.caption("Maturity / Kematangan (98/100)")
        
    st.success("Sistem mendeteksi proses berjalan optimal. Estimasi panen: 9 Hari lagi.")

