import streamlit as st
import pandas as pd
import os
import json

def show():
    st.title("📂 Manajemen Data & Laporan")
    st.markdown("### *Pusat Data Logistik & Transparansi*")
    st.markdown("Unduh data transaksi dan konfigurasi sistem untuk keperluan audit atau backup.")

    tab1, tab2 = st.tabs(["📊 Laporan Transaksi (Logbook)", "⚙️ Konfigurasi Harga"])

    # --- TAB 1: Transaction Data (CSV) ---
    with tab1:
        st.subheader("Rekap Transaksi Harian")
        csv_file = "data/waste_data.csv"
        
        if os.path.exists(csv_file):
            try:
                df = pd.read_csv(csv_file)
                st.dataframe(df, use_container_width=True)
                
                # Metrics Summary
                c1, c2, c3 = st.columns(3)
                with c1: st.metric("Total Transaksi", len(df))
                
                if 'Total_KG' in df.columns:
                    total_vol = df['Total_KG'].sum()
                    with c2: st.metric("Total Volume (kg)", f"{total_vol:,.1f}")
                
                if 'Total_Bayar_Nasabah' in df.columns:
                    total_paid = df['Total_Bayar_Nasabah'].sum()
                    with c3: st.metric("Uang Beredar (Nasabah)", f"Rp {total_paid:,.0f}")

                st.download_button(
                    label="📥 Unduh Laporan (.csv)",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name='Laporan_Bank_Sampah.csv',
                    mime='text/csv',
                    type="primary"
                )
            except Exception as e:
                st.error(f"Gagal memuat data CSV: {e}")
        else:
            st.warning("Belum ada data transaksi yang tersimpan (File tidak ditemukan).")
            
    # --- TAB 2: Pricing Config (JSON) ---
    with tab2:
        st.subheader("Backup Konfigurasi Harga")
        json_file = "data/waste_prices.json"
        
        if os.path.exists(json_file):
            with open(json_file, "r") as f:
                json_data = json.load(f)
            
            st.json(json_data)
            
            json_str = json.dumps(json_data, indent=4)
            st.download_button(
                label="📥 Unduh Konfigurasi (.json)",
                data=json_str,
                file_name='waste_prices_backup.json',
                mime='application/json'
            )
        else:
            st.info("Menggunakan konfigurasi default (Belum ada file custom).")
