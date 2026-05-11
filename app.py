import streamlit as st
import base64
import os

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- FUNZIONE RECUPERO IMMAGINE (PNG) ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

img_base64 = get_base64_image("header_yoga.png")

# --- DESIGN ESTETICO ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FDFCF0; }}
    
    .header-container {{
        width: 100%;
        background-color: white;
        border-bottom: 3px solid #C5A059;
        margin-bottom: 30px;
    }}
    
    .header-image {{
        width: 100%;
        height: 250px;
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

    .resource-link {{ 
        text-decoration: none; 
        color: #1A2E44 !important; 
        font-weight: bold; 
        display: block; 
        padding: 8px 0; 
        font-family: 'Lato', sans-serif;
    }}
    
    /* Stile per elenco testi (senza link) */
    .text-item {{
        color: #4A3E3E;
        font-family: 'Lato', sans-serif;
        padding: 5px 0;
        border-bottom: 1px dotted #C5A059;
    }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    
    <div class="header-container">
        <div class="header-image"></div>
        <div class="header-title-bar">S O R G E N T E &nbsp; Y O G A</div>
    </div>
    """, unsafe_allow_html=True)

# --- LOGICA DI ACCESSO ---
if 'admin' not in st.session_state:
    st.session_state['admin'] = False

col_main, col_nav = st.columns([0.7, 0.3], gap="large")

with col_main:
    if not st.session_state['admin']:
        with st.container():
            st.markdown("### 🔑 ACCESSO AUTORE")
            pwd = st.text_input("Inserisci password per scrivere", type="password", key="login_pwd")
            if pwd == "sorgente2026":
                st.session_state['admin'] = True
                st.rerun()
    
    if st.session_state['admin']:
        st.markdown("### ✍️ AREA EDITORIALE")
        titolo_input = st.text_input("Titolo Articolo", value=st.session_state.get('titolo_pub', ""))
        testo_input = st.text_area("Testo Articolo", height=400, value=st.session_state.get('testo_pub', ""))
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Aggiorna Online"):
                st.session_state['titolo_pub'] = titolo_input
                st.session_state['testo_pub'] = testo_input
                st.success("Articolo pubblicato!")
        with c2:
            if st.button("Logout"):
                st.session_state['admin'] = False
                st.rerun()
        st.markdown("---")

    t_f = st.session_state.get('titolo_pub', "Benvenuti su Sorgente Yoga")
    c_f = st.session_state.get('testo_pub', "Accedi per pubblicare contenuti.")
    
    st.markdown(f"""
    <div class="article-box">
        <h1>{t_f}</h1>
        <div class="author-sub">Ricerca e testi a cura di Luca Valenti</div>
        <div class="article-content">{c_f}</div>
    </div>
    """, unsafe_allow_html=True)

with col_nav:
    st.markdown("### 🏛️ BIBLIOTECA")

    # NUOVO TASTO: ELENCO TESTI ANTICHI
    with st.expander("📖 TESTI CLASSICI INSERITI", expanded=False):
        st.markdown("<div class='text-item'>• Yoga Sūtra (Patañjali)</div>", unsafe_allow_html=True)
        st.markdown("<div class='text-item'>• Haṭha Yoga Pradīpikā</div>", unsafe_allow_html=True)
        st.markdown("<div class='text-item'>• Gheraṇḍa Saṃhitā</div>", unsafe_allow_html=True)
        st.markdown("<div class='text-item'>• Bhagavad Gītā</div>", unsafe_allow_html=True)
        st.info("Aggiungeremo qui i testi man mano che verranno trattati nel blog.")

    with st.expander("📜 SITI DI STORIA E RICERCA", expanded=True):
        st.markdown(f'<a class="resource-link" href="http://hyp.soas.ac.uk/" target="_blank">Hatha Yoga Project ↗</a>', unsafe_allow_html=True)
        st.markdown(f'<a class="resource-link" href="https://journalofyogastudies.org/index.php/JoYS/issue/archive" target="_blank">Journal of Yoga Studies ↗</a>', unsafe_allow_html=True)

    with st.expander("🔬 RICERCA SCIENTIFICA", expanded=True):
        st.markdown(f'<a class="resource-link" href="https://sleep.hms.harvard.edu/faculty-staff/sat-bir-singh-khalsa" target="_blank">Harvard (Dr. Khalsa) ↗</a>', unsafe_allow_html=True)
        st.markdown(f'<a class="resource-link" href="https://www.iayt.org/" target="_blank">IAYT Yoga Therapy ↗</a>', unsafe_allow_html=True)
        st.markdown(f'<a class="resource-link" href="https://www.kym.org/" target="_blank">KYM Tradition ↗</a>', unsafe_allow_html=True)
