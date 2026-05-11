import streamlit as st
from Bio import Entrez

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- DESIGN AVANZATO (Layout a due colonne: Scrittura e Consultazione) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Lato:wght@300;400&display=swap" rel="stylesheet">
    <style>
    .stApp { background-color: #FDFCF0; }
    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1A2E44 !important; }
    p, li, div, span { font-family: 'Lato', sans-serif !important; color: #4A3E3E; }
    
    /* Area di scrittura centrale */
    .editor-container {
        background-color: #ffffff;
        padding: 40px;
        border-radius: 5px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        min-height: 800px;
        border-top: 4px solid #1A2E44;
    }
    
    /* Box strumenti laterali */
    .tool-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #C5A059;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stButton>button {
        background-color: #1A2E44 !important;
        color: #FDFCF0 !important;
        border-radius: 5px !important;
        font-size: 0.8rem !important;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI TECNICHE ---
def cerca_pubmed(query):
    Entrez.email = "tua_email@esempio.com"
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=3)
        record = Entrez.read(handle)
        results = []
        for id in record["IdList"]:
            h = Entrez.esummary(db="pubmed", id=id)
            r = Entrez.read(h)
            results.append({"titolo": r[0]['Title'], "link": f"https://pubmed.ncbi.nlm.nih.gov/{id}/"})
        return results
    except: return []

# --- LAYOUT A COLONNE ---
# Colonna sinistra (Scrittura: 65%) | Colonna destra (Consultazione: 35%)
col_main, col_tools = st.columns([0.65, 0.35], gap="large")

with col_main:
    st.markdown("<h1>SORGENTE YOGA</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-style: italic;'>Editoriale di Luca Valenti</p>", unsafe_allow_html=True)
    
    # Spazio per scrivere l'articolo principale
    st.markdown("<div class='editor-container'>", unsafe_allow_html=True)
    titolo_articolo = st.text_input("Titolo del tuo articolo", "Inserisci il titolo qui...")
    contenuto_articolo = st.text_area("Inizia a scrivere la tua ricerca...", height=600, placeholder="Oggi la pratica di asana incontra la fisiologia del nervo vago...")
    
    if st.button("Salva Bozza"):
        st.success("Articolo salvato localmente!")
    st.markdown("</div>", unsafe_allow_html=True)

with col_tools:
    st.markdown("### 📚 Strumenti di Ricerca")
    
    # Sezione Tradizione
    with st.expander("📜 TRADIZIONE & TESTI", expanded=True):
        st.markdown("""<div class='tool-card'>
            <small><b>Journal of Yoga Studies</b></small><br>
            <a href='https://journalofyogastudies.org/index.php/JoYS/issue/archive' target='_blank' style='color:#C5A059; font-size:0.9rem;'>Archivio JoYS →</a>
        </div>""", unsafe_allow_html=True)
        st.markdown("""<div class='tool-card'>
            <small><b>KYM Tradition</b></small><br>
            <a href='https://www.kym.org/' target='_blank' style='color:#C5A059; font-size:0.9rem;'>Portale KYM →</a>
        </div>""", unsafe_allow_html=True)

    # Sezione Scienza
    with st.expander("🔬 SCIENZA & HARVARD", expanded=True):
        if st.button("🔍 Studi Sat Bir Khalsa"):
            articoli = cerca_pubmed("Sat Bir Singh Khalsa")
            for art in articoli:
                st.markdown(f"<small style='color:#1A2E44;'>• {art['titolo']}</small>", unsafe_allow_html=True)
        
        if st.button("🧬 HRV & Neuroscienze"):
            articoli = cerca_pubmed("yoga heart rate variability")
            for art in articoli:
                st.markdown(f"<small style='color:#1A2E44;'>• {art['titolo']}</small>", unsafe_allow_html=True)

    # Sezione Immagini
    with st.expander("🖼️ ARCHIVIO VISIVO", expanded=False):
        uploaded_file = st.file_uploader("Carica riferimento visivo", type=["jpg","png"])
        if uploaded_file:
            st.image(uploaded_file, use_container_width=True)

    # Sezione Terapia
    with st.expander("🏥 TERAPIA CLINICA", expanded=False):
        st.link_button("Database IAYT", "https://www.iayt.org/")
