import streamlit as st
from Bio import Entrez

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- DESIGN PROFESSIONALE ---
st.markdown("""
    <style>
    .stApp { background-color: #FDFCF0; padding-top: 60px; }
    .top-bar {
        background-color: #1A2E44;
        height: 70px;
        width: 100%;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 999;
        display: flex;
        align-items: center;
        padding-left: 50px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .top-bar-title { color: #FDFCF0; font-family: 'serif'; font-size: 1.8rem; letter-spacing: 3px; }
    
    /* Stile Articolo Pubblico */
    .article-title { font-family: 'serif'; color: #1A2E44; font-size: 3rem; line-height: 1.2; margin-bottom: 10px; }
    .article-meta { font-style: italic; color: #C5A059; margin-bottom: 30px; font-size: 1.1rem; }
    .article-content { 
        font-family: 'serif'; 
        font-size: 1.3rem; 
        line-height: 1.8; 
        color: #2D2D2D;
        background: white;
        padding: 40px;
        border-radius: 2px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }
    
    /* Sidebar Risorse */
    .resource-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border-bottom: 3px solid #C5A059;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .resource-card:hover { transform: translateX(5px); }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    
    <div class="top-bar">
        <div class="top-bar-title">S O R G E N T E &nbsp; Y O G A</div>
    </div>
    """, unsafe_allow_html=True)

# --- STATO DELL'APP (Per gestire la password) ---
if 'admin' not in st.session_state:
    st.session_state['admin'] = False

# --- SIDEBAR DI CONTROLLO (Solo per te) ---
with st.sidebar:
    st.write("### 🔑 Accesso Autore")
    pwd = st.text_input("Inserisci Password", type="password")
    if pwd == "sorgente2026": # Puoi cambiare questa password
        st.session_state['admin'] = True
        st.success("Modalità Editor Attiva")
    else:
        st.session_state['admin'] = False

# --- LOGICA DI VISUALIZZAZIONE ---
col_main, col_nav = st.columns([0.7, 0.3], gap="large")

with col_main:
    if st.session_state['admin']:
        # VISTA EDITOR (Cosa vedi tu per scrivere)
        st.subheader("✍️ Editor Articolo")
        titolo_edit = st.text_input("Titolo Pubblico", value="Il Respiro tra Tradizione e Scienza")
        contenuto_edit = st.text_area("Contenuto del Blog", height=500, value="Scrivi qui il tuo articolo...")
        if st.button("Aggiorna Blog"):
            st.toast("Articolo Pubblicato!")
            # Qui memorizziamo temporaneamente i dati
            st.session_state['titolo_pub'] = titolo_edit
            st.session_state['testo_pub'] = contenuto_edit
    
    # VISTA PUBBLICA (Cosa vede la gente)
    t = st.session_state.get('titolo_pub', "Benvenuti su Sorgente Yoga")
    c = st.session_state.get('testo_pub', "Inizia la tua esplorazione attraverso la sidebar delle risorse.")
    
    st.markdown(f"<div class='article-title'>{t}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='article-meta'>Ricerca e testi di Luca Valenti</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='article-content'>{c}</div>", unsafe_allow_html=True)

with col_nav:
    st.markdown("### 🏛️ BIBLIOTECA DIGITALE")
    st.write("Seleziona una categoria per approfondire")
    
    # CATEGORIA: STORIA
    with st.expander("📜 STORIA E TESTI ANTICHI", expanded=True):
        st.markdown("""
        <div class='resource-card'>
            <a href='https://journalofyogastudies.org/index.php/JoYS/issue/archive' target='_blank' style='text-decoration:none; color:#1A2E44; font-weight:bold;'>Journal of Yoga Studies ↗</a><br>
            <small>Ricerca accademica internazionale</small>
        </div>
        <div class='resource-card'>
            <a href='https://www.kym.org/' target='_blank' style='text-decoration:none; color:#1A2E44; font-weight:bold;'>Krishnamacharya Yoga Mandiram ↗</a><br>
            <small>Tradizione vivente e Viniyoga</small>
        </div>
        """, unsafe_allow_html=True)

    # CATEGORIA: SCIENZA
    with st.expander("🔬 STUDI SCIENTIFICI", expanded=True):
        st.markdown("""
        <div class='resource-card'>
            <a href='https://sleep.hms.harvard.edu/faculty-staff/sat-bir-singh-khalsa' target='_blank' style='text-decoration:none; color:#1A2E44; font-weight:bold;'>Harvard Medical School ↗</a><br>
            <small>Laboratorio del Dr. Sat Bir Khalsa</small>
        </div>
        <div class='resource-card'>
            <a href='https://www.iayt.org/' target='_blank' style='text-decoration:none; color:#1A2E44; font-weight:bold;'>IAYT Yoga Therapy ↗</a><br>
            <small>Protocolli clinici e ricerca</small>
        </div>
        """, unsafe_allow_html=True)
        
    st.info("💡 Nuovi tasti e siti verranno aggiunti man mano alla tua biblioteca digitale.")
