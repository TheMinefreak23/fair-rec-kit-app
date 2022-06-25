"""This module tests the music detail functionality and the spotify api.

test_spotify_token(client): test the generating of a Spotify Auth token.
test_acousticbrainz_data(client): test if AcousticBrainz successfully gets requested.
test_background(client): test if a background is successfully generated.
test_collage(): test if the collage method works properly.
test_unique_album_background(client): test if a background is successfully generated.
test_spotify_data(): test if Spotify track data gets successfully requested.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import numpy as np
from sewar.full_ref import uqi
from PIL import Image
from project.blueprints.music_detail_bp import collage, get_acousticbrainz_data
from project.blueprints.music_detail_bp import request_spotify_data

URL_PREFIX = '/api/music'


def test_acousticbrainz_data():
    """Test if AcousticBrainz successfully gets requested."""
    ab_data = get_acousticbrainz_data('bab7f3de-56e3-42fd-be0d-f122960e6a13')
    assert ab_data


def test_background(client):
    """Test if a background is successfully generated.

    Args:
        client: The client component used to send requests to the server
    """
    response = client.get(URL_PREFIX + '/background')
    assert response.status_code == 200
    assert response.data == b'Background saved'


def test_collage():
    """Test if the collage method works properly."""
    input_img = "tests/thisisbingus.jpg"
    output_img = "tests/4bingus.jpg"

    test_input = Image.open(input_img)
    test_output = Image.open(output_img)

    result = collage([test_input, test_input, test_input, test_input], 2)
    assert uqi(np.asanyarray(test_output), np.asanyarray(result)) > 0.8


def test_unique_album_background(client):
    """Test if a background is successfully generated.

    Args:
        client: The client component used to send requests to the server
    """
    response = client.get(URL_PREFIX + '/unique-album-background')
    assert response.status_code == 200
    assert response.data == b'Background saved'


def test_spotify_data():
    """Test if Spotify track data gets successfully requested."""
    url = 'search?q=scatman%20john&type=track'
    result = request_spotify_data(url)
    assert "Scatman" in result['tracks']['items'][0]['album']['name']
