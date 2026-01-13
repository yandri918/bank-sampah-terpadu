import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.title("Dashboard Sirkular Ekonomi")
    st.markdown("Monitoring Ekosistem Bank Sampah")

    import os

    # Load Real Data if available
    file_path = "data/waste_data.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        df['Tanggal'] = pd.to_datetime(df['Tanggal'])
        
        # Calculate Metrics
        total_organic = df['Burnable'].sum() # Burnable is largely organic/compostable
        
        # Precision Materials (Recyclables)
        recyclable_cols = ['Paper', 'Cloth', 'Cans', 'Electronics', 'PET_Bottles', 'Plastic_Marks', 'White_Trays', 'Glass_Bottles', 'Metal_Small', 'Hazardous']
        total_precision = df[recyclable_cols].sum().sum()
        
        total_waste = total_organic + total_precision
        
        total_waste = total_organic + total_precision
        
        # Detailed Valuation Logic (Matching transformation.py base prices)
        # Prices defined as per Calculator Standard
        total_waste = total_organic + total_precision
        
        # Financial Metrics from Data (Preferred)
        if 'Est_Profit' in df.columns:
            total_revenue = df['Est_Pendapatan_Bank'].sum()
            total_cost = df['Total_Bayar_Nasabah'].sum()
            total_profit = df['Est_Profit'].sum()
        else:
            # Fallback (Old logic)
            base_prices = {
                'Burnable': 300, 'Paper': 3000, 'Cloth': 1500, 'Cans': 14000,
                'Electronics': 20000, 'PET_Bottles': 5500, 'Plastic_Marks': 2000,
                'White_Trays': 1000, 'Glass_Bottles': 1000, 'Metal_Small': 4500, 'Hazardous': 0
            }
            market_value = 0
            for col, price in base_prices.items():
                if col in df.columns:
                    market_value += df[col].sum() * price
            
            total_revenue = market_value
            total_cost = 0 # Unknown
            total_profit = market_value # Assumed 100% (wrong but safe fallback)
        
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
