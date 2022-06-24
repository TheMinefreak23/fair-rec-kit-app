/* This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences) */

import { API_URL } from '../api'

/**
 * Gets the LastFM and AcousticBrainz data from a song using their respecitve API's
 * @param {String}    track   - Name of the song
 * @param {String}    artist  - Name of the artist
 * @param {String}    mbid    - Unique MBID hash, that can be used in place of track and artist
 * @return {Object}   Object with AcousticBrainz and LastFM data
 */
async function getSongInfo(track, artist, mbid) {
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      track,
      artist,
      mbid,
    }),
  }
  const url = API_URL + '/music/song-info'
  const response = await fetch(url, requestOptions)
  return await response.json()
}

/**
 * Request Spotify data by making a query with artist and track name
 * @param {String} track - Track name
 * @param {String} artist - Artist name
 * @return    {[Array]} List of Spotify tracks found by query, each track containing data
 */
async function getSpotifyInfo(track, artist) {
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      track,
      artist,
    }),
  }
  const url = API_URL + '/music/spotify-info'
  const response = await fetch(url, requestOptions)
  return await response.json()
}

/**
 *
 * @param {String} id
 */
async function getSpotifyTrack(id) {
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id,
    }),
  }
  const url = API_URL + '/music/spotify-track'
  const response = await fetch(url, requestOptions)
  return await response.json()
}

export { getSongInfo, getSpotifyInfo, getSpotifyTrack }
