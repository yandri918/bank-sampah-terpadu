import streamlit as st
from modules import dashboard, waste_input, transformation

# Configure the page
st.set_page_config(
    page_title="Bank Sampah Terpadu | AgriSensa",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Green Gold" Aesthetics
st.markdown("""
<style>
    :root {
        --primary-color: #2E7d32; /* Green Gold */
        --secondary-color: #F9A825; /* Gold */
        --background-color: #F1F8E9; /* Light Green */
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #1B5E20;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stButton>button {
        background-color: #2E7d32;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1B5E20;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border-left: 5px solid #2E7d32;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/recycle-sign.png", width=80)
    st.title("Bank Sampah Terpadu")
    st.markdown("### *AgriSensa Ecosystem*")
    st.info("Transformasi Limbah Menjadi Emas Hijau & Bahan Baku Presisi")
    
    menu = st.radio(
        "Navigasi",
        ["Dashboard Utama", "Input Sampah (Pilah)", "Kalkulator Nilai Ekonomi", "Panduan 5R"],
        index=0
    )
    
    st.markdown("---")
    st.caption("© 2026 AgriSensa - Circular Economy")

# Router
if menu == "Dashboard Utama":
    dashboard.show()
elif menu == "Input Sampah (Pilah)":
    waste_input.show()
elif menu == "Kalkulator Nilai Ekonomi":
    transformation.show()
elif menu == "Panduan 5R":
    st.title("Panduan Pembuangan Sampah")
    st.markdown("Berikut adalah panduan visual klasifikasi sampah (Standard Acuan).")
    
    try:
        st.image("assets/guide_ref.jpg", caption="Panduan Klasifikasi Sampah Rumah Tangga", use_column_width=True)
    except:
        st.warning("Gambar panduan belum dimuat. Pastikan file 'assets/guide_ref.jpg' tersedia.")

    st.markdown("### Prinsip 5R")
    st.info("Refuse (Tolak), Reduce (Kurangi), Reuse (Gunakan Kembali), Repurpose (Alih Fungsi), Recycle (Daur Ulang)")
