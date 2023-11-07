# Following Spotipy tutorial at https://github.com/spotipy-dev/spotipy/blob/master/TUTORIAL.md

import spotipy
import pandas as pd
import json
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="1e247c491dfe432680d7203916b4b20a",
                                               client_secret="",
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
    df = df[['track_id', 'track_name', 'album_name', 'album_id']]
    return df
    
def get_track_audio_attributes(df: pd.DataFrame) :
    track_ids = df['track_id']
    tracks = sp.audio_features(track_ids)
    df = pd.concat([df, pd.DataFrame(tracks)], axis=1)
    return df

def get_5_songs(df: pd.DataFrame) :
    album_df = df['album_id']
    album_names = df['album_name']
    
    #print(album_ids)
    index = 0
    for album in album_df:
        albums = sp.album_tracks(album, limit=5, offset=0, market="ES")
        for i in range(5):
            new_dict = {
            'track_id': albums['items'][0]['id'],
            'track_name': albums['items'][0]['name'],
            'album_name': album_names[index],
            'album_id': album
            }
            new_df = pd.DataFrame(new_dict, index=[0])
            df = pd.concat([df, new_df], ignore_index=True)
        index+=1
        if (index == 10) :
            break
        
    return df
    #return pd.concat([df, item_names], ignore_index=True)
    """
    for track in album_ids:
        other_song = sp.album_tracks(track, limit=5, offset=0, market="ES")
        df.append(other_song)
    #df = pd.concat([df, pd.DataFrame(other_song)], axis=0)
    return df
    """
    
def get_track_audio_attributes(df: pd.DataFrame) :
    track_ids = df['track_id'] #[101:200] doesn't go in the correct rows
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
