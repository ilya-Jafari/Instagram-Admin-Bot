import sqlite3

def init_db():
    conn = sqlite3.connect('config.db')
    c = conn.cursor()
    # Tabelle für die Automatisierungs-Regeln
    c.execute('''CREATE TABLE IF NOT EXISTS rules
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  reel_id TEXT,
                  keyword TEXT,
                  dm_text TEXT,
                  public_reply TEXT)''')
    conn.commit()
    conn.close()

def add_rule(reel_id, keyword, dm_text, public_reply):
    conn = sqlite3.connect('config.db')
    c = conn.cursor()
    c.execute("INSERT INTO rules (reel_id, keyword, dm_text, public_reply) VALUES (?, ?, ?, ?)",
              (reel_id, keyword, dm_text, public_reply))
    conn.commit()
    conn.close()

def get_rule(reel_id, keyword):
    conn = sqlite3.connect('config.db')
    c = conn.cursor()
    # Wir suchen nach der Regel, die zur Reel-ID UND zum Keyword passt
    c.execute("SELECT dm_text, public_reply FROM rules WHERE reel_id=? AND keyword=?", (reel_id, keyword.strip().upper()))
    result = c.fetchone()
    conn.close()
    return result

if __name__ == "__main__":
    init_db()
    # Beispiel-Regel hinzufügen für einen Test
    add_rule("REEL123", "INFO", "Hier ist dein Link: https://deinlink.de", "Check deine DMs! 📩")
    print("Datenbank bereit und Test-Regel erstellt.")