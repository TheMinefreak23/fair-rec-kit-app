# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import unittest
from unittest.mock import MagicMock

url_prefix = '/api/music'


def test_spotify_token(client):
    response = client.post(url_prefix + '/token')
    assert response.status_code == 200


def test_acousticbrainz_data(client):
    response = client.get(url_prefix + '/token')
    assert response.status_code == 200


def test_background(client):
    response = client.get(url_prefix + '/background')
    assert response.status_code == 200


def test_collage():
    from project.music_detail import collage
    from sewar.full_ref import uqi

    assert uqi()
