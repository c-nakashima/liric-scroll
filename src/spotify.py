import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# .env ファイルの環境変数を読み込む
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8888/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-playback-state user-read-currently-playing"
))


def get_current_track():
    track = sp.current_user_playing_track()
    if track and track['is_playing']:
        song_name = track['item']['name']
        artist_name = track['item']['artists'][0]['name']
        progress_ms = track['progress_ms']  # ミリ秒単位
        return song_name, progress_ms / 1000  # 秒単位
    return None, None


# Get spotify's progress time
def get_current_playback_time():
    try:
        playback = sp.current_playback()
        if playback and playback['is_playing']:
            return playback['progress_ms'] / 1000  # ミリ秒を秒に変換
    except Exception as e:
        print("Error getting playback time:", e)
    return None

# def sync_playback_with_spotify():
#   try:
#     playback = sp.current_playback()
#     playback['progress_ms']