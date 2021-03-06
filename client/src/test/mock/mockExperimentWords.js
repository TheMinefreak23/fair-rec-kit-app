/*This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)*/

import words from 'an-array-of-english-words'
import { API_URL } from '../api'
import { store } from '../store'

var metadata = {}
var form = {}
async function sendMockData() {
  form = {
    recommendations: rand(),
    split: rand(),
    splitMethod: 'timesplit',
    approaches: randomWords(),
    metrics: randomWords(),
    datasets: randomWords(),
    filters: randomWords(),
  }

  metadata = {
    name: 'Test' + rand(),
    email: randomWord() + '@' + randomWord() + '.com',
    tags: randomWords(),
  }

  console.log(randomWords())

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ metadata: metadata, settings: form }),
  }
  console.log(form)
  const response = await fetch(API_URL + '/experiment/', requestOptions)

  // Update queue
  const data = response.json()
  store.queue = data
}

function rand(n = 1000) {
  return Math.floor(Math.random() * n)
}

function randomWord() {
  return words[Math.floor(Math.random() * words.length)]
}

function randomWords() {
  var array = []
  for (let i = 0; i < 5; i++) {
    array[i] = randomWord()
  }
  return toFormObject(array)
}

function toFormObject(obj) {
  return obj.map((x) => ({
    name: x,
    parameter: null,
  }))
}

export { sendMockData }
