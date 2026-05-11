import streamlit as st
from Bio import Entrez # Libreria per collegarsi ai database scientifici

# --- CONFIGURAZIONE SORGENTE YOGA ---
st.set_page_config(page_title="SORGENTE YOGA", layout="wide")

# Firma dell'autore
st.sidebar.markdown("### SORGENTE YOGA")
st.sidebar.info("Ricerca e cura di **Luca Valenti**")

# Titolo principale con stile "Storico"
st.markdown("<h1 style='text-align: center; color: #4A3E3E;'>SORGENTE YOGA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-style: italic;'>Dalle radici dei testi alla precisione della scienza</p>", unsafe_allow_html=True)

# --- FUNZIONE DI RICERCA SCIENTIFICA ---
def cerca_yoga_scienza(query):
    Entrez.email = "tua_email@esempio.com" # Serve per identificarsi a PubMed
    handle = Entrez.esearch(db="pubmed", term=query, retmax=5)
    record = Entrez.read(handle)
    return record["IdList"]

# --- INTERFACCIA APP ---
col1, col2 = st.columns(2)

with col1:
    st.header("📜 Storia e Manoscritti")
    st.write("Sezione dedicata all'Hatha Yoga Project e testi antichi.")
    # Qui inseriremo i feed dei ricercatori come Mallinson e Birch

with col2:
    st.header("🔬 Pillole di Scienza")
    st.write("Ultimi aggiornamenti da PubMed su HRV e Neuroscienze.")
    # Esempio di interazione
    if st.button("Aggiorna Ricerche Scientifiche"):
        ids = cerca_yoga_scienza("yoga vagus nerve")
        st.success(f"Trovati {len(ids)} nuovi articoli!")
        for id in ids:
            st.write(f"Articolo PubMed ID: {id} - [Leggi originale](https://pubmed.ncbi.nlm.nih.gov/{id}/)")
