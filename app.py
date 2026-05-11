import streamlit as st
import base64
import os

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- FUNZIONE RECUPERO IMMAGINE (PNG) ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            # Codifica specifica per PNG
            return base64.b64encode(img_file.read()).decode()
    return None

# Cerco il file 'header_yoga.png'
img_base64 = get_base64_image("header_yoga.png")

# --- DESIGN ESTETICO ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FDFCF0; }}
    
    /* Header con Immagine PNG */
    .header-container {{
        width: 100%;
        background-color: white;
        border-bottom: 3px solid #C5A059;
        margin-bottom: 30px;
    }}
    
    .header-image {{
        width: 100%;
        height: 250px;
        /* Specifica MIME per PNG */
        background-image: url('data:image/png;base64,{img_base64 if img_base64 else ""}');
        background-size: cover;
        background-position: center;
    }}
    
    .header-title-bar {{
        background-color: #1A2E44;
        padding: 15px;
        color: #FDFCF0;
        font-family: 'serif';
        font-size: 1.8rem;
        letter-spacing: 3px;
        text-align: center;
    }}
    
    /* Corpo Articolo */
    .article-box {{
        background-color: white;
        padding: 40px;
        border-radius: 5px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-top: 20px;
    }}
    
    h1 {{ font-family: 'serif'; color: #1A2E44; font-size: 2.8rem; margin-bottom: 5px; }}
    .author-sub {{ font-style: italic; color: #C5A059; font-size: 1.1rem; margin-bottom: 30px; }}
    
    .article-content {{ 
        font-family: 'serif'; font-size: 1.3rem; line-height: 1.8; color: #2D2D2D;
    }}

    /* Area Accesso (In pagina) */
    .access-box {{
        background-color: #f0ede0;
        padding: 20px;
        border-radius: 5px;
        border: 1px solid #C5A059;
        margin-bottom: 30px;
    }}

    /* Risorse a destra */
    .resource-link {{ 
        text-decoration: none; 
        color: #1A2E44 !important; 
        font-weight: bold; 
        display: block; 
        padding: 8px 0; 
        font-family: 'Lato', sans-serif;
    }}
    .stExpander {{ background-color: white !important; border-radius: 5px; }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    
    <div class="header-container">
        <div class="header-image"></div>
        <div class="header-title-bar">S O R G E N T E &nbsp; Y O G A</div>
    </div>
    """, unsafe_allow_html=True)

# --- LOGICA DI ACCESSO (In pagina) ---
if 'admin' not in st.session_state:
    st.session_state['admin'] = False

# Layout a due colonne
col_main, col_nav = st.columns([0.7, 0.3], gap="large")

with col_main:
    # Mostro il box di accesso solo se non sono loggato
    if not st.session_state['admin']:
        with st.container():
            st.markdown("### 🔑 ACCESSO AUTORE")
            pwd = st.text_input("Inserisci password per scrivere", type="password", key="login_pwd")
            if pwd == "sorgente2026":
                st.session_state['admin'] = True
                st.rerun() # Ricarico la pagina per mostrare l'editor
            elif pwd:
                st.error("Password errata.")
    
    # --- AREA SCRITTURA (Appare solo dopo il login) ---
    if st.session_state['admin']:
        st.markdown("### ✍️ AREA EDITORIALE (Luca Valenti)")
        
        # Carico i valori salvati o stringhe vuote
        default_title = st.session_state.get('titolo_pub', "")
        default_text = st.session_state.get('testo_pub', "")
        
        titolo_input = st.text_input("Titolo Articolo pubblico", value=default_title)
        testo_input = st.text_area("Testo Articolo pubblico", height=400, value=default_text)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Pubblica/Aggiorna Online"):
                st.session_state['titolo_pub'] = titolo_input
                st.session_state['testo_pub'] = testo_input
                st.success("Articolo pubblicato online!")
        with col_btn2:
            if st.button("Logout"):
                st.session_state['admin'] = False
                st.rerun()
        
        st.markdown("---")

    # --- VISUALIZZAZIONE PUBBLICA (Quello che leggono tutti) ---
    t_finale = st.session_state.get('titolo_pub', "Benvenuti su Sorgente Yoga")
    c_finale = st.session_state.get('testo_pub', "Esegui l'accesso sopra per inserire il tuo primo studio.")
    
    # Box dell'articolo
    st.markdown(f"""
    <div class="article-box">
        <h1>{t_finale}</h1>
        <div class="author-sub">Ricerca e testi a cura di Luca Valenti</div>
        <div class="article-content">{c_finale}</div>
    </div>
    """, unsafe_allow_html=True)

with col_nav:
    st.markdown("### 🏛️ BIBLIOTECA")

    # Menù a scomparsa
    with st.expander("📜 STORIA E TESTI ANTICHI", expanded=True):
        st.markdown(f'<a class="resource-link" href="http://hyp.soas.ac.uk/" target="_blank">Hatha Yoga Project ↗</a>', unsafe_allow_html=True)
        st.markdown(f'<a class="resource-link" href="https://journalofyogastudies.org/index.php/JoYS/issue/archive" target="_blank">Journal of Yoga Studies ↗</a>', unsafe_allow_html=True)

    with st.expander("🔬 STUDI SCIENTIFICI", expanded=True):
        st.markdown(f'<a class="resource-link" href="https://sleep.hms.harvard.edu/faculty-staff/sat-bir-singh-khalsa" target="_blank">Harvard (Dr. Khalsa) ↗</a>', unsafe_allow_html=True)
        st.markdown(f'<a class="resource-link" href="https://www.iayt.org/" target="_blank">IAYT Yoga Therapy ↗</a>', unsafe_allow_html=True)
        st.markdown(f'<a class="resource-link" href="https://www.kym.org/" target="_blank">KYM Tradition ↗</a>', unsafe_allow_html=True)
