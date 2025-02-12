from flask import Flask, render_template, request, jsonify
import concurrent.futures
import pylast
import os

from dotenv import load_dotenv
load_dotenv()

# Last.fm API credentials (replace with your own API key and secret)
API_KEY = os.getenv("LASTFM_API_KEY")
API_SECRET = os.getenv("LASTFM_API_SECRET")

# Default user list
user_list = ["vistencluse"]

# Initialize Last.fm network
network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)

app = Flask(__name__)

def add_track(tracks, track, username):
    try:
        tracks.append({
            "username": username,
            "track": track.title,
            "artist": track.artist.name,
            "url": track.get_url(),
            "image": track.get_cover_image()
        })
    except IndexError: # image not found
        tracks.append({
            "username": username,
            "track": track.title,
            "artist": track.artist.name,
            "url": track.get_url()
        });
    except pylast.WSError: # track not found
        tracks.append({
            "username": username,
            "track": track.title,
            "artist": track.artist.name,
            "url": track.artist.get_url()
        });

def fetch_user_data(username):
    user = network.get_user(username)
    track = user.get_now_playing()

    if track:
        return ("now_playing", username, track)
    
    recent_tracks = user.get_recent_tracks(limit=1)
    if recent_tracks:
        last_track = recent_tracks[0].track
        return ("last_played", username, last_track)

    return None  # If no data is found

@app.route('/')
def index():

    now_playing = []
    last_played = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_user_data, user_list))

    for result in results:
        if result:
            category, username, track = result
            if category == "now_playing":
                add_track(now_playing, track, username)
            else:
                add_track(last_played, track, username)

    return render_template('index.html', now_playing=now_playing, last_played=last_played, user_list=user_list)

@app.route('/bare')
def bare():
    return render_template('index.html', now_playing=[], last_played=[], user_list=[])

@app.route('/update_user_list', methods=['POST'])
def update_user_list():
    global user_list
    data = request.json
    user_list = data.get('user_list', [])
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=True)
