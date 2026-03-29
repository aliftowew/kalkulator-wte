import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="Kalkulator Listrik PSEL")

# --- Custom CSS ---
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

    .metric-box-teal { background-color: #004d40; color: #e0f2f1; }
    .metric-box-teal .metric-title, .metric-box-teal .metric-value, .metric-box-teal .metric-desc { color: #e0f2f1; }
    
    .metric-box-grey { background-color: #212121; color: #e6e6e6; border: 1px solid #424242; }
    .metric-box-grey .metric-title, .metric-box-grey .metric-value, .metric-box-grey .metric-desc { color: #e6e6e6; }
    
    .metric-box-red { background-color: #b71c1c; color: #ffebee; }
    .metric-box-red .metric-title, .metric-box-red .metric-value, .metric-box-red .metric-desc { color: #ffebee; }
    
    .latex-box {
        background-color: #171717;
        border-radius: 8px;
        padding: 15px;
        margin-top: 10px;
        margin-bottom: 10px;
        border: 1px solid #333;
    }
</style>
""", unsafe_allow_html=True)

# --- Konstanta Tetap ---
KAPASITAS_SAMPAH_TON = 1000
JAM_OPERASI = 24
HARGA_BELI_USD = 0.20 # USD 0.2/kWh (Feed-in Tariff PSEL)

# --- Header ---
st.markdown('<h1 style="color: white; font-size: 32px; margin-bottom: 20px;">⚡ Kalkulator Subsidi Listrik PSEL</h1>', unsafe_allow_html=True)

# --- Bagian 1: Pengaturan Parameter ---
st.markdown("### ⚙️ Pengaturan Parameter")
p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    kapasitas_mw = st.slider("Kapasitas PSEL (MW)", min_value=5, max_value=50, value=25, step=1)

with p_col2:
    kurs_usd = st.number_input("Kurs (Rp/USD)", min_value=14000, max_value=18000, value=16957, step=100)

with p_col3:
    bpp_usd = st.number_input("BPP Normal (USD/kWh)", min_value=0.010, max_value=0.200, value=0.068, step=0.001, format="%.3f")

# --- Perhitungan Matematika ---
kapasitas_kw = kapasitas_mw * 1000
e_ton = (kapasitas_kw * JAM_OPERASI) / KAPASITAS_SAMPAH_TON 
r_ton = HARGA_BELI_USD * e_ton * kurs_usd
bpp_ton = bpp_usd * e_ton * kurs_usd
selisih_bayar = r_ton - bpp_ton

def format_num(num):
    return f"{num:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_currency(num):
    return f"Rp {num:,.0f}".replace(",", ".")

# String formating untuk LaTeX
kw_str = f"{kapasitas_kw:,.0f}".replace(",", ".")
e_ton_str = f"{e_ton:,.1f}".replace(".", ",")
kurs_str = f"{kurs_usd:,.0f}".replace(",", ".")
bpp_usd_str = f"{bpp_usd:.3f}".replace(".", ",")
r_ton_str = f"{r_ton:,.0f}".replace(",", ".")
bpp_ton_str = f"{bpp_ton:,.0f}".replace(",", ".")
selisih_str = f"{selisih_bayar:,.0f}".replace(",", ".")

# --- Bagian 2: Metrik Utama ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-box metric-box-teal">
            <p class="metric-title">Listrik Dihasilkan PSEL</p>
            <p class="metric-value">{format_num(e_ton)} kWh</p>
            <p class="metric-desc">Dari {kapasitas_mw} MW & {KAPASITAS_SAMPAH_TON} Ton/Hari</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-box metric-box-grey">
            <p class="metric-title">Pembelian per Ton</p>
            <p class="metric-value">{format_currency(r_ton)}</p>
            <p class="metric-desc">USD {HARGA_BELI_USD}/kWh × Kurs Rp {kurs_str}</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-box metric-box-red">
            <p class="metric-title">Subsidi Pemerintah</p>
            <p class="metric-value">{format_currency(selisih_bayar)}</p>
            <p class="metric-desc">Selisih Bayar per Ton</p>
        </div>
    """, unsafe_allow_html=True)

# --- Bagian 3: Process Thinking & Formulas (LaTeX Render) ---
st.markdown("### 📈 Process Thinking & Formulas")

with st.expander("1. Menghitung Listrik Dihasilkan PSEL ($e_{ton}$)", expanded=True):
    st.markdown("Menghitung berapa kWh listrik yang dihasilkan dari setiap ton sampah yang diolah PSEL dalam sehari penuh (24 jam).")
    st.markdown('<div class="latex-box">', unsafe_allow_html=True)
    st.latex(r"e_{ton} = \frac{\text{Kapasitas (kW)} \times \text{Waktu Operasi (Jam)}}{\text{Kapasitas Sampah (Ton)}}")
    st.latex(rf"e_{{ton}} = \frac{{{kw_str} \text{{ kW}} \times {JAM_OPERASI} \text{{ jam}}}}{{{KAPASITAS_SAMPAH_TON} \text{{ ton}}}}")
    st.latex(rf"e_{{ton}} = {e_ton_str} \text{{ kWh/ton}}")
    st.markdown('</div>', unsafe_allow_html=True)

with st.expander("2. Menghitung Pembelian per Ton ($R_{ton}$)", expanded=True):
    st.markdown("Menghitung biaya yang dikeluarkan PLN untuk membeli listrik dari PSEL menggunakan tarif khusus *Feed-in Tariff* (USD) yang disesuaikan dengan kurs.")
    st.markdown('<div class="latex-box">', unsafe_allow_html=True)
    st.latex(r"R_{ton} = P_{beli} \times e_{ton} \times \text{Kurs USD}")
    st.latex(rf"R_{{ton}} = {HARGA_BELI_USD} \text{{ USD/kWh}} \times {e_ton_str} \text{{ kWh/ton}} \times {kurs_str}")
    st.latex(rf"R_{{ton}} = \text{{Rp }} {r_ton_str} \text{{ /ton}}")
    st.markdown('</div>', unsafe_allow_html=True)

with st.expander("3. Biaya Pokok Produksi (BPP) Listrik Normal ($BPP_{ton}$)", expanded=False):
    st.markdown("Menghitung biaya normal yang dikeluarkan PLN jika memproduksi listrik sendiri (rata-rata nasional), yang direpresentasikan dalam USD/kWh.")
    st.markdown('<div class="latex-box">', unsafe_allow_html=True)
    st.latex(r"BPP_{ton} = BPP \times e_{ton} \times \text{Kurs USD}")
    st.latex(rf"BPP_{{ton}} = {bpp_usd_str} \text{{ USD/kWh}} \times {e_ton_str} \text{{ kWh/ton}} \times {kurs_str}")
    st.latex(rf"BPP_{{ton}} = \text{{Rp }} {bpp_ton_str} \text{{ /ton}}")
    st.markdown('</div>', unsafe_allow_html=True)

with st.expander("4. Selisih Bayar / Subsidi Pemerintah ($\Delta$)", expanded=True):
    st.markdown("Negara harus menanggung selisih antara tingginya harga beli dari PSEL dengan biaya pokok (BPP) normal. Inilah nilai subsidi sebenarnya per ton sampah.")
    st.markdown('<div class="latex-box">', unsafe_allow_html=True)
    st.latex(r"\Delta = R_{ton} - BPP_{ton}")
    st.latex(rf"\Delta = {r_ton_str} - {bpp_ton_str}")
    st.latex(rf"\Delta = \text{{Rp }} {selisih_str} \text{{ /ton}}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Bagian 4: Grafik Analisis Sensitivitas ---
st.markdown("---")
st.markdown("### Analisis Sensitivitas: Fluktuasi Kurs terhadap Subsidi per Ton")
st.markdown("Grafik ini memproyeksikan tren bagaimana pelemahan atau penguatan Rupiah memengaruhi beban subsidi pemerintah, dengan asumsi BPP konstan.")

# Generate data untuk grafik
kurs_range = np.arange(14000, 18001, 100)
df_chart = pd.DataFrame({'Kurs (Rp/USD)': kurs_range})

# Hitung array r_ton dan bpp_ton
r_ton_array = HARGA_BELI_USD * e_ton * df_chart['Kurs (Rp/USD)']
bpp_ton_array = bpp_usd * e_ton * df_chart['Kurs (Rp/USD)']
df_chart['Subsidi Pemerintah per Ton (Rp)'] = r_ton_array - bpp_ton_array

mark_data = pd.DataFrame({'Kurs (Rp/USD)': [kurs_usd], 'Subsidi Pemerintah per Ton (Rp)': [selisih_bayar]})

# Plotting
fig = px.line(df_chart, x='Kurs (Rp/USD)', y='Subsidi Pemerintah per Ton (Rp)', 
              color_discrete_sequence=['#b71c1c'], template='plotly_dark')

fig.add_trace(px.scatter(mark_data, x='Kurs (Rp/USD)', y='Subsidi Pemerintah per Ton (Rp)', color_discrete_sequence=['white']).data[0])

fig.update_layout(
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font_color='#e6e6e6',
    showlegend=False,
    margin=dict(l=0, r=0, t=30, b=0),
    hovermode=False, 
    dragmode=False   
)
fig.update_yaxes(tickprefix="Rp ", tickformat=",.0f")
fig.update_xaxes(tickprefix="Rp ", tickformat=",.0f")

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- Footer Branding Simpel ---
st.markdown("""
<div style="text-align: center; color: #b3b3b3; font-size: 14px; margin-top: 50px; padding-top: 20px; border-top: 1px solid #333;">
    <b>Semua Bisa Dihitung</b><br>
    <i>by Alif Towew</i>
</div>
<div style="text-align: center; color: #b3b3b3; font-size: 12px; margin-top: 10px;">
    Kalkulator ini disusun berdasarkan data asumsi investasi PSEL dan analisis makroekonomi.
</div>
""", unsafe_allow_html=True)
