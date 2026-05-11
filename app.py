import streamlit as st
import base64
import os

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- FUNZIONE RECUPERO IMMAGINE ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

# CAMBIA IL NOME QUI SOTTO SE LA TUA IMMAGINE SI CHIAMA DIVERSAMENTE
img_base64 = get_base64_image("header_yoga.png")

# --- DESIGN ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FDFCF0; }}
    
    /* Header con Immagine */
    .header-container {{
        width: 100%;
        background-color: white;
        border-bottom: 3px solid #C5A059;
        margin-bottom: 30px;
    }}
    
    .header-image {{
        width: 100%;
        height: 250px;
        background-image: url('data:image/jpg;base64,{img_base64 if img_base64 else ""}');
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
    
    /* Box Articolo */
    .article-content {{ 
        font-family: 'serif'; font-size: 1.3rem; line-height: 1.8; color: #2D2D2D;
        background: white; padding: 40px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }}

    /* Stile per i link nei sottomenù */
    .resource-link {{ text-decoration: none; color: #1A2E44; font-weight: bold; display: block; padding: 5px 0; }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    
    <div class="header-container">
        <div class="header-image"></div>
        <div class="header-title-bar">S O R G E N T E &nbsp; Y O G A</div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Accesso Autore) ---
with st.sidebar:
    st.markdown("### 🔒 AREA AUTORE")
    password = st.text_input("Inserisci password per scrivere", type="password")
    
    if password == "sorgente2026":
        st.session_state['admin'] = True
        st.success("Modalità Scrittura Attiva")
    else:
        st.session_state['admin'] = False

# --- LAYOUT PRINCIPALE ---
col_main, col_nav = st.columns([0.7, 0.3], gap="large")

with col_main:
    # AREA DI SCRITTURA (Appare solo con password)
    if st.session_state.get('admin'):
        st.markdown("### ✍️ Crea il tuo Articolo")
        titolo_input = st.text_input("Titolo dell'articolo", value=st.session_state.get('titolo_pub', ""))
        testo_input = st.text_area("Testo dell'articolo", height=400, value=st.session_state.get('testo_pub', ""))
        if st.button("Pubblica Online"):
            st.session_state['titolo_pub'] = titolo_input
            st.session_state['testo_pub'] = testo_input
            st.balloons()

    # VISUALIZZAZIONE PUBBLICA
    titolo_finale = st.session_state.get('titolo_pub', "Benvenuti su Sorgente Yoga")
    testo_finale = st.session_state.get('testo_pub', "Effettua l'accesso nella barra a sinistra per pubblicare il tuo primo contenuto.")
    
    st.markdown(f"<h1 style='color:#1A2E44;'>{titolo_finale}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='article-content'>{testo_finale}</div>", unsafe_allow_html=True)

with col_nav:
    st.markdown("### 🏛️ RISORSE")

    # SOTTOMENU A SCOMPARSA
    with st.expander("📜 STORIA E TESTI ANTICHI"):
        st.markdown("<a class='resource-link' href='http://hyp.soas.ac.uk/' target='_blank'>Hatha Yoga Project ↗</a>", unsafe_allow_html=True)
        st.markdown("<a class='resource-link' href='https://journalofyogastudies.org/index.php/JoYS/issue/archive' target='_blank'>Journal of Yoga Studies ↗</a>", unsafe_allow_html=True)

    with st.expander("🔬 STUDI SCIENTIFICI"):
        st.markdown("<a class='resource-link' href='https://sleep.hms.harvard.edu/faculty-staff/sat-bir-singh-khalsa' target='_blank'>Harvard (Dr. Khalsa) ↗</a>", unsafe_allow_html=True)
        st.markdown("<a class='resource-link' href='https://www.iayt.org/' target='_blank'>IAYT Yoga Therapy ↗</a>", unsafe_allow_html=True)
        st.markdown("<a class='resource-link' href='https://www.kym.org/' target='_blank'>KYM Tradition ↗</a>", unsafe_allow_html=True)
