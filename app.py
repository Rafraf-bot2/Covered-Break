import requests
from flask import Flask, request, redirect, send_file
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()


CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
VIDEO_FOLDER = os.path.abspath('./assets/output')



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
    return jsonify({"message": "Access token generated", "access_token": access_token})

@app.route('/video')
def serve_video():
    video_filename = 'output_video.mp4'
    video_path = os.path.join(VIDEO_FOLDER, video_filename)
    return send_file(video_path, as_attachment=False)

@app.route('/publish_reel', methods=['POST'])
def publish_reel():
    """
    Endpoint pour publier une vidéo en reel Instagram.
    """
    data = request.json
    video_url = data.get('video_url')  # URL de la vidéo (par exemple exposée via Ngrok)
    caption = data.get('caption')  # Légende du reel

    if not video_url or not caption:
        return jsonify({"error": "Missing video_url or caption"}), 400

    try:
        result = upload_local_video(video_url, caption)
        return jsonify({"message": "Reel published successfully", "post_id": result["id"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=80)