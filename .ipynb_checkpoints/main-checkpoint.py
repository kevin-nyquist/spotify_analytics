# Following Spotipy tutorial at https://github.com/spotipy-dev/spotipy/blob/master/TUTORIAL.md

import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="1e247c491dfe432680d7203916b4b20a",
                                               client_secret="282d5d0b742748769f02966467b45c93",
                                               redirect_uri="http://localhost:1234",
                                               scope="user-library-read"))

def get_playlist() :
    top_200_id = "7dPdaFrplLZD90rvfG8ZuB"
    return sp.playlist(top_200_id, fields="tracks.items(track(name,id))", market="ES", additional_types=('track', ))

def main() :
    taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'

    results = sp.artist_albums(taylor_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])
    
    playlist = get_playlist()
    print(playlist)

if __name__ == '__main__':
    main()
