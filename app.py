import streamlit as st
import base64, os, json, requests
from datetime import datetime as dt

st.set_page_config(page_title="SORGENTE YOGA", layout="wide", page_icon="🧘")

# --- CONFIGURAZIONE GITHUB ---
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN")
GITHUB_REPO = st.secrets.get("GITHUB_REPO")
FILE_PATH = "archivio_articoli.json"

def save_to_github(content):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    
    # Prendi lo SHA del file esistente per poterlo sovrascrivere
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None
    
    data = {
        "message": f"Aggiornamento archivio {dt.now()}",
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "sha": sha
    }
    requests.put(url, headers=headers, data=json.dumps(data))

# --- FUNZIONI DATI ---
def load_a():
    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r", encoding="utf-8") as f:
                d = json.load(f)
                return d if isinstance(d, list) else []
        except: return []
    return []

def save_a(arts):
    content = json.dumps(arts, ensure_ascii=False, indent=4)
    # Salva localmente
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    # Salva su GitHub se configurato
    if GITHUB_TOKEN and GITHUB_REPO:
        save_to_github(content)

# --- IL RESTO DEL CODICE (STILE E NAVIGAZIONE) RIMANE UGUALE ---
# [Copia qui la parte di Stile, Navigazione e Area Contenuto del messaggio precedente]
