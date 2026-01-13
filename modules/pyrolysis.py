import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

def show():
    st.title("🛢️ Waste-to-Energy: Pyrolysis Center")
    st.markdown("### *Chemical Recycling Facility*")
    st.markdown("Konversi sampah plastik residu (Low Value) menjadi Bahan Bakar Minyak Sintetis (Synthetic Fuel).")

    # --- Sidebar Controls ---
    with st.sidebar:
        st.header("⚙️ Reactor Control")
        input_plastic_kg = st.number_input("Input Plastik Residu (kg)", min_value=50, step=50, value=100)
        
        st.subheader("🔥 Parameter Proses")
        target_temp = st.slider("Target Suhu Reaktor (°C)", 300, 500, 400, step=10, help="Optimal: 380-420°C untuk Solar")
        heating_rate = st.select_slider("Laju Pemanasan", options=["Lambat", "Sedang", "Cepat"], value="Sedang")
        
        st.markdown("---")
        st.header("⛽ Harga Pasar")
        price_oil = st.number_input("Harga Minyak Bakar (Rp/Liter)", value=12000)
        price_char = st.number_input("Harga Arang/Carbon (Rp/kg)", value=2000)

    # --- 1. Simulation Engine ---
    
    # Yield Logic based on Temp
    # Ideal temp for oil is around 400C.
    # < 350: Low conversion, high wax.
    # > 450: High gas (Syngas), less oil.
    
    efficiency_factor = 1.0
    if target_temp < 350: efficiency_factor = 0.7 # Incomplete cracking
    if target_temp > 450: efficiency_factor = 0.6 # Over-cracking to gas
    
    # Standard Pyrolysis Yields (polyolefins)
    yield_oil_pct = 0.60 * efficiency_factor # 60% Oil
    yield_gas_pct = 0.20 + (0.60 * (1-efficiency_factor)) # Gas increases if efficiency drops (overheat)
    yield_char_pct = 0.20 # Char residue
    
    output_oil_liters = (input_plastic_kg * yield_oil_pct) / 0.85 # Density approx 0.85 kg/L
    output_gas_kg = input_plastic_kg * yield_gas_pct
    output_char_kg = input_plastic_kg * yield_char_pct
    
    # --- 2. Dashboard UI ---
    
    # Top Metrics
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric("Input Feedstock", f"{input_plastic_kg} kg", "Plastik Residu")
    with c2:
        st.metric("Reactor Status", "ACTIVE", f"{target_temp}°C (Set Point)")
    with c3:
        st.metric("Oil Yield (Est)", f"{output_oil_liters:.1f} Liter", f"{(yield_oil_pct*100):.0f}% Konversi")

    st.markdown("---")

    # Process Visualization
    col_vis, col_tank = st.columns([2, 1])
    
    with col_vis:
        st.subheader("🌡️ Reactor Temperature Profile")
        
        # Simulated curve
        timesteps = np.linspace(0, 4, 50) # 4 Hours process
        temp_curve = target_temp * (1 - np.exp(-timesteps)) # Heating curve
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=timesteps, y=temp_curve, mode='lines', name='Actual Temp', fill='tozeroy', line=dict(color='#FF5722')))
        fig.add_hline(y=target_temp, line_dash="dash", annotation_text="Target Setpoint")
        
        fig.update_layout(
            title="Suhu Reaktor (4 Jam Siklus)",
            xaxis_title="Waktu (Jam)",
            yaxis_title="Suhu (°C)",
            height=300
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_tank:
        st.subheader("🛢️ Storage Tank")
        
        # Tank Level Animation
        tank_fill =  min(100, (output_oil_liters / 200) * 100) # Assume 200L Drum
        
        fig_tank = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = output_oil_liters,
            title = {'text': "Level Minyak (Liter)"},
            gauge = {
                'axis': {'range': [0, 200]},
                'bar': {'color': "#FBC02D"}, # Oil color
                'shape': "bullet",
            }
        ))
        fig_tank.update_layout(height=250)
        st.plotly_chart(fig_tank, use_container_width=True)

    # --- 3. Fractionation Results ---
    st.subheader("⚗️ Hasil Distilasi Fraksinasi")
    
    f1, f2, f3 = st.columns(3)
    
    with f1:
        st.info("⛽ **Fraksi Minyak (BBM)**")
        st.markdown(f"**{output_oil_liters:.1f} Liter**")
        st.caption("Setara Solar/Minyak Tanah. Bisa untuk mesin diesel statis atau kompor.")
        
    with f2:
        st.warning("💨 **Syngas (Non-Condensable)**")
        st.markdown(f"**{output_gas_kg:.1f} kg** (Equivalent)")
        st.caption("Gas Methane/Ethane. Dialirkan kembali untuk memanaskan reaktor (Self-powering).")
        
    with f3:
        st.success("⚫ **Carbon Char (Arang)**")
        st.markdown(f"**{output_char_kg:.1f} kg**")
        st.caption("Residu padat karbon hitam. Bisa dipress menjadi Briket Arang.")

    # --- 4. Economic Value ---
    st.markdown("---")
    st.subheader("💰 Nilai Ekonomi")
    
    revenue_oil = output_oil_liters * price_oil
    revenue_char = output_char_kg * price_char
    total_revenue = revenue_oil + revenue_char
    
    # Approximate Cost: LPG/Wood for heating (if external) or Electricity
    # Assume Rp 2000 per kg plastic input for operational cost
    op_cost = input_plastic_kg * 2000
    profit = total_revenue - op_cost
    
    e1, e2, e3 = st.columns(3)
    
    with e1:
        st.metric("Total Revenue", f"Rp {total_revenue:,.0f}", "Dari Minyak & Arang")
    with e2:
        st.metric("Operational Cost", f"Rp {op_cost:,.0f}", "Estimasi Energi & SDM")
    with e3:
        roi = (profit / op_cost) * 100 if op_cost > 0 else 0
        st.metric("Net Profit", f"Rp {profit:,.0f}", f"ROI: {roi:.1f}%")

    if profit > 0:
        st.balloons()
