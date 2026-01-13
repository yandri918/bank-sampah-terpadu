import streamlit as st
import pandas as pd
from modules.price_service import load_prices, save_prices

def show():
    st.title("⚙️ Pengaturan Harga Pasar")
    st.markdown("Kelola standar **Harga Beli (Nasabah)** dan **Harga Jual (Industri)** untuk sinkronisasi sistem.")

    # Load current prices
    current_prices = load_prices()
    
    # Convert to DataFrame for easier editing
    data = []
    for category, rates in current_prices.items():
        data.append({
            "Kategori": category,
            "Harga Beli (Rp/kg)": rates['buy'],
            "Harga Jual (Rp/kg)": rates['sell'],
            "Margin (Rp/kg)": rates['sell'] - rates['buy'],
            "Margin (%)": round(((rates['sell'] - rates['buy']) / rates['sell'] * 100), 1) if rates['sell'] > 0 else 0
        })
    
    df = pd.DataFrame(data)
    
    # Editor
    st.subheader("Tabel Harga Terpusat")
    st.info("Ubah harga di bawah ini. Perubahan akan otomatis diterapkan pada menu 'Input Sampah'.")
    
    edited_df = st.data_editor(
        df,
        column_config={
            "Kategori": st.column_config.TextColumn("Kategori", disabled=True),
            "Harga Beli (Rp/kg)": st.column_config.NumberColumn("Harga Beli (Nasabah)", min_value=0, step=100, format="Rp %d"),
            "Harga Jual (Rp/kg)": st.column_config.NumberColumn("Harga Jual (Industri)", min_value=0, step=100, format="Rp %d"),
            "Margin (Rp/kg)": st.column_config.NumberColumn("Profit", disabled=True, format="Rp %d"),
            "Margin (%)": st.column_config.ProgressColumn("Margin %", format="%.1f%%", min_value=0, max_value=100),
        },
        use_container_width=True,
        hide_index=True,
        num_rows="fixed"
    )
    
    # Save Button
    if st.button("💾 Simpan Perubahan Harga"):
        new_prices = {}
        for index, row in edited_df.iterrows():
            cat = row['Kategori']
            new_prices[cat] = {
                "buy": int(row['Harga Beli (Rp/kg)']),
                "sell": int(row['Harga Jual (Rp/kg)'])
            }
        
        save_prices(new_prices)
        st.success("✅ Konfigurasi Harga Berhasil Diperbarui! Data baru akan menggunakan standar ini.")
        st.balloons()
        
    st.markdown("---")
    st.markdown("### 📊 Analisis Margin Saat Ini")
    
    # Calculate avg margin
    avg_margin = edited_df['Margin (%)'].mean()
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Rata-rata Margin Profit", f"{avg_margin:.1f}%")
        
    with c2:
        potential_profit_1ton = edited_df['Margin (Rp/kg)'].mean() * 1000
        st.metric("Potensi Profit per 1 Ton", f"Rp {potential_profit_1ton:,.0f}")
