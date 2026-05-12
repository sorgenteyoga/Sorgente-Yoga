import streamlit as st
import base64, os, json
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

def get_img(p):
    if os.path.exists(p):
        with open(p, "rb") as f: return base64.b64encode(f.read()).decode()
    return ""

def load_a():
    if os.path.exists("archivio_articoli.json"):
        with open("archivio_articoli.json", "r", encoding="utf-8") as f: return json.load(f)
    return []

def save_a(arts):
    with open("archivio_articoli.json", "w", encoding="utf-8") as f: json.dump(arts, f, ensure_ascii=False, indent=4)

ih, i_a, i_t, i_s, i_z = get_img("header_yoga.png"), get_img("icona_archivio.png"), get_img("icona_testi.png"), get_img("icona_storia.png"), get_img("icona_scienza.png")

st.markdown(f"""<style>
.stApp {{ background:#FDFCF0; }}
.block-container {{ padding: 1rem 5% !important; }}
.header-image {{ width:100%; height:110px; background:url('data:image/png;base64,{ih}') no-repeat center; background-size:contain; border-bottom:3px solid #C5A059; }}
.header-bar {{ background:#1A2E44; padding:8px; color:#FDFCF0; font-family:serif; text-align:center; letter-spacing:2px; }}
.art-box {{ background:white; padding:30px; border-radius:5px; box-shadow:0 2px 10px rgba(0,0,0,0.05); }}
@media (max-width:768px) {{ .header-image {{ height:70px; }} .art-box {{ padding:15px; }} }}
.i-title {{ display:flex; align-items:center; gap:8px; margin-top:15px; font-family:serif; font-weight:bold; color:#1A2E44; }}
.r-link {{ text-decoration:none; color:#1A2E44 !important; font-weight:bold; display:block; padding:4px 0; border-bottom:1px solid #eee; }}
#MainMenu, footer, header {{ visibility:hidden; }}
</style>
<div class="header-image"></div><div class="header-bar">S O R G E N T E &nbsp; Y O G A</div>""", unsafe_allow_html=True)

if 'adm' not in st.session_state: st.session_state['adm'] = False
if 'sel' not in st.session_state: st.session_state['sel'] = None

all_a = load_a()
b_a = [a for a in all_a if a.get('cat', 'BLOG') == 'BLOG']
t_a = [a for a in all_a if a.get('cat') == 'TESTI']

c1, c2 = st.columns([0.7, 0.3], gap="large")

with c1:
    if not st.session_state['adm']:
        with st.expander("🔑"):
            if st.text_input("Pwd", type="password") == "sorgente2026":
                st.session_state['adm'] = True; st.rerun()
    else:
        st.info("✍️ EDITORE")
        st.download_button("📥 BACKUP", json.dumps(all_a, ensure_ascii=False), "yoga.json")
        with st.expander("📝 NUOVO"):
            ct = st.radio("Sezione", ["BLOG", "TESTI"], key="new_cat")
            tt = st.text_input("Titolo")
            tx = st.text_area("Testo", height=500)
            if st.button("🚀") and tt and tx:
                all_a.insert(0, {"data": dt.now().strftime("%d/%m/%Y"), "titolo": tt, "testo": tx, "cat": ct})
                save_a(all_a); st.rerun()
        with st.expander("✏️ MOD"):
            if all_a:
                s = st.selectbox("Art", [x['titolo'] for x in all_a])
                i = [x['titolo'] for x in all_a].index(s)
                all_a[i]['cat'] = st.radio("Sezione", ["BLOG", "TESTI"], index=0 if all_a[i].get('cat', 'BLOG') == "BLOG" else 1, key="edit_cat")
                all_a[i]['titolo'] = st.text_input("Tit", all_a[i]['titolo'])
                all_a[i]['testo'] = st.text_area("Txt", all_a[i]['testo'], height=600)
                if st.button("💾"): save_a(all_a); st.rerun()
                if st.button("🗑️"): all_a.pop(i); save_a(all_a); st.rerun()
        if st.button("🔒"): st.session_state['adm'] = False; st.rerun()

    cur = st.session_state['sel'] if st.session_state['sel'] else (all_a[0] if all_a else None)
    if cur:
        st.markdown(f'<div class="art-box"><h1 style="font-family:serif; color:#1A2E44;">{cur["titolo"]}</h1><p style="color:#C5A059;">{cur["data"]}</p><div style="font-family:serif; font-size:1.15rem; line-height:1.7;">{cur["testo"].replace("\n","<br>")}</div></div>', unsafe_allow_html=True)

with c2:
    st.markdown("### 🏛️ BIBLIOTECA")
    st.markdown(f'<div class="i-title"><img src="data:image/png;base64,{i_a}" width="22"> ARCHIVIO</div>', unsafe_allow_html=True)
    with st.expander("Blog", expanded=True):
        for idx, a in enumerate(b_a):
            if st.button(f"📄 {a['titolo']}", key=f"b{idx}"): st.session_state['sel'] = a; st.rerun()
    st.markdown(f'<div class="i-title"><img src="data:image/png;base64,{i_t}" width="22"> TESTI ANTICHI</div>', unsafe_allow_html=True)
    with st.expander("Elenco"):
        for jdx, a in enumerate(t_a):
            if st.button(f"📜 {a['titolo']}", key=f"t{jdx}"): st.session_state['sel'] = a; st.rerun()
    st.markdown(f'<div class="i-title"><img src="data:image/png;base64,{i_s}" width="22"> STORIA</div>', unsafe_allow_html=True)
    st.markdown('<a class="r-link" href="http://hyp.soas.ac.uk/" target="_blank">Hatha Yoga Project ↗</a>', unsafe_allow_html=True)
    st.markdown(f'<div class="i-title"><img src="data:image/png;base64,{i_z}" width="22"> SCIENZA</div>', unsafe_allow_html=True)
    st.markdown('<a class="r-link" href="https://www.iayt.org/" target="_blank">IAYT Yoga Therapy ↗</a>', unsafe_allow_html=True)
