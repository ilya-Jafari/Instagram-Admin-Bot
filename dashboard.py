import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="InstaBot Dashboard", layout="wide")

st.title("📱 Instagram Automation Dashboard")
st.markdown("Verwalte hier deine Keywords und Antworten für deine Reels.")

# Funktion zum Laden der Daten
def get_data():
    conn = sqlite3.connect('config.db')
    df = pd.read_sql_query("SELECT * FROM rules", conn)
    conn.close()
    return df

# Bereich: Neue Regel erstellen
with st.expander("➕ Neue Regel hinzufügen"):
    with st.form("new_rule_form"):
        reel_id = st.text_input("Reel ID (z.B. REEL123)")
        keyword = st.text_input("Keyword (WakeUpWord)", placeholder="z.B. INFO")
        dm_text = st.text_area("DM Antwort-Text", placeholder="Hi! Hier ist dein Link...")
        public_reply = st.text_input("Öffentlicher Kommentar", placeholder="Check deine DMs! 📩")
        
        submit = st.form_submit_button("Regel speichern")
        
        if submit:
            if reel_id and keyword:
                conn = sqlite3.connect('config.db')
                c = conn.cursor()
                c.execute("INSERT INTO rules (reel_id, keyword, dm_text, public_reply) VALUES (?, ?, ?, ?)",
                          (reel_id, keyword.upper(), dm_text, public_reply))
                conn.commit()
                conn.close()
                st.success("Regel erfolgreich gespeichert!")
                st.rerun()
            else:
                st.error("Bitte Reel ID und Keyword ausfüllen.")

# Bereich: Aktive Regeln anzeigen
st.subheader("📋 Deine aktiven Regeln")
df = get_data()

if not df.empty:
    # Wir zeigen die Tabelle schön an
    st.dataframe(df[['reel_id', 'keyword', 'dm_text', 'public_reply']], use_container_width=True)
    
    if st.button("Alle Regeln löschen (Reset)"):
        conn = sqlite3.connect('config.db')
        conn.cursor().execute("DELETE FROM rules")
        conn.commit()
        conn.close()
        st.warning("Alle Regeln wurden gelöscht.")
        st.rerun()
else:
    st.info("Noch keine Regeln vorhanden. Erstelle deine erste oben!")