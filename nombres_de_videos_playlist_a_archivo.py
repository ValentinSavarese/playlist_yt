import os
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

# Defino las credenciales de la API (configurar en la consola de desarrolladores de Google)
CLIENT_SECRETS_FILE = "my_file.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

# Creo una instancia autenticación de OAuth
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRETS_FILE, SCOPES)

# Autentica
credentials = flow.run_local_server(port=0)
youtube_service = build("youtube", "v3", credentials=credentials)

# ID de la lista de reproducción privada(reemplaza por tu YT playlist ID)
playlist_id = "PLc0GQbx3FFKCQhIL1PocsakYMEhJN94Bj"

next_page_token = None
total_results = []

while True:
    playlist_items = youtube_service.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50, #YT solo deja 50 max por query
        pageToken=next_page_token
    ).execute()

    total_results.extend(playlist_items.get("items"))

    next_page_token = playlist_items.get("nextPageToken")

    if not next_page_token:
        break

#Creo/Abro el archivo y copio lo de total_results en el archivo
with open("titulos_videos_en_lista.txt", "w", encoding ="utf-8") as archivo:
    for item in total_results:
        titulo_video = item["snippet"]["title"]
        archivo.write(titulo_video + "\n")
archivo.close()

