import streamlit as st
import base64, os, json

# Configurazione pagina
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

def get_img(p):
    if os.path.exists(p):
        try:
            with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
        except: return ""
    return ""

def load_a():
    if os.path.exists("archivio_articoli.json"):
        try:
            with open("archivio_articoli.json", "r", encoding="utf-8") as f:
                d = json.load(f)
                return d if isinstance(d, list) else []
        except: return []
    return []

all_a = load_a()
ih = get_img("header_yoga.png")

# --- CSS INTEGRATO ---
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
</style>
<div class="header-img"></div>
<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>
""", unsafe_allow_html=True)

# --- STATO DELLA SESSIONE ---
if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
if 'mode' not in st.session_state: st.session_state['mode'] = 'view'

st.write("<br>", unsafe_allow_html=True)

# --- NAVIGAZIONE (TENDINE) ---
c1, c2, c3 = st.columns(3)

with c1:
    with st.popover("📂 ARCHIVIO", use_container_width=True):
        for i, a in enumerate(all_a):
            # Filtro per categoria BLOG o vuota
            if str(a.get('cat','')).upper() in ['BLOG', '']:
                if st.button(a['titolo'], key=f"ar_{i}", use_container_width=True):
                    st.session_state.sel_idx = i
                    st.session_state.mode = 'view'
                    st.rerun() # Forza la chiusura della tendina e il refresh del contenuto

with c2:
    with st.popover("📜 TESTI ANTICHI", use_container_width=True):
        for i, a in enumerate(all_a):
            # Filtro per categoria TESTI (es. Hatha Yoga Pradipika)
            if str(a.get('cat','')).upper() == 'TESTI':
                if st.button(a['titolo'], key=f"te_{i}", use_container_width=True):
                    st.session_state.sel_idx = i
                    st.session_state.mode = 'view'
                    st.rerun()

with c3:
    with st.popover("🔬 SCIENZA", use_container_width=True):
        for i, a in enumerate(all_a):
            # Filtro per ricerca scientifica e anatomia
            if str(a.get('cat','')).upper() == 'SCIENZA':
                if st.button(a['titolo'], key=f"sc_{i}", use_container_width=True):
                    st.session_state.sel_idx = i
                    st.session_state.mode = 'view'
                    st.rerun()

st.write("---")

# --- AREA CONTENUTO PRINCIPALE ---
if st.session_state.mode == "view" and st.session_state.sel_idx is not None:
    art = all_a[st.session_state.sel_idx]
    st.markdown(f"""
    <div style="background: white; padding:40px; border-radius:8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44;">
        <h1 style="font-family:serif; margin-top:0;">{art['titolo']}</h1>
        <p style="color:#C5A059; font-style:italic;">{art['data']}</p>
        <hr style="border:0; border-top:1px solid #eee; margin: 20px 0;">
        <div style="font-size:1.15rem; line-height:1.8; font-family:serif;">
            {art['testo'].replace(chr(10), '<br>')}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- EDITOR (MODULI) ---
elif st.session_state.mode == "new":
    st.subheader("➕ Nuovo Articolo")
    with st.form("new_art"):
        t = st.text_input("Titolo")
        cat = st.selectbox("Categoria", ["BLOG", "TESTI", "SCIENZA"])
        txt = st.text_area("Contenuto", height=300)
        if st.form_submit_button("Salva"):
            # Qui andrebbe la logica di salvataggio su GitHub
            st.success("Articolo creato!")
            st.session_state.mode = "view"
            st.rerun()
    if st.button("Annulla"):
        st.session_state.mode = "view"; st.rerun()

# --- TASTI DI GESTIONE IN FONDO ---
st.write("<br><br>", unsafe_allow_html=True)
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("➕ NUOVO ARTICOLO", use_container_width=True):
        st.session_state.mode = 'new'
        st.rerun()
with col_btn2:
    if st.button("📝 MODIFICA QUESTO", use_container_width=True):
        st.session_state.mode = 'edit'
        st.rerun()
