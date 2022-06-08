"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import numpy as np
from sewar.full_ref import uqi
from PIL import Image
from project.music_detail import collage
from project.music_detail import request_spotify_data
import imageio

URL_PREFIX = '/api/music'


def test_spotify_token(client):
    """ Tests the generating of a Spotify Auth token

    Args:
        client (Client): The client
    """
    response = client.get(URL_PREFIX + '/token')
    assert response.status_code == 200


def test_acousticbrainz_data(client):
    """ Tests if acousticbrainz gets succesfully requested

    Args:
        client (Client): The client
    """
    params = {'mbid': 'bab7f3de-56e3-42fd-be0d-f122960e6a13'}
    response = client.post(URL_PREFIX + '/AcousticBrainz', json=params)
    assert response.status_code == 200


def test_background(client):
    """ Tests if a background is succesfully generated

    Args:
        client (Client): The client
    """
    response = client.get(URL_PREFIX + '/background')
    assert response.status_code == 200


def test_collage():
    """Tests if the collage method works properly
    """
    input_img = "tests/thisisbingus.jpg"
    output_img = "tests/4bingus.jpg"

    test_input = Image.open(input_img)
    test_output = Image.open(output_img)

    result = collage([test_input, test_input, test_input, test_input], 2)
    # result.save('../client/public/bingusresult.png')

    # print(test_output.size)
    # print(result.size)
    assert (uqi(np.asanyarray(test_output), np.asanyarray(result)) > 0.8)


def test_unique_album_background(client):
    """ Tests if a background is succesfully generated

    Args:
        client (Client): The client
    """
    response = client.get(URL_PREFIX + '/unique-album-background')
    assert response.status_code == 200


def test_spotify_data():
    """ Tests if spotify track data gets succesfully requested
    """
    url = 'https://api.spotify.com/v1/search?q=scatman%20john&type=track'
    result = request_spotify_data(url)
    assert "Scatman" in result['tracks']['items'][0]['album']['name']
