import streamlit as st
import datetime

def show():
    # Market Selling Prices (Harga Jual ke Pabrik/Pengepul Besar)
    selling_prices = {
        "Burnable": 300,        # Jual Listrik/Kompos
        "Paper": 3000,          # Jual Pabrik Kertas
        "Cloth": 1500,          # Jual Upcycle
        "Cans": 14000,          # Jual Peleburan
        "Electronics": 20000,   # Jual Komponen
        "PET_Bottles": 5500,    # Jual Pencacah
        "Plastic_Marks": 2000,  # Jual Pelet
        "White_Trays": 1000,    # Jual Daur Ulang
        "Glass_Bottles": 1000,  # Jual Pabrik Kaca
        "Metal_Small": 4500,    # Jual Besi Tua
        "Hazardous": 0          # Cost
    }
    
    # Default Buying Prices (Harga Beli dari Nasabah - Margin ~30-40%)
    buying_defaults = {k: int(v * 0.7) for k, v in selling_prices.items()}

    with st.form("waste_input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            tanggal_setor = st.date_input("Tanggal Setor", datetime.date.today())
            nasabah = st.text_input("Nama Nasabah / Sumber", placeholder="Contoh: RT 04 / Bpk. Budi")
        
        with col2:
            petugas = st.text_input("Nama Petugas Penerima")
            lokasi = st.selectbox("Lokasi Bank Sampah", ["Unit Pusat", "Unit Satelit 1", "Unit Satelit 2"])

        st.markdown("---")
        st.markdown("### Kategori Sampah (Input Berat & Harga Beli)")
        
        # Helper to create input row
        def input_row(label, key_prefix, default_buy, help_text):
            c_w, c_p = st.columns([2, 1])
            with c_w:
                weight = st.number_input(f"{label} (kg)", min_value=0.0, step=0.1, help=help_text, key=f"w_{key_prefix}")
            with c_p:
                price = st.number_input(f"Beli (Rp/kg)", value=int(default_buy), step=100, help="Harga bayar ke nasabah", key=f"p_{key_prefix}")
            return weight, price

        # Group 1: Basics
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🔥 Bisa Dibakar (Burnable)")
            w_burn, p_burn = input_row("Sampah Dapur/Residu", "Burnable", buying_defaults["Burnable"], "Sampah dapur, kotoran, produk kulit.")
            
            st.markdown("#### 📄 Kertas (Paper)")
            w_paper, p_paper = input_row("Koran/Kardus", "Paper", buying_defaults["Paper"], "Koran, majalah, kardus.")
            
            st.markdown("#### 👕 Kain (Cloth)")
            w_cloth, p_cloth = input_row("Pakaian/Kain", "Cloth", buying_defaults["Cloth"], "Pakaian layak, perca.")

            st.markdown("#### 🥫 Kaleng (Cans)")
            w_cans, p_cans = input_row("Kaleng Logam", "Cans", buying_defaults["Cans"], "Kaleng aluminium/besi.")

            st.markdown("#### 🔌 Elektronik Kecil")
            w_elec, p_elec = input_row("E-Waste", "Electronics", buying_defaults["Electronics"], "Gadget, mainan baterai.")

        with c2:
            st.markdown("#### 🍾 Botol PET")
            w_pet, p_pet = input_row("Botol Plastik", "PET", buying_defaults["PET_Bottles"], "Botol bening/biru.")

            st.markdown("#### 🧴 Plastik (Wadah)")
            w_plas, p_plas = input_row("Wadah Plastik", "Plastic", buying_defaults["Plastic_Marks"], "Ember, gayung, mainan plastik.")

            st.markdown("#### 🍽️ Nampan Putih")
            w_tray, p_tray = input_row("Styrofoam/Busa", "Trays", buying_defaults["White_Trays"], "Nampan putih bersih.")

            st.markdown("#### 🏺 Botol Kaca")
            w_glass, p_glass = input_row("Kaca/Beling", "Glass", buying_defaults["Glass_Bottles"], "Botol sirup, piring pecah.")
            
            st.markdown("#### 🏗️ Lainnya")
            w_metal, p_metal = input_row("Logam Campur", "Metal", buying_defaults["Metal_Small"], "Panci rusak, besi tua.")
            w_haz, p_haz = input_row("Limbah B3", "Hazardous", buying_defaults["Hazardous"], "Baterai, lampu neon.")

        submitted = st.form_submit_button("Simpan Data Transaksi")
        
        if submitted:
            # 1. Calculate Expenses (Paid to Nasabah)
            total_paid = (w_burn * p_burn) + (w_paper * p_paper) + (w_cloth * p_cloth) + (w_cans * p_cans) + \
                         (w_elec * p_elec) + (w_pet * p_pet) + (w_plas * p_plas) + (w_tray * p_tray) + \
                         (w_glass * p_glass) + (w_metal * p_metal) + (w_haz * p_haz)
            
            # 2. Calculate Potential Revenue (Sell to Industry)
            total_revenue = (w_burn * selling_prices["Burnable"]) + (w_paper * selling_prices["Paper"]) + \
                            (w_cloth * selling_prices["Cloth"]) + (w_cans * selling_prices["Cans"]) + \
                            (w_elec * selling_prices["Electronics"]) + (w_pet * selling_prices["PET_Bottles"]) + \
                            (w_plas * selling_prices["Plastic_Marks"]) + (w_tray * selling_prices["White_Trays"]) + \
                            (w_glass * selling_prices["Glass_Bottles"]) + (w_metal * selling_prices["Metal_Small"]) + \
                            (w_haz * selling_prices["Hazardous"])

            # 3. Calculate Gross Profit
            gross_profit = total_revenue - total_paid

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
                "Total_Bayar_Nasabah": [total_paid],
                "Est_Pendapatan_Bank": [total_revenue],
                "Est_Profit": [gross_profit]
            }
            df_new = pd.DataFrame(new_data)
            
            # Save to CSV
            file_path = "data/waste_data.csv"
            os.makedirs("data", exist_ok=True)
            
            if not os.path.exists(file_path):
                df_new.to_csv(file_path, index=False)
            else:
                try:
                    df_existing = pd.read_csv(file_path)
                    # Align columns
                    df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                    df_combined.to_csv(file_path, index=False)
                except:
                    df_new.to_csv(file_path, mode='a', header=False, index=False)

            st.success(f"✅ Transaksi Berhasil Disimpan!")
            
            # Financial Summary Cards
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Bayar ke Nasabah", f"Rp {total_paid:,.0f}", f"{total_kg:.1f} kg")
            with m2:
                st.metric("Potensi Jual (Bank)", f"Rp {total_revenue:,.0f}", "Harga Pasar")
            with m3:
                st.metric("Estimasi Profit", f"Rp {gross_profit:,.0f}", f"{(gross_profit/total_revenue*100) if total_revenue else 0:.1f}% Margin")
            
            st.balloons()
