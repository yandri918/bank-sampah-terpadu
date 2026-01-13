import streamlit as st
from modules import dashboard, waste_input, transformation, fertilizer_processing, price_settings, plastic_upcycling, ai_simulator

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
        ["Dashboard Utama", "Input Sampah (Pilah)", "Kalkulator Nilai Ekonomi", "Pupuk Organik Premium", "Pengaturan Harga", "Upcycling: Plastik ke Filamen", "AI Logic: Strategic Simulator", "Panduan 5R"],
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
elif menu == "Pupuk Organik Premium":
    fertilizer_processing.show()
elif menu == "Pengaturan Harga":
    price_settings.show()
elif menu == "Upcycling: Plastik ke Filamen":
    plastic_upcycling.show()
    
elif menu == "AI Logic: Strategic Simulator":
    ai_simulator.show()

elif menu == "Panduan 5R":
    st.title("Panduan Pembuangan Sampah")
    st.markdown("Berikut adalah panduan visual klasifikasi sampah (Standard Acuan).")
    
    try:
        st.image("assets/guide_ref.jpg", caption="Panduan Klasifikasi Sampah Rumah Tangga", use_column_width=True)
    except:
        st.warning("Gambar panduan belum dimuat. Pastikan file 'assets/guide_ref.jpg' tersedia.")

    st.markdown("### Prinsip 5R: Menuju Nol Limbah")
    st.info("Penerapan pola pikir sirkular untuk meminimalkan dampak lingkungan.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("1. Refuse (Tolak) 🚫", expanded=True):
            st.markdown("""
            **Definisi:** Menolak barang yang tidak perlu atau berpotensi menjadi sampah sulit urai.
            - **Contoh:** 
                - Tolak kantong plastik saat belanja, gunakan tas kain.
                - Tolak sedotan plastik di restoran.
                - Tolak brosur/spam mail fisik jika tersedia versi digital.
            """)

        with st.expander("2. Reduce (Kurangi) 📉", expanded=True):
            st.markdown("""
            **Definisi:** Mengurangi konsumsi sumber daya dan penggunaan barang sekali pakai.
            - **Contoh:**
                - Beli produk dalam kemasan besar (bulk) untuk kurangi sampah sachet.
                - Kurangi penggunaan kertas dengan mencetak bolak-balik.
                - Hemat energi dan air di rumah.
            """)

        with st.expander("3. Reuse (Gunakan Kembali) 🔄", expanded=True):
            st.markdown("""
            **Definisi:** Menggunakan kembali barang untuk fungsi yang sama atau berbeda tanpa mengubah bentuk drastis.
            - **Contoh:**
                - Gunakan botol kaca bekas selai untuk wadah bumbu.
                - Sumbangkan pakaian layak pakai alih-alih membuangnya.
                - Gunakan baterai isi ulang (rechargeable).
            """)

    with col2:
        with st.expander("4. Repurpose (Alih Fungsi) 🎨", expanded=True):
            st.markdown("""
            **Definisi:** Memodifikasi barang bekas untuk kegunaan baru yang kreatif (Upcycling).
            - **Contoh:**
                - Ban bekas disulap menjadi kursi atau pot tanaman.
                - Kulit buah jeruk diolah menjadi eco-enzyme pembersih lantai.
                - Kaos bekas dijadikan kain lap atau tote bag.
            """)

        with st.expander("5. Recycle (Daur Ulang) ♻️", expanded=True):
            st.markdown("""
            **Definisi:** Mengolah sampah menjadi bahan baku baru melalui proses industri atau pengomposan.
            - **Contoh:**
                - **Bank Sampah:** Setor botol PET untuk dilebur jadi bijih plastik.
                - **Kompos:** Olah sisa makanan menjadi pupuk organik (Emas Hijau).
                - **Kertas:** Daur ulang kardus bekas menjadi bubur kertas.
            """)
    
    st.success("Mulai dari langkah kecil: **Pilah Sampahmu dari Rumah!**")
