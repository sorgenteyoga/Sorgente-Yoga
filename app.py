import streamlit as st
from Bio import Entrez

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- DESIGN AVANZATO ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Lato:wght@300;400&display=swap" rel="stylesheet">
    <style>
    .stApp { background-color: #FDFCF0; }
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1A2E44 !important; }
    p, li, div, span { font-family: 'Lato', sans-serif !important; color: #4A3E3E; }
    .card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #C5A059;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #1A2E44 !important;
        color: #FDFCF0 !important;
        border-radius: 20px !important;
        border: none !important;
        padding: 10px 25px !important;
    }
    [data-testid="stSidebar"] { background-color: #1A2E44 !important; }
    [data-testid="stSidebar"] * { color: #FDFCF0 !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🧘<br>SORGENTE YOGA</h2>", unsafe_allow_html=True)
    st.write("---")
    st.markdown("<p style='text-align: center; opacity: 0.8;'>Ricerca e cura di</p>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #C5A059 !important;'>Luca Valenti</h3>", unsafe_allow_html=True)

# --- INTESTAZIONE ---
st.markdown("<h1 style='text-align: center; font-size: 3rem;'>SORGENTE YOGA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic; font-size: 1.2rem;'>L'unione tra il rigore dei manoscritti e l'evidenza della scienza.</p>", unsafe_allow_html=True)
st.write("<br>", unsafe_allow_html=True)

# --- CONTENUTO ---
tab1, tab2, tab3 = st.tabs(["📜 TRADIZIONE", "🔬 SCIENZA", "🏥 TERAPIA"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""<div class='card'>
            <h3>Journal of Yoga Studies</h3>
            <p>Esplora l'eccellenza della ricerca indologica. Studi peer-reviewed sui testi sanscriti.</p>
            <a href='https://journalofyogastudies.org/index.php/JoYS/issue/archive' target='_blank' style='color:#C5A059; text-decoration:none; font-weight:bold;'>Vai all'Archivio →</a>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='card'>
            <h3>KYM Tradition</h3>
            <p>Insegnamenti di T. Krishnamacharya. Risorse su Viniyoga e pranayama tradizionale.</p>
            <a href='https://www.kym.org/' target='_blank' style='color:#C5A059; text-decoration:none; font-weight:bold;'>Visita il Portale →</a>
        </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='card'><h3>Osservatorio Scientifico</h3><p>Monitoraggio database medici mondiali.</p></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 Studi Dr. Sat Bir Khalsa"):
            st.info("Ricerca in corso...")
    with c2:
        if st.button("🧬 HRV & Sistema Nervoso"):
            st.info("Interrogando PubMed...")

with tab3:
    st.markdown("""<div class='card'>
        <h3>IAYT Resources</h3>
        <p>Standard internazionali per lo Yoga Therapy clinico.</p>
        <a href='https://www.iayt.org/' target='_blank' style='color:#C5A059; text-decoration:none; font-weight:bold;'>Accedi al Database →</a>
    </div>""", unsafe_allow_html=True)
