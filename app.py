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

img_base64 = get_base64_image("header_yoga.png")

# --- DESIGN BLINDATO ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #FDFCF0; }}
    
    /* Header Header */
    .fixed-header {{
        width: 100%;
        background-color: #FDFCF0;
        border-bottom: 3px solid #C5A059;
        margin-bottom: 20px;
    }}
    
    .header-image-strip {{
        width: 100%;
        height: 250px;
        background-image: url('data:image/png;base64,{img_base64 if img_base64 else ""}');
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        background-color: white;
    }}
    
    .header-title-bar {{
        background-color: #1A2E44;
        padding: 15px 50px;
        color: #FDFCF0;
        font-family: 'serif';
        font-size: 1.8rem;
        letter-spacing: 3px;
        text-align: center;
    }}
    
    /* Box Articolo */
    .article-content {{ 
        font-family: 'serif'; font-size: 1.2rem; line-height: 1.7; color: #2D2D2D;
        background: white; padding: 30px; border-radius: 5px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}

    /* Risorse a destra (Evita sovrapposizioni) */
    .resource-card {{
        background-color: white; padding: 10px; border-radius: 5px;
        border-left: 4px solid #C5A059; margin-bottom: 10px;
    }}
    .resource-link {{ text-decoration: none; color: #1A2E44; font-weight: bold; font-size: 0.9rem; }}
    
    #MainMenu, footer, header {{visibility: hidden;}}
    </style>
    
    <div class="fixed-header">
        <div class="header-image-strip"></div>
        <div class="header-title-bar">S O R G E N T E &nbsp; Y O G A</div>
    </div>
    """, unsafe_allow_html=True)

# --- GESTIONE PASSWORD (Per vedere l'editor) ---
if 'admin' not in st.session_state: st.session_state['admin'] = False

with st.sidebar:
    st.write("### Accesso Autore")
    pwd = st.text_input("Password", type="password")
    if pwd == "sorgente2026":
        st.session_state['admin'] = True
    else:
        st.session_state['admin'] = False

# --- LAYOUT ---
col_main, col_nav = st.columns([0.7, 0.3], gap="medium")

with col_main:
    if st.session_state['admin']:
        st.markdown("### ✍️ Area di Scrittura")
        titolo_edit = st.text_input("Inserisci il Titolo", value=st.session_state.get('titolo_pub', "Titolo Articolo"))
        contenuto_edit = st.text_area("Scrivi il tuo articolo qui...", height=400, value=st.session_state.get('testo_pub', ""))
        if st.button("Pubblica Articolo"):
            st.session_state['titolo_pub'] = titolo_edit
            st.session_state['testo_pub'] = contenuto_edit
            st.success("Pubblicato!")

    # Pagina Pubblica
    t = st.session_state.get('titolo_pub', "Benvenuti su Sorgente Yoga")
    c = st.session_state.get('testo_pub', "Usa la barra laterale per accedere come autore e scrivere il tuo primo articolo.")
    
    st.markdown(f"<h1 style='color:#1A2E44;'>{t}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='article-content'>{c}</div>", unsafe_allow_html=True)

with col_nav:
    st.markdown("### 🏛️ BIBLIOTECA")
    
    st.markdown("**📜 STORIA E TESTI**")
    st.markdown("""
    <div class='resource-card'><a class='resource-link' href='http://hyp.soas.ac.uk/' target='_blank'>Hatha Yoga Project ↗</a></div>
    <div class='resource-card'><a class='resource-link' href='https://journalofyogastudies.org/index.php/JoYS/issue/archive' target='_blank'>Journal of Yoga Studies ↗</a></div>
    """, unsafe_allow_html=True)

    st.markdown("**🔬 SCIENZA**")
    st.markdown("""
    <div class='resource-card'><a class='resource-link' href='https://sleep.hms.harvard.edu/faculty-staff/sat-bir-singh-khalsa' target='_blank'>Harvard (Dr. Khalsa) ↗</a></div>
    <div class='resource-card'><a class='resource-link' href='https://www.iayt.org/' target='_blank'>IAYT Yoga Therapy ↗</a></div>
    <div class='resource-card'><a class='resource-link' href='https://www.kym.org/' target='_blank'>KYM Tradition ↗</a></div>
    """, unsafe_allow_html=True)
