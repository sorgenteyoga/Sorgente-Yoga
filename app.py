# --- VISUALIZZAZIONE ARTICOLO ---
    art = st.session_state['articolo_selezionato'] if st.session_state['articolo_selezionato'] else (tutti_gli_articoli[0] if tutti_gli_articoli else None)
    if art:
        testo_html = art['testo'].replace('\n', '<br>')
        st.markdown(f"""
        <div class="article-box">
            <h1 style='font-family:serif; color:#1A2E44; margin-top:0; margin-bottom:10px;'>{art['titolo']}</h1>
            <p style='font-style:italic; color:#C5A059; margin-bottom:30px;'>{art['data']} • Luca Valenti</p>
            <div style="font-family:serif; font-size:1.2rem; line-height:1.7; color:#1A2E44; display:block;">
                {testo_html}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.write("Benvenuti su Sorgente Yoga.")

with col_nav:
    st.markdown("### 🏛️ BIBLIOTECA")
    
    st.markdown(f'<div class="icon-title-container"><img src="data:image/png;base64,{icon_archivio}" class="icon-img"><span class="icon-text">ARCHIVIO BLOG</span></div>', unsafe_allow_html=True)
    with st.expander("Sfoglia articoli", expanded=True):
        if tutti_gli_articoli:
            for i, a in enumerate(tutti_gli_articoli):
                if st.button(f"📄 {a['titolo']}", key=f"nav_{i}"):
                    st.session_state['articolo_selezionato'] = a
                    st.rerun()
        else:
            st.caption("Nessun articolo presente.")

    st.markdown(f'<div class="icon-title-container"><img src="data:image/png;base64,{icon_testi}" class="icon-img"><span class="icon-text">TESTI CLASSICI</span></div>', unsafe_allow_html=True)
    with st.expander("Elenco testi"):
        st.write("• Yoga Sūtra (Patañjali)")
        st.write("• Haṭha Yoga Pradīpikā")
        st.write("• Gheraṇḍa Saṃhitā")
        st.write("• Bhagavad Gītā")

    st.markdown(f'<div class="icon-title-container"><img src="data:image/png;base64,{icon_storia}" class="icon-img"><span class="icon-text">RICERCA STORICA</span></div>', unsafe_allow_html=True)
    with st.expander("Siti e Progetti"):
        st.markdown('<a class="resource-link" href="http://hyp.soas.ac.uk/" target="_blank">Hatha Yoga Project ↗</a>', unsafe_allow_html=True)
        st.markdown('<a class="resource-link" href="https://journalofyogastudies.org/index.php/JoYS/issue/archive" target="_blank">Journal of Yoga Studies ↗</a>', unsafe_allow_html=True)

    st.markdown(f'<div class="icon-title-container"><img src="data:image/png;base64,{icon_scienza}" class="icon-img"><span class="icon-text">SCIENZA</span></div>', unsafe_allow_html=True)
    with st.expander("Istituti e Ricerche"):
        st.markdown('<a class="resource-link" href="https://sleep.hms.harvard.edu/faculty-staff/sat-bir-singh-khalsa" target="_blank">Harvard (Dr. Khalsa) ↗</a>', unsafe_allow_html=True)
        st.markdown('<a class="resource-link" href="https://www.iayt.org/" target="_blank">IAYT Yoga Therapy ↗</a>', unsafe_allow_html=True)
