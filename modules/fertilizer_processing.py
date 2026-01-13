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
        
        st.subheader("🗓️ Waktu Produksi")
        start_date = st.date_input("Tanggal Mulai", datetime.now() - timedelta(days=12))
        start_time = st.time_input("Jam Mulai", datetime.now().time())
        
        st.button("🔄 Refresh Data Sensor")

    # --- 0. Biological Management ---
    with st.expander("🧬 Manajemen Biologi & Agen Hayati (Bio-Activator)", expanded=False):
        st.markdown("Integrasi Bioaktivator dari Laboratorium Pupuk Organik untuk akselerasi dekomposisi.")
        
        bio_data = {
            "Agen Hayati": ["ROTAN (Ramuan Organik)", "Trichoderma sp.", "Molase / Gula Baru", "Asam Humat"],
            "Fungsi Utama": ["Probiotik Sempurna (Selulolitik & Penambat N)", "Antifungi (Perlindungan Akar)", "Sumber Energi Mikroba (Karbon)", "Pembenah Tanah & Khelasi Nutrisi"],
            "Dosis": ["10-20ml / Liter air", "50gr / m3 sampah", "100ml / 10L air", "2gr / Liter kocor"]
        }
        st.table(pd.DataFrame(bio_data))

    # --- Logic: Calculate Real-Time metrics based on Inputs ---
    start_datetime = datetime.combine(start_date, start_time)
    current_time = datetime.now()
    delta = current_time - start_datetime
    days_running = delta.days
    hours_running = delta.seconds // 3600
    total_days_target = 21 # 3 Weeks Fermentation Standard
    
    # 1. Batch Progress
    progress_pct = min(100, max(0, (days_running / total_days_target) * 100))
    progress_label = f"Day {days_running}" if days_running >= 0 else "Pending"
    
    # 2. C/N Ratio Simulation (Decomposes from 30:1 down to ~15:1 usually)
    # y = mx + c -> Start 30, Target 15 at day 21
    cn_start = 30
    cn_current = max(10, cn_start - (days_running * (15/21)))
    cn_display = f"{cn_current:.1f}:1"
    
    # 3. Quality Score Simulation (Increases as it matures, sensitive to temp stability)
    # Base score increases with time, maxing at 98. Add some simulated fluctuation.
    if days_running < 0:
        quality_score = 0
    else:
        base_quality = 50 + (progress_pct * 0.45) # Max ~95 from progress
        live_fluctuation = np.random.uniform(-0.5, 1.5) # Sensor noise
        quality_score = min(99.9, base_quality + live_fluctuation)
        
    quality_delta = np.random.uniform(-0.5, 0.8) # Week over week change

    # --- 1. KPI Scorecard ---
    st.subheader("📊 KPI Scorecard (Live Calculation)")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0">Quality Score</h4>
            <h1 style="color:#2E7d32; margin:0">{quality_score:.1f}</h1>
            <p style="color:green">{'▲' if quality_delta > 0 else '▼'} {abs(quality_delta):.1f}% vs Target</p>
        </div>
        """, unsafe_allow_html=True)
        
    with kpi2:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0">Batch Progress</h4>
            <h1 style="color:#F9A825; margin:0">{progress_label}</h1>
            <p style="color:grey">dari {total_days_target} Hari ({int(progress_pct)}%)</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi3:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0">C/N Ratio</h4>
            <h1 style="color:#1565C0; margin:0">{cn_display}</h1>
            <p style="color:green">✅ Ideal Range</p>
            <p style="font-size:0.8em; color:grey; margin-top:5px;">Progres: Turun dari {cn_start}:1 (Hari 0)</p>
        </div>
        """, unsafe_allow_html=True)

    with kpi4:
         estimated_yield = input_waste_kg * 0.4 # Yield 40% (1000kg -> 400kg)
         polybag_count = int(estimated_yield / 0.1) # 100gr per polybag
         st.markdown(f"""
        <div class="metric-card">
            <h4 style="margin:0">Estimasi Output</h4>
            <h1 style="color:#424242; margin:0">{estimated_yield:,.0f} kg</h1>
            <p>Supply: <strong>{polybag_count}</strong> Polybag</p>
        </div>
        """, unsafe_allow_html=True)
         
    st.markdown("---")
    
    # --- 1.5 Nursery Application Recommendations ---
    st.info(f"""
    **📝 Rekomendasi Dosis Aplikasi Nursery (Output: {estimated_yield:,.0f} kg):**
    - **Media Semai:** Campur 1 bagian pupuk : 3 bagian tanah (Top Soil).
    - **Polybag (Bibit):** 50-100gr per pohon, frekuensi 2 minggu sekali. (Cukup untuk {polybag_count} bibit/aplikasi)
    - **Pupuk Cair (POC):** Fermentasi 1kg hasil olahan + 10L air (Dosis 1:10 kocor).
    """)

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
    
    # Mock Time Series Data based on INPUT DATE
    # start_datetime already defined above
    # current_time already defined above
    
    # Generate hourly data points from start to now (capped at last 50 points to keep chart clean if long duration)
    total_hours = int((current_time - start_datetime).total_seconds() / 3600)
    if total_hours < 1: total_hours = 1
    
    # Create time range
    display_hours = min(total_hours, 168) # Show max last 7 days (168 hours) or total duration
    time_range = [current_time - timedelta(hours=x) for x in range(display_hours)]
    time_range.reverse()
    
    # Generate synthetic trend based on fermentation stage (Day 1-3 Rising, Day 4-15 Stable High, Day 15+ Cooling)
    temps = []
    phs = []
    
    for t in time_range:
        elapsed_days = (t - start_datetime).days
        noise = np.random.normal(0, 0.5)
        
        # Temp Logic
        if elapsed_days < 3: temp_val = 30 + (elapsed_days * 10) + noise # Rising phase
        elif elapsed_days < 15: temp_val = 60 + np.sin(t.hour/4)*2 + noise # Thermophilic phase
        else: temp_val = 45 - (elapsed_days - 15) + noise # Cooling phase
        temps.append(temp_val)
        
        # pH Logic
        if elapsed_days < 5: ph_val = 6.0 - (elapsed_days * 0.1) + (noise*0.1) # Acidic start
        else: ph_val = 6.5 + min((elapsed_days-5)*0.1, 1.0) + (noise*0.1) # Stabilizing to neutral
        phs.append(ph_val)

    df_log = pd.DataFrame({
        'Waktu': time_range,
        'Suhu (°C)': temps,
        'pH Tanah': phs
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
        fig_ph.update_yaxes(range=[4, 9])
        st.plotly_chart(fig_ph, use_container_width=True)

    # --- 3.5 Related Info (Logs) ---
    with st.expander("📝 Log Catatan & Informasi Terkait", expanded=True):
        st.markdown(f"**Batch Start:** {start_datetime.strftime('%d %B %Y %H:%M')}")
        st.info("ℹ️ Fase Saat Ini: **Termofilik (Suhu Tinggi)** - Membunuh patogen & biji gulma.")
        
        st.table(pd.DataFrame({
            "Tanggal": [(current_time - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(3)],
            "Aktivitas": ["Pengecekan Rutin", "Pembalikan Tumpukan", "Inokulasi Aktivator Awal"],
            "Operator": ["Budi", "Siti", "Budi"],
            "Catatan": ["Suhu aman", "Kelembaban turun (siram air)", "Start proses"]
        }))

    # --- 4. Quality Grading ---
    # --- 4. Quality Grading & Lab Simulation ---
    st.subheader("📊 Analisis Kandungan Hara (NPK Lab Simulation)")
    st.markdown("Hasil simulasi uji laboratorium berdasarkan standarisasi **SNI 19-7030-2004** untuk kompos berkualitas.")
    
    c_lab1, c_lab2 = st.columns([1, 2])
    
    with c_lab1:
        st.success("**🔬 Kesimpulan Lab**")
        st.metric("C/N Ratio", "12.5", "Matang Sempurna")
        st.caption("Kompos sudah MATANG SEMPURNA dan aman untuk media tanam nursery.")
        
        st.warning("**Note:** Kandungan Nitrogen (2.65%) di atas standar SNI menandakan bahan baku sisa dapur Anda kaya akan protein, sangat baik untuk fase vegetatif sayuran.")
        
    with c_lab2:
        lab_data = {
            "Grup": ["Primer", "Primer", "Primer", "Sekunder", "Sekunder", "Sekunder", "Mikro", "Mikro", "Mikro", "Lainnya"],
            "Parameter": ["Nitrogen (N)", "Phosphate (P)", "Kalium (K)", "Kalsium (Ca)", "Magnesium (Mg)", "Sulfur (S)", "Besi (Fe)", "Mangan (Mn)", "Seng (Zn)", "C/N Ratio"],
            "Hasil (%)": [2.65, 1.95, 2.30, 1.10, 0.45, 0.35, 0.05, 0.02, 0.015, 12.50],
            "SNI Min (%)": [2.00, 1.50, 1.50, 0.80, 0.30, 0.25, 0.03, 0.01, 0.01, 20.00],
            "Fungsi Saintifik": [
                "Pembentukan Klorofil & Vegetatif", "Perkembangan Akar & Pembungaan", "Transportasi Nutrisi & Imun",
                "Dinding Sel & Aktivasi Enzim", "Inti Klorofil (Fotosintesis)", "Sintesis Protein & Aroma",
                "Transfer Elektron dalam Sel", "Aktivator Metabolisme Nitrogen", "Sintesis Hormon Auksin (Tumbuh)", "Indikator Kematangan Kompos"
            ]
        }
        df_lab = pd.DataFrame(lab_data)
        st.dataframe(df_lab.style.format({"Hasil (%)": "{:.4f}", "SNI Min (%)": "{:.4f}"}))

    # --- 5. Balanced Scorecard ---
    st.markdown("---")
    st.subheader("🏆 Balanced Scorecard: Pupuk Organik Premium")
    st.markdown("Key Performance Indicators untuk menjamin kualitas setara industri.")
    
    # Radar Chart Data
    categories = ['Financial', 'Process Efficiency', 'Quality Compliance', 'Environmental Impact']
    r_values = [75, 95, 88, 60] # Mock scores out of 100
    
    col_radar1, col_radar2 = st.columns([1, 2])
    
    with col_radar1:
        # Radar Chart
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=r_values,
            theta=categories,
            fill='toself',
            line_color='#2E7d32'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.caption("Overall Performance Radar")

    with col_radar2:
        # Perspectives Details
        tab_fin, tab_proc, tab_qual, tab_env = st.tabs(["💰 Financial", "⚙️ Process", "🔬 Quality", "🌍 Environmental"])
        
        with tab_fin:
            f1, f2, f3 = st.columns(3)
            with f1: st.metric("Revenue TARGET", "Rp 18.0M", "Dari Sidebar")
            with f2: st.metric("Revenue AKTUAL", "Rp 0.0M", "0% (WIP)")
            with f3: st.metric("ROI Target", "63.9%", "Proyeksi")
            
            st.markdown("""
            - **Biaya/kg**: Rp 104 (Hemat)
            - **Margin/kg**: Rp 2,396 (Profit Tinggi)
            """)

        with tab_proc:
            p1, p2 = st.columns(2)
            with p1: st.metric("Cycle Time", "21 Hari", "Standar") # Adjusted to input logic
            with p2: st.metric("Rendemen", "40%", "Efisiensi Massa")
            st.metric("Throughput", f"{input_waste_kg/21:.1f} kg/hari", "Rata-rata Harian")

        with tab_qual:
            q1, q2 = st.columns(2)
            with q1: st.metric("NPK Score", "95%", "vs Target")
            with q2: st.metric("Defect Rate", "2.5%", "-0.5% (Good)")
            st.metric("SNI Compliance", "75%", "SNI 19-7030 (On Track)")

        with tab_env:
            e1, e2 = st.columns(2)
            with e1: st.metric("Carbon Offset", "0 kg", "CO2e")
            with e2: st.metric("Methane Avoided", "0 kg", "CH4")
            st.metric("Landfill Saved", "0.0 m³", "Volume Sampah")

    st.success(f"Sistem mendeteksi proses berjalan optimal. Estimasi panen: {max(0, 21 - days_running)} Hari lagi.")

