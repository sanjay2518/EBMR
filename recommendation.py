import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="2a7dcbf8deeb49abac534747e4eff598", 
                                                           client_secret="50495fb1a1974a5b89917c4258ce0be1"))

# Define music recommendations based on emotion
def recommend_music(emotion):
    emotions_to_genres = {
        'happy': ['pop', 'dance', 'upbeat'],
        'sad': ['blues', 'classical', 'jazz'],
        'angry': ['rock', 'metal', 'punk'],
        'fear': ['ambient', 'classical'],
        'surprise': ['indie', 'electronic'],
        'neutral': ['chill', 'lo-fi']
    }
    
    genres = emotions_to_genres.get(emotion, ['chill'])
    recommendations = []
    
    for genre in genres:
        results = sp.search(q=f'genre:{genre} Tamil', type='track', limit=5, market='IN')
        tracks = results['tracks']['items']
        for track in tracks:
            recommendations.append(track['name'] + " by " + track['artists'][0]['name'])
    
    return recommendations
