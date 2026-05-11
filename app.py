import streamlit as st
from Bio import Entrez

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- DESIGN BLINDATO (Rimosse scritte in alto) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400&display=swap" rel="stylesheet">
    <style>
    .stApp { background-color: #FDFCF0; }
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1A2E44 !important; }
    p, div, span, label { font-family: 'Lato', sans-serif !important; color: #4A3E3E; }
    
    .editor-container {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        min-height: 700px;
        border-top: 5px solid #1A2E44;
    }
    
    .sidebar-button-container {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #C5A059;
        margin-bottom: 20px;
    }

    .stButton>button {
        background-color: #1A2E44 !important;
        color: #FDFCF0 !important;
        border-radius: 5px !important;
        font-weight: bold !important;
        height: 3em !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONE PUBMED ---
def cerca_pubmed(query):
    Entrez.email = "tua_email@esempio.com"
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=3)
        record = Entrez.read(handle)
        res = []
        for id in record["IdList"]:
            h = Entrez.esummary(db="pubmed", id=id)
            r = Entrez.read(h)
            res.append({"t": r[0]['Title'], "l": f"https://pubmed.ncbi.nlm.nih.gov/{id}/"})
        return res
    except: return []

# --- LAYOUT ---
col_main, col_tools = st.columns([0.65, 0.35], gap="large")

with col_main:
    st.markdown("<h1>SORGENTE YOGA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-style: italic; margin-bottom: 20px;'>Editoriale a cura di Luca Valenti</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='editor-container'>", unsafe_allow_html=True)
    titolo = st.text_input("Titolo dell'articolo", placeholder="Scrivi il titolo qui...")
    testo = st.text_area("Corpo della ricerca", height=600, placeholder="Inizia la tua stesura...")
    st.markdown("</div>", unsafe_allow_html=True)

with col_tools:
    st.markdown("### 🛠️ Strumenti di Ricerca")
    st.write("---")
    
    # BLOCCO 1: STORIA
    st.markdown("#### 📜 STORIA E TESTI ANTICHI")
    with st.container():
        st.markdown("<div class='sidebar-button-container'>", unsafe_allow_html=True)
        st.write("Fonti: JoYS e KYM")
        st.markdown("[Apri Archivio Journal of Yoga Studies →](https://journalofyogastudies.org/index.php/JoYS/issue/archive)")
        st.markdown("[Apri Portale KYM →](https://www.kym.org/)")
        st.markdown("</div>", unsafe_allow_html=True)

    # BLOCCO 2: SCIENZA
    st.markdown("#### 🔬 STUDI SCIENTIFICI")
    with st.container():
        st.markdown("<div class='sidebar-button-container'>", unsafe_allow_html=True)
        if st.button("🔍 Cerca Studi Sat Bir Khalsa"):
            st.write("Ultimi studi da Harvard:")
            articoli = cerca_pubmed("Sat Bir Singh Khalsa")
            for a in articoli:
                st.markdown(f"- [{a['t']}]({a['l']})")
        
        st.write("<br>", unsafe_allow_html=True)
        
        if st.button("🧬 Cerca HRV & Neuroscienze"):
            st.write("Ultimi studi da PubMed:")
            articoli = cerca_pubmed("yoga heart rate variability")
            for a in articoli:
                st.markdown(f"- [{a['t']}]({a['l']})")
        st.markdown("</div>", unsafe_allow_html=True)

    # BLOCCO 3: IMMAGINI
    st.markdown("#### 🖼️ ARCHIVIO VISIVO")
    with st.container():
        up = st.file_uploader("Carica immagine", type=["jpg","png","jpeg"], label_visibility="collapsed")
        if up:
            st.image(up)
