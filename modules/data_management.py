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
        
        from modules import auth_db
        # Filter by Current Logged In User
        current_user_name = st.session_state.get('user_info', {}).get('name')
        df = auth_db.get_all_transactions(petugas_filter=current_user_name)
        
        if not df.empty:
            try:
                
                # --- 1. Simplified Summary View ---
                st.markdown("#### 📋 Ringkasan Transaksi")
                
                # Filter & Rename Columns for Clarity
                # Check which columns actually exist to avoid errors
                cols_to_show = ['Tanggal', 'Nama_Nasabah', 'Total_KG', 'Total_Bayar_Nasabah']
                available_cols = [c for c in cols_to_show if c in df.columns]
                
                df_summary = df[available_cols].copy()
                df_summary.rename(columns={
                    'Nama_Nasabah': 'Nasabah',
                    'Total_KG': 'Berat Total (kg)',
                    'Total_Bayar_Nasabah': 'Dibayarkan (Rp)'
                }, inplace=True)
                
                # Display Interactive Table
                st.dataframe(
                    df_summary,
                    use_container_width=True,
                    column_config={
                        "Dibayarkan (Rp)": st.column_config.NumberColumn(format="Rp %d"),
                        "Berat Total (kg)": st.column_config.NumberColumn(format="%.2f kg"),
                        "Tanggal": st.column_config.DateColumn(format="DD/MM/YYYY"),
                    },
                    hide_index=True
                )
                
                # --- 2. Detailed View (Collapsible) ---
                with st.expander("🔍 Lihat Detail Lengkap (Semua Jenis Sampah)"):
                    st.dataframe(df, use_container_width=True)

                # Metrics Summary
                st.markdown("---")
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

                # --- PDF Export Logic ---
                try:
                    from fpdf import FPDF
                    
                    def create_pdf(dataframe):
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", size=12)
                        
                        # Title
                        pdf.set_font("Arial", style="B", size=16)
                        pdf.cell(200, 10, txt="Laporan Transaksi Bank Sampah", ln=True, align='C')
                        pdf.ln(10)
                        
                        # Table Header
                        pdf.set_font("Arial", style="B", size=10)
                        cols = ["Tanggal", "Nasabah", "Total KG", "Rp Dibayar"]
                        col_widths = [40, 60, 30, 40]
                        
                        for i, col in enumerate(cols):
                            pdf.cell(col_widths[i], 10, col, 1, 0, 'C')
                        pdf.ln()
                        
                        # Table Rows
                        pdf.set_font("Arial", size=10)
                        for _, row in dataframe.iterrows():
                            # Safe string conversion and formatting
                            pdf.cell(col_widths[0], 10, str(row['Tanggal']), 1)
                            pdf.cell(col_widths[1], 10, str(row['Nama_Nasabah'])[:25], 1) # Truncate long names
                            pdf.cell(col_widths[2], 10, f"{row['Total_KG']:.1f}", 1, 0, 'R')
                            pdf.cell(col_widths[3], 10, f"{int(row['Total_Bayar_Nasabah']):,}", 1, 0, 'R')
                            pdf.ln()
                            
                        return pdf.output(dest='S').encode('latin-1', 'replace')

                    pdf_bytes = create_pdf(df)
                    
                    st.download_button(
                        label="📄 Unduh Laporan (.pdf)",
                        data=pdf_bytes,
                        file_name='Laporan_Bank_Sampah.pdf',
                        mime='application/pdf'
                    )
                except ImportError:
                    st.warning("Library 'fpdf' belum terinstall. PDF tidak tersedia.")
                except Exception as e:
                    st.error(f"Gagal membuat PDF: {e}")

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
