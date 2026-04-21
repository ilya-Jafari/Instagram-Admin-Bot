import sqlite3

DB_NAME = "bot_data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Tabelle für Regeln (Keywords)
    c.execute('''CREATE TABLE IF NOT EXISTS rules 
                 (keyword TEXT, media_id TEXT, dm_text TEXT, reply_text TEXT)''')
    # Tabelle für Statistiken
    c.execute('''CREATE TABLE IF NOT EXISTS stats 
                 (user_id TEXT, keyword TEXT, media_id TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_response_for_keyword(keyword, media_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Sucht erst nach einer Regel für das spezifische Reel, sonst allgemein
    c.execute("SELECT dm_text, reply_text FROM rules WHERE keyword=? AND (media_id=? OR media_id='ALL')", (keyword, media_id))
    result = c.fetchone()
    conn.close()
    return result

def log_interaction(user_id, keyword, media_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO stats (user_id, keyword, media_id) VALUES (?, ?, ?)", (user_id, keyword, media_id))
    conn.commit()
    conn.close()

# Initialisiere die DB beim ersten Import
init_db()