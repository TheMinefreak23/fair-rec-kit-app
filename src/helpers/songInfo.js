import { API_URL } from '../api'

const SPOTIFY_API = 'https://api.spotify.com/v1/'
const SPOTIFY_ClientID = '7e49545dfb45473cbe595d8bb1e22071'
const SPOTIFY_ClientSecret = 'd5a9e8febef2468b94a5edabe2c5ddeb'

const AB_API = 'https://acousticbrainz.org/api/v1/'
const LFM_API = 'http://ws.audioscrobbler.com/2.0/'
const LFM_key = '5ffe852eb4ffb7e7d5d53e71981cad7f'

async function getSongInfo(token, track, artist, musicbrainzId = '') {
  /*var spotifyID = getSpotifyID(token, track, artist)
  return spotifyID*/
  return getSpotifyInfo(token, track, artist)
}

async function getSpotifyToken() {
  const response = await fetch(API_URL + '/music/token')
  const data = await response.json()
  console.log('token:', data)
  return data
}

async function getSpotifyInfo(token, track, artist) {
  const requestOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      Authorization: token.token_type + ' ' + token.access_token,
    },
  }
  console.log(requestOptions)
  const response = await fetch(
    SPOTIFY_API +
      'search?q=' +
      'artist:' +
      artist +
      '+' +
      'track:' +
      track +
      '&type=track',
    requestOptions
  )
  /*
  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ track: track, artist: artist }),
  }
  const response = await fetch(API_URL + '/music/info', requestOptions)*/
  const data = await response.json()
  console.log(data)
  return data.tracks
}

export { getSongInfo, getSpotifyToken }
