import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="Kalkulator Investasi PSEL")

# --- Custom CSS untuk Tampilan Modern & Menarik ---
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;
        color: #e6e6e6;
        font-family: 'Open Sans', sans-serif;
    }
    
    .metric-box {
        border-radius: 8px;
        padding: 20px;
        color: white;
        text-align: left;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        margin-bottom: 20px;
    }
    .metric-title {
        font-size: 14px;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 8px;
        opacity: 0.9;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin-top: 0px;
        margin-bottom: 5px;
    }
    .metric-desc {
        font-size: 13px;
        opacity: 0.8;
    }

    .metric-box-teal { background-color: #40e0d0; color: #1a1a1a; }
    .metric-box-teal .metric-title, .metric-box-teal .metric-value, .metric-box-teal .metric-desc { color: #1a1a1a; }
    
    .metric-box-grey { background-color: #e0e0e0; color: #1a1a1a; }
    .metric-box-grey .metric-title, .metric-box-grey .metric-value, .metric-box-grey .metric-desc { color: #1a1a1a; }
    
    .metric-box-orange { background-color: #ff9800; }

    /* Styling for formula box dengan Highlight */
    .formula-box {
        background-color: #171717;
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
        margin-bottom: 10px;
        border: 1px solid #333;
    }
    .formula-text {
        font-size: 16px;
        color: #e6e6e6;
        margin: 0;
        font-family: monospace;
    }
    
    /* Highlight variable colors */
    .hl-blue { color: #64b5f6; font-weight: bold; }
    .hl-green { color: #81c784; font-weight: bold; }
    .hl-yellow { color: #ffd54f; font-weight: bold; }
    .hl-orange { color: #ffb74d; font-weight: bold; }
    
</style>
""", unsafe_allow_html=True)

# --- Definisi Konstanta ---
TOTAL_INVESTASI_RP = 91_000_000_000_000 # 91 Triliun
JUMLAH_PSEL = 33

# --- Tampilan Utama ---
st.markdown('<h1 style="color: white; font-size: 32px; margin-bottom: 20px;">♻️ Kalkulator Analisis Investasi PSEL</h1>', unsafe_allow_html=True)

# --- Bagian 1: Pengaturan Parameter ---
st.markdown("### ⚙️ Pengaturan Parameter")
p_col1, p_col2 = st.columns(2)

with p_col1:
    usia_fasilitas = st.slider("Usia Fasilitas Beroperasi (Tahun)", 10, 50, 30, step=1)

with p_col2:
    kapasitas_per_psel = st.slider("Kapasitas Harian per PSEL (Ton/Hari)", 100, 5000, 1000, step=100)

# Perhitungan
total_kapasitas_harian = JUMLAH_PSEL * kapasitas_per_psel
total_sampah_dikelola = total_kapasitas_harian * usia_fasilitas * 365
biaya_per_ton = TOTAL_INVESTASI_RP / total_sampah_dikelola if total_sampah_dikelola > 0 else 0

def format_num(num):
    return f"{num:,.0f}".replace(",", ".")

def format_currency(num):
    return f"Rp {num:,.0f}".replace(",", ".")

# --- Bagian 2: Metrik Utama ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-box metric-box-teal">
            <p class="metric-title">TOTAL KAPASITAS HARIAN</p>
            <p class="metric-value">{format_num(total_kapasitas_harian)} Ton/Hari</p>
            <p class="metric-desc">({JUMLAH_PSEL} PSEL × {format_num(kapasitas_per_psel)} Ton/hari)</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-box metric-box-grey">
            <p class="metric-title">TOTAL SAMPAH DIKELOLA</p>
            <p class="metric-value">{format_num(total_sampah_dikelola)} Ton</p>
            <p class="metric-desc">(Selama {usia_fasilitas} Tahun)</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-box metric-box-orange">
            <p class="metric-title">BIAYA INVESTASI PER TON</p>
            <p class="metric-value">{format_currency(biaya_per_ton)}</p>
            <p class="metric-desc">Investasi / Total Ton</p>
        </div>
    """, unsafe_allow_html=True)

# --- Bagian 3: Process Thinking (Menggunakan Expander) ---
st.markdown("### 📈 Process Thinking & Formulas")

with st.expander("1. Mengapa PSEL adalah Investasi Lingkungan Jangka Panjang?", expanded=False):
    st.markdown("""
    PSEL (Pengolah Sampah Energi Listrik) membutuhkan modal awal yang besar (CAPEX). Namun, jika dilihat dari kacamata umur proyek *(project life)*, biaya ini sebenarnya adalah investasi jangka panjang untuk mengatasi krisis lahan TPA dan menghasilkan energi alternatif.
    """)

with st.expander("2. Perhitungan Kapasitas Total & Masa Hidup", expanded=True):
    st.markdown("Kapasitas Total Harian didapat dari perkalian jumlah PSEL dengan kapasitas masing-masing fasilitas. Total Sampah Dikelola selama masa operasi adalah total harian dikalikan hari dalam setahun, lalu dikalikan usia fasilitas.")
    
    # Perhatikan: HTML ini ditaruh rata kiri (tanpa spasi di awal) agar tidak terbaca sebagai code block oleh Markdown!
    html_rumus_1 = f"""
<div class="formula-box">
<p class="formula-text">
<span class="hl-blue">Rumus:</span> Total Sampah Dikelola = 
(<span class="hl-green">{JUMLAH_PSEL} PSEL</span> × <span class="hl-green">{kapasitas_per_psel} Ton/hari</span>) × 
<span class="hl-yellow">{usia_fasilitas} Tahun</span> × 
<span class="hl-yellow">365 Hari/Tahun</span>
</p>
</div>
"""
    st.markdown(html_rumus_1, unsafe_allow_html=True)

with st.expander("3. Perhitungan Biaya Investasi per Ton", expanded=True):
    st.markdown("Menghitung titik impas atau biaya investasi rata-rata per ton sampah yang berhasil dikelola hingga fasilitas mencapai akhir masa pakainya.")
    
    html_rumus_2 = f"""
<div class="formula-box">
<p class="formula-text">
<span class="hl-blue">Rumus:</span> Biaya per Ton = 
<span class="hl-orange">Total Investasi (Rp 91 Triliun)</span> ÷ 
<span class="hl-green">Total Sampah Dikelola ({format_num(total_sampah_dikelola)} Ton)</span>
<br><br>
<span class="hl-blue">Hasil:</span> {format_currency(biaya_per_ton)}
</p>
</div>
"""
    st.markdown(html_rumus_2, unsafe_allow_html=True)


# --- Bagian 4: Grafik Analisis Sensitivitas (Statik/View Only) ---
st.markdown("---")
st.markdown("### Analisis Sensitivitas: Biaya per Ton vs Usia Fasilitas")
st.markdown("Grafik ini bersifat **view-only** (tidak bisa digeser/di-zoom) untuk melihat proyeksi penurunan biaya per ton jika umur fasilitas semakin lama.")

usia_range = np.arange(10, 51, 1)
current_kapasitas_per_psel = kapasitas_per_psel

df_chart = pd.DataFrame({'Usia Fasilitas': usia_range})
df_chart['Total Sampah Dikelola'] = (JUMLAH_PSEL * current_kapasitas_per_psel) * df_chart['Usia Fasilitas'] * 365
df_chart['Biaya per Ton'] = TOTAL_INVESTASI_RP / df_chart['Total Sampah Dikelola']

current_cost = TOTAL_INVESTASI_RP / ((JUMLAH_PSEL * current_kapasitas_per_psel) * usia_fasilitas * 365)
mark_data = pd.DataFrame({'Usia Fasilitas': [usia_fasilitas], 'Biaya per Ton': [current_cost]})

fig = px.line(df_chart, x='Usia Fasilitas', y='Biaya per Ton', 
              color_discrete_sequence=['#64b5f6'], template='plotly_dark')

fig.add_trace(px.scatter(mark_data, x='Usia Fasilitas', y='Biaya per Ton', color_discrete_sequence=['#ff9800']).data[0])

fig.update_layout(
    xaxis_title='Usia Fasilitas (Tahun)',
    yaxis_title='Biaya Investasi per Ton (Rp)',
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font_color='#e6e6e6',
    showlegend=False,
    margin=dict(l=0, r=0, t=30, b=0),
    hovermode=False, # Mematikan hover
    dragmode=False   # Mematikan drag/zoom agar view-only
)
fig.update_yaxes(tickprefix="Rp ", tickformat=",.0f")

# Menonaktifkan modebar (tombol-tombol plotly) agar benar-benar view-only
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: left; color: #b3b3b3; font-size: 13px;">
    Kalkulator ini disusun berdasarkan data asumsi investasi PSEL.
</div>
""", unsafe_allow_html=True)
