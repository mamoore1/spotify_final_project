"""
File holding the code for the web application part of the project. Allows the user to input
their playlist, etc., and returns the results
"""

from flask import Flask, redirect, render_template, request

from spotify import get_playlist_id, playlist_track_generator

# Configure application
app = Flask(__name__)


# Define index page
@app.route("/")
def index():
    """
    The homepage for the site. Allows the user to input a spotify playlist url which is then passed to the tracks page.
    The form on this page makes a GET request using the playlist ID to the tracks page.
    """
    # Display the home page
    return render_template("index.html")


# Define track list page
@app.route("/tracks", methods=["GET", "POST"])
def tracks():
    """
    A webpage which receives the playlist information entered by the author and displays the tracks in the playlist (up
    to a certain limit, probably around 20. This page then allows the user to choose which features to sort the playlist
    by, as well as determine the length of the final playlist.
    """
    # Define the list of features that the user can pick from to order the playlist. Drawn from:
    # https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
    features = ["acousticness", "danceability", "energy", "instrumentalness", "liveness", "loudness", "speechiness",
                "valence", "tempo"]

    # POST case: the user has either: 1) passed a playlist to the page or 2) ordered the playlist by some feature
    if request.method == "POST":
        pass

    # GET case: the user has accessed the page, ideally with a playlist id
    else:
        # try to access the playlist url
        playlist_url = request.args.get("playlist_url")
        if not playlist_url:
            return redirect("/")

        # Use the url to get the playlist id, and use the id to get the list of tracks
        id = get_playlist_id(playlist_url)
        playlist_name, *tracks = playlist_track_generator(id)

        # Access tracks more easily
        tracks = tracks[0]

        # Combine artist names into one name
        for track in tracks:
            if len(track['artist']) > 1:
                artist = ", ".join(track['artist'])
            else:
                artist = track['artist'][0]
            track['artist'] = artist

        # Pass tracks to tracks.html
        return render_template("tracks.html", tracks=tracks)



