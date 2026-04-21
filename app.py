import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from database import get_response_for_keyword, log_interaction

# Lade die Geheimnisse aus der .env Datei
load_dotenv()

app = Flask(__name__)

# Konfiguration
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
INSTAGRAM_ACCOUNT_ID = None # Wird beim ersten Start automatisch ermittelt

def get_instagram_account_id():
    """Ermittelt die Instagram ID, die mit der Facebook Seite verknüpft ist."""
    url = f"https://graph.facebook.com/v19.0/me?fields=instagram_business_account&access_token={ACCESS_TOKEN}"
    response = requests.get(url).json()
    return response.get('instagram_business_account', {}).get('id')

@app.route('/webhook', methods=['GET'])
def verify():
    """Webhook Verifizierung für Meta."""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge, 200
    return "Verification failed", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    """Empfängt Benachrichtigungen über neue Kommentare."""
    data = request.json
    
    if data.get('object') == 'instagram':
        for entry in data.get('entry', []):
            for change in entry.get('changes', []):
                if change.get('field') == 'comments':
                    comment_id = change['value']['id']
                    text = change['value']['text'].upper()
                    user_id = change['value']['from']['id']
                    media_id = change['value']['media']['id']

                    print(f"Neuer Kommentar: {text}")

                    # Datenbank nach Antwort suchen
                    response_data = get_response_for_keyword(text, media_id)
                    
                    if response_data:
                        dm_text, reply_text = response_data
                        send_instagram_dm(user_id, dm_text)
                        reply_to_comment(comment_id, reply_text)
                        log_interaction(user_id, text, media_id)

    return "EVENT_RECEIVED", 200

def send_instagram_dm(recipient_id, message_text):
    """Sendet eine Direktnachricht."""
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post(url, json=payload)

def reply_to_comment(comment_id, message_text):
    """Antwortet öffentlich auf einen Kommentar."""
    url = f"https://graph.facebook.com/v19.0/{comment_id}/replies?access_token={ACCESS_TOKEN}"
    payload = {"message": message_text}
    requests.post(url, json=payload)

if __name__ == '__main__':
    # Flask starten
    app.run(port=5000, debug=True)