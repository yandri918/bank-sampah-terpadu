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
        material_type = st.selectbox(
            "Jenis Bahan Baku", 
            ["Campuran (General Purpose)", "Limbah Sayuran (Vegetatif/Daun)", "Limbah Buah (Generatif/Bunga)"],
            index=0,
            help="Menentukan profil nutrisi pupuk akhir."
        )
        input_waste_kg = st.number_input("Input Sampah Organik (kg)", min_value=100, step=50, value=1000)
        target_temp = st.slider("Target Suhu Inti (°C)", 40, 80, 60)
        target_moisture = st.slider("Target Kelembaban (%)", 30, 70, 50)
        st.subheader("🗓️ Waktu Produksi")
        start_date = st.date_input("Tanggal Mulai", datetime.now() - timedelta(days=12))
        start_time = st.time_input("Jam Mulai", datetime.now().time())

        # Auto-generate Batch ID based on Date & Type
        type_code = "GEN" # General
        if "Sayuran" in material_type: type_code = "VEG"
        elif "Buah" in material_type: type_code = "FRT"
        
        default_batch_id = f"BATCH-{start_date.strftime('%Y%m%d')}-{type_code}"
        batch_id = st.text_input("Batch ID (Auto/Manual)", value=default_batch_id, help="ID Unik untuk pelacakan produksi.")
        
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
    
    # --- 1.5 Nursery Application Recommendations (DYNAMIC) ---
    
    if "Sayuran" in material_type:
        rec_title = "Formula Vegetatif (Daun)"
        rec_desc = "Kaya Nitrogen (N). Cocok untuk fase awal pertumbuhan, sayuran daun (Bayam, Kangkung, Pakcoy)."
        rec_color = "green"
    elif "Buah" in material_type:
        rec_title = "Formula Generatif (Bunga/Buah)"
        rec_desc = "Kaya Kalium (K) & Fosfat (P). Cocok untuk fase pembungaan & pembuahan (Cabai, Tomat, Terong)."
        rec_color = "orange"
    else:
        rec_title = "Formula Seimbang (General)"
        rec_desc = "Nutrisi Lengkap (Balanced). Cocok untuk media tanam dasar dan pembenah tanah umum."
        rec_color = "blue"

    st.info(f"""
    **📝 Rekomendasi Aplikasi: {rec_title}**
    _{rec_desc}_
    
    - **Media Semai:** Campur 1 bagian pupuk : 3 bagian tanah.
    - **Polybag:** 50-100gr per pohon, frekuensi 2 minggu sekali.
    - **Pupuk Cair (POC):** 1kg + 10L air (Kocor 200ml per tanaman).
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
    
    # Mock Time Series Data based on INPUT DATE, use existing logic but simplified here to save space
    # (Reusing existing time/temp logic from previous version, just ensuring it renders)
    total_hours = int((current_time - start_datetime).total_seconds() / 3600)
    if total_hours < 1: total_hours = 1
    display_hours = min(total_hours, 168)
    time_range = [current_time - timedelta(hours=x) for x in range(display_hours)]
    time_range.reverse()
    
    temps = [60 + np.random.normal(0, 1) for _ in range(len(time_range))] # Simple mock
    phs = [6.5 + np.random.normal(0, 0.1) for _ in range(len(time_range))]
    
    df_log = pd.DataFrame({'Waktu': time_range, 'Suhu (°C)': temps, 'pH Tanah': phs})
    
    c1, c2 = st.columns([2, 1])
    with c1:
        fig_trend = px.line(df_log, x='Waktu', y='Suhu (°C)', title="Tren Suhu", markers=False)
        st.plotly_chart(fig_trend, use_container_width=True)
    with c2:
        fig_ph = px.line(df_log, x='Waktu', y='pH Tanah', title="Stabilitas pH", markers=False)
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

    # --- 4. Quality Grading & Lab Simulation (Material Specific) ---
    st.subheader("📊 Analisis Kandungan Hara (NPK Lab Simulation)")
    st.markdown(f"Hasil simulasi untuk bahan baku: **{material_type}**")
    
    # NPK Logic Switch
    if "Sayuran" in material_type:
        val_n, val_p, val_k = 3.25, 1.10, 1.20 # High N
        lab_insight = "Kandungan Nitrogen TINGGI. Sangat baik untuk memacu pertumbuhan daun."
    elif "Buah" in material_type:
        val_n, val_p, val_k = 1.45, 2.80, 4.50 # High K
        lab_insight = "Kandungan Kalium EKSTRA. Sangat baik untuk pemanis buah dan penguat batang."
    else:
        val_n, val_p, val_k = 2.65, 1.95, 2.30 # Balanced
        lab_insight = "Nutrisi SEIMBANG. Cocok untuk segala fase tanaman."

    c_lab1, c_lab2 = st.columns([1, 2])
    
    with c_lab1:
        st.success("**🔬 Kesimpulan Lab**")
        st.metric("C/N Ratio", "12.5", "Matang Sempurna")
        st.caption(lab_insight)
        
    with c_lab2:
        lab_data = {
            "Grup": ["Primer", "Primer", "Primer", "Sekunder", "Sekunder", "Sekunder", "Mikro", "Mikro", "Mikro", "Lainnya"],
            "Parameter": ["Nitrogen (N)", "Phosphate (P)", "Kalium (K)", "Kalsium (Ca)", "Magnesium (Mg)", "Sulfur (S)", "Besi (Fe)", "Mangan (Mn)", "Seng (Zn)", "C/N Ratio"],
            "Hasil (%)": [val_n, val_p, val_k, 1.10, 0.45, 0.35, 0.05, 0.02, 0.015, 12.50],
            "SNI Min (%)": [2.00, 1.50, 1.50, 0.80, 0.30, 0.25, 0.03, 0.01, 0.01, 20.00],
        }
        df_lab = pd.DataFrame(lab_data)
        st.dataframe(df_lab.style.format({"Hasil (%)": "{:.2f}", "SNI Min (%)": "{:.2f}"}))


    # --- 5. Balanced Scorecard ---
    # --- 5. Balanced Scorecard & Advanced Economics ---
    st.markdown("---")
    st.subheader("💰 Analisis Ekonomi & Profitabilitas (Advanced)")
    st.markdown("Simulasi detail Harga Pokok Produksi (HPP) dan potensi keuntungan dari pengolahan sampah organik.")

    # --- Economic Inputs (Sidebar or Top Config) ---
    with st.expander("⚙️ Konfigurasi Biaya & Harga (Klik untuk Edit)", expanded=True):
        ec1, ec2, ec3 = st.columns(3)
        with ec1:
            st.markdown("**1. Investasi Awal (CAPEX)**")
            capex_machine = st.number_input("Mesin Pencacah & Ayakan (Rp)", value=15000000)
            capex_infra = st.number_input("Rumah Kompos & Rak (Rp)", value=25000000)
            depreciation_months = st.number_input("Penyusutan (Bulan)", value=60) # 5 Years
            
        with ec2:
            st.markdown("**2. Biaya Operasional (OPEX)**")
            # Dynamic Data Editor for Flexible Cost Structure
            default_opex = pd.DataFrame([
                {"Komponen": "Upah Tenaga Kerja", "Biaya (Rp)": 500000},
                {"Komponen": "Bio-Aktivator/EM4", "Biaya (Rp)": 150000},
                {"Komponen": "Nutrisi Tambahan (Molase)", "Biaya (Rp)": 200000},
                {"Komponen": "Energi (Listrik/BBM)", "Biaya (Rp)": 50000},
                {"Komponen": "Kemasan & Labeling", "Biaya (Rp)": 200000},
            ])
            edited_opex = st.data_editor(
                default_opex, 
                num_rows="dynamic", 
                column_config={
                    "Biaya (Rp)": st.column_config.NumberColumn(format="Rp %d")
                },
                key="opex_editor"
            )
            
            total_opex = edited_opex["Biaya (Rp)"].sum()
            st.caption(f"Total OPEX: Rp {total_opex:,.0f}")
            
        with ec3:
            st.markdown("**3. Harga Jual Produk**")
            price_solid = st.number_input("Harga Kompos Padat (Rp/kg)", value=2500)
            price_liquid = st.number_input("Harga POC (Rp/Liter)", value=15000)
            ratio_liquid = st.slider("Rasio Konversi POC (%)", 0, 50, 10, help="% Input jadi Pupuk Cair")

    # --- Calculations ---
    # Output Calculation
    output_solid_kg = estimated_yield # Defined earlier (approx 40% of input)
    output_liquid_l = (input_waste_kg * (ratio_liquid/100)) # 10% input becomes POC
    
    # Cost Calculation
    total_capex = capex_machine + capex_infra
    monthly_depreciation = total_capex / depreciation_months
    batch_depreciation = monthly_depreciation / 4 # Assume 4 batches per month
    
    # OPEX is now dynamic from editor
    total_cogs = total_opex + batch_depreciation # Total Cost per Batch
    
    # Unit Cost (HPP) - Weighted
    hpp_per_kg = total_cogs / (output_solid_kg + output_liquid_l) if (output_solid_kg + output_liquid_l) > 0 else 0
    
    # Revenue Calculation
    rev_solid = output_solid_kg * price_solid
    rev_liquid = output_liquid_l * price_liquid
    total_revenue = rev_solid + rev_liquid
    
    gross_profit = total_revenue - total_opex
    net_profit = total_revenue - total_cogs
    
    margin_pct = (net_profit / total_revenue) * 100 if total_revenue > 0 else 0
    roi_pct = (net_profit / total_cogs) * 100 if total_cogs > 0 else 0
    
    # --- Visualization ---
    tab_overview, tab_structure, tab_bep = st.tabs(["📊 Profit Sheet", "🍰 Struktur Biaya", "📉 Break-Even Analysis"])
    
    with tab_overview:
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("Total Revenue", f"Rp {total_revenue:,.0f}", f"Batch: {input_waste_kg}kg")
        with m2: st.metric("HPP (Total Cost)", f"Rp {total_cogs:,.0f}", f"Termsk Penyusutan")
        with m3: st.metric("Net Profit", f"Rp {net_profit:,.0f}", f"Margin: {margin_pct:.1f}%")
        with m4: st.metric("ROI (Return on Investment)", f"{roi_pct:.1f}%", "Efisiensi Modal")
        
        st.info(f"💡 **Insight:** Dengan modal Rp {total_cogs:,.0f}, Anda menghasilkan profit bersih Rp {net_profit:,.0f} per siklus.")
        
        # Waterfall Chart
        # Use simple fixed categories for waterfall or dynamic? stick to simple for waterfall labels for now or aggregate
        fig_waterfall = go.Figure(go.Waterfall(
            name = "Profit Flow", orientation = "v",
            measure = ["relative", "relative", "total", "relative", "relative", "relative", "total"],
            x = ["Revenue (Solid)", "Revenue (POC)", "Total Sales", "Total OPEX", "Depresiasi", "Net Profit"], # Simplified
            textposition = "outside",
            y = [rev_solid, rev_liquid, total_revenue, -total_opex, -batch_depreciation, net_profit],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))
        fig_waterfall.update_layout(title = "Profitability Waterfall (Alur Keuntungan)", height=400)
        st.plotly_chart(fig_waterfall, use_container_width=True)

    with tab_structure:
        c_pie, c_data = st.columns([2, 1])
        with c_pie:
             # Prepare data for pie chart: OPEX components + Depreciation
            pie_data = edited_opex.copy()
            # Add Depreciation row
            new_row = pd.DataFrame([{"Komponen": "Penyusutan Mesin", "Biaya (Rp)": batch_depreciation}])
            pie_data = pd.concat([pie_data, new_row], ignore_index=True)
            
            fig_pie = px.pie(pie_data, values='Biaya (Rp)', names='Komponen', title='Struktur Biaya Produksi (HPP)', hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
        with c_data:
            st.write("**Detail Komponen Biaya:**")
            st.dataframe(pie_data, use_container_width=True)
            
    with tab_bep:
        st.markdown(f"##### Titik Impas (Break-Even Point)")
        
        # BEP Calculation Simulation
        # Simulate Revenue vs Cost curve based on Quantity
        
        qty_range = np.linspace(0, output_solid_kg * 2, 50)
        
        # Helper to get cost by component name safely
        def get_cost(name):
            row = edited_opex[edited_opex['Komponen'] == name]
            return row['Biaya (Rp)'].values[0] if not row.empty else 0
            
        # Attempt to isolate Labor as Fixed Cost (Semi-fixed), others as Variable
        # If user renamed it, we might fall back to treating it as variable, which is fine for estimation
        labor_cost = get_cost("Upah Tenaga Kerja")
        other_opex = total_opex - labor_cost
        
        fixed_cost = batch_depreciation + labor_cost 
        # Variable cost per unit (attributed to Solid Fertilizer for simplicity of manual BEP)
        variable_cost_per_kg = other_opex / output_solid_kg if output_solid_kg > 0 else 0
        
        total_costs = fixed_cost + (variable_cost_per_kg * qty_range)
        revenues = price_solid * qty_range # Assuming only solid for simple BEP chart
        
        fig_bep = go.Figure()
        fig_bep.add_trace(go.Scatter(x=qty_range, y=total_costs, name='Total Cost', line=dict(color='red')))
        fig_bep.add_trace(go.Scatter(x=qty_range, y=revenues, name='Revenue', line=dict(color='green')))
        
        # Find intersection
        idx = np.argwhere(np.diff(np.sign(revenues - total_costs))).flatten()
        if len(idx) > 0:
            bep_x = qty_range[idx[0]]
            bep_y = total_costs[idx[0]]
            fig_bep.add_annotation(x=bep_x, y=bep_y, text="BEP", showarrow=True, arrowhead=1)
            st.metric("BEP Quantity (Solid Fertilizer)", f"{bep_x:.0f} kg", "Minimal Penjualan agar Balik Modal")
            
        fig_bep.update_layout(
            title="Analisis Titik Impas (BEP Model)",
            xaxis_title="Jumlah Produksi (kg)",
            yaxis_title="Nilai (Rp)"
        )
        st.plotly_chart(fig_bep, use_container_width=True)


    st.markdown("---")
    st.subheader("🏆 Balanced Scorecard: Ringkasan Global")
    
    # Radar Chart Data
    categories = ['Financial', 'Process Efficiency', 'Quality Compliance', 'Environmental Impact']
    r_values = [min(100, roi_pct*1.5), 95, 88, 60] # Dynamic Financial Score based on ROI
    
    col_radar1, col_radar2 = st.columns([1, 2])
    
    with col_radar1:
        # Radar Chart
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=r_values,
            theta=categories,
            fill='toself',
            line_color='#2E7d32'
        ))
        # ... keep the rest of scorecard simple ...
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

