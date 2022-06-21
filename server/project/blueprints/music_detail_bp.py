"""This module handles the retrieval of the music details that are displayed in the result tables.

methods:
    token_to_dict
    collage
    get_unique_n
    request_spotify_data

blueprint routes:
    get_spotify_token
    get_acousticbrainz_data
    get_background
    first_100_album_collage

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

from flask import Blueprint, request

from project.blueprints.constants import BAD_REQUEST_RESPONSE
from project.models import token as tok

blueprint = Blueprint('music', __name__, url_prefix='/api/music')

SPOTIFY_API = 'https://api.spotify.com/v1'
AB_API = 'https://acousticbrainz.org/api/v1/'
MAX_TRACK_LIMIT = 50


def token_to_dict(token):
    """Convert a token to a dictionary format.

    Args:
        token: the token to convert

    Returns:
        the token in dictionary form
    """
    return {'access_token': token.access_token,
            'token_type': token.token_type,
            'expiration_time': token.expiration_time}


@blueprint.route('/token', methods=['GET'])
def get_spotify_token():
    """Route: Get Spotify auth TOKEN using id and secret.

    Returns: the spotify TOKEN
    """
    if (not tok.access_token) or tok.expiration_time - 100 > time.time():
        spotify_id = '7e49545dfb45473cbe595d8bb1e22071'
        spotify_secret = 'd5a9e8febef2468b94a5edabe2c5ddeb'
        message = (spotify_id + ':' + spotify_secret).encode()
        encoded = base64.b64encode(message)
        headers = {'Authorization': 'Basic ' + encoded.decode(),
                   'Content-Type': 'application/x-www-form-urlencoded'}
        data = 'grant_type=client_credentials'
        res = requests.post(
            'https://accounts.spotify.com/api/token', data=data, headers=headers)
        token_data = json.loads(res.text)
        tok.expiration_time = time.time() + token_data['expires_in']
        tok.token_type = token_data['token_type']
        tok.access_token = token_data['access_token']
    return token_to_dict(tok)


@blueprint.route('/AcousticBrainz', methods=['POST'])
def get_acousticbrainz_data():
    """Request High-Level audio features from the AcousticBrainz API using a MusicBrainzID.

    Returns:
        Dict: Dictionary with all High-Level audiofeatures
    """
    json_data = request.json
    try:
        musicbrainz_id = json_data['mbid']
    except KeyError:
        return BAD_REQUEST_RESPONSE

    url = AB_API + 'high-level' + '?recording_ids=' + musicbrainz_id
    res = requests.get(url)
    return json.loads(res.text)


@blueprint.route('/background', methods=['GET'])
def get_background():
    """Generate a background from the album covers of a Spotify Playlist.

    Returns:
        Image: Background-image
    """
    playlist1 = '6KnSfElksjrqygPIc4TDmf'  # Playlist with nice album art

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
        if offset == 0:
            playlist_length = playlist['total']
        offset += MAX_TRACK_LIMIT
    urls = [item['track']['album']['images'][1]['url'] for item in items]
    images = [Image.open(BytesIO(requests.get(url).content)) for url in urls]
    collage(images)
    return 'Background saved'


def collage(images, size=10):
    """Create collage from images.

    Args:
        urls: the image urls

    Returns:
        the collage in PNG format
    """
    image_width, image_height = images[0].size
    width = image_width * size
    height = image_width * size
    background = Image.new('RGB', (width, height))
    index = 0
    for i in range(0, width, image_width):
        for j in range(0, height, image_height):
            background.paste(images[index], (i, j))
            index += 1
            # Handle contents size smaller than image count (flip).
            if index == len(images) - 1:
                np.flip(images)
                index = 0
    background.save('../client/public/background.png')
    return background


@blueprint.route('/unique-album-background', methods=['GET'])
def first_100_album_collage():
    """Route: Make a collage from the first 100 relevant albums from Spotify.

    Returns:
        an PNG image with the collage
    """
    # Get all items by setting year to maximal span.
    # Going negative in the year causes a non-year query.
    albums = get_unique_n('q=year:0-10000', 100, 'album', True)
    images = [Image.open(BytesIO(requests.get(url).content)) for url in albums]

    collage(images)
    return 'Background saved'


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
    url = SPOTIFY_API + '/search?' + query + \
          '&type=' + category + '&limit=' + str(limit)

    items = []
    # Get next until we have n items.
    while len(items) < amount:
        query = request_spotify_data(url)
        category_data = query[category + 's']
        if image:
            items = list(set(items + [item['images'][1]['url']
                                      for item in category_data['items']]))
        else:
            items += list(set(items + [item['id']
                                       for item in category_data['items']]))
        if len(items) < limit:
            break  # Stop if there are less items left than the limit
        url = category_data['next']

    return items


def request_spotify_data(url):
    """Make an authorised Spotify JSON request from the url.

    Args:
        url: the url at which to do the request

    Returns:
        the response text
    """
    if not tok:
        get_spotify_token()
    headers = {'Authorization': tok.token_type + ' ' + tok.access_token,
               'Content-Type': 'application/json'}
    res = requests.get(url, headers=headers)
    return json.loads(res.text)
