import requests

# Configuration
INSTAGRAM_ACCOUNT_ID = '1541922900048797'

def upload_local_video(video_url, caption):
    """
    Publie une vidéo locale sur Instagram en tant que reel.
    """
    # Étape 1 : Crée un conteneur média
    url = f"https://graph.facebook.com/v12.0/{INSTAGRAM_ACCOUNT_ID}/media"
    payload = {
        "media_type": "VIDEO",
        "video_url": video_url,
        "caption": caption,
        "access_token": access_token
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()  # Vérifie les erreurs HTTP
    media_container = response.json()
    print(f"Media container created: {media_container}")

    # Étape 2 : Publie le conteneur
    publish_url = f"https://graph.facebook.com/v12.0/{INSTAGRAM_ACCOUNT_ID}/media_publish"
    publish_payload = {
        "creation_id": media_container["id"],
        "access_token": access_token
    }
    publish_response = requests.post(publish_url, data=publish_payload)
    publish_response.raise_for_status()
    return publish_response.json()
