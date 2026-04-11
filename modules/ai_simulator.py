import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from modules.price_service import load_prices

def show():
    st.title("🤖 AI Strategic Simulator")
    st.markdown("### *Dynamic Operational Blueprint*")
    st.markdown("Simulasi kebutuhan operasional berbasis target finansial (Reverse Engineering Strategy).")

    # --- 1. Strategic Inputs (Sidebar) ---
    st.sidebar.header("🎯 Financial Targets")
    target_revenue_juta = st.sidebar.number_input("Target Omzet (Juta Rp/Bulan)", min_value=1, value=50, step=5)
    target_revenue = target_revenue_juta * 1_000_000
    
    st.sidebar.header("⚙️ Operational Parameters")
    days_per_month = st.sidebar.slider("Hari Kerja/Bulan", 20, 30, 26)
    partner_capacity = st.sidebar.slider("Avg Setoran Mitra (kg/hari)", 10, 100, 20)
    pickup_capacity = st.sidebar.slider("Kapasitas Pickup (kg/trip)", 100, 1000, 300)
    
    # --- 2. AI Calculation Engine ---
    
    # A. Calculate Weighted Average Sell Price (Estimated Mix)
    # Assumption: 60% Organic (Low Value), 40% Inorganic (High Value)
    prices = load_prices()
    
    # Get representative prices
    p_organic = prices.get("Burnable", {"sell": 300})['sell'] # Compost/Feed
    p_plastic = prices.get("PET_Bottles", {"sell": 5500})['sell'] 
    p_paper = prices.get("Paper", {"sell": 3000})['sell']
    p_metal = prices.get("Metal_Small", {"sell": 4500})['sell']
    
    # Simple weighted avg for simulation (can be refined with real data later)
    # Mix: 50% Organic, 20% Plastic, 20% Paper, 10% Metal
    avg_price_per_kg = (0.5 * p_organic) + (0.2 * p_plastic) + (0.2 * p_paper) + (0.1 * p_metal)
    
    # B. Reverse Engineer Volume
    required_revenue_daily = target_revenue / days_per_month
    required_volume_daily = required_revenue_daily / avg_price_per_kg
    required_volume_monthly = required_volume_daily * days_per_month
    
    # C. Logistics Load
    required_partners = np.ceil(required_volume_daily / partner_capacity)
    required_pickups = np.ceil(required_volume_daily / pickup_capacity)
    
    # D. Energy & Carbon
    # Energy: ~0.05 kWh/kg for sorting/shredding machines
    energy_factor = 0.05 
    daily_energy = required_volume_daily * energy_factor
    
    # Carbon Offset: ~2.5 kgCO2e saved per kg recycled (vs landfill)
    carbon_factor = 2.5
    daily_carbon = required_volume_daily * carbon_factor

    # --- 3. High-Fidelity Blueprint Display ---
    
    st.markdown("---")
    
    # Top Level Strategy
    st.subheader(f"Blueprint untuk Target: Rp {target_revenue_juta} Juta/Bulan")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Raw Material</h3>
            <h2>{required_volume_daily:,.0f} kg/day</h2>
            <p>Input Stream (Mix)</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Logistics Load</h3>
            <h2>{int(required_partners)} Partners</h2>
            <p>{int(required_pickups)} Pickups/Day</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Energy Load</h3>
            <h2>{daily_energy:.1f} kWh</h2>
            <p>Daily Machine Usage</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>Net Carbon Offset</h3>
            <h2 style="color:var(--primary-color)">{daily_carbon:,.1f} kg</h2>
            <p>CO2e Avoided</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Detailed Analysis
    c_chart, c_text = st.columns([2,1])
    
    with c_chart:
        st.subheader("📈 Proyeksi Pertumbuhan")
        # Generate dummy projection curve
        days = list(range(1, 31))
        cumulative_rev = [required_revenue_daily * d / 1_000_000 for d in days]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=cumulative_rev, mode='lines+markers', name='Revenue (M)', line=dict(color='#2E7d32', width=3)))
        fig.add_trace(go.Scatter(x=days, y=[target_revenue_juta]*30, mode='lines', name='Target', line=dict(dash='dash', color='gray')))
        fig.update_layout(title="Revenue Accrual (Daily)", xaxis_title="Hari ke-", yaxis_title="Juta Rupiah", height=300)
        st.plotly_chart(fig, use_container_width=True)

    with c_text:
        st.subheader("📋 Executive Summary")
        st.info(f"""
        **Strategi Pencapaian:**
        Untuk mencapai omzet **Rp {target_revenue_juta} Juta**, fasilitas harus mengolah rata-rata **{required_volume_daily/1000:.1f} Ton sampah per hari**.
        
        **Kebutuhan Sumber Daya:**
        1. **SDM**: Membutuhkan jaringan minimal **{int(required_partners)} mitra aktif** (Bank Sampah Unit/Pengepul).
        2. **Logistik**: Armada harus siap melakukan **{int(required_pickups)} rit** penjemputan kapasitas {pickup_capacity}kg.
        3. **Operasional**: Biaya listrik estimasi untuk mesin pencacah/press sekitar **{(daily_energy*1500):,.0f} IDR/hari**.
        """)
        
    st.success("💡 **Recommendation:** Fokus pada akuisisi mitra baru untuk memenuhi kuota volume harian.")
