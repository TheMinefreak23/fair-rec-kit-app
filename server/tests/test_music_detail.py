# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import unittest
from unittest.mock import MagicMock
from io import BytesIO
from sewar.full_ref import uqi
from PIL import Image
import requests
    
from project.music_detail import collage


URL_PREFIX = '/api/music'


def test_spotify_token(client):
    """ Tests the generating of a Spotify Auth token

    Args:
        client (Client): The client
    """
    response = client.post(URL_PREFIX + '/token')
    assert response.status_code == 200


def test_acousticbrainz_data(client):
    """ Tests if acousticbrainz gets succesfully requested

    Args:
        client (Client): The client
    """
    response = client.get(URL_PREFIX + '/token')
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
    input_img = 'https://i.imgur.com/ejJgMEw.jpg'
    output_img = 'https://i.imgur.com/QbY6IJV.jpg'

    test_input = Image.open(BytesIO(requests.get(input_img).content))
    test_output = Image.open(BytesIO(requests.get(output_img).content))

    result = collage([test_input,test_input,test_input,test_input])
    assert uqi(test_output, result) > 0.8
