import re
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp


CLIENT_ID = "1c04e5a151984556b1e233b4f4b5593c"
CLIENT_SECRET = "8282ed66f79f44b8849b0f7d976b290e"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
TARGET_PLAYLIST_ID = "5HxxeuCDaVdeWf7onVRhkp"
YT_PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLljVKqOj2ihposFJ0nVR1wCQn3OKrlEDg"


def get_yt_titles(url):
    ydl_opts = {
        'extract_flat': True,
        'skip_download': True,
        'ignoreerrors': True
    }
    titles = []
    print("Lese YouTube-Playlist aus...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            for entry in info['entries']:
                if entry and entry.get('title'):
                    clean_title = re.sub(
                        r'\(.*?\)|\[.*?\]|Official Video|Audio|HD|LYRICS', 
                        '', 
                        entry['title'], 
                        flags=re.IGNORECASE
                    ).strip()
                    if clean_title:
                        titles.append(clean_title)
    return titles


if __name__ == "__main__":

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-modify-public playlist-modify-private",
        cache_path="cache_v3.json"
    ))

    yt_titles = get_yt_titles(YT_PLAYLIST_URL)
    batch_uris = []

    print(f"\nSuche {len(yt_titles)} Songs auf Spotify...")
    for idx, title in enumerate(yt_titles, 1):
        success = False
        
        while not success:
            try:
                results = sp.search(q=title, limit=1, type='track')
                tracks = results['tracks']['items']
                
                if tracks:
                    uri = tracks[0]['uri']
                    batch_uris.append(uri)
                    print(f"[{idx}/{len(yt_titles)}] Gefunden: {tracks[0]['name']} - {tracks[0]['artists'][0]['name']}")
                else:
                    print(f"[{idx}/{len(yt_titles)}] Nicht gefunden: {title}")
                    
                success = True
                
            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 429:
                    retry_after = int(e.headers.get("Retry-After", 5))
                    print(f"\n[!] Rate Limit! Warte {retry_after} Sekunden...")
                    time.sleep(retry_after + 1)
                else:
                    print(f"[{idx}/{len(yt_titles)}] Fehler: {e}")
                    success = True

      
        time.sleep(0.9)

        
        if len(batch_uris) >= 30:
            sp.playlist_add_items(TARGET_PLAYLIST_ID, batch_uris)
            print(f"--> [Zwischenstand] {len(batch_uris)} Songs zu Spotify hinzugefügt.")
            batch_uris.clear()
            time.sleep(1)

  
    if batch_uris:
        sp.playlist_add_items(TARGET_PLAYLIST_ID, batch_uris)
        print(f"--> Letzte {len(batch_uris)} Songs hinzugefügt.")

    print("\nFertig! Alle verfügbaren Songs wurden übertragen.")