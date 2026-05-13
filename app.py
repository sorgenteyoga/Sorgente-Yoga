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

# Carichiamo i dati reali
all_a = load_a()
ih = get_img("header_yoga.png")

# --- CSS DEFINITIVO PER ALTA LEGGIBILITÀ ---
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
        margin-bottom: 20px;
    }}
</style>
<div class="header-img"></div>
<div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>
""", unsafe_allow_html=True)

# --- STATO DELLA SESSIONE ---
if 'sel_idx' not in st.session_state: st.session_state['sel_idx'] = 0 if all_a else None
if 'cat_view' not in st.session_state: st.session_state['cat_view'] = 'BLOG'
if 'mode' not in st.session_state: st.session_state['mode'] = 'view'

# --- NAVIGAZIONE A PULSANTI (ADDIO TENDINE) ---
# Usiamo 3 colonne con bottoni semplici: clicchi e vai.
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("📂 ARCHIVIO / BLOG", use_container_width=True):
        st.session_state.cat_view = 'BLOG'; st.rerun()
with c2:
    if st.button("📜 TESTI ANTICHI", use_container_width=True):
        st.session_state.cat_view = 'TESTI'; st.rerun()
with c3:
    if st.button("🔬 SCIENZA", use_container_width=True):
        st.session_state.cat_view = 'SCIENZA'; st.rerun()

st.write("---")

# --- ELENCO ARTICOLI DELLA CATEGORIA SCELTA ---
articoli_filtrati = [
    (i, a) for i, a in enumerate(all_a) 
    if str(a.get('cat', 'BLOG')).upper() == st.session_state.cat_view 
    or (st.session_state.cat_view == 'BLOG' and a.get('cat') == '')
]

if articoli_filtrati:
    # Mostriamo i titoli come bottoni piccoli per scegliere l'articolo
    st.markdown(f"**Stai guardando:** *{st.session_state.cat_view}*")
    cols = st.columns(len(articoli_filtrati) if len(articoli_filtrati) < 5 else 5)
    for idx, (original_idx, art) in enumerate(articoli_filtrati):
        with cols[idx % 5]:
            if st.button(art['titolo'], key=f"sel_{original_idx}", use_container_width=True):
                st.session_state.sel_idx = original_idx
                st.session_state.mode = 'view'
                st.rerun()

    # --- VISUALIZZAZIONE CORPO ARTICOLO ---
    st.write("<br>", unsafe_allow_html=True)
    if st.session_state.sel_idx is not None:
        art_corrente = all_a[st.session_state.sel_idx]
        st.markdown(f"""
        <div style="background: white; padding:40px; border-radius:8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color:#1A2E44;">
            <h1 style="font-family:serif; margin-top:0;">{art_corrente['titolo']}</h1>
            <p style="color:#C5A059; font-style:italic;">{art_corrente['data']}</p>
            <hr style="border:0; border-top:1px solid #eee; margin: 20px 0;">
            <div style="font-size:1.15rem; line-height:1.8; font-family:serif;">
                {art_corrente['testo'].replace(chr(10), '<br>')}
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning(f"Nessun articolo trovato nella categoria {st.session_state.cat_view}")

# --- TASTI SERVIZIO ---
st.write("<br><br>", unsafe_allow_html=True)
ce1, ce2 = st.columns(2)
with ce1:
    if st.button("➕ NUOVO ARTICOLO", use_container_width=True):
        st.session_state.mode = 'new'; st.rerun()
with ce2:
    if st.button("📝 MODIFICA QUESTO", use_container_width=True):
        st.session_state.mode = 'edit'; st.rerun()
