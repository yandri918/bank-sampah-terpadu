import streamlit as st
import datetime
import pandas as pd
import os
import base64

from modules.price_service import load_prices

def show():
    # Load Real-Time Configured Prices
    prices_config = load_prices()
    
    # Extract maps for easy lookup
    selling_prices = {k: v['sell'] for k, v in prices_config.items()}
    buying_defaults = {k: v['buy'] for k, v in prices_config.items()}

    st.title("🗑️ Penerimaan Bank Sampah")
    st.markdown("*Input data penimbangan nasabah secara real-time.*")

    with st.container():
        # --- Top Section: Transaction Metadata ---
        c_date, c_cust, c_staff, c_loc = st.columns([1, 2, 2, 2])
        with c_date:
            tanggal_setor = st.date_input("📅 Tanggal", datetime.date.today())
        with c_cust:
            nasabah = st.text_input("👤 Nama Nasabah", placeholder="Contoh: Bu Siti / RT 05")
        with c_staff:
            petugas = st.text_input("👮 Petugas", placeholder="Nama Admin")
        with c_loc:
            lokasi = st.selectbox("📍 Lokasi", ["Unit Pusat", "Unit Satelit 1", "Unit Satelit 2"])

    st.markdown("---")

    # --- Middle Section: Waste Inputs (Organized) ---
    st.subheader("📦 Input Penimbangan")
    
    # Init inputs dictionary to store values
    inputs = {}
    
    with st.form("waste_input_form", clear_on_submit=False):
        # Helper function for cleaner input rows with custom styling
        def input_card(label, key_prefix, default_buy, icon="♻️"):
            st.markdown(f"**{icon} {label}**")
            c_w, c_p = st.columns([1, 1])
            with c_w:
                w = st.number_input("Berat (kg)", min_value=0.0, step=0.1, key=f"w_{key_prefix}", label_visibility="collapsed")
            with c_p:
                p = st.number_input("Harga/kg", value=int(default_buy), step=100, key=f"p_{key_prefix}", label_visibility="collapsed")
            return w, p

        # Layout using Tabs for cleaner interface
        tab1, tab2, tab3 = st.tabs(["🏠 Rumah Tangga & Kertas", "🍾 Plastik & Kemasan", "⚙️ Logam & Elektronik"])
        
        with tab1:
            c1, c2 = st.columns(2)
            with c1:
                w_burn, p_burn = input_card("Residu/Dapur", "Burnable", buying_defaults["Burnable"], "🔥")
                st.markdown("---")
                w_paper, p_paper = input_card("Koran/Kardus", "Paper", buying_defaults["Paper"], "📄")
            with c2:
                w_cloth, p_cloth = input_card("Kain/Pakaian", "Cloth", buying_defaults["Cloth"], "👕")
        
        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                w_pet, p_pet = input_card("Botol PET (Bening)", "PET", buying_defaults["PET_Bottles"], "🍾")
                st.markdown("---")
                w_plas, p_plas = input_card("Plastik Campur", "Plastic", buying_defaults["Plastic_Marks"], "🧴")
            with c2:
                w_tray, p_tray = input_card("Styrofoam/Busa", "Trays", buying_defaults["White_Trays"], "🍽️")
                st.markdown("---")
                w_glass, p_glass = input_card("Botol Kaca", "Glass", buying_defaults["Glass_Bottles"], "🏺")

        with tab3:
            c1, c2 = st.columns(2)
            with c1:
                w_cans, p_cans = input_card("Kaleng Aluminium", "Cans", buying_defaults["Cans"], "🥫")
                st.markdown("---")
                w_metal, p_metal = input_card("Besi/Logam", "Metal", buying_defaults["Metal_Small"], "🏗️")
            with c2:
                w_elec, p_elec = input_card("Elektronik (E-Waste)", "Electronics", buying_defaults["Electronics"], "🔌")
                st.markdown("---")
                w_haz, p_haz = input_card("Limbah B3", "Hazardous", buying_defaults["Hazardous"], "⚠️")

        st.markdown("")
        submit_col1, submit_col2 = st.columns([1, 4])
        with submit_col1:
            submitted = st.form_submit_button("✅ Simpan Transaksi", type="primary", use_container_width=True)

    if submitted:
        if not nasabah:
            st.error("⚠️ Nama Nasabah wajib diisi!")
            return

        # --- 1. Calculation Logic ---
        # Map inputs to variables for easier calc
        total_paid = (w_burn * p_burn) + (w_paper * p_paper) + (w_cloth * p_cloth) + (w_cans * p_cans) + \
                     (w_elec * p_elec) + (w_pet * p_pet) + (w_plas * p_plas) + (w_tray * p_tray) + \
                     (w_glass * p_glass) + (w_metal * p_metal) + (w_haz * p_haz)
        
        total_revenue = (w_burn * selling_prices["Burnable"]) + (w_paper * selling_prices["Paper"]) + \
                        (w_cloth * selling_prices["Cloth"]) + (w_cans * selling_prices["Cans"]) + \
                        (w_elec * selling_prices["Electronics"]) + (w_pet * selling_prices["PET_Bottles"]) + \
                        (w_plas * selling_prices["Plastic_Marks"]) + (w_tray * selling_prices["White_Trays"]) + \
                        (w_glass * selling_prices["Glass_Bottles"]) + (w_metal * selling_prices["Metal_Small"]) + \
                        (w_haz * selling_prices["Hazardous"])

        gross_profit = total_revenue - total_paid
        total_kg = w_burn + w_paper + w_cloth + w_cans + w_elec + w_pet + w_plas + w_tray + w_glass + w_metal + w_haz
        
        # Rounding for cleanliness
        total_kg = round(total_kg, 2)
        total_paid = round(total_paid, 0)
        total_revenue = round(total_revenue, 0)
        gross_profit = round(gross_profit, 0)

        # --- 2. Data Persistence ---
        new_data = {
            "Timestamp": [datetime.datetime.now()],
            "Tanggal": [tanggal_setor],
            "Nasabah": [nasabah],
            "Petugas": [petugas],
            "Lokasi": [lokasi],
            # Weights
            "Burnable": [w_burn], "Paper": [w_paper], "Cloth": [w_cloth], "Cans": [w_cans],
            "Electronics": [w_elec], "PET_Bottles": [w_pet], "Plastic_Marks": [w_plas],
            "White_Trays": [w_tray], "Glass_Bottles": [w_glass], "Metal_Small": [w_metal], "Hazardous": [w_haz],
            # Financials
            "Total_Bayar_Nasabah": [total_paid],
            "Est_Pendapatan_Bank": [total_revenue],
            "Est_Profit": [gross_profit]
        }
        df_new = pd.DataFrame(new_data)
        
        file_path = "data/waste_data.csv"
        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists(file_path):
            df_new.to_csv(file_path, index=False)
        else:
            try:
                df_new.to_csv(file_path, mode='a', header=False, index=False)
            except Exception as e:
                st.error(f"Gagal menyimpan data: {e}")

        # --- 3. Visual Feedback (Financial Dashboard) ---
        st.success("Transaksi Berhasil Disimpan!")
        
        # Styled Metrics using HTML/CSS
        st.markdown("""
        <style>
            .metric-box {
                padding: 15px; border-radius: 10px; text-align: center; color: white;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            .metric-val { font-size: 24px; font-weight: bold; margin: 5px 0; }
            .metric-lbl { font-size: 14px; opacity: 0.9; }
        </style>
        """, unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"""
            <div class="metric-box" style="background: linear-gradient(45deg, #FF7043, #D84315);">
                <div class="metric-lbl">Total Bayar ke Nasabah ({total_kg} kg)</div>
                <div class="metric-val">Rp {total_paid:,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with m2:
            st.markdown(f"""
            <div class="metric-box" style="background: linear-gradient(45deg, #66BB6A, #2E7D32);">
                <div class="metric-lbl">Potensi Pendapatan Bank</div>
                <div class="metric-val">Rp {total_revenue:,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with m3:
            profit_margin = (gross_profit/total_revenue*100) if total_revenue else 0
            st.markdown(f"""
            <div class="metric-box" style="background: linear-gradient(45deg, #FFA726, #F57C00);">
                <div class="metric-lbl">Estimasi Margin Profit ({profit_margin:.1f}%)</div>
                <div class="metric-val">Rp {gross_profit:,.0f}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # --- 4. Receipt & Export Logic ---
        row1, row2 = st.columns(2)
        
        # A. HTML Receipt Generation
        items_html = ""
        items_list = [
            ("Residu", w_burn, p_burn), ("Kertas", w_paper, p_paper), ("Kain", w_cloth, p_cloth),
            ("Kaleng", w_cans, p_cans), ("Elektro", w_elec, p_elec), ("Botol PET", w_pet, p_pet),
            ("Plastik", w_plas, p_plas), ("Styrofoam", w_tray, p_tray), ("Kaca", w_glass, p_glass),
            ("Logam", w_metal, p_metal), ("B3", w_haz, p_haz)
        ]
        
        for name, w, p in items_list:
            if w > 0:
                items_html += f"<tr><td>{name}</td><td>{round(w, 2)} kg</td><td style='text-align:right'>Rp {w*p:,.0f}</td></tr>"

        html_receipt = f"""
        <html>
        <body style="font-family: monospace; width: 300px; font-size: 12px;">
            <center><h3>BANK SAMPAH TERPADU</h3></center>
            <center>AgriSensa Eco-System</center>
            <hr>
            <div>Tgl: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}</div>
            <div>Nasabah: {nasabah}</div>
            <div>Petugas: {petugas}</div>
            <hr>
            <table style="width:100%">
                {items_html}
            </table>
            <hr>
            <div style="display:flex; justify-content:space-between">
                <b>TOTAL BERAT</b>
                <b>{total_kg} kg</b>
            </div>
            <div style="display:flex; justify-content:space-between">
                <b>TOTAL BAYAR</b>
                <b>Rp {total_paid:,.0f}</b>
            </div>
            <hr>
            <center>Terima Kasih - Salam Lestari 🌱</center>
        </body>
        </html>
        """
        b64_receipt = base64.b64encode(html_receipt.encode()).decode()
        
        with row1:
            st.subheader("🧾 Cetak Struk")
            href = f'<a href="data:text/html;base64,{b64_receipt}" download="struk_{nasabah}_{datetime.date.today()}.html" target="_blank"><button style="background-color:#4CAF50; color:white; padding:10px 24px; border:none; border-radius:4px; cursor:pointer;">🖨️ Download Struk (Siap Print)</button></a>'
            st.markdown(href, unsafe_allow_html=True)
            st.caption("*Klik tombol di atas untuk mengunduh struk HTML yang bisa dicetak printer thermal.*")

    # --- Global Data Export Section (Outside Form) ---
    st.markdown("---")
    with st.expander("📂 Database & Ekspor Laporan"):
        file_path = "data/waste_data.csv"
        if os.path.exists(file_path):
            df_all = pd.read_csv(file_path)
            st.dataframe(df_all.tail(5), use_container_width=True)
            
            csv = df_all.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Semua Data (CSV/Excel)",
                data=csv,
                file_name=f'laporan_bank_sampah_{datetime.date.today()}.csv',
                mime='text/csv',
                type="secondary"
            )
        else:
            st.info("Belum ada data transaksi tersimpan.")
