# Bank Sampah Terpadu (Integrated Waste Management System)

Modul ini adalah bagian dari ekosistem **AgriSensa**, yang didedikasikan untuk pengelolaan sampah berbasis **Circular Economy** dengan mengadaptasi disiplin pengelolaan sampah ala Jepang.

## Fitur Utama

- **Dashboard Monitoring**: Visualisasi real-time dari sampah yang terkumpul.
- **Dashboard Google Form**: Menarik data response Google Form dari Google Sheet dan menampilkan:
  - Database Nasabah
  - Alur Sampah
  - Pembukuan
  - Keuangan
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

## Integrasi Google Form

1. Buka Google Form Anda dan masuk ke tab **Responses**.
2. Klik ikon Google Sheet untuk membuat lembar response.
3. Ubah sharing Google Sheet menjadi **Anyone with the link can view**.
4. Jalankan app Streamlit, lalu buka menu **Dashboard Google Form**.
5. Tempel URL Google Sheet response ke field yang tersedia.

Opsional via secrets Streamlit:

```toml
# .streamlit/secrets.toml
BANK_SAMPAH_SHEET_URL = "https://docs.google.com/spreadsheets/d/<sheet_id>/edit#gid=0"
```

## Teknologi

- Built with [Streamlit](https://streamlit.io)
- Plotly untuk Visualisasi Data
- Pandas untuk Pengolahan Data

---
Part of AgriSensa Ecosystem.
