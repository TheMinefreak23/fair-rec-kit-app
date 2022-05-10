"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import base64
import json
import time

import requests as requests
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
    data = request.get_json()
    print(data)
    ab_api = 'https://acousticbrainz.org/api/v1/'
    musicbrainz_id = data.get('mbid')
    url = ab_api + 'high-level' + '?recording_ids=' + musicbrainz_id
    print(url)
    res = requests.get(url)
    print(res.status_code)
    return json.loads(res.text)
