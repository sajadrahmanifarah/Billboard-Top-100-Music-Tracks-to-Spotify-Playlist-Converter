import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

redirect_uri = "http://example.com"
client_id = "Your Client ID"
client_secret = "Your Client Secret"
user_id = "Your User ID"
date = input("enter date in this format yyyy-mm-dd: ")
year = date.split('-')[0]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
data = response.text
soup = BeautifulSoup(data, 'html.parser')
titles = soup.select(selector='li h3#title-of-a-story')
song_titles = [item.getText().strip() for item in titles]
print(song_titles)
track_id = []

access = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                      scope="playlist-modify-private", show_dialog=True, cache_path="token.txt")
login = spotipy.Spotify(auth_manager=access)
for track in song_titles:
    show = login.search(q='track:' + f'{track}', type='track')
    try:
        track_id.append(show['tracks']['items'][0]["id"])
    except:
        continue
print(track_id)
playlist = login.user_playlist_create(user_id, f"{date} 's top 100", public=False)
print(playlist)
login.playlist_add_items(playlist_id=playlist['id'],items=track_id)
