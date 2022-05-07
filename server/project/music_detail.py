"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import base64
import json
import time
import requests as requests
import numpy as np

from PIL import Image
from io import BytesIO
from flask import Blueprint, request, send_file

detail_bp = Blueprint('music', __name__, url_prefix='/api/music')

token = None

MAX_TRACK_LIMIT = 50

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


@detail_bp.route('/background', methods=['GET'])
def get_background():
    """Generates a background from the album covers of a Spotify Playlist

    Returns:
        Image: Background-image
    """

    if not token:
        get_spotify_token()

    kek = '5PorskWxAZMSnVB8nG9ojL'
    kekw = '6KnSfElksjrqygPIc4TDmf'
    TOP_50 = '37i9dQZEVXbMDoHDwVN2tF'
    TOP_100 = '3IsxzDS04BvejFJcQ0iVyW'
    playlist_id = kekw

    items = []
    # Keep querying until we have all playlist items
    offset = 0
    playlist_length = 0
    while offset < playlist_length or offset == 0:
        url = 'https://api.spotify.com/v1/playlists/' \
              + playlist_id + '/tracks?limit=' \
              + str(MAX_TRACK_LIMIT) + '&offset=' \
              + str(offset)
        headers = {'Authorization': 'Bearer ' + token['access_token'], 'Content-Type': 'application/json'}
        res = requests.get(url, headers=headers)
        playlist = json.loads(res.text)

        items += playlist['items']
        if offset == 0: # TODO refactor into separate request and for loop?
            playlist_length = playlist['total']
            print('playlist length', playlist_length)
        offset += MAX_TRACK_LIMIT

    images = []
    for item in items:
        response = requests.get(item['track']['album']['images'][1]['url'])
        img = Image.open(BytesIO(response.content))
        images.append(img)

    # DEV check for duplicates
    #items.append(items[0])
    duplicates = [item for item in items if items.count(item) > 1]
    print('item duplicates', set([x['track']['name'] for x in duplicates]))
    duplicates = [index for index in range(len(images)) if images.count(images[index]) > 1]
    print('image duplicates', set([(items[i]['track']['album']['name'],
                                    images.count(images[i])) for i in duplicates]))
    """
    print('image duplicates', [(items[i]['track']['name'],
                                    items[i]['track']['album']['name'],
                                    json.dumps([artist['name'] for artist in items[i]['track']['artists']]),
                                    images.count(images[i])) for i in duplicates])
                                    """

    print('image size', images[0].size)
    image_count = MAX_TRACK_LIMIT*2
    image_scale = image_count // 10
    image_width, image_height = images[0].size
    w, h = image_width*image_scale, image_height*image_scale
    max_width, max_height = w // image_scale, h // image_scale
    background = Image.new('RGB', (w, h))

    index = 0
    for i in range(0, w, max_width):
        for j in range(0, h, max_height):
            background.paste(images[index], (i, j))
            index += 1
            # Handle playlist size smaller than image count (flip)
            if index == playlist_length - 1:
                np.flip(images)
                index = 0
    background.save('background.png')

    #return "Background saved"
    # TODO why do we need to go back once tho
    return send_file('../background.png', mimetype='image/png')

