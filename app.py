import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="Kalkulator Listrik PSEL")

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
        line-height: 1.6;
    }
    
    /* Highlight variable colors */
    .hl-blue { color: #64b5f6; font-weight: bold; }
    .hl-green { color: #81c784; font-weight: bold; }
    .hl-yellow { color: #ffd54f; font-weight: bold; }
    .hl-orange { color: #ffb74d; font-weight: bold; }
    .hl-red { color: #ef5350; font-weight: bold; }
    
</style>
""", unsafe_allow_html=True)

# --- Konstanta Tetap ---
KAPASITAS_SAMPAH_TON = 1000
JAM_OPERASI = 24
HARGA_BELI_USD = 0.20 # USD 0.2/kWh
HARGA_JUAL_PLN = 1699.53 # Rp 1.699,53/kWh

# --- Header ---
st.markdown('<h1 style="color: white; font-size: 32px; margin-bottom: 20px;">⚡ Kalkulator Subsidi Listrik PSEL</h1>', unsafe_allow_html=True)

# --- Bagian 1: Pengaturan Parameter ---
st.markdown("### ⚙️ Pengaturan Parameter")
p_col1, p_col2 = st.columns(2)

with p_col1:
    kapasitas_mw = st.slider("Kapasitas Listrik per PSEL (MW)", min_value=5, max_value=50, value=15, step=1)

with p_col2:
    kurs_usd = st.slider("Nilai Tukar (Kurs Rupiah per 1 USD)", min_value=14000, max_value=18000, value=16957, step=1)


# --- Perhitungan Matematika ---
# 1. Energi per Ton (e_ton)
kapasitas_kw = kapasitas_mw * 1000
e_ton = (kapasitas_kw * JAM_OPERASI) / KAPASITAS_SAMPAH_TON # Menghasilkan kWh/ton

# 2. Pembelian per Ton (R_ton)
r_ton = HARGA_BELI_USD * e_ton * kurs_usd

# 3. Penjualan PLN ke Pelanggan (S_ton)
s_ton = HARGA_JUAL_PLN * e_ton

# 4. Selisih Bayar (Delta)
selisih_bayar = r_ton - s_ton

def format_num(num):
    return f"{num:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_currency(num):
    return f"Rp {num:,.0f}".replace(",", ".")

# --- Bagian 2: Metrik Utama ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
        <div class="metric-box metric-box-teal">
            <p class="metric-title">Energi per Ton (e_ton)</p>
            <p class="metric-value">{format_num(e_ton)} kWh</p>
            <p class="metric-desc">Dari {kapasitas_mw} MW & {KAPASITAS_SAMPAH_TON} Ton/Hari</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-box metric-box-grey">
            <p class="metric-title">Pembelian per Ton (R_ton)</p>
            <p class="metric-value">{format_currency(r_ton)}</p>
            <p class="metric-desc">USD {HARGA_BELI_USD}/kWh × Kurs Rp {kurs_usd}</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-box metric-box-orange">
            <p class="metric-title">Subsidi Pemerintah (Δ)</p>
            <p class="metric-value">{format_currency(selisih_bayar)}</p>
            <p class="metric-desc">Selisih Bayar per Ton</p>
        </div>
    """, unsafe_allow_html=True)

# --- Bagian 3: Process Thinking & Formulas ---
st.markdown("### 📈 Process Thinking & Formulas")

with st.expander("1. Menghitung Potensi Energi per Ton (e_ton)", expanded=True):
    st.markdown("Menghitung berapa kWh listrik yang dihasilkan dari setiap ton sampah yang diolah PSEL dalam sehari penuh (24 jam).")
    
    html_rumus_1 = f"""
<div class="formula-box">
<p class="formula-text">
<span class="hl-blue">Rumus:</span> e_ton = 
(<span class="hl-green">{kapasitas_kw:,.0f} kW</span> × <span class="hl-yellow">{JAM_OPERASI} jam</span>) ÷ 
<span class="hl-yellow">{KAPASITAS_SAMPAH_TON} ton</span>
<br><br>
<span class="hl-blue">Hasil:</span> <span class="hl-orange">{format_num(e_ton)} kWh/ton</span>
</p>
</div>
"""
    st.markdown(html_rumus_1, unsafe_allow_html=True)

with st.expander("2. Menghitung Pembelian per Ton (R_ton)", expanded=True):
    st.markdown("Menghitung biaya yang dikeluarkan PLN/Pemerintah untuk membeli listrik dari PSEL (menggunakan tarif *Feed-in Tariff* USD dan disesuaikan dengan kurs).")
    
    html_rumus_2 = f"""
<div class="formula-box">
<p class="formula-text">
<span class="hl-blue">Rumus:</span> R_ton = P × e_ton × kurs
<br>
<span class="hl-blue">Hitungan:</span> 
<span class="hl-green">{HARGA_BELI_USD} USD/kWh</span> × 
<span class="hl-yellow">{format_num(e_ton)} kWh/ton</span> × 
<span class="hl-green">{kurs_usd:,}</span>
<br><br>
<span class="hl-blue">Hasil:</span> <span class="hl-orange">{format_currency(r_ton)} /ton</span>
</p>
</div>
"""
    st.markdown(html_rumus_2, unsafe_allow_html=True)

with st.expander("3. Penjualan PLN ke Pelanggan (S_ton)", expanded=False):
    st.markdown("Menghitung nilai jual listrik tersebut jika PLN menjualnya ke masyarakat menggunakan tarif dasar listrik yang berlaku.")
    
    html_rumus_3 = f"""
<div class="formula-box">
<p class="formula-text">
<span class="hl-blue">Rumus:</span> S_ton = P_jual × e_ton
<br>
<span class="hl-blue">Hitungan:</span> 
<span class="hl-green">Rp {HARGA_JUAL_PLN:,.2f} /kWh</span> × 
<span class="hl-yellow">{format_num(e_ton)} kWh/ton</span>
<br><br>
<span class="hl-blue">Hasil:</span> <span class="hl-orange">{format_currency(s_ton)} /ton</span>
</p>
</div>
"""
    st.markdown(html_rumus_3, unsafe_allow_html=True)

with st.expander("4. Selisih Bayar (Jumlah yang harus dibayar Pemerintah)", expanded=True):
    st.markdown("Selisih antara biaya pembelian listrik dari PSEL dan pendapatan dari penjualan ke masyarakat. Angka ini merepresentasikan beban atau subsidi yang ditanggung pemerintah (Tipping Fee/Subsidi).")
    
    html_rumus_4 = f"""
<div class="formula-box">
<p class="formula-text">
<span class="hl-blue">Rumus:</span> Δ = R_ton - S_ton
<br>
<span class="hl-blue">Hitungan:</span> 
<span class="hl-red">{format_currency(r_ton)}</span> - 
<span class="hl-green">{format_currency(s_ton)}</span>
<br><br>
<span class="hl-blue">Hasil (Subsidi):</span> <span class="hl-orange">{format_currency(selisih_bayar)} /ton</span>
</p>
</div>
"""
    st.markdown(html_rumus_4, unsafe_allow_html=True)


# --- Bagian 4: Grafik Analisis Sensitivitas (View Only) ---
st.markdown("---")
st.markdown("### Analisis Sensitivitas: Fluktuasi Kurs terhadap Subsidi per Ton")
st.markdown("Grafik ini bersifat **view-only** untuk melihat tren bagaimana pelemahan atau penguatan Rupiah (Kurs) memengaruhi beban selisih bayar (subsidi) pemerintah.")

# Generate data untuk grafik (Kurs dari 14.000 sampai 18.000)
kurs_range = np.arange(14000, 18001, 100)
df_chart = pd.DataFrame({'Kurs (Rp/USD)': kurs_range})

# Hitung array selisih bayar
r_ton_array = HARGA_BELI_USD * e_ton * df_chart['Kurs (Rp/USD)']
df_chart['Subsidi Pemerintah per Ton (Rp)'] = r_ton_array - s_ton

# Titik saat ini (berdasarkan slider)
mark_data = pd.DataFrame({'Kurs (Rp/USD)': [kurs_usd], 'Subsidi Pemerintah per Ton (Rp)': [selisih_bayar]})

# Plotting dengan Plotly
fig = px.line(df_chart, x='Kurs (Rp/USD)', y='Subsidi Pemerintah per Ton (Rp)', 
              color_discrete_sequence=['#ff9800'], template='plotly_dark')

fig.add_trace(px.scatter(mark_data, x='Kurs (Rp/USD)', y='Subsidi Pemerintah per Ton (Rp)', color_discrete_sequence=['#ef5350']).data[0])

fig.update_layout(
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font_color='#e6e6e6',
    showlegend=False,
    margin=dict(l=0, r=0, t=30, b=0),
    hovermode=False, # Mematikan hover
    dragmode=False   # Mematikan drag/zoom
)
fig.update_yaxes(tickprefix="Rp ", tickformat=",.0f")
fig.update_xaxes(tickprefix="Rp ", tickformat=",.0f")

# Render grafik tanpa modebar
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
