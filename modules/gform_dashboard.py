import re
from typing import Dict, Iterable, Optional

import pandas as pd
import plotly.express as px
import streamlit as st


EXPECTED_FIELDS: Dict[str, Iterable[str]] = {
    "tanggal": ("timestamp", "tanggal", "date"),
    "nama_nasabah": ("nama nasabah", "nasabah", "nama", "name"),
    "rt_rw": ("rt/rw", "rt rw", "rt", "rw"),
    "jenis_sampah": ("jenis sampah", "kategori sampah", "sampah"),
    "berat_kg": ("berat", "kg", "berat (kg)", "berat_kg"),
    "harga_per_kg": ("harga", "harga/kg", "harga per kg", "rate"),
    "nilai_rp": ("nilai", "total", "rupiah", "rp", "subtotal"),
    "status_alur": ("status", "alur", "proses", "tahap"),
    "pembayaran": ("pembayaran", "dibayar", "cash out", "transfer"),
}


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", str(text).strip().lower()).strip()


def _find_col(columns: Iterable[str], aliases: Iterable[str]) -> Optional[str]:
    normalized = {_slugify(col): col for col in columns}
    for alias in aliases:
        alias_key = _slugify(alias)
        for key, original in normalized.items():
            if alias_key in key:
                return original
    return None


def _normalize_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()
    mapped_cols = {}

    for field_name, aliases in EXPECTED_FIELDS.items():
        found = _find_col(df.columns, aliases)
        if found:
            mapped_cols[field_name] = found

    if "tanggal" in mapped_cols:
        df["tanggal"] = pd.to_datetime(df[mapped_cols["tanggal"]], errors="coerce")
    else:
        df["tanggal"] = pd.NaT

    if "nama_nasabah" in mapped_cols:
        df["nama_nasabah"] = df[mapped_cols["nama_nasabah"]].astype(str)
    else:
        df["nama_nasabah"] = "Tidak Diketahui"

    if "jenis_sampah" in mapped_cols:
        df["jenis_sampah"] = df[mapped_cols["jenis_sampah"]].astype(str)
    else:
        df["jenis_sampah"] = "Lainnya"

    if "status_alur" in mapped_cols:
        df["status_alur"] = df[mapped_cols["status_alur"]].fillna("Belum Diproses").astype(str)
    else:
        df["status_alur"] = "Belum Diproses"

    for num_field in ("berat_kg", "harga_per_kg", "nilai_rp", "pembayaran"):
        if num_field in mapped_cols:
            parsed = (
                df[mapped_cols[num_field]]
                .astype(str)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
                .str.replace(r"[^0-9.\-]", "", regex=True)
            )
            df[num_field] = pd.to_numeric(parsed, errors="coerce").fillna(0.0)
        else:
            df[num_field] = 0.0

    if (df["nilai_rp"] <= 0).all() and (df["berat_kg"] > 0).any() and (df["harga_per_kg"] > 0).any():
        df["nilai_rp"] = df["berat_kg"] * df["harga_per_kg"]

    return df


@st.cache_data(ttl=120)
def _load_gsheet_csv(csv_url: str) -> pd.DataFrame:
    return pd.read_csv(csv_url)


def _build_sheet_csv_url(sheet_url: str) -> str:
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", sheet_url)
    if not match:
        return ""
    spreadsheet_id = match.group(1)
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv"


def show():
    st.title("Google Form Bank Sampah")
    st.caption("Integrasi data Google Form -> visual dashboard operasional bank sampah.")

    st.markdown(
        """
        Gunakan 2 langkah ini:
        1. Buka tab **Responses** di Google Form Anda -> klik ikon Google Sheet (buat sheet respon).
        2. Set sharing sheet menjadi **Anyone with the link can view**, lalu tempel URL sheet di bawah.
        """
    )

    default_form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdXSuFX_RaEspHEZ7HLsdQ4cGHYJUO4IUQrE8qk1DexHJ9-HA/viewform"
    default_sheet_url = st.secrets.get("BANK_SAMPAH_SHEET_URL", "")

    with st.expander("Konfigurasi Integrasi Google", expanded=True):
        st.link_button("Buka Google Form Anda", default_form_url, use_container_width=True)
        sheet_url = st.text_input(
            "URL Google Sheet Responses",
            value=default_sheet_url,
            placeholder="https://docs.google.com/spreadsheets/d/<sheet_id>/edit#gid=0",
            help="Tempel URL Google Sheet yang menampung response Google Form.",
        )
        csv_url = _build_sheet_csv_url(sheet_url) if sheet_url else ""
        if csv_url:
            st.code(csv_url, language="text")
            st.caption("URL CSV di atas dipakai Streamlit untuk mengambil data realtime.")

    if not sheet_url:
        st.info("Masukkan URL Google Sheet terlebih dulu untuk memuat data.")
        return

    csv_url = _build_sheet_csv_url(sheet_url)
    if not csv_url:
        st.error("Format URL Google Sheet tidak valid.")
        return

    try:
        raw_df = _load_gsheet_csv(csv_url)
    except Exception as exc:
        st.error(
            "Gagal mengambil data Google Sheet. Pastikan sheet public-view dan URL benar."
        )
        st.exception(exc)
        return

    if raw_df.empty:
        st.warning("Data response masih kosong.")
        return

    df = _normalize_dataframe(raw_df)
    st.success(f"Data berhasil dimuat: {len(df)} baris transaksi.")

    tab_nasabah, tab_alur, tab_pembukuan, tab_keuangan, tab_data = st.tabs(
        ["Database Nasabah", "Alur Sampah", "Pembukuan", "Keuangan", "Data Mentah"]
    )

    with tab_nasabah:
        st.subheader("Database Nasabah")
        nasabah_df = (
            df.groupby("nama_nasabah", as_index=False)
            .agg(
                total_transaksi=("nama_nasabah", "count"),
                total_berat_kg=("berat_kg", "sum"),
                total_nilai_rp=("nilai_rp", "sum"),
            )
            .sort_values("total_nilai_rp", ascending=False)
        )
        st.dataframe(nasabah_df, use_container_width=True, hide_index=True)

        if not nasabah_df.empty:
            fig_nasabah = px.bar(
                nasabah_df.head(10),
                x="nama_nasabah",
                y="total_nilai_rp",
                title="Top 10 Nasabah berdasarkan Nilai Setoran",
            )
            st.plotly_chart(fig_nasabah, use_container_width=True)

    with tab_alur:
        st.subheader("Alur Sampah")
        flow_df = df.groupby(["status_alur", "jenis_sampah"], as_index=False)["berat_kg"].sum()
        st.dataframe(flow_df, use_container_width=True, hide_index=True)

        if not flow_df.empty:
            fig_flow = px.sunburst(
                flow_df,
                path=["status_alur", "jenis_sampah"],
                values="berat_kg",
                title="Distribusi Alur Proses Sampah",
            )
            st.plotly_chart(fig_flow, use_container_width=True)

    with tab_pembukuan:
        st.subheader("Pembukuan")
        book_df = df.copy()
        book_df["bulan"] = book_df["tanggal"].dt.to_period("M").astype(str)
        monthly_book = (
            book_df.groupby("bulan", as_index=False)
            .agg(
                jumlah_transaksi=("nama_nasabah", "count"),
                total_berat_kg=("berat_kg", "sum"),
                total_nilai_rp=("nilai_rp", "sum"),
                total_pembayaran=("pembayaran", "sum"),
            )
            .sort_values("bulan")
        )
        st.dataframe(monthly_book, use_container_width=True, hide_index=True)

        if not monthly_book.empty:
            fig_book = px.line(
                monthly_book,
                x="bulan",
                y=["total_nilai_rp", "total_pembayaran"],
                markers=True,
                title="Tren Pembukuan Bulanan",
            )
            st.plotly_chart(fig_book, use_container_width=True)

    with tab_keuangan:
        st.subheader("Keuangan")
        total_pendapatan = float(df["nilai_rp"].sum())
        total_pengeluaran = float(df["pembayaran"].sum())
        saldo = total_pendapatan - total_pengeluaran

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Pendapatan", f"Rp {total_pendapatan:,.0f}")
        c2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
        c3.metric("Saldo", f"Rp {saldo:,.0f}", delta=f"{(saldo / total_pendapatan * 100) if total_pendapatan else 0:.1f}%")

        finance_df = pd.DataFrame(
            {
                "Komponen": ["Pendapatan", "Pengeluaran", "Saldo"],
                "Nilai": [total_pendapatan, total_pengeluaran, saldo],
            }
        )
        fig_fin = px.bar(finance_df, x="Komponen", y="Nilai", color="Komponen", title="Ringkasan Keuangan")
        st.plotly_chart(fig_fin, use_container_width=True)

    with tab_data:
        st.subheader("Data Mentah dari Google Form")
        st.dataframe(raw_df, use_container_width=True, hide_index=True)
        st.download_button(
            "Unduh CSV Response",
            raw_df.to_csv(index=False).encode("utf-8"),
            file_name="bank_sampah_response.csv",
            mime="text/csv",
        )
