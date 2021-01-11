"""
File for final project for CS50: Holds all interactions with spotify API
Accesses playlist tracks, orders by feature, returns playlist
"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


"""
DEVELOPMENT PURPOSES ONLY:
"""
CLIENT_ID = "fceeacda58604cc188ad999363e1bc65"
CLIENT_SECRET = "0cec66a1af2549de8d6151f3321451c6"

""" Main Body Below """

# Creating .Spotify instance
auth_manager = SpotifyClientCredentials(client_id = CLIENT_ID, client_secret = CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

"""
Completed:

Access playlist
1. Get playlist id from user (User enters a url, we use re (probably?) to access the playlist id)
2. Use the Spotify.playlist or .playlist_tracks method to access the relevant playlist

Use the playlist id to access the song ids for the tracks in the playlist

Use sp.audio_analysis() to get audio analysis for a given track


TODO:
Create function to order playlist by a given feature

Figure out most efficient way to organise (e.g., should I just iterate over it, or should I sort it first) [Probably iterate, as we might want to sort the same playlist by different criteria]

"""

def main():
    """
    Main function
    """
    """
    PSEUDOCODE:
    
    Get playlist url from user
    Get feature to order the playlist by
    Optionally, get length of playlist to be produced
    
    Return playlist
        
    """
    url, feature, length = user_input()
    id = get_playlist_id(url)
    playlist = sort_tracks_by_feature(playlist_track_generator, id, feature=feature, length=length)
    for song in playlist:
        artists = song[3]
        if len(artists) > 1:
            artists = " and ".join(artists)
        else:
            artists = artists[0]
        print(f"{feature}: {song[1]}; {song[2]} - {artists}")
    

def user_input():
    playlist = input("Enter a playlist url: ")
    feature = input("Enter a feature to sort the playlist by: ")
    length = int(input("Choose the length of the final playlist (type '0' for unlimited length): "))
    
    # If length is 0, set length equal to None
    if not length:
        length = None
    
    return playlist, feature, length
    
    
def get_audio_features(id=None):
    """
    Takes in a track id, uses sp.audio_features to access the audio features, returns a dictionary of the relevant features
    
    :param:: string: track id
    :return:: dictionary: track information
    """
    audio_features = sp.audio_features([id])[0]
    
    # From the audio features dict, we only want several features: danceability, energy, loudness, instrumentalness, acousticness and tempo. Initialise a list to hold those features and a dictionary to hold the results
    features = ["danceability", "energy", "loudness", "tempo", "instrumentalness", "acousticness"]
    feature_dict = {}
    
    for feature in features:
        feature_dict[feature] = audio_features[feature]
    
    return feature_dict

    
def get_playlist_id(url):
    """
    Takes in a url from the user, identifies the playlist ID and uses the ID to access the given playlist
    
    :param:: string: playlist url
    :return:: string: playlist id
    """
    # For test purposes, we will be using a set playlist url
    # playlist_url = "https://open.spotify.com/playlist/2ORMMekJes4b8Zi27Ae1T7?si=DyoJgA8jQCqDwXlOhYpJVg"
    playlist_url = url
    
    
    # Split the url on the forward slashes. Then check if one of the split items is "playlist". If not, raise an error. If there is, then the section after the playlist is the playlist id.
    playlist_split = playlist_url.split("/")
    if "playlist" not in playlist_split:
        raise ValueError("Please enter a Spotify playlist url")
    
    # Find the index of "playlist" in the list: the next item is the playlist id
    playlist_index = playlist_split.index("playlist")
    playlist_id = playlist_split[playlist_index + 1]
    
    # Check whether any additional tags have been added after the playlist id, e.g., "?si=..."
    if "?" in playlist_id:
        playlist_id = playlist_id.split("?")[0]
    
    return playlist_id


def playlist_track_generator(playlist_id):
    """
    A generator function which takes.
    
    :param:: string: playlist id
    :yield:: dictionary: track information
    """
    # For test purposes, we use a predetermined playlist id
    # playlist_id = "2ORMMekJes4b8Zi27Ae1T7"
    
    # Access playlist_tracks. Relevant fields are artist name, track name, track id
    tracks = sp.playlist_tracks(playlist_id, fields='items.track.artists.name,items.track.name,items.track.id')["items"]
    
    # Yield the tracks and their information
    for track in tracks:
        yield track['track']


def sort_tracks_by_feature(generator, playlist_id, feature="danceability", length=None):
    """
    Takes in the get_audio_features generator function and a feature by which to sort the list. Returns a list of track ids, ordered by the feature.
    
    :param:: generator: function, yields track information
    :param:: feature: string, a feature of a track's audio information
    :param:: length: optional integer, the length of the playlist
    :return:: list of tuples containing track id, feature, track name and track artists(s)
    
    """
    # Initialise a list to hold the sorted playlist
    playlist = []
    
    # Iterate through the tracks in the generator and access the track ids
    for track in generator(playlist_id):
        track_artist = [artist['name'] for artist in track['artists']]
        track_name = track['name']
        track_id = track['id']
        
        # Pass the track id to the get_audio_features function and access the relevant feature
        audio_features = get_audio_features(track_id)
        feature_value = audio_features[feature]
        
        # Create a dictionary holding the track id and feature value
        track_value = (track_id, feature_value, track_name, track_artist)
        playlist.append(track_value)
    
    # Sort list using sorted() with a lambda function to sort by the second item in the tuple
    sorted_playlist = sorted(playlist, key=lambda x: x[1], reverse=True)
    
    # If an optional length was given, set the length of the playlist to that length
    if not length:
        length = len(sorted_playlist)
    sorted_playlist = sorted_playlist[:length]
    
    return sorted_playlist


main()
