import streamlit as st
import pandas as pd
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Kalkulator Investasi PSEL", layout="wide")

st.title("♻️ Kalkulator Analisis Investasi PSEL")
st.markdown("Dashboard ini menganalisis biaya investasi per ton sampah yang dikelola berdasarkan total nilai investasi, umur fasilitas, dan kapasitas harian.")

# --- INPUT SIDEBAR (SLIDER) ---
st.sidebar.header("⚙️ Parameter Asumsi")
st.sidebar.markdown("Geser angka di bawah ini untuk melihat simulasi:")

years = st.sidebar.slider(
    "Usia Fasilitas Beroperasi (Tahun)", 
    min_value=5, max_value=50, value=30, step=1
)

capacity_per_psel = st.sidebar.slider(
    "Kapasitas per PSEL (Ton/Hari)", 
    min_value=100, max_value=5000, value=1000, step=100
)

# --- KONSTANTA DARI DATA ---
total_investasi_t = 91 # dalam Triliun Rupiah
total_investasi_rp = total_investasi_t * 1_000_000_000_000
jumlah_psel = 33
hari_per_tahun = 365

# --- PERHITUNGAN MATEMATIKA ---
total_kapasitas_harian = jumlah_psel * capacity_per_psel
total_kapasitas_umur = years * hari_per_tahun * total_kapasitas_harian
investasi_per_ton = total_investasi_rp / total_kapasitas_umur if total_kapasitas_umur > 0 else 0

# --- TAMPILAN METRIK UTAMA ---
st.header("📊 Ringkasan Hasil")
col1, col2, col3 = st.columns(3)
col1.metric("Total Kapasitas Harian", f"{total_kapasitas_harian:,.0f} Ton/Hari")
col2.metric("Total Sampah Dikelola", f"{total_kapasitas_umur:,.0f} Ton")
col3.metric("Biaya Investasi per Ton", f"Rp {investasi_per_ton:,.0f}")

# --- PENJELASAN LOGIKA & RUMUS ---
st.header("🧠 Proses Berpikir & Formula")
st.markdown("""
Perhitungan ini didasarkan pada parameter tetap berikut:
- **Total Investasi ($I$)** = 91 Triliun Rupiah
- **Jumlah PSEL ($n$)** = 33 fasilitas
- **Hari per tahun ($d$)** = 365 hari

Berikut adalah tahapan perhitungannya beserta simbolnya:
""")

st.subheader("1. Menghitung Total Kapasitas Harian ($C_{total}$)")
st.markdown("Kapasitas total per hari didapat dengan mengalikan jumlah fasilitas dengan kapasitas masing-masing fasilitas ($C_{psel}$).")
st.latex(r"C_{total} = n \times C_{psel}")
st.markdown(f"**Simulasi Saat Ini:** 33 × {capacity_per_psel} = **{total_kapasitas_harian:,}** ton/hari")

st.subheader("2. Menghitung Total Kapasitas Selama Beroperasi ($C_{life}$)")
st.markdown("Total sampah yang dikelola adalah kapasitas harian dikalikan jumlah hari dalam setahun, lalu dikalikan dengan usia fasilitas beroperasi ($t$).")
st.latex(r"C_{life} = t \times d \times C_{total}")
st.markdown(f"**Simulasi Saat Ini:** {years} × 365 × {total_kapasitas_harian:,} = **{total_kapasitas_umur:,}** ton")

st.subheader("3. Menghitung Biaya Investasi per Ton ($Cost_{ton}$)")
st.markdown("Terakhir, total nilai investasi dibagi dengan total kapasitas sampah yang dikelola selama masa hidup fasilitas.")
st.latex(r"Cost_{ton} = \frac{I}{C_{life}}")
st.markdown(f"**Simulasi Saat Ini:** 91.000.000.000.000 / {total_kapasitas_umur:,} = **Rp {investasi_per_ton:,.0f}**")

# --- VISUALISASI GRAFIK ---
st.header("📈 Analisis Sensitivitas (Grafik)")
st.markdown("Grafik ini memproyeksikan perubahan **Biaya Investasi per Ton** seiring bertambahnya atau berkurangnya **Usia Fasilitas**, dengan asumsi kapasitas per PSEL yang Anda pilih saat ini.")

# Membuat dataframe untuk grafik
df_plot = pd.DataFrame({'Usia Fasilitas (Tahun)': range(10, 51)})
df_plot['Total Sampah (Ton)'] = df_plot['Usia Fasilitas (Tahun)'] * hari_per_tahun * total_kapasitas_harian
df_plot['Biaya Investasi per Ton (Rp)'] = total_investasi_rp / df_plot['Total Sampah (Ton)']

# Plotting menggunakan Plotly Express
fig = px.line(df_plot, x='Usia Fasilitas (Tahun)', y='Biaya Investasi per Ton (Rp)',
              markers=True, 
              title=f"Kurva Biaya Investasi per Ton vs Usia Fasilitas ({capacity_per_psel} ton/hari per PSEL)")

# Menyoroti titik yang sedang dipilih pada slider
fig.add_scatter(x=[years], y=[investasi_per_ton], mode='markers', 
                marker=dict(color='red', size=12), name='Skenario Terpilih')

st.plotly_chart(fig, use_container_width=True)
