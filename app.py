import streamlit as st
from Bio import Entrez

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- DESIGN DEFINITIVO (Barra Superiore e Pulizia) ---
st.markdown("""
    <style>
    /* Barra Superiore Elegante */
    .top-bar {
        background-color: #1A2E44;
        height: 60px;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    .top-bar-title {
        color: #FDFCF0;
        font-family: 'serif';
        font-size: 1.5rem;
        letter-spacing: 2px;
    }
    /* Regolazioni Corpo Pagina */
    .stApp { background-color: #FDFCF0; padding-top: 80px; }
    h1, h2, h3 { font-family: 'serif' !important; color: #1A2E44 !important; }
    .editor-container {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        min-height: 700px;
    }
    .tool-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #C5A059;
        margin-bottom: 20px;
    }
    /* Nascondi Elementi Streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    
    <div class="top-bar">
        <div class="top-bar-title">S O R G E N T E &nbsp; Y O G A</div>
    </div>
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

# --- LAYOUT PRINCIPALE ---
col_main, col_tools = st.columns([0.65, 0.35], gap="large")

with col_main:
    st.markdown("<div class='editor-container'>", unsafe_allow_html=True)
    st.markdown("<h1>Editoriale</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-style: italic;'>A cura di Luca Valenti</p>", unsafe_allow_html=True)
    
    titolo = st.text_input("TITOLO DELL'ARTICOLO", value="Il Respiro tra Tradizione e Scienza")
    testo = st.text_area("CORPO DELLA RICERCA", height=600, placeholder="Inizia a scrivere...")
    
    if st.button("Pubblica/Salva Ricerca"):
        st.success("Articolo salvato correttamente!")
    st.markdown("</div>", unsafe_allow_html=True)

with col_tools:
    st.markdown("<h3>Strumenti</h3>", unsafe_allow_html=True)
    
    # SEZIONE STORIA
    st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
    st.markdown("<b>STORIA E TESTI ANTICHI</b>", unsafe_allow_html=True)
    st.markdown("<br><a href='https://journalofyogastudies.org/index.php/JoYS/issue/archive' target='_blank'>Journal of Yoga Studies ↗</a>", unsafe_allow_html=True)
    st.markdown("<br><a href='https://www.kym.org/' target='_blank'>Krishnamacharya Yoga Mandiram ↗</a>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # SEZIONE SCIENZA
    st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
    st.markdown("<b>STUDI SCIENTIFICI</b>", unsafe_allow_html=True)
    if st.button("🔍 Cerca Sat Bir Khalsa"):
        articoli = cerca_pubmed("Sat Bir Singh Khalsa")
        for a in articoli:
            st.markdown(f"<small>• <a href='{a['l']}'>{a['t']}</a></small>", unsafe_allow_html=True)
    
    st.write("")
    
    if st.button("🧬 Cerca HRV & Neuro"):
        articoli = cerca_pubmed("yoga heart rate variability")
        for a in articoli:
            st.markdown(f"<small>• <a href='{a['l']}'>{a['t']}</a></small>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # SEZIONE IMMAGINI
    st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
    st.markdown("<b>ARCHIVIO VISIVO</b>", unsafe_allow_html=True)
    up = st.file_uploader("Carica file", type=["jpg","png","jpeg"], label_visibility="collapsed")
    if up:
        st.image(up)
    st.markdown("</div>", unsafe_allow_html=True)
