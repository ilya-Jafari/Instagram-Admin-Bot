from flask import Flask, request, jsonify
import database

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # 1. Verifizierung für Meta (wird später wichtig)
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == 'subscribe' and token == 'MEIN_GEHEIMES_TOKEN':
            return challenge, 200
        return 'Forbidden', 403

    # 2. Logik für eingehende Kommentare
    if request.method == 'POST':
        data = request.json
        print(f"Eingehendes Event: {data}")

        # Wir simulieren hier die Extraktion der Daten aus dem JSON von Meta
        try:
            # In echt ist das JSON tiefer verschachtelt, das passen wir später an
            reel_id = data.get('reel_id')
            comment_text = data.get('text', '').upper()
            user_id = data.get('user_id')

            # Datenbank prüfen
            rule = database.get_rule(reel_id, comment_text)

            if rule:
                dm_content, public_content = rule
                print(f"TREFFER! Sende DM: '{dm_content}' und Reply: '{public_content}' an User {user_id}")
                # Hier kommen später die API-Aufrufe an Meta rein
            else:
                print("Keine passende Regel gefunden.")

        except Exception as e:
            print(f"Fehler bei der Verarbeitung: {e}")

        return "OK", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)