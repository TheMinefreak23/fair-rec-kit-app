import words from 'an-array-of-english-words'
import { API_URL } from '../api'
import { store } from '../store'
import {ref} from 'vue'

var metadata = {}
var form = {}

const options = ref()


// GET request: Get available options for selection from server
async function getOptions() {
  const response = await fetch(API_URL + '/computation/options')
  const data = await response.json()
  options.value = data.options
}

async function sendMockData() {
  await getOptions()
  form = {
    recommendations: rand(100),
    split: rand(100),
    splitMethod: 'timesplit',
    approaches: generateRandomApproach(),
    metrics: generateRandomMetrics(),
    datasets: randomItems(options.value.datasets),
    filters: randomWords(),
  }

  metadata = {
    name: 'Test' + rand() + ': ' + randomWord(),
    email: randomWord() + '@' + randomWord() + '.com',
    tags: randomWords(),
  }

  const requestOptions = {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ metadata: metadata, settings: form }),
  }
  const response = await fetch(
    API_URL + '/computation/calculation',
    requestOptions
  )
  // Update queue
  const data = response.json()
  store.queue = data
}

function generateRandomApproach() {
  let libraries = options.value.approaches.libraries
  let result = []
  for (let i = 0; i < (1 + Math.floor(Math.random * 3)); i++) {
    approaches = randomItems(randomItems(libraries, 1).options, 1)
    approachName = approaches.name
    choices = approaches.params.options

    randomOption = randomItems(choices, 1)
    randomOptionName = randomOption.map(x => x.text)
    randomOptionValue = randomOption.map(x => randomItems(x.options, 1))

    values = approaches.params.values

    randomValue = randomItems(values, 1)
    randomValuesName = randomValue.map(x => x.text)
    randomValuesValue = randomValue.map(x => (getRandomInt(x.min, x.max)))

    params = [{
      'name': randomOptionName,
      'value': randomOptionValue
    },
    {
      'name': randomValueName,
      'value': randomValueValue
    }]=

    result[i] = {
      'name': approachName,
      'parameter': params}
  }
  console.log(result)
  return result
}

function generateRandomMetrics(){
  let result = []
  for (let i = 0; i < (1 + Math.floor(Math.random * 3)) ; i++) {

    randomOption = randomItems(options.value.metrics, 1)
    randomOptionName = randomOption.map(x => x.text)

    result[i] = {
      'name': randomOptionName,
      'parameter': rand(20)
    }
  }
  return result
}

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
}

function rand(n = 1000) {
  return Math.floor(Math.random() * n)
}

function randomWord() {
  return words[Math.floor(Math.random() * words.length)]
}

function randomWords() {
  let array = []
  for (let i = 0; i < 5; i++) {
    array[i] = randomWord()
  }
  return toFormObject(array)
}

function randomItems(list, n = Math.floor(Math.random() * list.length)) {
  let set = new Set()
  for (let i = 0; i < n; i++) {
    set.add(list[Math.floor(Math.random() * list.length)])
  }
  if (set.size == 0) {
    return randomItems(list)
  }
  return toFormObject([...set])
}

function toFormObject(obj) {
  return obj.map((x) => ({
    name: x,
    parameter: null,
  }))
}

export { sendMockData }
