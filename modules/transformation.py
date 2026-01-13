import streamlit as st
import pandas as pd

def show():
    st.title("Kalkulator Nilai Ekonomi (Trash to Cash)")
    st.markdown("Konversi limbah menjadi potensi pendapatan nyata berdasarkan kategori presisi.")

    # Pricing Table based on Indonesian Waste Bank Averages (Estimates)
    prices = {
        "Bisa Dibakar (Organik/Residu)": 200,   # Low value, mostly for compost/incineration
        "Kertas (Koran/Kardus)": 2500,          # High value
        "Kain (Perca/Baju Layak)": 1000,        # Medium value (upcycle potential)
        "Kaleng (Aluminium/Besi)": 12000,       # Very High value
        "Elektronik Kecil (E-Waste)": 15000,    # Per unit approx or kg
        "Botol PET (Bersih)": 4500,             # High value
        "Plastik (Wadah/Bungkus)": 1500,        # Medium
        "Nampan Putih (Styrofoam)": 500,        # Low
        "Botol Kaca": 500,                      # Low
        "Logam Kecil": 3500,                    # Medium
        "Limbah Berbahaya": 0                   # Cost to dispose usually
    }

    st.subheader("Simulasi Pendapatan")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Input Volume")
        inputs = {}
        for item, price in prices.items():
            # Use columns for compact view
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"**{item}**")
                st.caption(f"Est. Rp {price}/kg")
            with c2:
                val = st.number_input(f"Kg {item}", min_value=0.0, step=0.5, key=f"p_{item}", label_visibility="collapsed")
            inputs[item] = val

    with col2:
        st.markdown("### Hasil Perhitungan")
        total_income = 0
        df_list = []
        
        for item, weight in inputs.items():
            if weight > 0:
                subtotal = weight * prices[item]
                total_income += subtotal
                df_list.append({"Kategori": item, "Berat (kg)": weight, "Harga/kg": prices[item], "Total (Rp)": subtotal})
        
        if df_list:
            df = pd.DataFrame(df_list)
            st.dataframe(df, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            st.markdown(f"""
            <div style="background-color: #d4edda; padding: 25px; border-radius: 15px; border: 2px solid #28a745; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h3 style="color: #155724; margin:0; text-transform: uppercase; font-size: 0.9em; letter-spacing: 1px;">Total Estimasi Nilai</h3>
                <h1 style="color: #28a745; font-size: 3.5em; margin: 10px 0; font-weight: 800;">Rp {total_income:,.0f}</h1>
                <p style="color: #155724; margin:0; font-style: italic;">*Potensi Emas Hijau</p>
            </div>
            """, unsafe_allow_html=True)
            
        else:
            st.info("⬅️ Masukkan data di panel kiri untuk kalkulasi.")
            
        st.markdown("### 📊 Proporsi Nilai")
        if df_list:
             import plotly.express as px
             fig = px.pie(df, values='Total (Rp)', names='Kategori', title='Kontribusi Nilai per Kategori', hole=0.4)
             fig.update_traces(textposition='inside', textinfo='percent+label')
             st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    with st.expander("Lihat Referensi Harga Pasar"):
        st.table(pd.DataFrame(list(prices.items()), columns=["Kategori", "Harga Referensi (Rp/kg)"]))
