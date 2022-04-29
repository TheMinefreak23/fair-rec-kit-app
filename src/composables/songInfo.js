import { onMounted } from 'vue'

const SPOTIFY_API = 'https://api.spotify.com/v1/'
const SPOTIFY_ClientID = '7e49545dfb45473cbe595d8bb1e22071'
const SPOTIFY_ClientSecret = 'd5a9e8febef2468b94a5edabe2c5ddeb'

const AB_API = 'https://acousticbrainz.org/api/v1/'
const LFM_API = 'http://ws.audioscrobbler.com/2.0/'
const LFM_key = "5ffe852eb4ffb7e7d5d53e71981cad7f"

var SPOTIFY_TOKEN


export async function getSongInfo(token, track, artist, musicbrainzId = "") {
    
    var spotifyID = getSpotifyID(token, track, artist)
    return spotifyID
}

async function getSpotifyID(track, artist) {
    const requestOptions = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + SPOTIFY_TOKEN }
    }
    console.log(requestOptions)
    const response = await fetch(SPOTIFY_API + "search/q=" + artist + "+" + track +"&type=track", requestOptions)
    console.log(response)
    const data = await response.data
    const songID = data.tracks.items[0].id
    return songID;
}

async function spotifyAuthenticate() {
    var authOptions = {
        method: 'POST',
        headers: {
            'Authorization': 'Basic ' + (client_id + ':' + client_secret).toString('base64')
        },
        body: {
            grant_type: 'client_credentials'
        },
        json: true
    };

    const response = await fetch('https://accounts.spotify.com/api/token', authOptions)
    console.log(response)
    const data = await response.data
    SPOTIFY_TOKEN = data.access_token
}