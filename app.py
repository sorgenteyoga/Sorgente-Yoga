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

img_base64 = get_base64_image("header_yoga.jpg")

# --- DESIGN ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FDFCF0; }}
    
    /* Forza visibilità Sidebar */
    [data-testid="stSidebar"] {{
        background-color: #f0ede0 !important;
        border-right: 1px solid #C5A059;
    }}

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
    
    .article-content {{ 
        font-family: 'serif'; font-size: 1.3rem; line-height: 1.8; color: #2D2D2D;
        background: white; padding: 40px; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }}

    .resource-link {{ text-decoration: none; color: #1A2E44; font-weight: bold; display: block; padding: 8px 0; }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    
    <div class="header-container">
        <div class="header-image"></div>
        <div class="header-title-bar">S O R G E N T E &nbsp; Y O G A</div>
    </div>
    """, unsafe_allow_html=True)

# --- SIDEBAR (Barra a Sinistra) ---
with st.sidebar:
    st.markdown("<h2 style='color:#1A2E44;'>🔑 ACCESSO</h2>", unsafe_allow_html=True)
    password = st.text_input("Inserisci password per scrivere", type="password")
    
    if password == "sorgente2026":
        st.session_state['admin'] = True
        st.success("Modalità Scrittura Attiva")
    else:
        st.session_state['admin'] = False
    
    st.write("---")
    st.caption("Gestione contenuti riservata a Luca Valenti")

# --- LAYOUT PRINCIPALE ---
col_main, col_nav = st.columns([0.7, 0.3], gap="large")

with col_main:
    if st.session_state.get('admin'):
        st.markdown("### ✍️ Area Editoriale")
        titolo_input = st.text_input("Titolo dell'articolo", value=st.session_state.get('titolo_pub', ""))
        testo_input = st.text_area("Testo dell'articolo", height=400, value=st.session_state.get('testo_pub', ""))
        if st.button("Pubblica Ora"):
            st.session_state['titolo_pub'] = titolo_input
            st.session_state['testo_pub'] = testo_input
            st.toast("Articolo aggiornato con successo!")

    t_finale = st.session_state.get('titolo_pub', "Benvenuti su Sorgente Yoga")
    c_finale = st.session_state.get('testo_pub', "Esegui il login nella barra laterale per inserire i tuoi studi.")
    
    st.markdown(f"<h1 style='color:#1A2E44;'>{t_finale}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='article-content'>{c_finale}</div>", unsafe_allow_html=True)

with col_nav:
    st.markdown("### 🏛️ BIBLIOTECA")

    with st.expander("📜 STORIA E TESTI ANTICHI"):
        st.markdown("<a class='resource-link' href='http://hyp.soas.ac.uk/' target='_blank'>Hatha Yoga Project ↗</a>", unsafe_allow_html=True)
        st.markdown("<a class='resource-link' href='https://journalofyogastudies.org/index.php/JoYS/issue/archive' target='_blank'>Journal of Yoga Studies ↗</a>", unsafe_allow_html=True)

    with st.expander("🔬 STUDI SCIENTIFICI"):
        st.markdown("<a class='resource-link' href='https://sleep.hms.harvard.edu/faculty-staff/sat-bir-singh-khalsa' target='_blank'>Harvard (Dr. Khalsa) ↗</a>", unsafe_allow_html=True)
        st.markdown("<a class='resource-link' href='https://www.iayt.org/' target='_blank'>IAYT Yoga Therapy ↗</a>", unsafe_allow_html=True)
        st.markdown("<a class='resource-link' href='https://www.kym.org/' target='_blank'>KYM Tradition ↗</a>", unsafe_allow_html=True)
