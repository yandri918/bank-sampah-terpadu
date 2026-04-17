# ♻️ Bank Sampah Terpadu — AgriSensa Hub

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg)](https://agrisensa-bank-sampah.streamlit.app/)
[![Project Status: Active](https://img.shields.io/badge/Project%20Status-Active-brightgreen.svg)]()
[![Ecosystem: AgriSensa](https://img.shields.io/badge/Ecosystem-AgriSensa-darkgreen.svg)]()

**Bank Sampah Terpadu** adalah platform manajemen limbah modern yang mengintegrasikan prinsip **Circular Economy** dengan disiplin pengelolaan sampah presisi. Aplikasi ini dirancang untuk mengubah operasional bank sampah tradisional menjadi entitas bisnis yang terukur, aman, dan berorientasi pada profitabilitas "Emas Hijau".

---

## 🌟 Fitur Unggulan

### 🔒 Arsitektur Keamanan & Multi-Tenant
- **Secure Authentication**: Sistem login berbasis enkripsi yang terintegrasi dengan database SQLite.
- **Data Isolation**: Logika multi-user yang memastikan setiap petugas hanya dapat mengelola dan melihat data sesuai otoritasnya (Data Privacy).

### 📊 Integrasi Operasional & Finansial
- **Interactive Input (Pilah)**: Pencatatan setoran sampah dengan klasifikasi standar (Plastik, Kertas, Logam, Elektronik, dll).
- **Simulasi Live & Prediksi**: Profit simulator real-time dengan parameter harga beli (nasabah) dan harga jual (industri) yang dinamis.
- **Kalkulator Efisiensi**: Analisis nilai ekonomi per kategori untuk menentukan komoditas paling menguntungkan.

### 🤖 AI Strategic Simulator
- **Reverse Engineering Strategy**: Masukkan target omzet bulanan, dan sistem akan mengestimasi kebutuhan volume sampah, jumlah mitra, serta kapasitas logistik yang diperlukan untuk mencapainya.

### 🏭 Transformasi Limbah ke Energi & Produk
- **Organic to Gold**: Manajemen produksi Pupuk Organik Premium dan Budidaya Maggot BSF.
- **Upcycling Plastic**: Monitoring konversi plastik menjadi Filamen 3D Printing.
- **Waste to Energy**: Pencatatan log operasional Pyrolysis (konversi plastik menjadi BBM).

---

## 🚀 Menu Navigasi

1.  **Dashboard Utama**: Ringkasan eksekutif performa bank sampah.
2.  **Input Sampah (Pilah)**: Digitalisasi setoran harian nasabah.
3.  **Simulasi Live & Prediksi**: Laboratorium simulasi keuntungan.
4.  **Kalkulator Nilai Ekonomi**: Prediksi pendapatan berbasis fluktuasi harga pasar.
5.  **Pupuk Organik & Maggot BSF**: Operasional biokonversi limbah organik.
6.  **Upcycling & Pyrolysis**: Monitoring teknologi pengolahan sampah tingkat lanjut.
7.  **AI Logic Strategic Simulator**: Blueprint operasional berbasis target finansial.
8.  **Manajemen Data & Laporan**: Export data SQLite ke format CSV untuk audit.

---

## 🛠️ Instalasi Lokal

1.  **Clone Repository**:
    ```bash
    git clone https://github.com/yandri918/bank-sampah-terpadu.git
    cd bank-sampah-terpadu
    ```

2.  **Persiapkan Lingkungan (Environment)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Running Application**:
    ```bash
    streamlit run app.py
    ```

---

## 🏗️ Teknologi yang Digunakan

- **Core**: [Streamlit](https://streamlit.io/) (High-performance web framework).
- **Database**: [SQLite](https://sqlite.org/) (Lightweight, robust relational database).
- **Visualization**: [Plotly](https://plotly.com/) & [Matplotlib](https://matplotlib.org/).
- **Data Engine**: [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/).

---

## 🌿 Filosofi 5R

Project ini mendukung penuh implementasi **5R**:
- **Refuse**: Menolak bahan yang susah urai.
- **Reduce**: Mengurangi volume timbulan sampah.
- **Reuse**: Memanfaatkan kembali barang layak guna.
- **Repurpose**: Upcycling limbah menjadi produk bernilai (Filamen, Kerajinan).
- **Recycle**: Daur ulang sistematis melalui Bank Sampah.

---

© 2026 **AgriSensa Ecosystem** - *Transforming Waste into Green Gold.*
