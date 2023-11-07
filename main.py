# Following Spotipy tutorial at https://github.com/spotipy-dev/spotipy/blob/master/TUTORIAL.md

import spotipy
import pandas as pd
import json
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="1e247c491dfe432680d7203916b4b20a",
                                               client_secret="1e14d1db06d54f0cb6122aac6902b273",
                                               redirect_uri="http://localhost:1234",
                                               scope="user-library-read"))

def get_playlist() :
    top_200_id = "7dPdaFrplLZD90rvfG8ZuB"
    playlist = sp.playlist(top_200_id, fields="tracks.items(track(name,id,album(name,id)))", market="ES", additional_types=('track', ))
    items = playlist['tracks']['items']
    df = pd.DataFrame(items)
    df['track_id'] = df['track'].apply(lambda x: x['id'])
    df['track_name'] = df['track'].apply(lambda x: x['name'])
    df['album_name'] = df['track'].apply(lambda x: x['album']['name'])
    df['album_id'] = df['track'].apply(lambda x: x['album']['id'])
    df['popular'] = True
    df = df[['track_id', 'track_name', 'album_name', 'album_id', 'popular']]
    return df
    
def get_track_audio_attributes(df: pd.DataFrame) :
    track_ids = df['track_id']
    tracks = sp.audio_features(track_ids)
    df = pd.concat([df, pd.DataFrame(tracks)], axis=1)
    return df

def get_5_songs(df: pd.DataFrame) :
    album_df = df['album_id']
    album_names = df['album_name']
    track_names = df['track_name']
    
    #print(track_names)
    index = 0
    for album in album_df:
        albums = sp.album_tracks(album, limit=5, offset=0, market="ES")
        for i in range(5):
            try :
                if (albums['items'][i]['name'] != track_names[index]) :
                    new_dict = {
                    'track_id': albums['items'][i]['id'],
                    'track_name': albums['items'][i]['name'],
                    'album_name': album_names[index],
                    'album_id': album,
                    'popular': False
                    }
                    new_df = pd.DataFrame(new_dict, index=[0])
                    df = pd.concat([df, new_df], ignore_index=True)
            except IndexError as e :
                    break
        index+=1
    return df
    
def get_track_audio_attributes(df: pd.DataFrame) :
    track_ids = df['track_id'] #preformed [1:100], [100:200], [200:300], [300:400], and [400:]
    tracks = sp.audio_features(track_ids)
    df = pd.concat([df, pd.DataFrame(tracks)], axis=1)
    return df
    

def main() :
    """
    taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'

    results = sp.artist_albums(taylor_uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])
    """
    df = get_playlist()
    #df = get_track_audio_attributes(df)
    df = get_5_songs(df)
    print(df)

if __name__ == '__main__':
    main()
