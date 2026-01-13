import streamlit as st
import datetime

def show():
    st.title("Input Penyetoran Sampah (Pilah)")
    st.markdown("Catat sampah yang masuk sesuai **Panduan Pembuangan Sampah Rumah Tangga**.")

    with st.form("waste_input_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.date_input("Tanggal Setor", datetime.date.today())
            nasabah = st.text_input("Nama Nasabah / Sumber", placeholder="Contoh: RT 04 / Bpk. Budi")
        
        with col2:
            petugas = st.text_input("Nama Petugas Penerima")
            lokasi = st.selectbox("Lokasi Bank Sampah", ["Unit Pusat", "Unit Satelit 1", "Unit Satelit 2"])

        st.markdown("---")
        st.markdown("### Kategori Sampah (Sesuai Panduan)")
        
        # Group 1: Basics
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### 🔥 Bisa Dibakar (Burnable)")
            burnable = st.number_input("Sampah Dapur/Kayu/Karet (kg)", min_value=0.0, step=0.1, help="Sampah dapur, kotoran, produk kulit, sepatu, tas, dll.")
            
            st.markdown("#### 📄 Kertas (Paper)")
            paper = st.number_input("Koran/Majalah/Kardus (kg)", min_value=0.0, step=0.1, help="Koran, majalah, kotak kardus, amplop, dll.")
            
            st.markdown("#### 👕 Kain (Cloth)")
            cloth = st.number_input("Pakaian/Selimut/Tirai (kg)", min_value=0.0, step=0.1, help="Pakaian, selimut, tirai kain, karpet kapas, dll.")

            st.markdown("#### 🥫 Kaleng (Cans)")
            cans = st.number_input("Kaleng Minuman/Makanan (kg)", min_value=0.0, step=0.1, help="Kaleng aluminium, kaleng besi, kaleng spray.")

            st.markdown("#### 🔌 Elektronik Kecil")
            electronics = st.number_input("Perabotan Elektronik Kecil (unit/kg)", min_value=0.0, step=1.0, help="Komputer, mainan baterai, jam tangan, dll.")

        with c2:
            st.markdown("#### 🍾 Botol PET")
            pet_bottles = st.number_input("Botol Plastik Minuman (kg)", min_value=0.0, step=0.1, help="Botol PET dengan label dilepas & dibilas.")

            st.markdown("#### 🧴 Plastik (Wadah/Bungkus)")
            plastic_marks = st.number_input("Wadah Plastik/Bungkus (kg)", min_value=0.0, step=0.1, help="Botol deterjen, cup puding, bungkus snack, nampan berwarna.")

            st.markdown("#### 🍽️ Nampan Putih")
            white_trays = st.number_input("Nampan Styrofoam Putih (kg)", min_value=0.0, step=0.1, help="Nampan putih bersih.")

            st.markdown("#### 🏺 Botol Kaca")
            glass_bottles = st.number_input("Botol Kaca/Beling (kg)", min_value=0.0, step=0.1, help="Botol sirup, minuman energi, dll.")
            
            st.markdown("#### 🏗️ Lainnya")
            metal_small = st.number_input("Logam Kecil (Panci/Pisau) (kg)", min_value=0.0, step=0.1)
            hazardous = st.number_input("Limbah Berbahaya (Baterai/Lampu) (kg)", min_value=0.0, step=0.1)

        submitted = st.form_submit_button("Simpan Data Transaksi")
        
        if submitted:
            total_kg = burnable + paper + cloth + cans + electronics + pet_bottles + plastic_marks + white_trays + glass_bottles + metal_small + hazardous
            st.success(f"Diterima: {total_kg:.2f} kg sampah dari {nasabah}. Data berhasil disimpan ke sistem.")
            st.balloons()
