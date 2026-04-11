import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import numpy as np
from modules.price_service import load_prices

def create_gauge(title, value, min_val, max_val, suffix="", color="green"):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        number = {'suffix': suffix},
        gauge = {
            'axis': {'range': [min_val, max_val]},
            'bar': {'color': color},
            'steps': [
                {'range': [min_val, max_val*0.3], 'color': "lightgray"},
                {'range': [max_val*0.3, max_val*0.7], 'color': "gray"}],
        }
    ))
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=40, b=10))
    return fig

def show():
    st.title("🏭 Plant Upcycling: Plastik ke Filamen 3D")
    st.markdown("Transformasi botol PET menjadi **High-Value 3D Printing Filament** melalui proses manufaktur presisi.")
    
    # Load Prices for Economic Calc
    prices = load_prices()
    pet_price_raw = prices.get("PET_Bottles", {"sell": 5500})['sell']
    filament_price = prices.get("Filament_rPET", {"sell": 150000})['sell']

    # Sidebar Controls
    st.sidebar.markdown("### 🎛️ Parameter Ekstrusi")
    target_temp = st.sidebar.slider("Suhu Ekstruder (°C)", 200, 270, 255)
    motor_speed = st.sidebar.slider("Kecepatan Motor (RPM)", 0, 50, 25)
    input_qty = st.sidebar.number_input("Input Flakes PET (kg)", min_value=0.0, value=1.0, step=0.1)
    
    start_process = st.sidebar.button("▶️ Jalankan Produksi")
    
    # 1. IoT Monitoring Dashboard
    st.subheader("🖥️ IoT Monitoring Dashboard (Live Simulation)")
    
    # Simulated metrics
    current_temp = target_temp + np.random.uniform(-2, 2)
    diameter = 1.75 + np.random.uniform(-0.03, 0.03) # Target 1.75mm
    motor_load = (motor_speed / 50) * 100 + np.random.uniform(-5, 5)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(create_gauge("Suhu Nozzle", current_temp, 0, 300, "°C", "#FF5722"), use_container_width=True)
        st.caption(f"Target: {target_temp}°C")
    with c2:
        color_diam = "#4CAF50" if 1.70 <= diameter <= 1.80 else "#F44336"
        st.plotly_chart(create_gauge("Diameter Filamen", diameter, 1.5, 2.0, " mm", color_diam), use_container_width=True)
        st.caption("Target: 1.75mm ±0.05")
    with c3:
        st.plotly_chart(create_gauge("Motor Load", motor_load, 0, 100, "%", "#2196F3"), use_container_width=True)
        st.caption(f"Speed: {motor_speed} RPM")

    st.markdown("---")

    # 2. Process Flow & OEE
    col_proc, col_eco = st.columns([2, 1])
    
    with col_proc:
        st.subheader("⚙️ Alur Proses Manufaktur")
        
        # Simple Process Steps visualization
        steps = ["Washing", "Drying", "Shredding", "Extrusion", "Cooling", "Spooling"]
        # Simulate active step based on random or state (just static active for now)
        st.info("Status: ✅ System Ready | 🟢 Heater Active | 🟢 Puller Synced")
        
        # OEE Calculation
        # Quality: % of time diameter is within tolerance (simulated 95%)
        # Performance: Actual Speed / Max Speed
        # Availability: Uptime (simulated 98%)
        
        quality = 95.0
        performance = (motor_speed / 50) * 100
        availability = 98.0
        oee = (quality/100) * (performance/100) * (availability/100) * 100
        
        st.markdown(f"### 📊 Overall Equipment Effectiveness (OEE): **{oee:.1f}%**")
        c_oee1, c_oee2, c_oee3 = st.columns(3)
        c_oee1.metric("Availability", f"{availability}%")
        c_oee2.metric("Performance", f"{performance:.0f}%")
        c_oee3.metric("Quality", f"{quality}%")

    with col_eco:
        st.subheader("💰 Nilai Ekonomi")
        
        raw_value = input_qty * pet_price_raw
        # Yield loss during extrusion ~5%
        output_qty = input_qty * 0.95
        filament_value_total = output_qty * filament_price
        
        added_value = filament_value_total - raw_value
        margin_pct = (added_value / raw_value * 100) if raw_value > 0 else 0
        
        st.markdown("""
        <div style="background-color: #e8f5e9; padding: 15px; border-radius: 10px; border: 1px solid #c8e6c9;">
            <h4 style="margin:0; color: #2e7d32; font-size: 0.9rem;">Estimated Uplift</h4>
        </div>
        """, unsafe_allow_html=True)
        
        st.metric("Nilai Bahan Baku (PET)", f"Rp {raw_value:,.0f}", f"{input_qty} kg")
        st.metric("Nilai Produk (Filamen)", f"Rp {filament_value_total:,.0f}", f"{output_qty:.2f} kg")
        st.metric("Value Added", f"Rp {added_value:,.0f}", f"+{margin_pct:,.0f}%")
        
        with st.expander("ℹ️ Analisis Margin"):
            st.write(f"Satu botol PET (~10g) berharga Rp {pet_price_raw/100:,.0f} sebagai sampah.")
            st.write(f"Setelah diubah menjadi filamen, nilainya menjadi Rp {filament_price/100:,.0f}.")
            st.write("**Upcycling menaikkan nilai ekonomi hingga 30x lipat.**")

    if start_process:
        st.toast("🚀 Proses Ekstrusi Dimulai...")
        time.sleep(1)
        st.toast("🌡️ Pemanasan Zona 1-3 Complete")
        time.sleep(1)
        st.toast("✅ Filamen Keluar: Diameter Stabil 1.75mm")
        st.balloons()
