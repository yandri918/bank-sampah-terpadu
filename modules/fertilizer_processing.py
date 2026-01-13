import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show():
    st.title("Transformasi: Limbah ke Pupuk Organik Premium")
    st.markdown("### Sistem Pengolahan Terkontrol")
    st.info("Menghasilkan nutrisi berkualitas tinggi yang setara dengan pupuk industri melalui proses fermentasi presisi.")

    # 1. Input Material
    st.subheader("1. Komposisi Bahan Baku (Input)")
    
    col1, col2 = st.columns(2)
    with col1:
        c_organic = st.slider("Kandungan C-Organik (%)", 10.0, 60.0, 45.0)
        nitrogen = st.slider("Kandungan Nitrogen (%)", 0.5, 5.0, 1.5)
        moisture = st.slider("Kelembaban Awal (%)", 20.0, 80.0, 60.0)
    
    with col2:
        st.markdown("**Target Kualitas:**")
        st.write("- C/N Ratio Ideal: 15-25")
        st.write("- Kelembaban Ideal: 40-60%")
        
        cn_ratio = c_organic / nitrogen
        st.metric("C/N Ratio Saat Ini", f"{cn_ratio:.1f}")
        
        if 15 <= cn_ratio <= 25:
            st.success("✅ Rasio C/N Ideal untuk Fermentasi")
        elif cn_ratio < 15:
            st.warning("⚠️ C/N Terlalu Rendah (Tambahkan Serbuk Gergaji/Karbon)")
        else:
            st.warning("⚠️ C/N Terlalu Tinggi (Tambahkan Limbah Hijau/Nitrogen)")

    st.markdown("---")

    # 2. Process Control
    st.subheader("2. Kontrol Proses (Simulasi)")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🦠 Bio-Aktivator")
        activator = st.selectbox("Jenis Aktivator", ["EM4 Pertanian", "Trichoderma sp.", "Lokal (Mols)", "Tanpa Aktivator"])
    with c2:
        st.markdown("#### 🌡️ Suhu Fermentasi")
        temp = st.slider("Suhu Inti (°C)", 30, 80, 60, help="Suhu 55-65°C mematikan patogen.")
    with c3:
        st.markdown("#### ⏳ Durasi")
        duration = st.number_input("Waktu Peraman (Hari)", 7, 60, 21)

    # Simulation Result
    st.markdown("---")
    st.subheader("3. Estimasi Output Produk Premium")
    
    quality_score = 0
    if 55 <= temp <= 70: quality_score += 30
    if 15 <= cn_ratio <= 25: quality_score += 30
    if activator != "Tanpa Aktivator": quality_score += 20
    if 40 <= moisture <= 60: quality_score += 20
    
    # Visual Gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = quality_score,
        title = {'text': "Skor Kualitas Pupuk"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#2E7d32"},
            'steps': [
                {'range': [0, 50], 'color': "#FFEBEE"},
                {'range': [50, 80], 'color': "#E8F5E9"},
                {'range': [80, 100], 'color': "#C8E6C9"}],
            'threshold': {
                'line': {'color': "gold", 'width': 4},
                'thickness': 0.75,
                'value': 90}}))
    
    st.plotly_chart(fig, use_container_width=True)
    
    result_col1, result_col2 = st.columns(2)
    with result_col1:
        if quality_score >= 80:
            st.success(f"🌟 **Grade A (Premium)**: Setara pupuk industri NPK Organik. Cocok untuk hortikultura bernilai tinggi.")
        elif quality_score >= 50:
            st.info(f"🌿 **Grade B (Standar)**: Pupuk kompos matang, baik untuk pembenah tanah dasar.")
        else:
            st.error(f"⚠️ **Grade C (Belum Matang)**: Perlu perbaikan parameter proses.")
            
    with result_col2:
        st.markdown("**Estimasi Kandungan Nutrisi Akhir:**")
        st.json({
            "N (Nitrogen)": f"{nitrogen * 1.2:.1f}% (Terkonsentrasi)",
            "P (Fosfor)": "0.8 - 1.5%",
            "K (Kalium)": "1.0 - 2.0%",
            "C-Organik": f"{c_organic * 0.6:.1f}% (Stabil)"
        })

