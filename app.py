import streamlit as st
import os

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- VERIFICA E CODIFICA IMMAGINE (Per l'Header) ---
import base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# Codifica l'immagine caricata su GitHub
img_base64 = get_base64_image("header_yoga.png")

# --- DESIGN DEFINITIVO (Header con Immagine Fissa) ---
st.markdown(f"""
    <style>
    /* Reset e Sfondo */
    .stApp {{ background-color: #FDFCF0; padding-top: 0px; }}
    
    /* Header Fisso con Immagine e Titolo */
    .fixed-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 999;
        background-color: #FDFCF0; /* Fondo crema sotto l'immagine */
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    
    /* L'immagine storica come fregio continuo */
    .header-image-strip {{
        width: 100%;
        height: 180px; /* Altezza adattata per mostrare le vignette */
        background-image: url('data:image/png;base64,{img_base64 if img_base64 else ""}');
        background-size: cover; /* L'immagine copre tutta la larghezza */
        background-position: center;
        border-bottom: 3px solid #C5A059; /* Linea oro */
    }}
    
    /* La fascia con il Titolo sotto l'immagine */
    .header-title-bar {{
        background-color: #1A2E44; /* Blu navy */
        height: 60px;
        display: flex;
        align-items: center;
        padding-left: 50px;
    }}
    .top-bar-title {{ color: #FDFCF0; font-family: 'serif'; font-size: 1.8rem; letter-spacing: 3px; }}
    
    /* Regolazione corpo pagina per non finire sotto l'header */
    [data-testid="stVerticalBlock"] > div:first-child {{
        margin-top: 250px; /* Altezza Immagine (180) + Titolo (60) + Margine */
    }}
    
    /* Stili Contenuti */
    h1, h2, h3 {{ font-family: 'serif' !important; color: #1A2E44 !important; }}
    p, li, div, span {{ font-family: 'Lato', sans-serif !important; color: #4A3E3E; }}
    
    .article-content {{ 
        font-family: 'serif'; font-size: 1.3rem; line-height: 1.8; color: #2D2D2D;
        background: white; padding: 40px; border-radius: 2px; box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }}
    
    .resource-card {{
        background-color: white; padding: 15px; border-radius: 8px;
        border-bottom: 3px solid #C5A059; margin-bottom: 15px; transition: 0.3s;
    }}
    .resource-card:hover {{ transform: translateX(5px); }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    
    <div class="fixed-header">
        <div class="header-image-strip"></div>
        <div class="header-title-bar">
            <div class="top-bar-title">S O R G E N T E &nbsp; Y O G A</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- STATO DELL'APP ---
if 'admin' not in st.session_state: st.session_state['admin'] = False

# --- SIDEBAR DI CONTROLLO (Solo per te) ---
with st.sidebar:
    st.write("### 🔑 Accesso Autore")
    pwd = st.text_input("Inserisci Password", type="password")
    if pwd == "sorgente2026": # PASSWORD TEMP
        st.session_state['admin'] = True
        st.success("Modalità Editor Attiva")
    else: st.session_state['admin'] = False

# --- LAYOUT PRINCIPALE ---
col_main, col_nav = st.columns([0.7, 0.3], gap="large")

with col_main:
    if st.session_state['admin']:
        st.subheader("✍️ Editor Articolo")
        titolo_edit = st.text_input("Titolo Pubblico", value="Il Respiro tra Tradizione e Scienza")
        contenuto_edit = st.text_area("Contenuto del Blog (Usa Markdown)", height=500, value="Scrivi qui il tuo articolo...")
        if st.button("Aggiorna Blog"):
            st.session_state['titolo_pub'] = titolo_edit
            st.session_state['testo_pub'] = contenuto_edit
            st.toast("Articolo Pubblicato!")
    
    # Vista Pubblica
    t = st.session_state.get('titolo_pub', "Benvenuti su Sorgente Yoga")
    c = st.session_state.get('testo_pub', "Esplora i contenuti attraverso i link di ricerca a destra.")
    
    st.markdown(f"<h1>{t}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-style: italic; color:#C5A059;'>Ricerca e testi di Luca Valenti</p>", unsafe_allow_html=True)
    st.markdown(f"<div class='article-content'>{c}</div>", unsafe_allow_html=True)

with col_nav:
    st.markdown("### 🏛️ BIBLIOTECA DIGITALE")
    
    # SEZIONE STORIA
    with st.expander("📜 STORIA E TESTI ANTICHI", expanded=True):
        st.markdown("""
        <div class='resource-card'>
            <a href='http://hyp.soas.ac.uk/' target='_blank' style='text-decoration:none; color:#1A2E44; font-weight:bold;'>Hatha Yoga Project (SOAS) ↗</a><br>
            <small>Ricerca filologica sui manoscritti</small>
        </div>
        <div class='resource-card'>
            <a href='https://journalofyogastudies.org/index.php/JoYS/issue/archive' target='_blank' style='text-decoration:none; color:#1A2E44; font-weight:bold;'>Journal of Yoga Studies ↗</a><br>
            <small>Rivista accademica internazionale</small>
        </div>
        """, unsafe_allow_html=True)

    # SEZIONE SCIENZA
    with st.expander("🔬 STUDI SCIENTIFICI", expanded=True):
        st.markdown("""
        <div class='resource-card'>
            <a href='https://sleep.hms.harvard.edu/faculty-staff/sat-bir-singh-khalsa' target='_blank' style='text-decoration:none; color:#1A2E44; font-weight:bold;'>Harvard (Dr. Khalsa) ↗</a><br>
            <small>Scienza del sonno e yoga</small>
        </div>
        <div class='resource-card'>
            <a href='https://www.iayt.org/' target='_blank' style='text-decoration:none; color:#1A2E44; font-weight:bold;'>IAYT Yoga Therapy ↗</a><br>
            <small>Ricerca clinica e professionale</small>
        </div>
        <div class='resource-card'>
            <a href='https://www.kym.org/' target='_blank' style='text-decoration:none; color:#1A2E44; font-weight:bold;'>KYM Tradition ↗</a><br>
            <small>Lignaggio e pratica terapeutica</small>
        </div>
        """, unsafe_allow_html=True)
