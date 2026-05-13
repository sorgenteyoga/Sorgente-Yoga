import streamlit as st
import base64, os, json

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

def get_img(p):
    if os.path.exists(p):
        try:
            with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
        except: return ""
    return ""

ih = get_img("header_yoga.png")

# --- CSS PULITO E "ALTO" ---
st.markdown(f"""
<style>
    [data-testid="stHeader"] {{ display: none !important; }}
    .block-container {{ padding-top: 0rem !important; margin-top: -45px !important; }}
    .stApp {{ background-color: #FDFCF0 !important; }}
    .header-img {{ 
        width:100%; height:200px; 
        background: url('data:image/png;base64,{ih}') no-repeat center; 
        background-size: contain; 
    }}
    .header-bar {{ 
        background:#1A2E44 !important; padding:20px; color:#FDFCF0 !important; 
        font-family: serif; text-align:center; font-size:1.8rem; 
        letter-spacing:3px; border-bottom: 4px solid #C5A059;
    }}
    /* Stile per i bottoni di selezione */
    .stButton>button {{
        border-radius: 20px;
        border: 1px solid #1A2E44;
        color: #1A2E44;
    }}
</style>
<div class="header-img"></div>
<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>
""", unsafe_allow_html=True)

# --- LOGICA DI NAVIGAZIONE SENZA TENDINE ---
if 'cat_sel' not in st.session_state: st.session_state['cat_sel'] = "BLOG"
if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0

st.write("<br>", unsafe_allow_html=True)

# Selettore di Categoria (Sempre visibile, addio tendine)
cat_opzioni = {"BLOG": "📂 ARCHIVIO", "TESTI": "📜 TESTI ANTICHI", "SCIENZA": "🔬 SCIENZA"}
scelta = st.radio("Seleziona sezione:", list(cat_opzioni.keys()), 
                  format_func=lambda x: cat_opzioni[x], 
                  horizontal=True, label_visibility="collapsed")

st.session_state.cat_sel = scelta

# Carica articoli filtrati per la categoria scelta
all_a = [] # Qui carichi i tuoi dati dal JSON
articoli_filtrati = [a for a in all_a if str(a.get('cat','BLOG')).upper() == scelta]

# Sidebar o Menu laterale per i titoli (molto più comodo per leggere)
with st.sidebar:
    st.markdown("### Articoli in questa sezione")
    for i, art in enumerate(articoli_filtrati):
        if st.button(art['titolo'], key=f"btn_{i}", use_container_width=True):
            st.session_state.sel_idx = i
            st.rerun()

st.write("---")

# Visualizzazione Articolo
if articoli_filtrati:
    art = articoli_filtrati[st.session_state.sel_idx]
    st.markdown(f"""
    <div style="background: white; padding:40px; border-radius:8px; shadow: 0 2px 10px rgba(0,0,0,0.05);">
        <h1 style="font-family:serif;">{art['titolo']}</h1>
        <div style="font-size:1.1rem; line-height:1.7; font-family:serif;">
            {art['testo'].replace(chr(10), '<br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)
