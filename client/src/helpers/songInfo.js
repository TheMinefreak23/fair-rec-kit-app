import { API_URL } from '../api'

const SPOTIFY_API = 'https://api.spotify.com/v1/'
const SPOTIFY_ClientID = '7e49545dfb45473cbe595d8bb1e22071'
const SPOTIFY_ClientSecret = 'd5a9e8febef2468b94a5edabe2c5ddeb'

const AB_API = 'https://acousticbrainz.org/api/v1/'
const LFM_API = 'http://ws.audioscrobbler.com/2.0/'
const LFM_key = '5ffe852eb4ffb7e7d5d53e71981cad7f'

function authorisedGetRequestOptions(token) {
  return {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: token.token_type + ' ' + token.access_token,
    },
  }
}

/**
 * Does magical things to foo.
 * @param {String}    foo    - foo is a sentence in bla. 
 * @param {Int}        fa    - How often each letter in foo occurs.
 * @return    {[Int]} Array of counts of each letter.
 */
async function getInfoFromSpotifyID(token, id) {
  //console.log(requestOptions)
  const url = SPOTIFY_API + 'tracks/' + id
  const response = await fetch(url, authorisedGetRequestOptions(token))
  const track = await response.json()
  // console.log('Spotify track from id', id, ':', track)
  return track
}
/**
 * Gets the LastFM and AcousticBrainz data from a song using their respecitve API's
 * @param {String}    track   - Name of the song
 * @param {String}    artist  - Name of the artist
 * @param {String}    mbid    - Unique MBID hash, that can be used in place of track and artist
 * @return {Object}   Object with AcousticBrainz and LastFM data
 */
async function getSongInfo(track, artist, mbid) {
  const lastFMData = await getLastFMinfo(artist, track, mbid)

  if (mbid == undefined && lastFMData.track) {
    mbid = lastFMData.track.mbid
    // console.log('mbid', mbid)
  } /* else {
    track = lastFMData.track.name
    artist = lastFMData.track.artist.name
  }*/

  return {
    //Spotify: token ? await getSpotifyInfo(token, track, artist) : null,
    AcousticBrainz: mbid ? await getAcousticBrainzInfo(mbid) : null,
    LastFM: lastFMData,
  }
}

/**
 * Request an authentication token from the Spotify API
 * @return    {Object} JSON-object containing Auth-token.
 */

async function getSpotifyToken() {
  const response = await fetch(API_URL + '/music/token')
  const data = await response.json()
  // console.log('token:', data)
  return data
}

/**
 * Request Spotify data by making a query with artist and track name
 * @param {String} token - Spotify Authentication Token
 * @param {String} track - Track name
 * @param {String} artist - Artist name
 * @return    {[Array]} List of Spotify tracks found by query, each track containing data
 */

async function getSpotifyInfo(token, track, artist) {
  //console.log(requestOptions)
  const url =
    SPOTIFY_API +
    'search?q=' +
    (artist && 'artist:' + artist) +
    (track && '+' + 'track:' + track) +
    '&type=track'
  const response = await fetch(url, authorisedGetRequestOptions(token))
  const data = await response.json()
  //console.log('Spotify:', data)
  return data.tracks
}

// Request song-data from LastFM
/**
 * 
 * @param {String} artist - Artist name
 * @param {String} track - Track name
 * @param {String} mbid - MBID unique hash-token, which can be used instead of artist and track name
 * @returns {Object} - Object containing all LastFM data about a track
 */
async function getLastFMinfo(artist, track, mbid) {
  var url

  if (mbid != (null || undefined)) {
    url =
      LFM_API +
      '?method=track.getInfo&api_key=' +
      LFM_key +
      '&mbid=' +
      mbid +
      '&autocorrect=1&format=json'
  } else {
    url =
      LFM_API +
      '?method=track.getInfo&api_key=' +
      LFM_key +
      '&artist=' +
      artist +
      '&track=' +
      track +
      '&autocorrect=1&format=json'
  }
  const response = await fetch(url)
  const data = await response.json()
  return data
}

/**
 * Request AcousticBrainz data
 * @param {String} musicbrainzId - Unique MusicBrainz identifier, which can be retrieved from LastFM 
 * @returns {Object} data containing AcousticBrainz data, including high/low-level audio features
 */
async function getAcousticBrainzInfo(musicbrainzId) {
  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      mbid: musicbrainzId,
    }),
  }

  const url = API_URL + '/music/AcousticBrainz'
  const response = await fetch(url, requestOptions)
  const data = await response.json()
  return data[musicbrainzId]
}

export { getSongInfo, getSpotifyInfo, getSpotifyToken, getInfoFromSpotifyID }
