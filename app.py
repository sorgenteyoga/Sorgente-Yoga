import streamlit as st
from Bio import Entrez

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# Stile CSS Personalizzato
st.markdown("""
    <style>
    .main { background-color: #FDFCF0; }
    h1 { color: #1A2E44; font-family: 'serif'; border-bottom: 2px solid #1A2E44; }
    h2, h3 { color: #4A3E3E; }
    .stButton>button { background-color: #1A2E44; color: white; width: 100%; border-radius: 8px; }
    .source-box { padding: 15px; border-radius: 10px; border: 1px solid #1A2E44; margin-bottom: 10px; background-color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI DI RICERCA ---
def cerca_scienza(query):
    Entrez.email = "tua_email@esempio.com"
    handle = Entrez.esearch(db="pubmed", term=query, retmax=3)
    record = Entrez.read(handle)
    results = []
    for id in record["IdList"]:
        h = Entrez.esummary(db="pubmed", id=id)
        r = Entrez.read(h)
        results.append({"titolo": r[0]['Title'], "link": f"https://pubmed.ncbi.nlm.nih.gov/{id}/"})
    return results

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🧘 SORGENTE YOGA")
    st.write("---")
    st.markdown("**Curatore:** Luca Valenti")
    st.write("Database attivi:")
    st.caption("- PubMed (Neuroscienze)\n- IAYT (Terapia)\n- JoYS (Filologia)\n- KYM (Tradizione)\n- Harvard Medical School")

# --- CORPO PRINCIPALE ---
st.title("SORGENTE YOGA")
st.markdown("*Integrazione tra saggezza antica e ricerca moderna*")

tab1, tab2, tab3 = st.tabs(["🔬 Scienza & Harvard", "📜 Tradizione & Testi", "🏥 Terapia Clinica"])

with tab1:
    st.header("Ricerca Scientifica e Clinica")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Monitora Dr. Sat Bir Khalsa"):
            st.subheader("Ultimi studi (Harvard):")
            res = cerca_scienza("Sat Bir Singh Khalsa")
            for r in res:
                st.markdown(f"• [{r['titolo']}]({r['link']})")
    with col_b:
        if st.button("Aggiorna HRV & Neuroscienze"):
            st.subheader("Ultime da PubMed:")
            res = cerca_scienza("yoga heart rate variability")
            for r in res:
                st.markdown(f"• [{r['titolo']}]({r['link']})")

with tab2:
    st.header("Storia, Filologia e Tradizione")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class='source-box'>
        <h3>Journal of Yoga Studies</h3>
        <p>Accedi alle ultime pubblicazioni accademiche peer-reviewed.</p>
        <a href='https://journalofyogastudies.org/index.php/JoYS/issue/archive' target='_blank'>Apri Archivio JoYS</a>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='source-box'>
        <h3>KYM (Tradizione)</h3>
        <p>Insegnamenti di T. Krishnamacharya e Desikachar.</p>
        <a href='https://www.kym.org/' target='_blank'>Visita il Mandiram</a>
        </div>""", unsafe_allow_html=True)

with tab3:
    st.header("Applicazioni Terapeutiche")
    st.markdown("### IAYT - International Association of Yoga Therapists")
    st.write("Accedi alle risorse per lo Yoga Therapy professionale.")
    st.link_button("Vai al database IAYT", "https://www.iayt.org/")
