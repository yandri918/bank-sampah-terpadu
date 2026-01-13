import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.title("Dashboard Sirkular Ekonomi")
    st.markdown("Monitoring Ekosistem Bank Sampah")

    # Mock Data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card"><h3>Total Sampah</h3><h2>1,250 kg</h2><p>Bulan Ini</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>Emas Hijau (Organik)</h3><h2>850 kg</h2><p>Terproses jadi Kompos</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>Material Presisi</h3><h2>400 kg</h2><p>Plastik & Logam</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>Estimasi Nilai</h3><h2>Rp 4.5 Juta</h2><p>Potensi Ekonomi</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Charts
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Komposisi Sampah (Japanese Standard)")
        data = pd.DataFrame({
            'Kategori': ['Moeru Gomi (Burnable)', 'Moenai Gomi (Non-burnable)', 'Shigen Gomi (Recyclable)', 'Sodai Gomi (Large)'],
            'Berat (kg)': [600, 150, 450, 50]
        })
        fig = px.pie(data, values='Berat (kg)', names='Kategori', color_discrete_sequence=px.colors.sequential.Greens_r, hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
        
    with c2:
        st.subheader("Tren Pengumpulan Harian")
        dates = pd.date_range(start='2026-01-01', periods=7)
        trend_data = pd.DataFrame({
            'Tanggal': dates,
            'Berat (kg)': [45, 52, 48, 60, 55, 70, 65]
        })
        fig2 = px.line(trend_data, x='Tanggal', y='Berat (kg)', markers=True, line_shape='spline')
        fig2.update_traces(line_color='#2E7d32')
        st.plotly_chart(fig2, use_container_width=True)
