# Bank Sampah Terpadu (Integrated Waste Management System)

Modul ini adalah bagian dari ekosistem **AgriSensa**, yang didedikasikan untuk pengelolaan sampah berbasis **Circular Economy** dengan mengadaptasi disiplin pengelolaan sampah ala Jepang.

## Fitur Utama

- **Dashboard Monitoring**: Visualisasi real-time dari sampah yang terkumpul.
- **Standar Pemilahan Jepang**:
  - *Moeru Gomi* (Sampah yang bisa dibakar/Organik)
  - *Shigen Gomi* (Sampah Daur Ulang bernilai)
  - *Moenai Gomi* (Tidak bisa dibakar)
- **Kalkulator "Trash to Cash"**: Mengubah persepsi sampah menjadi "Emas Hijau" dengan kalkulasi nilai ekonomi presisi.
- **Integrasi AgriSensa**: Fokus pada transformasi limbah organik menjadi sarana produksi pertanian (Kompos/Pakan Maggot).

## Cara Menjalankan

1. Pastikan python terinstall.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```bash
   streamlit run app.py
   ```

## Teknologi

- Built with [Streamlit](https://streamlit.io)
- Plotly untuk Visualisasi Data
- Pandas untuk Pengolahan Data

---
Part of AgriSensa Ecosystem.
