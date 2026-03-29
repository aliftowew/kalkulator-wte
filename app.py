import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="Kalkulator Investasi PSEL")

# --- Custom CSS untuk Tampilan Modern & Menarik ---
# CSS ini akan membuat metric boxes dan formula boxes terlihat rapi seperti di gambar.
st.markdown("""
<style>
    /* Mengatur tema gelap dan font secara keseluruhan */
    .stApp {
        background-color: #1a1a1a;
        color: #e6e6e6;
        font-family: 'Open Sans', sans-serif;
    }
    
    /* Common for all metrics */
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 30px;
    }
    
    .metric-box {
        flex: 1;
        border-radius: 12px;
        padding: 25px;
        color: white;
        text-align: left;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }
    .metric-title {
        font-size: 15px;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 12px;
        opacity: 0.9;
    }
    .metric-value {
        font-size: 40px;
        font-weight: bold;
        margin-top: 0px;
        margin-bottom: 5px;
    }
    .metric-desc {
        font-size: 14px;
        opacity: 0.8;
    }

    /* Teal metric */
    .metric-box-teal {
        background-color: #00897b; /* Teal tua */
    }
    
    /* Grey metric */
    .metric-box-grey {
        background-color: #d8dee9; /* Abu-abu terang */
        color: black;
    }
    .metric-box-grey .metric-value {
        color: black;
    }
    .metric-box-grey .metric-desc {
        color: black;
        opacity: 0.8;
    }
    
    /* Orange metric */
    .metric-box-orange {
        background-color: #ff9800; /* Oranye terang */
    }

    /* Common styling for info blocks */
    .info-block {
        margin-bottom: 25px;
    }
    .process-subheading {
        font-size: 18px;
        font-weight: bold;
        color: #e6e6e6;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    .info-text {
        font-size: 16px;
        color: #b3b3b3;
        margin-bottom: 15px;
        line-height: 1.6;
    }

    /* Styling for formula box */
    .formula-box {
        background-color: #262626;
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
        margin-bottom: 25px;
        border: 1px solid #4d4d4d;
    }
    .formula-title {
        color: #8c8c8c;
        font-size: 16px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .formula-text {
        font-family: monospace;
        font-size: 18px;
        color: #e6e6e6;
        margin-bottom: 10px;
    }
    
    /* Variable specific coloring */
    .var-psel { color: #ffab40; }       /* Kuning/Oranye */
    .var-cap { color: #ffff8d; }        /* Kuning terang */
    .var-d { color: #80cbc4; }         /* Teal muda */
    .var-dy { color: #b2dfdb; }        /* Teal lebih muda */
    .var-t { color: #ffccbc; }         /* Peach muda */
    .var-total_inv { color: #ffab40; }  /* Kuning/Oranye */
    .var-cost_per_ton { color: #ffff8d; } /* Kuning terang */
    .var-num { color: #e6e6e6; }        /* generic for numbers and separators */

</style>
""", unsafe_allow_html=True)

# --- Definisi Konstanta dan Perhitungan ---
# Berdasarkan data dari KPI boxes:
TOTAL_INVESTASI_RP = 91_000_000_000_000 # 91 Triliun Rupiah
JUMLAH_PSEL = 33

# --- Tampilan Utama ---

# Row Header
with st.container():
    col_icon, col_title = st.columns([1, 10])
    with col_icon:
        st.markdown('<h1 style="color: #66bb6a; font-size: 45px; margin-top: -5px;">♻️</h1>', unsafe_allow_html=True)
    with col_title:
        st.markdown('<h1 style="color: white; font-size: 36px; margin-top: 5px;">Kalkulator Analisis Investasi PSEL</h1>', unsafe_allow_html=True)

# Bagian 1: Metrik Utama
st.markdown("---")
# Kita akan mendefinisikan slider terlebih dahulu untuk mendapatkan variabel update
# agar perhitungan KPIbox bisa ikut berubah (interaktif).

# Bagian 2: Pengaturan Parameter
# st.markdown("---")
st.header("⚙️ Pengaturan Parameter")

# Parameter columns
p_col1, p_col2 = st.columns(2)

with p_col1:
    st.markdown("**Usia Fasilitas Beroperasi (Tahun)**")
    # Slider 1: 10 hingga 50 tahun, default 30
    usia_fasilitas = st.slider("Usia Fasilitas Beroperasi (Tahun)", 10, 50, 30, step=1, label_visibility="collapsed")

with p_col2:
    st.markdown("**Kapasitas Harian per PSEL (Ton/Hari)**")
    # Slider 2: 100 hingga 5000 ton/hari, default 1000
    kapasitas_per_psel = st.slider("Kapasitas Harian per PSEL (Ton/Hari)", 100, 5000, 1000, step=100, label_visibility="collapsed")

# Lakukan perhitungan berdasarkan input slider
total_kapasitas_harian = JUMLAH_PSEL * kapasitas_per_psel
total_sampah_dikelola = total_kapasitas_harian * usia_fasilitas * 365
biaya_per_ton = TOTAL_INVESTASI_RP / total_sampah_dikelola if total_sampah_dikelola > 0 else 0

# Format angka untuk tampilan
def format_num(num):
    return f"{num:,.0f}".replace(",", ".")

def format_currency(num):
    return f"Rp {num:,.0f}".replace(",", ".")

# Render metric boxes dalam HTML/CSS agar terlihat persis seperti di gambar
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

# Bagian 3: Process Thinking
st.markdown("---")
st.header("📈 Process Thinking & Formulas")

# Subsection 1
st.markdown("""
<div class="info-block">
    <p class="process-subheading">👇 1. Mengapa PSEL adalah Investasi Lingkungan Jangka Panjang?</p>
</div>
""", unsafe_allow_html=True)

# Subsection 2
st.markdown(f"""
<div class="info-block">
    <p class="process-subheading">👇 2. Perhitungan Kapasitas Total & Masa Hidup</p>
    <p class="info-text">Kapasitas Total = (Jumlah PSEL × Kapasitas/PSEL) × d × d_y × t</p>
    <p class="info-text">Rumus: Total Sampah Dikelola = ({JUMLAH_PSEL} PSEL) × 365 Hari × (Selama {usia_fasilitas} Tahun)</p>
    
    <div class="formula-box">
        <p class="formula-text">
            Rumus: Total Sampah Dikelola = (
            <span class="var-psel">Jumlah PSEL</span> <span class="var-num">×</span>
            <span class="var-cap">Kapasitas/PSEL</span>)
            <span class="var-num">×</span>
            <span class="var-d">d</span>
            <span class="var-num">×</span>
            <span class="var-dy">d_y</span>
            <span class="var-num">×</span>
            <span class="var-t">t</span>
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Subsection 3
st.markdown("""
<div class="info-block">
    <p class="process-subheading">👇 3. Perhitungan Biaya Investasi per Ton</p>
    <p class="info-text">Menghitung Biaya Investasi Per Ton Sampah Yang Dikelola.</p>
    
    <div class="formula-box">
        <p class="formula-text">
            Rumus: Biaya per Ton = \\frac{{
            <span class="var-total_inv">Total Investasi</span>}}
            {{<span class="var-cost_per_ton">Total Sampah Dikelola</span>}}
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Bagian 4: Grafik Analisis Sensitivitas
st.markdown("---")
st.header("Analisis Sensitivitas")
st.markdown("**Biaya per Ton vs Usia Fasilitas**")

# Mempersiapkan data untuk grafik
# Generate rentang usia fasilitas: 10 hingga 50
usia_range = np.arange(10, 51, 1)

# Menggunakan nilai kapasitas per PSEL saat ini dari slider
current_kapasitas_per_psel = kapasitas_per_psel

# Buat dataframe
df_chart = pd.DataFrame({'Usia Fasilitas': usia_range})
df_chart['Total Sampah Dikelola'] = (JUMLAH_PSEL * current_kapasitas_per_psel) * df_chart['Usia Fasilitas'] * 365
df_chart['Biaya per Ton'] = TOTAL_INVESTASI_RP / df_chart['Total Sampah Dikelola']

# Filter data untuk menandai titik saat ini di grafik
current_cost = TOTAL_INVESTASI_RP / ((JUMLAH_PSEL * current_kapasitas_per_psel) * usia_fasilitas * 365)
mark_data = pd.DataFrame({'Usia Fasilitas': [usia_fasilitas], 'Biaya per Ton': [current_cost]})

# Plotting dengan Plotly
fig = px.line(df_chart, x='Usia Fasilitas', y='Biaya per Ton', markers=True, 
              color_discrete_sequence=['white'], template='plotly_dark')

# Highlight titik saat ini
fig.add_trace(px.scatter(mark_data, x='Usia Fasilitas', y='Biaya per Ton', color_discrete_sequence=['gold']).data[0])

fig.update_layout(
    xaxis_title='Usia Fasilitas (Tahun)',
    yaxis_title='Biaya Investasi per Ton (Rp)',
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font_color='#e6e6e6',
    showlegend=False
)
fig.update_yaxes(tickprefix="Rp ", tickformat=",.0f")

# Render grafik
st.plotly_chart(fig, use_container_width=True)

# Bagian 5: Footer
st.markdown("---")
# Custom HTML untuk footer dengan gold icons
st.markdown("""
<div style="text-align: center; color: #b3b3b3; margin-top: 20px; font-size: 14px;">
    Kalkulator ini disusun berdasarkan data asumsi investasi PSEL.
    <br/>
    <span style="font-size: 16px; color: gold;">★★★</span>
</div>
""", unsafe_allow_html=True)
