import streamlit as st
from Bio import Entrez

# --- CONFIGURAZIONE ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# Stile CSS Personalizzato (Crema e Blu Navy)
st.markdown("""
    <style>
    .main { background-color: #FDFCF0; }
    h1 { color: #1A2E44; font-family: 'serif'; border-bottom: 2px solid #1A2E44; }
    h2, h3 { color: #4A3E3E; }
    .stButton>button { background-color: #1A2E44; color: white; width: 100%; border-radius: 8px; }
    .source-box { padding: 15px; border-radius: 10px; border: 1px solid #1A2E44; margin-bottom: 10px; background-color: white; min-height: 180px; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNZIONI DI RICERCA ---
def cerca_scienza(query):
    Entrez.email = "tua_email@esempio.com"
    try:
        handle = Entrez.esearch(db="pubmed", term=query, retmax=3)
        record = Entrez.read(handle)
        results = []
        for id in record["IdList"]:
            h = Entrez.esummary(db="pubmed", id=id)
            r = Entrez.read(h)
            results.append({"titolo": r[0]['Title'], "link": f"https://pubmed.ncbi.nlm.nih.gov/{id}/"})
        return results
    except:
        return [{"titolo": "Errore di connessione a PubMed", "link": "#"}]

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## 🧘 SORGENTE YOGA")
    st.write("---")
    st.markdown("**Curatore:** Luca Valenti")
    st.write("Database integrati:")
    st.caption("- JoYS (Filologia)\n- KYM (Tradizione)\n- PubMed (Neuroscienze)\n- Harvard Medical School\n- IAYT (Terapia)")

# --- CORPO PRINCIPALE ---
st.title("SORGENTE YOGA")
st.markdown("*Dalle radici dei manoscritti alla precisione della scienza*")

# ORDINE DELLE TAB: Tradizione per prima
tab1, tab2, tab3 = st.tabs(["📜 Tradizione & Testi", "🔬 Scienza & Harvard", "🏥 Terapia Clinica"])

with tab1:
    st.header("Storia, Filologia e Tradizione")
    st.write("Esplora i testi classici e la ricerca indologica moderna.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class='source-box'>
        <h3>Journal of Yoga Studies</h3>
        <p>Accedi alle ultime pubblicazioni accademiche e ricerche sui manoscritti dell'Hatha Yoga.</p>
        <a href='https://journalofyogastudies.org/index.php/JoYS/issue/archive' target='_blank'>Apri Archivio JoYS</a>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='source-box'>
        <h3>KYM (Tradizione)</h3>
        <p>Insegnamenti e risorse dal Krishnamacharya Yoga Mandiram di Chennai.</p>
        <a href='https://www.kym.org/' target='_blank'>Visita il portale KYM</a>
        </div>""", unsafe_allow_html=True)

with tab2:
    st.header("Ricerca Scientifica e Clinica")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Harvard Medical School")
        if st.button("Monitora Dr. Sat Bir Khalsa"):
            with st.spinner("Cerco studi del Dr. Khalsa..."):
                res = cerca_scienza("Sat Bir Singh Khalsa")
                for r in res:
                    st.markdown(f"• [{r['titolo']}]({r['link']})")
    with col_b:
        st.subheader("Neuroscienze")
        if st.button("Aggiorna HRV & Nervo Vago"):
            with st.spinner("Interrogando PubMed..."):
                res = cerca_scienza("yoga heart rate variability OR yoga vagus nerve")
                for r in res:
                    st.markdown(f"• [{r['titolo']}]({r['link']})")

with tab3:
    st.header("Applicazioni Terapeutiche")
    st.markdown("""<div class='source-box'>
    <h3>IAYT - International Association of Yoga Therapists</h3>
    <p>Il punto di riferimento mondiale per lo Yoga Therapy clinico e professionale.</p>
    </div>""", unsafe_allow_html=True)
    st.link_button("Accedi al Database IAYT", "https://www.iayt.org/")
