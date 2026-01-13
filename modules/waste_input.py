import streamlit as st
import datetime

def show():
    st.title("Input Penyetoran Sampah (Pilah)")
    st.markdown("Catat sampah yang masuk sesuai **Panduan Pembuangan Sampah Rumah Tangga**.")

    # Base Prices (Defaults)
    default_prices = {
        "Burnable": 200, "Paper": 2500, "Cloth": 1000, "Cans": 12000, 
        "Electronics": 15000, "PET_Bottles": 4500, "Plastic_Marks": 1500, 
        "White_Trays": 500, "Glass_Bottles": 500, "Metal_Small": 3500, "Hazardous": 0
    }

    with st.form("waste_input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            tanggal_setor = st.date_input("Tanggal Setor", datetime.date.today())
            nasabah = st.text_input("Nama Nasabah / Sumber", placeholder="Contoh: RT 04 / Bpk. Budi")
        
        with col2:
            petugas = st.text_input("Nama Petugas Penerima")
            lokasi = st.selectbox("Lokasi Bank Sampah", ["Unit Pusat", "Unit Satelit 1", "Unit Satelit 2"])

        st.markdown("---")
        st.markdown("### Kategori Sampah (Input Berat & Harga)")
        
        # Helper to create input row
        def input_row(label, key_prefix, default_p, help_text):
            c_w, c_p = st.columns([2, 1])
            with c_w:
                weight = st.number_input(f"{label} (kg)", min_value=0.0, step=0.1, help=help_text, key=f"w_{key_prefix}")
            with c_p:
                price = st.number_input(f"Harga (Rp/kg)", value=int(default_p), step=100, key=f"p_{key_prefix}")
            return weight, price

        # Group 1: Basics
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🔥 Bisa Dibakar (Burnable)")
            w_burn, p_burn = input_row("Sampah Dapur/Residu", "Burnable", default_prices["Burnable"], "Sampah dapur, kotoran, produk kulit.")
            
            st.markdown("#### 📄 Kertas (Paper)")
            w_paper, p_paper = input_row("Koran/Kardus", "Paper", default_prices["Paper"], "Koran, majalah, kardus.")
            
            st.markdown("#### 👕 Kain (Cloth)")
            w_cloth, p_cloth = input_row("Pakaian/Kain", "Cloth", default_prices["Cloth"], "Pakaian layak, perca.")

            st.markdown("#### 🥫 Kaleng (Cans)")
            w_cans, p_cans = input_row("Kaleng Logam", "Cans", default_prices["Cans"], "Kaleng aluminium/besi.")

            st.markdown("#### 🔌 Elektronik Kecil")
            w_elec, p_elec = input_row("E-Waste", "Electronics", default_prices["Electronics"], "Gadget, mainan baterai.")

        with c2:
            st.markdown("#### 🍾 Botol PET")
            w_pet, p_pet = input_row("Botol Plastik", "PET", default_prices["PET_Bottles"], "Botol bening/biru.")

            st.markdown("#### 🧴 Plastik (Wadah)")
            w_plas, p_plas = input_row("Wadah Plastik", "Plastic", default_prices["Plastic_Marks"], "Ember, gayung, mainan plastik.")

            st.markdown("#### 🍽️ Nampan Putih")
            w_tray, p_tray = input_row("Styrofoam/Busa", "Trays", default_prices["White_Trays"], "Nampan putih bersih.")

            st.markdown("#### 🏺 Botol Kaca")
            w_glass, p_glass = input_row("Kaca/Beling", "Glass", default_prices["Glass_Bottles"], "Botol sirup, piring pecah.")
            
            st.markdown("#### 🏗️ Lainnya")
            w_metal, p_metal = input_row("Logam Campur", "Metal", default_prices["Metal_Small"], "Panci rusak, besi tua.")
            w_haz, p_haz = input_row("Limbah B3", "Hazardous", default_prices["Hazardous"], "Baterai, lampu neon.")

        submitted = st.form_submit_button("Simpan Data Transaksi")
        
        if submitted:
            # Calculate Total Value
            total_value = (w_burn * p_burn) + (w_paper * p_paper) + (w_cloth * p_cloth) + (w_cans * p_cans) + \
                          (w_elec * p_elec) + (w_pet * p_pet) + (w_plas * p_plas) + (w_tray * p_tray) + \
                          (w_glass * p_glass) + (w_metal * p_metal) + (w_haz * p_haz)
                          
            total_kg = w_burn + w_paper + w_cloth + w_cans + w_elec + w_pet + w_plas + w_tray + w_glass + w_metal + w_haz

            # Create Data Record
            import pandas as pd
            import os

            new_data = {
                "Tangent": [datetime.datetime.now()],
                "Tanggal": [tanggal_setor],
                "Nasabah": [nasabah],
                "Petugas": [petugas],
                "Lokasi": [lokasi],
                # Weights
                "Burnable": [w_burn], "Paper": [w_paper], "Cloth": [w_cloth], "Cans": [w_cans],
                "Electronics": [w_elec], "PET_Bottles": [w_pet], "Plastic_Marks": [w_plas],
                "White_Trays": [w_tray], "Glass_Bottles": [w_glass], "Metal_Small": [w_metal], "Hazardous": [w_haz],
                # Financials
                "Total_Nilai_Rp": [total_value]
            }
            df_new = pd.DataFrame(new_data)
            
            # Save to CSV
            file_path = "data/waste_data.csv"
            os.makedirs("data", exist_ok=True)
            
            if not os.path.exists(file_path):
                df_new.to_csv(file_path, index=False)
            else:
                # Check for schema mismatch if adding new column to existing CSV
                # For simplicity, we assume append works or file is fresh. 
                # If file exists but lacks 'Total_Nilai_Rp', pandas append might fail or misalign.
                # Ideally, we read, concat, and write.
                try:
                    df_existing = pd.read_csv(file_path)
                    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                    df_combined.to_csv(file_path, index=False)
                except:
                    df_new.to_csv(file_path, mode='a', header=False, index=False)

            st.success(f"✅ Transaksi Berhasil!")
            st.markdown(f"**Total Berat:** {total_kg:.2f} kg | **Total Nilai:** Rp {total_value:,.0f}")
            st.balloons()
