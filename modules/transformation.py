import streamlit as st
import pandas as pd
import plotly.express as px
from modules.price_service import load_prices

def show():
    st.title("🎯 Simulasi & Prediksi Nilai (Live)")
    st.markdown("Simulasikan potensi pendapatan dengan mengubah **Volume Sampah** atau **Harga Pasar** secara real-time.")

    # 1. Init Data
    # Load base prices from system config but allow edits in session
    if 'sim_data' not in st.session_state:
        # Load from central config
        base_prices = load_prices()
        # Transform to list of dicts for DataFrame
        initial_data = []
        for cat, val in base_prices.items():
            initial_data.append({
                "Kategori": cat,
                "Harga (Rp/kg)": int(val['sell']), # Default to Selling Price vs Buying? User said "Prediksi Nilai", usually implies Selling Potential
                "Berat (kg)": 0.0,
                "Estimasi (Rp)": 0
            })
        st.session_state.sim_data = pd.DataFrame(initial_data)

    # 2. Interactive Editor (Excel-like)
    st.subheader("📝 Input Parameter Simulasi")
    
    # Configure columns
    column_cfg = {
        "Kategori": st.column_config.TextColumn("Kategori", disabled=True, width="medium"),
        "Harga (Rp/kg)": st.column_config.NumberColumn("Harga Pasar (Rp)", step=100, format="Rp %d", width="small", help="Ubah harga untuk simulasi kenaikan/penurunan pasar"),
        "Berat (kg)": st.column_config.NumberColumn("Volume (kg)", step=0.5, min_value=0.0, format="%.1f kg", width="small"),
        "Estimasi (Rp)": st.column_config.NumberColumn("Total", disabled=True, format="Rp %d")  # Computed dynamically
    }

    # Layout: Editor (Left) vs Visuals (Right)
    col_edit, col_viz = st.columns([1.2, 1])

    with col_edit:
        # We use data_editor to allow direct editing
        edited_df = st.data_editor(
            st.session_state.sim_data,
            column_config=column_cfg,
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            key="simulator_editor"
        )
        
        # Recalculate Logic (Reactive)
        # Apply edits to calculation
        edited_df["Estimasi (Rp)"] = edited_df["Harga (Rp/kg)"] * edited_df["Berat (kg)"]
        
        # Rounding for precision
        edited_df["Estimasi (Rp)"] = edited_df["Estimasi (Rp)"].astype(int)
        
        # Save back to state to persist edits during reruns
        st.session_state.sim_data = edited_df

        # Summary Metrics within Edit Column for quick view
        total_omzet = edited_df["Estimasi (Rp)"].sum()
        total_weight = edited_df["Berat (kg)"].sum()
        
        st.info("💡 **Tips:** Klik sel pada tabel di atas untuk mengubah angka secara langsung.")

    with col_viz:
        st.subheader("📊 Analisis Real-Time")
        
        # Metric Cards
        tm1, tm2 = st.columns(2)
        with tm1:
            st.metric("Total Potensi Pendapatan", f"Rp {total_omzet:,.0f}", delta="Proyeksi")
        with tm2:
            st.metric("Total Volume Target", f"{total_weight:.1f} kg")

        if total_omzet > 0:
            # 1. Treemap (Better than Pie for many categories)
            fig_tree = px.treemap(
                edited_df[edited_df["Estimasi (Rp)"] > 0],
                path=['Kategori'],
                values='Estimasi (Rp)',
                color='Estimasi (Rp)',
                color_continuous_scale='Greens',
                title="Peta Dominasi Nilai (Treemap)"
            )
            fig_tree.update_layout(margin=dict(t=30, l=10, r=10, b=10), height=300)
            st.plotly_chart(fig_tree, use_container_width=True)

            # 2. Bar Chart for Price Sensitivity
            # Compare Estimated Income vs Weight
            chart_df = edited_df[edited_df["Berat (kg)"] > 0].copy()
            if not chart_df.empty:
                st.caption("Perbandingan Efisiensi (Nilai per Kg)")
                chart_df['Efficiency'] = chart_df['Estimasi (Rp)'] / chart_df['Berat (kg)']
                fig_bar = px.bar(
                    chart_df, x='Kategori', y='Estimasi (Rp)',
                    color='Efficiency', title="Revenue Breakdown",
                    color_continuous_scale='Oranges'
                )
                fig_bar.update_layout(xaxis={'categoryorder':'total descending'}, height=300)
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("⚠️ Belum ada aktivitas prediksi. Silakan isi volume di tabel samping.")

    # 3. Action Bar
    st.markdown("---")
    st.subheader("🚀 Tindakan")
    
    ac1, ac2 = st.columns([1, 4])
    with ac1:
        if st.button("🔄 Reset Simulasi"):
            del st.session_state.sim_data
            st.rerun()
    with ac2:
        if total_omzet > 0:
            # Export Scenario
            csv = edited_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="💾 Simpan Skenario (CSV)",
                data=csv,
                file_name='skenario_bank_sampah.csv',
                mime='text/csv',
                type="primary"
            )
