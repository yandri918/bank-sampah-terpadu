import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.title("Dashboard Sirkular Ekonomi")
    st.markdown("Monitoring Ekosistem Bank Sampah")

    import os
    from modules import auth_db

    # Load Real Data if available
    # Filter by Current Logged In User
    current_user_name = st.session_state.get('user_info', {}).get('name')
    df = auth_db.get_all_transactions(petugas_filter=current_user_name)
    
    if not df.empty:
        # df['Tanggal'] already handled by get_all_transactions or needs to be ensured as datetime
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
        
        # Calculate Metrics
        total_organic = df['Burnable'].sum() # Burnable is largely organic/compostable
        
        # Precision Materials (Recyclables)
        recyclable_cols = ['Paper', 'Cloth', 'Cans', 'Electronics', 'PET_Bottles', 'Plastic_Marks', 'White_Trays', 'Glass_Bottles', 'Metal_Small', 'Hazardous']
        total_precision = df[recyclable_cols].sum().sum()
        
        total_waste = total_organic + total_precision
        
        total_waste = total_organic + total_precision
        
        # Financial Metrics: Dynamic Valuation (Live Market Prices)
        from modules.price_service import load_prices
        prices_config = load_prices()
        
        # Calculate Current Inventory Value based on LATEST Sell Prices (Market-to-Market)
        current_market_value = 0
        for category, rates in prices_config.items():
            if category in df.columns:
                current_market_value += df[category].sum() * rates['sell']
        
        # Cost is Historical (Cash Out)
        if 'Total_Bayar_Nasabah' in df.columns:
            total_cost = df['Total_Bayar_Nasabah'].sum()
        else:
            total_cost = 0 # Assume 0 if legacy data
            
        total_revenue = current_market_value
        total_profit = total_revenue - total_cost
        
        # Display Financial Dashboard
        st.subheader("💰 Financial Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'<div class="metric-card"><h3>Total Sampah</h3><h2>{total_waste:,.1f} kg</h2><p>Real-time Accumulation</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><h3>Revenue (Bank)</h3><h2>Rp {total_revenue:,.0f}</h2><p>Potensi Jual ke Industri</p></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><h3>Cost (Nasabah)</h3><h2>Rp {total_cost:,.0f}</h2><p>Uang Keluar</p></div>', unsafe_allow_html=True)
        with col4:
            margin_pct = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
            st.markdown(f'<div class="metric-card"><h3>Net Profit</h3><h2 style="color:#2E7d32">Rp {total_profit:,.0f}</h2><p>Margin: {margin_pct:.1f}%</p></div>', unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Charts using Real Data
        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Komposisi Sampah (Live)")
            # Sum each column for composition
            comp_data = df[['Burnable'] + recyclable_cols].sum().reset_index()
            comp_data.columns = ['Kategori', 'Berat (kg)']
            comp_data = comp_data[comp_data['Berat (kg)'] > 0] # Hide zeros
            
            if not comp_data.empty:
                fig = px.pie(comp_data, values='Berat (kg)', names='Kategori', color_discrete_sequence=px.colors.sequential.Greens_r, hole=0.4)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Belum ada data komposisi.")

        with c2:
            st.subheader("Tren Pengumpulan Harian")
            daily_trend = df.groupby('Tanggal')[['Burnable'] + recyclable_cols].sum().sum(axis=1).reset_index()
            daily_trend.columns = ['Tanggal', 'Berat (kg)']
            
            if not daily_trend.empty:
                fig2 = px.line(daily_trend, x='Tanggal', y='Berat (kg)', markers=True, line_shape='spline')
                fig2.update_traces(line_color='#2E7d32')
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("Belum ada data tren harian.")

    else:
        st.info("⚠️ Belum ada data transaksi tersimpan. Silakan input data di menu 'Input Sampah'.")
        # Show Zeros
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.markdown('<div class="metric-card"><h3>Total Sampah</h3><h2>0 kg</h2></div>', unsafe_allow_html=True)
        with col2: st.markdown('<div class="metric-card"><h3>Emas Hijau</h3><h2>0 kg</h2></div>', unsafe_allow_html=True)
        with col3: st.markdown('<div class="metric-card"><h3>Material Presisi</h3><h2>0 kg</h2></div>', unsafe_allow_html=True)
        with col4: st.markdown('<div class="metric-card"><h3>Estimasi Nilai</h3><h2>Rp 0</h2></div>', unsafe_allow_html=True)
