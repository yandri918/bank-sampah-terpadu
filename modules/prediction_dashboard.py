import streamlit as st
import pandas as pd
import plotly.express as px
from modules.price_service import load_prices

def show():
    st.title("💸 Simulasi Live & Prediksi")
    st.markdown("### *Interactive Profit Simulator*")
    st.caption("Ubah angka 'Berat' di tabel untuk melihat potensi keuntungan secara real-time.")

    # 1. Load Prices
    prices = load_prices()
    
    # 2. Initialize Data for Editor if not in session
    if 'sim_data' not in st.session_state:
        # Create initial dataframe structure
        data = []
        for cat, val in prices.items():
            data.append({
                "Kategori": cat,
                "Berat (kg)": 0.0, # Default 0
                "Harga Beli (Rp)": val['buy'],
                "Harga Jual (Rp)": val['sell']
            })
        st.session_state['sim_data'] = pd.DataFrame(data)

    # 3. Interactive Data Editor
    # We use data_editor to let user input weights
    st.info("👇 **Edit kolom 'Berat (kg)' di bawah ini:**")
    
    edited_df = st.data_editor(
        st.session_state['sim_data'],
        column_config={
            "Kategori": st.column_config.TextColumn(disabled=True),
            "Berat (kg)": st.column_config.NumberColumn(min_value=0, step=1, format="%.1f kg"),
            "Harga Beli (Rp)": st.column_config.NumberColumn(disabled=True, format="Rp %d"),
            "Harga Jual (Rp)": st.column_config.NumberColumn(disabled=True, format="Rp %d"),
        },
        use_container_width=True,
        hide_index=True,
        key="editor"
    )

    # 4. Real-time Calculations
    # Calculate totals based on edited dataframe
    edited_df['Total Beli'] = edited_df['Berat (kg)'] * edited_df['Harga Beli (Rp)']
    edited_df['Total Jual'] = edited_df['Berat (kg)'] * edited_df['Harga Jual (Rp)']
    
    total_weight = edited_df['Berat (kg)'].sum()
    total_cost = edited_df['Total Beli'].sum()
    total_revenue = edited_df['Total Jual'].sum()
    total_profit = total_revenue - total_cost
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

    st.markdown("---")

    # 5. Visual Feedback (Big Metrics)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Berat", f"{total_weight:,.1f} kg")
    with col2:
        st.metric("Modal (Bayar ke Nasabah)", f"Rp {total_cost:,.0f}")
    with col3:
        st.metric("Estimasi Pendapatan", f"Rp {total_revenue:,.0f}")
    with col4:
        st.metric("Estimasi Profit", f"Rp {total_profit:,.0f}", f"{profit_margin:.1f}%")

    st.markdown("---")

    # 6. Charts
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("📊 Potensi Pendapatan per Kategori")
        # Filter only items with weight > 0
        active_items = edited_df[edited_df['Berat (kg)'] > 0]
        
        if not active_items.empty:
            fig_bar = px.bar(
                active_items, 
                x="Kategori", 
                y="Total Jual",
                text_auto='.2s',
                color="Kategori",
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            fig_bar.update_layout(showlegend=False, yaxis_title="Rupiah")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Masukkan berat di tabel untuk melihat grafik.")

    with c2:
        st.subheader("⚖️ Komposisi Berat")
        if not active_items.empty:
            fig_pie = px.pie(
                active_items,
                values="Berat (kg)",
                names="Kategori",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Belum ada data input.")
            
    # Reset Button
    if st.button("🔄 Reset Simulasi"):
        del st.session_state['sim_data']
        st.rerun()
