"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import base64
import json
import time
from io import BytesIO
import requests
import numpy as np
from PIL import Image

from flask import Blueprint, request, send_file

detail_bp = Blueprint('music', __name__, url_prefix='/api/music')

token = None

SPOTIFY_API = 'https://api.spotify.com/v1'
MAX_TRACK_LIMIT = 50


@detail_bp.route('/token', methods=['GET'])
def get_spotify_token():
    """Route: Get Spotify auth token using id and secret

    Returns: the spotify token
    """
    global token
    if not (token and token['expiration_time'] - 100 > time.time()):
        spotify_id = '7e49545dfb45473cbe595d8bb1e22071'
        spotify_secret = 'd5a9e8febef2468b94a5edabe2c5ddeb'
        message = (spotify_id + ':' + spotify_secret).encode()
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
    playlist1 = '6KnSfElksjrqygPIc4TDmf' # Playlist with nice album art
    #TOP_50 = '37i9dQZEVXbMDoHDwVN2tF' # Spotify top 50 chart

    playlist_id = playlist1

    items = []
    # Keep querying until we have all playlist items.
    offset = 0
    playlist_length = 0
    while offset < playlist_length or offset == 0:
        url = SPOTIFY_API + '/playlists/' \
              + playlist_id + '/tracks?limit=' \
              + str(MAX_TRACK_LIMIT) + '&offset=' \
              + str(offset)
        playlist = request_spotify_data(url)

        items += playlist['items']
        if offset == 0: # TODO refactor into separate request and for loop?
            playlist_length = playlist['total']
            print('playlist length', playlist_length)
        offset += MAX_TRACK_LIMIT

    return collage([item['track']['album']['images'][1]['url'] for item in items])


def collage(urls):
    """Create collage from image urls

    Args:
        urls: the image urls

    Returns:
        the collage in PNG format
    """
    images = [Image.open(BytesIO(requests.get(url).content)) for url in urls]

    print('image size', images[0].size)
    image_count = MAX_TRACK_LIMIT*2
    image_scale = image_count // 10
    image_width, image_height = images[0].size
    width, height = image_width*image_scale, image_height*image_scale
    w_step, h_step = width // image_scale, height // image_scale
    background = Image.new('RGB', (width, height))

    index = 0
    for i in range(0, width, w_step):
        for j in range(0, height, h_step):
            background.paste(images[index], (i, j))
            index += 1
            # Handle contents size smaller than image count (flip).
            if index == len(urls) - 1:
                np.flip(images)
                index = 0
    background.save('../client/public/background.png')

    #return "Background saved"
    # TODO why do we need to go back once tho
    return send_file('../background.png', mimetype='image/png')


@detail_bp.route('/unique-album-background', methods=['GET'])
def first_100_album_collage():
    """Route: Make a collage from the first 100 relevant albums from Spotify

    Returns:
        an PNG image with the collage
    """
    # TODO can we get all items a different way?
    # Get all items by setting year to maximal span.
    # Going negative in the year causes a non-year query.
    albums = get_unique_n('q=year:0-10000', 100, 'album', True)
    return collage(albums)


def get_unique_n(query, amount, category, image):
    """Route: Given a Spotify query, find the n most relevant (first) unique items.

    Args:
        query: the query to do in the Spotify search
        amount: the amount of unique items
        category: the query object category (tracks/albums/playlists/etc.)
        image(bool): whether image items should be retrieved

    Returns:
        the n unique items
    """
    # Amount of items returned are a multiple of 10.
    limit = 10
    url = SPOTIFY_API + '/search?' + query + '&type=' + category + '&limit=' + str(limit)

    items = []
    # Get next until we have n items.
    while len(items) < amount:
        query = request_spotify_data(url)
        category_data = query[category+'s']
        print('total items', category_data['total'])
        if image:
            items = list(set(items+[item['images'][1]['url'] for item in category_data['items']]))
        else:
            items += list(set(items+[item['id'] for item in category_data['items']]))
        if len(items) < limit:
            break # Stop if there are less items left than the limit
        url = category_data['next']
    print('items length', len(items))

    return items


def request_spotify_data(url):
    """Make an authorised Spotify JSON request from the url

    Args:
        url: the url at which to do the request

    Returns:
        the response text
    """
    # TODO exception
    if not token:
        get_spotify_token()
    headers = {'Authorization': 'Bearer ' + token['access_token'],
               'Content-Type': 'application/json'}
    res = requests.get(url, headers=headers)
    return json.loads(res.text)
