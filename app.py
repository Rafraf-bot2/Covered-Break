import requests
from flask import Flask, request, redirect
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Meta attend souvent un token de vérification pour valider l'URL
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        # Remplace 'my_secret_token' par le token que tu as configuré sur Meta
        if verify_token == 'my_secret_token':
            return challenge, 200
        else:
            return 'Verification token mismatch', 403
    else:
        # Logique pour traiter les données envoyées par le webhook en POST
        data = request.json
        # Ajoute ton traitement ici
        return 'Webhook received', 200

@app.route('/login')
def login():
    auth_url = (
        f"https://api.instagram.com/oauth/authorize"
        f"?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=instagram_business_basic,instagram_business_content_publish&response_type=code"
    )
    return redirect(auth_url)

@app.route('/redirect')
def callback():
    auth_code = request.args.get('code')
    token_url = "https://api.instagram.com/oauth/access_token"
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': REDIRECT_URI,
        'code': auth_code
    }
    response = requests.post(token_url, data=payload)
    access_token = response.json().get("access_token")
    return "Access token received: " + access_token

if __name__ == '__main__':
    app.run(port=80)