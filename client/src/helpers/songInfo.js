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

async function getInfoFromSpotifyID(token, id) {
  //console.log(requestOptions)
  const url = SPOTIFY_API + 'tracks/' + id
  const response = await fetch(url, authorisedGetRequestOptions(token))
  const track = await response.json()
  console.log('Spotify track from id', id, ':', track)
  return track
}

async function getSongInfo(token, track, artist, mbid) {
  const lastFMData = await getLastFMinfo(artist, track, mbid)

  //console.log('mbid', musicbrainzId)
  var track = track
  var artist = artist
  if (mbid == undefined) {
    mbid = await lastFMData.track.mbid
    console.log('mbid', mbid)
  } else {
    track = await lastFMData.track.name
    artist = await lastFMData.track.artist.name
  }
  return {
    Spotify: await getSpotifyInfo(token, track, artist),
    AcousticBrainz: await getAcousticBrainzInfo(mbid),
    LastFM: lastFMData,
  }
}

// Request an authentication token from the Spotify API
async function getSpotifyToken() {
  const response = await fetch(API_URL + '/music/token')
  const data = await response.json()
  console.log('token:', data)
  return data
}

//Request Spotify data from artist and track name
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
  console.log('LastFM', data)
  return data
}

// Request High-level audio features from AcousticBrainz using a musicbrainzID
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
  const json = await response.json()
  console.log('AcousticBrainz:', json)
  return json
}

export { getSongInfo, getSpotifyToken, getInfoFromSpotifyID }
