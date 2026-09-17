import re
import time
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import yt_dlp

CLIENT_ID = "SPOTIFY DEV ID"
CLIENT_SECRET = "SPOTIFY API LINK"
REDIRECT_URI = "http://127.0.0.1:8888/callback"
TARGET_PLAYLIST_ID = "SPOTIFY PLAYLIST ID"
YT_PLAYLIST_URL = "PUT HERE YOUR YT PLAYLIST"


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
        retries = 0  

       
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
                    retries += 1
                    header_retry = e.headers.get("Retry-After")
                    
                    if header_retry and header_retry.isdigit():
                        wait_time = int(header_retry) + 2
                    else:
                        wait_time = (2 ** retries) + 5  

                    print(f"\n[!] Rate Limit! Versuch {retries}. Warte {wait_time} Sekunden...")
                    time.sleep(wait_time)
                else:
                    print(f"[{idx}/{len(yt_titles)}] Fehler: {e}")
                    success = True  

        time.sleep(random.uniform(1.2, 2.2))

        if len(batch_uris) >= 20:
            try:
                sp.playlist_add_items(TARGET_PLAYLIST_ID, batch_uris)
                print(f"--> [Zwischenstand] {len(batch_uris)} Songs zu Spotify hinzugefügt.")
                batch_uris.clear()
                time.sleep(3.0)  
            except spotipy.exceptions.SpotifyException as e:
                print(f"Fehler beim Hinzufügen zur Playlist: {e}")


    if batch_uris:
        try:
            sp.playlist_add_items(TARGET_PLAYLIST_ID, batch_uris)
            print(f"--> Letzte {len(batch_uris)} Songs hinzugefügt.")
        except spotipy.exceptions.SpotifyException as e:
            print(f"Fehler beim Hinzufügen der letzten Songs: {e}")

    print("\nFertig! Alle verfügbaren Songs wurden übertragen.")