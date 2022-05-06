"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import base64
import json
import time
from turtle import back
import requests as requests
import numpy as np

from PIL import Image
from io import BytesIO
from flask import Blueprint, request

detail_bp = Blueprint('music', __name__, url_prefix='/api/music')

token = None


# Route: Spotify token.
@detail_bp.route('/token', methods=['GET'])
def get_spotify_token():
    global token
    if not (token and token['expiration_time'] - 100 > time.time()):
        id = '7e49545dfb45473cbe595d8bb1e22071'
        secret = 'd5a9e8febef2468b94a5edabe2c5ddeb'
        message = (id + ':' + secret).encode()
        encoded = base64.b64encode(message)
        # print('encoded',encoded)
        headers = {'Authorization': 'Basic ' + encoded.decode()
            , 'Content-Type': 'application/x-www-form-urlencoded'}
        data = 'grant_type=client_credentials'
        res = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
        # print(res.text)
        token = json.loads(res.text)
        token['expiration_time'] = time.time() + token['expires_in']
    print(time.time(), token['expiration_time'])
    return token

@detail_bp.route('/AcousticBrainz', methods=['POST'])
def get_acousticbrainz_data():
    """Requests High-Level audio features from the AcousticBrainz API using a MusicBrainzID

    Returns:
        Dict: Dictionary with all High-Level audiofeatures
    """
    data = request.get_json()
    print(data)
    ab_api = 'https://acousticbrainz.org/api/v1/'
    musicbrainz_id = data.get('mbid')
    url = ab_api + 'high-level' + '?recording_ids=' + musicbrainz_id
    res = requests.get(url)
    return json.loads(res.text)

@detail_bp.route('/background', methods = ["GET"])
def get_background():
    """Generates a background from the album covers of a Spotify Playlist

    Returns:
        Image: Background-image
    """``
    playlist_id = '37i9dQZEVXbMDoHDwVN2tF'
    url = 'https://api.spotify.com/v1/playlists/' + playlist_id + '/tracks?limit=50'
    headers = {'Authorization': 'Bearer ' + token['access_token'], 'Content-Type': 'application/json'}
    res = requests.get(url, headers=headers)
    if(res.status_code == 401):
        get_spotify_token()
        get_background()
    playlist = json.loads(res.text)
    images = []
    for item in (playlist['items']):
        response = requests.get(item['track']['album']['images'][1]['url'])
        img = Image.open(BytesIO(response.content))
        images.append(img)
    background = Image.new('RGB', (3000, 3000))
    w, h = background.size
    index = 0
    for i in range(0, w, 300):
        for j in range(0, h, 300):
            background.paste(images[index], (i,j))
            index+=1
            if(index == 49):
                np.flip(images)
                index = 0
    background.save('../background.png')
    return background
