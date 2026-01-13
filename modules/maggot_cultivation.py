import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def create_gauge(title, value, max_val, suffix=""):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        number = {'suffix': suffix},
        gauge = {
            'axis': {'range': [None, max_val]},
            'bar': {'color': "#795548"}, # Maggot brown color? Or Green
            'steps': [
                {'range': [0, max_val*0.4], 'color': "lightgray"},
                {'range': [max_val*0.4, max_val], 'color': "#D7CCC8"}],
        }
    ))
    fig.update_layout(height=150, margin=dict(l=10, r=10, t=30, b=10))
    return fig

def show():
    st.title("🦗 Bioconversion Center (Maggot BSF)")
    st.markdown("### *Integrated Waste-to-Protein System*")
    st.markdown("Konversi sampah organik menjadi protein tinggi (Pakan Ternak) & pupuk organik (Kasgot) menggunakan *Black Soldier Fly*.")

    # --- Sidebar Controls ---
    with st.sidebar:
        st.header("⚙️ Cultivation Input")
        waste_input_daily = st.number_input("Input Sampah Organik (kg/hari)", min_value=10, value=50, step=10)
        gram_telur = st.number_input("Input Telur BSF (gram)", min_value=1.0, value=5.0, step=1.0)
        
        st.markdown("---")
        st.header("🧮 Pricing Simulation")
        price_fresh = st.number_input("Harga Maggot Segar (Rp/kg)", value=6000)
        price_dried = st.number_input("Harga Maggot Kering (Rp/kg)", value=45000)
        price_kasgot = st.number_input("Harga Kasgot (Rp/kg)", value=1000)

    # --- 1. Growth Cycle Simulation ---
    st.subheader("🔄 Siklus Hidup & FCR Estimation")
    
    col_metrics, col_visual = st.columns([1, 2])
    
    # Bioconversion Parameters
    bioconversion_rate = 0.20 # 20% waste becomes Maggot biomass
    residue_rate = 0.30       # 30% waste becomes Kasgot (Residue)
    reduction_rate = 0.50     # 50% waste reduced (Water loss/Metabolism)
    
    # Calculation
    est_maggot_biomass = waste_input_daily * bioconversion_rate
    est_kasgot = waste_input_daily * residue_rate
    
    # FCR (Feed Conversion Ratio)
    # How much feed needed for 1kg biomass. E.g. 5kg waste -> 1kg maggot = FCR 5.
    fcr = waste_input_daily / est_maggot_biomass if est_maggot_biomass > 0 else 0
    
    with col_metrics:
        st.metric("Waste Reduction Index", f"{reduction_rate*100:.0f}%", "Volume Berkurang")
        st.metric("FCR (Feed Conversion Ratio)", f"{fcr:.1f}", "Target: < 3.0")
        st.metric("Survival Rate (Est)", "85%", "Kepadatan Optimal")

    with col_visual:
        # Sankey Diagram for Mass Balance
        labels = ["Organic Waste Input", "Maggot Biomass", "Kasgot (Fertilizer)", "Water Vapor/Metabolism"]
        source = [0, 0, 0]
        target = [1, 2, 3]
        value = [est_maggot_biomass, est_kasgot, waste_input_daily * reduction_rate]
        
        fig = go.Figure(data=[go.Sankey(
            node = dict(
              pad = 15,
              thickness = 20,
              line = dict(color = "black", width = 0.5),
              label = labels,
              color = ["#2E7d32", "#FF9800", "#795548", "#B0BEC5"]
            ),
            link = dict(
              source = source,
              target = target,
              value = value
            ))])
        fig.update_layout(title_text="Mass Balance (Harian)", height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    
    # --- 2. Production Schedule ---
    st.subheader("📅 Jadwal Panen (Forecast)")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.info("**Fase Penetasan**\n3-4 Hari")
    with c2:
        st.warning("**Fase Biokonversi**\n14-18 Hari (Makan Aktif)")
    with c3:
        st.success("**Panen Maggot**\nHari ke-18 sd 21")
    with c4:
        st.error("**Fase Prepupa**\nStop Makan (Indukan)")
        
    # --- 3. Economic Potential ---
    st.subheader("💰 Potensi Ekonomi (Harian)")
    
    revenue_fresh = est_maggot_biomass * price_fresh
    # Dry maggot usually 30% weight of fresh
    revenue_dry = (est_maggot_biomass * 0.3) * price_dried 
    revenue_kasgot = est_kasgot * price_kasgot
    
    total_rev_fresh_market = revenue_fresh + revenue_kasgot
    total_rev_dry_market = revenue_dry + revenue_kasgot
    
    ce1, ce2 = st.columns(2)
    
    with ce1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Skenario A: Jual Segar (Fresh)</h4>
            <h2>Rp {total_rev_fresh_market:,.0f}</h2>
            <p>Maggot: {est_maggot_biomass:.1f} kg + Kasgot: {est_kasgot:.1f} kg</p>
        </div>
        """, unsafe_allow_html=True)
        
    with ce2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>Skenario B: Jual Kering (Dried)</h4>
            <h2>Rp {total_rev_dry_market:,.0f}</h2>
            <p>Dried Maggot: {(est_maggot_biomass*0.3):.1f} kg + Kasgot: {est_kasgot:.1f} kg</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Rumus: Output Maggot ≈ 20% Input Sampah")
