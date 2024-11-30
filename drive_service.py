
import os.path, io, random

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

VIDEO_FOLDER_ID = '1jpOA1etk47sPjjFih8L7-pE9VvHX6Z-g'
AUDIO_FOLDER_ID = '1vSz_K-Lw0wgmxrH-i9nGAYd70CVD6r-X'

# Initialisation du service Google Drive
def init_drive():
    creds = None
    # The file token.json stores the user's access and 'refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

drive_service = init_drive()

# Lister les fichiers d'un dossier
def list_folder_files(folder_id):
    query = f"'{folder_id}' in parents"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

# Telecharger un fichier
def download_file(file_id, local_path):
    request = drive_service.files().get_media(fileId=file_id)
    with io.FileIO(local_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Téléchargement: {int(status.progress() * 100)}%.")

# REcuperer un fichier aleatoire par dossier
def get_random_file_from_folder(folder_id, download_path):
    files = list_folder_files(folder_id)
    if not files:
        print(f"Aucun fichier trouvé dans le dossier avec ID {folder_id}.")
        return None
    random_file = random.choice(files)
    print(f"Fichier sélectionné aléatoirement: {random_file['name']}")
    download_file(random_file['id'], download_path)
    return random_file['name']

video_file_name = get_random_file_from_folder(VIDEO_FOLDER_ID, './assets/input/video_output.mp4')
audio_file_name = get_random_file_from_folder(AUDIO_FOLDER_ID, './assets/input/audio_output.mp3')

print(f"Fichiers téléchargés: Vidéo - {video_file_name}, Audio - {audio_file_name}")



""" def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API
        results = (
            service.files()
            .list(pageSize=10, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return
        print("Files:")
        for item in items:
            print(f"{item['name']} ({item['id']})")
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
# [END drive_quickstart] """